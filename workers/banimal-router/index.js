/**
 * Banimal Router — Cloudflare Worker
 * banimal.co.za/api/* and banimal.co.za/webhooks/*
 * v2.0 — 2026-06-26 — Added: CapitecPay, digital delivery, full product catalog
 */

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const { pathname } = url;

    const cors = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, x-paystack-signature, Authorization',
    };

    if (request.method === 'OPTIONS') return new Response(null, { headers: cors });

    const json = (data, status = 200, extra = {}) =>
      new Response(JSON.stringify(data), {
        status,
        headers: { ...cors, 'Content-Type': 'application/json', ...extra },
      });

    // ── Health ────────────────────────────────────────────────────────────────
    if (pathname === '/health') {
      return json({
        status: 'ok', service: 'banimal-router', version: '2.0',
        ts: Date.now(),
        features: ['paystack-webhook','capitecpay','apple-pay','delivery-rates','exchange-rates','digital-delivery','product-catalog'],
        bobgo_live: !!env.BOBGO_API_KEY,
        exchange_live: !!env.EXCHANGE_RATE_API_KEY,
        resend_live: !!env.RESEND_API_KEY,
      });
    }

    // ── Giving stats ──────────────────────────────────────────────────────────
    if (pathname === '/api/giving/stats' && request.method === 'GET') {
      const totalZAR = parseFloat(await env.BANIMAL_KV?.get('giving:total_zar') || '0');
      const count = parseInt(await env.BANIMAL_KV?.get('giving:count') || '0');
      const lastUpdated = await env.BANIMAL_KV?.get('giving:last_updated') || null;
      return json({ totalZAR, count, lastUpdated, rate: 0.1501 }, 200, { 'Cache-Control': 'public, max-age=60' });
    }

    // ── CapitecPay initialization ─────────────────────────────────────────────
    // POST { amount_kobo, email, product_id, callback_url }
    if (pathname === '/api/payment/capitec-init' && request.method === 'POST') {
      let body = {};
      try { body = await request.json(); } catch {}
      const { amount_kobo, email, product_id, callback_url, metadata } = body;
      if (!amount_kobo || !email) return json({ error: 'amount_kobo and email required' }, 400);

      const init = await fetch('https://api.paystack.co/transaction/initialize', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${env.PAYSTACK_SECRET_KEY}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          amount: amount_kobo,
          channels: ['bank_transfer'],
          bank: { code: '470099' },  // Capitec Bank code
          callback_url: callback_url || 'https://banimal.co.za/checkout/order-complete',
          metadata: { product_id, ...metadata, capitec: true },
        }),
      });
      const initData = await init.json();
      if (!initData.status) return json({ error: initData.message }, 502);
      return json({
        authorization_url: initData.data.authorization_url,
        reference: initData.data.reference,
        access_code: initData.data.access_code,
      });
    }

    // ── Generic Paystack initialize ───────────────────────────────────────────
    if (pathname === '/api/payment/initialize' && request.method === 'POST') {
      let body = {};
      try { body = await request.json(); } catch {}
      const init = await fetch('https://api.paystack.co/transaction/initialize', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${env.PAYSTACK_SECRET_KEY}`, 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      const initData = await init.json();
      return json(initData, init.status);
    }

    // ── Digital download link ─────────────────────────────────────────────────
    if (pathname.startsWith('/api/digital/') && request.method === 'GET') {
      const ref = pathname.split('/api/digital/')[1];
      if (!ref) return json({ error: 'reference required' }, 400);
      const stored = await env.BANIMAL_KV?.get(`digital:${ref}`);
      if (!stored) return json({ error: 'not found or expired' }, 404);
      const data = JSON.parse(stored);
      if (data.expiry && Date.now() > data.expiry) return json({ error: 'link expired' }, 410);
      return json({ download_url: data.url, sku: data.sku, expires_at: new Date(data.expiry).toISOString() });
    }

    // ── Paystack Webhook ──────────────────────────────────────────────────────
    if (pathname === '/webhooks/paystack' && request.method === 'POST') {
      const rawBody = await request.text();
      let parsed = {};
      try { parsed = JSON.parse(rawBody); } catch {}

      // Verify HMAC signature
      if (env.PAYSTACK_SECRET_KEY) {
        const sig = request.headers.get('x-paystack-signature');
        const encoder = new TextEncoder();
        const keyData = encoder.encode(env.PAYSTACK_SECRET_KEY);
        const msgData = encoder.encode(rawBody);
        const cryptoKey = await crypto.subtle.importKey('raw', keyData, { name: 'HMAC', hash: 'SHA-512' }, false, ['sign']);
        const signatureBuffer = await crypto.subtle.sign('HMAC', cryptoKey, msgData);
        const computed = Array.from(new Uint8Array(signatureBuffer)).map(b => b.toString(16).padStart(2, '0')).join('');
        if (sig && computed !== sig) {
          return json({ error: 'invalid signature' }, 401);
        }
      }

      const event = parsed?.event;
      const data = parsed?.data || {};

      ctx.waitUntil((async () => {
        // ── charge.success: update giving counter + handle digital delivery ──
        if (event === 'charge.success' && env.BANIMAL_KV) {
          const amountKobo = data.amount || 0;
          const amountZAR = amountKobo / 100;
          const givingZAR = Math.round(amountZAR * 0.1501 * 100) / 100;
          const prev = parseFloat(await env.BANIMAL_KV.get('giving:total_zar') || '0');
          const count = parseInt(await env.BANIMAL_KV.get('giving:count') || '0');
          await Promise.all([
            env.BANIMAL_KV.put('giving:total_zar', String(Math.round((prev + givingZAR) * 100) / 100)),
            env.BANIMAL_KV.put('giving:count', String(count + 1)),
            env.BANIMAL_KV.put('giving:last_updated', new Date().toISOString()),
          ]);

          // Digital product? Generate download link
          const meta = data.metadata || {};
          const digitalAsset = meta.digital_asset_key;
          if (digitalAsset && env.BANIMAL_KV) {
            const expiry = Date.now() + 24 * 60 * 60 * 1000; // 24h
            // In production: generate CF R2 signed URL here
            const downloadUrl = `https://banimal.co.za/api/digital/${data.reference}`;
            await env.BANIMAL_KV.put(`digital:${data.reference}`, JSON.stringify({
              url: downloadUrl,
              sku: meta.sku,
              expiry,
              email: data.customer?.email,
              asset: digitalAsset,
            }), { expirationTtl: 90000 });
            // Send email via Resend (if configured)
            if (env.RESEND_API_KEY) {
              await fetch('https://api.resend.com/emails', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
                body: JSON.stringify({
                  from: 'Banimal <shop@banimal.co.za>',
                  to: data.customer?.email,
                  subject: `Your Sam Fox art is ready to download!`,
                  html: `<h2>Thank you for your purchase!</h2>
                  <p>Your digital download is ready:</p>
                  <p><a href="${downloadUrl}" style="background:#2D7A46;color:white;padding:12px 24px;border-radius:6px;text-decoration:none;">Download Your Art</a></p>
                  <p><em>This link expires in 24 hours.</em></p>
                  <p>— Banimal, proudly South African 🇿🇦</p>`,
                }),
              });
            }
          }
        }
      })());

      return json({ received: true });
    }

    // ── Paystack address callback ─────────────────────────────────────────────
    if (pathname === '/api/paystack/address-callback' && request.method === 'POST') {
      let body = {};
      try { body = await request.json(); } catch {}
      const ref = body?.reference || '';
      if (env.BANIMAL_KV && ref) {
        ctx.waitUntil(env.BANIMAL_KV.put(`addr:${ref}`, JSON.stringify(body?.data?.shipping_address || {}), { expirationTtl: 86400 }));
      }
      return json({ redirect_url: `https://banimal.co.za/checkout/order-received/?ref=${encodeURIComponent(ref)}` });
    }

    // ── Delivery rates ────────────────────────────────────────────────────────
    if (pathname === '/api/delivery/rates' && request.method === 'POST') {
      let body = {};
      try { body = await request.json(); } catch {}
      const { toPostalCode, orderValueZAR = 0 } = body;
      if (env.BOBGO_API_KEY && toPostalCode) {
        try {
          const r = await fetch('https://api.bobgo.co.za/2010-10-01/rates', {
            method: 'POST',
            headers: { 'Authorization': `Basic ${btoa(env.BOBGO_API_KEY + ':')}`, 'Content-Type': 'application/json' },
            body: JSON.stringify({ to_address: { code: toPostalCode, country: 'ZA' }, from_address: { code: env.BOBGO_FROM_POSTAL || '0001', country: 'ZA' }, parcels: [{ weight: 0.5, length: 30, width: 25, height: 5 }] }),
          });
          if (r.ok) {
            const d = await r.json();
            const rates = (d.rates || []).map(x => ({ service: x.service_level_name, price: Math.round(x.rate || 0), days: `${x.transit_days || '?'} days` }));
            if (rates.length) return json({ rates, source: 'bobgo' });
          }
        } catch {}
      }
      const free = Number(orderValueZAR) >= 500;
      return json({ rates: [
        { service: 'Standard Delivery', price: free ? 0 : 85, days: '3–5 business days' },
        { service: 'Express Delivery',  price: free ? 60 : 145, days: '1–2 business days' },
      ], source: 'fallback' });
    }

    // ── Exchange rates ────────────────────────────────────────────────────────
    if (pathname === '/api/exchange-rates') {
      const base = url.searchParams.get('base') || 'ZAR';
      try {
        const key = env.EXCHANGE_RATE_API_KEY;
        const apiUrl = key ? `https://v6.exchangerate-api.com/v6/${key}/latest/${base}` : `https://open.er-api.com/v6/latest/${base}`;
        const r = await fetch(apiUrl);
        if (r.ok) {
          const d = await r.json();
          return json({ base: d.base_code || base, rates: d.rates || d.conversion_rates, updated: d.time_last_update_utc || new Date().toISOString() }, 200, { 'Cache-Control': 'public, max-age=3600' });
        }
      } catch {}
      return json({ base: 'ZAR', rates: { ZAR: 1, USD: 0.054, EUR: 0.050, GBP: 0.043, NGN: 85, GHS: 0.80, XRP: 0.017, BTC: 0.00000090, ETH: 0.0000140 }, updated: new Date().toISOString(), source: 'fallback' });
    }

    // ── FAA Wallet ───────────────────────────────────────────────────────────
    if (pathname === '/api/faa-wallet') {
      return json({ wallet_id: 'FAA-WALLET-001-HS', node: 'GEN-ALPHA-ASIVEREIGER', assets: ['ETH', 'BTC', 'USDT', 'XRP', 'BODCOIN', 'GRIPTO'], fiat_bridge: ['Paystack', 'Valr', 'Stripe'], eth_address: env.FAA_ETH_ADDRESS || null, btc_address: env.FAA_BTC_ADDRESS || null, usdt_address: env.FAA_USDT_ADDRESS || null, xrp_address: env.FAA_XRP_ADDRESS || null });
    }

    // ── Default passthrough ───────────────────────────────────────────────────
    return fetch(request);
  },
};
