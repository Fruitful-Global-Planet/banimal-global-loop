/**
 * Banimal Router v3 — Cloudflare Worker
 * banimal.co.za/api/* + banimal.co.za/webhooks/* + banimal.co.za/port/5000/*
 * Payments: Paystack + CapitecPay
 */

async function verifyHmac(body, signature, secret) {
  if (!secret || !signature) return true; // skip if no secret configured
  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey(
    'raw', enc.encode(secret), { name: 'HMAC', hash: 'SHA-512' }, false, ['verify']
  );
  const sigBytes = new Uint8Array(signature.match(/.{1,2}/g).map(b => parseInt(b, 16)));
  const bodyBytes = enc.encode(body);
  return crypto.subtle.verify('HMAC', key, sigBytes, bodyBytes);
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const { pathname } = url;

    const cors = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, x-paystack-signature, x-capitecpay-signature, Authorization',
    };

    if (request.method === 'OPTIONS') return new Response(null, { headers: cors });

    // ── Health ────────────────────────────────────────────────────────────
    if (pathname === '/health') {
      return Response.json({
        status: 'ok', service: 'banimal-router', version: '3.0',
        features: ['paystack-webhook', 'capitecpay-webhook', 'giving-loop', 'delivery-rates', 'exchange-rates', 'digital-delivery', 'faa-wallet', 'orders'],
        paystack_hmac: !!env.PAYSTACK_SECRET_KEY,
        capitecpay_hmac: !!env.CAPITECPAY_SECRET,
        bobgo_live: !!env.BOBGO_API_KEY,
        ts: Date.now(),
      }, { headers: cors });
    }

    // ── Giving stats ──────────────────────────────────────────────────────
    if (pathname === '/api/giving/stats') {
      const [totalZAR, count, lastUpdated] = await Promise.all([
        env.BANIMAL_KV?.get('giving:total_zar').then(v => parseFloat(v||'0')),
        env.BANIMAL_KV?.get('giving:count').then(v => parseInt(v||'0')),
        env.BANIMAL_KV?.get('giving:last_updated'),
      ]);
      return Response.json({ totalZAR, count, lastUpdated, rate: 0.1501 }, { headers: cors });
    }

    // ── ORDER INIT — React checkout posts here ────────────────────────────
    // Handles both /port/5000/api/orders (legacy) and /api/orders (clean)
    if ((pathname === '/port/5000/api/orders' || pathname === '/api/orders') && request.method === 'POST') {
      let body = {};
      try { body = await request.json(); } catch {}

      const { customerName, email, currency = 'ZAR', totalZar, totalUsd, itemsJson } = body;

      if (!email || !totalZar) {
        return Response.json({ error: 'missing email or totalZar' }, { status: 400, headers: cors });
      }

      const amountKobo = Math.round(parseFloat(totalZar) * 100);
      const reference = `ban-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;

      // Initialize Paystack transaction
      const paystackRes = await fetch('https://api.paystack.co/transaction/initialize', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${env.PAYSTACK_SECRET_KEY}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          amount: amountKobo,
          currency: 'ZAR',
          reference,
          callback_url: 'https://www.banimal.co.za/checkout?paystack_callback=true',
          metadata: {
            custom_fields: [
              { display_name: 'Customer Name', variable_name: 'customer_name', value: customerName || '' },
              { display_name: 'Order Items', variable_name: 'items', value: itemsJson || '' },
            ],
          },
        }),
      });

      const paystackData = await paystackRes.json();

      if (!paystackData.status) {
        return Response.json({ error: paystackData.message || 'Paystack init failed' }, { status: 502, headers: cors });
      }

      // Store pending order in KV
      if (env.BANIMAL_KV) {
        ctx.waitUntil(env.BANIMAL_KV.put(`order:${reference}`, JSON.stringify({
          ref: reference,
          email,
          customerName,
          amount_zar: parseFloat(totalZar),
          giving_zar: Math.round(parseFloat(totalZar) * 0.1501 * 100) / 100,
          items: itemsJson,
          status: 'pending',
          ts: new Date().toISOString(),
        }), { expirationTtl: 7776000 }));
      }

      return Response.json({
        status: true,
        reference,
        authorization_url: paystackData.data.authorization_url,
        access_code: paystackData.data.access_code,
      }, { headers: cors });
    }

    // ── Paystack webhook ──────────────────────────────────────────────────
    if (pathname === '/webhooks/paystack' && request.method === 'POST') {
      const rawBody = await request.text();
      const sig = request.headers.get('x-paystack-signature') || '';

      const valid = await verifyHmac(rawBody, sig, env.PAYSTACK_SECRET_KEY);
      if (!valid) return new Response('Unauthorized', { status: 401 });

      let parsed = {};
      try { parsed = JSON.parse(rawBody); } catch {}

      if (parsed?.event === 'charge.success' && env.BANIMAL_KV) {
        const amountZAR = (parsed.data?.amount || 0) / 100;
        const givingZAR = Math.round(amountZAR * 0.1501 * 100) / 100;
        const ref = parsed.data?.reference || '';
        const meta = parsed.data?.metadata || {};

        const [prev, cnt] = await Promise.all([
          env.BANIMAL_KV.get('giving:total_zar').then(v => parseFloat(v||'0')),
          env.BANIMAL_KV.get('giving:count').then(v => parseInt(v||'0')),
        ]);

        ctx.waitUntil(Promise.all([
          env.BANIMAL_KV.put('giving:total_zar', String(Math.round((prev + givingZAR)*100)/100)),
          env.BANIMAL_KV.put('giving:count', String(cnt + 1)),
          env.BANIMAL_KV.put('giving:last_updated', new Date().toISOString()),
          env.BANIMAL_KV.put(`order:${ref}`, JSON.stringify({
            ref, amount_zar: amountZAR, giving_zar: givingZAR,
            email: parsed.data?.customer?.email, ts: new Date().toISOString(),
            meta, status: 'paid',
          }), { expirationTtl: 7776000 }),
        ]));

        const productType = meta?.type;
        if (productType === 'digital' && env.RESEND_API_KEY && parsed.data?.customer?.email) {
          const redirectUrl = meta?.redirect_url || '';
          ctx.waitUntil(fetch('https://api.resend.com/emails', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
            body: JSON.stringify({
              from: 'Banimal <noreply@banimal.co.za>',
              to: [parsed.data.customer.email],
              subject: `Your Sam Fox Digital Certificate — ${meta?.sku || ''}`,
              html: `<p>Thank you for your purchase! Your digital certificate is ready:</p><p><a href="${redirectUrl}">Download your certificate here</a></p><p>— The Fruitful Team</p>`,
            }),
          }));
        }
      }

      return Response.json({ received: true }, { headers: cors });
    }

    // ── CapitecPay webhook ────────────────────────────────────────────────
    if (pathname === '/webhooks/capitecpay' && request.method === 'POST') {
      const rawBody = await request.text();
      const sig = request.headers.get('x-capitecpay-signature') || '';

      const valid = await verifyHmac(rawBody, sig, env.CAPITECPAY_SECRET);
      if (!valid) return new Response('Unauthorized', { status: 401 });

      let parsed = {};
      try { parsed = JSON.parse(rawBody); } catch {}

      if ((parsed?.status === 'SUCCESS' || parsed?.paymentStatus === 'SUCCESSFUL') && env.BANIMAL_KV) {
        const amountZAR = (parsed.amount || parsed.totalAmount || 0) / 100;
        const givingZAR = Math.round(amountZAR * 0.1501 * 100) / 100;
        const ref = parsed.merchantReference || parsed.reference || parsed.transactionId || '';

        const [prev, cnt] = await Promise.all([
          env.BANIMAL_KV.get('giving:total_zar').then(v => parseFloat(v||'0')),
          env.BANIMAL_KV.get('giving:count').then(v => parseInt(v||'0')),
        ]);
        ctx.waitUntil(Promise.all([
          env.BANIMAL_KV.put('giving:total_zar', String(Math.round((prev + givingZAR)*100)/100)),
          env.BANIMAL_KV.put('giving:count', String(cnt + 1)),
          env.BANIMAL_KV.put('giving:last_updated', new Date().toISOString()),
          env.BANIMAL_KV.put(`order:cap:${ref}`, JSON.stringify({
            ref, amount_zar: amountZAR, giving_zar: givingZAR,
            provider: 'capitecpay', ts: new Date().toISOString(), raw: parsed,
          }), { expirationTtl: 7776000 }),
        ]));
      }

      return Response.json({ received: true }, { headers: cors });
    }

    // ── Address callback ──────────────────────────────────────────────────
    if (pathname === '/api/paystack/address-callback' && request.method === 'POST') {
      let body = {};
      try { body = await request.json(); } catch {}
      const ref = body?.reference || '';
      if (env.BANIMAL_KV && ref) {
        ctx.waitUntil(env.BANIMAL_KV.put(`addr:${ref}`, JSON.stringify(body?.data?.shipping_address||{}), { expirationTtl: 86400 }));
      }
      return Response.json({
        redirect_url: `https://banimal.co.za/checkout/order-received/?paystack_ref=${encodeURIComponent(ref)}`
      }, { headers: cors });
    }

    // ── Order lookup ──────────────────────────────────────────────────────
    if (pathname.startsWith('/api/order/') && request.method === 'GET') {
      const ref = pathname.split('/api/order/')[1];
      if (!ref) return Response.json({ error: 'missing ref' }, { status: 400, headers: cors });
      const order = await env.BANIMAL_KV?.get(`order:${ref}`) || await env.BANIMAL_KV?.get(`order:cap:${ref}`);
      if (!order) return Response.json({ error: 'not found' }, { status: 404, headers: cors });
      return Response.json(JSON.parse(order), { headers: cors });
    }

    // ── Delivery rates ────────────────────────────────────────────────────
    if (pathname === '/api/delivery/rates' && request.method === 'POST') {
      let body = {};
      try { body = await request.json(); } catch {}
      const { toPostalCode, orderValueZAR = 0 } = body;

      if (env.BOBGO_API_KEY && toPostalCode) {
        try {
          const bobgoResp = await fetch('https://api.bobgo.co.za/2010-10-01/rates', {
            method: 'POST',
            headers: { 'Authorization': `Basic ${btoa(env.BOBGO_API_KEY + ':')}`, 'Content-Type': 'application/json' },
            body: JSON.stringify({
              to_address: { code: toPostalCode, country: 'ZA' },
              from_address: { code: env.BOBGO_FROM_POSTAL || '0044', country: 'ZA' },
              parcels: [{ weight: 1, length: 30, width: 20, height: 10 }],
            }),
          });
          if (bobgoResp.ok) {
            const data = await bobgoResp.json();
            const rates = (data.rates||[]).map(r => ({ service: r.service_level_name||r.service, price: Math.round(r.rate||r.price||0), days: r.transit_days ? `${r.transit_days} business days` : 'See tracking' }));
            if (rates.length > 0) return Response.json({ rates, source: 'bobgo' }, { headers: cors });
          }
        } catch {}
      }

      const free = Number(orderValueZAR) >= 500;
      return Response.json({
        rates: [
          { service: 'Standard Delivery', price: free ? 0 : 85, days: '3–5 business days' },
          { service: 'Express Delivery', price: free ? 60 : 145, days: '1–2 business days' },
        ],
        source: 'fallback', free_from: 500,
      }, { headers: cors });
    }

    // ── Exchange rates ────────────────────────────────────────────────────
    if (pathname === '/api/exchange-rates') {
      const base = url.searchParams.get('base') || 'ZAR';
      try {
        const apiKey = env.EXCHANGE_RATE_API_KEY;
        const apiUrl = apiKey ? `https://v6.exchangerate-api.com/v6/${apiKey}/latest/${base}` : `https://open.er-api.com/v6/latest/${base}`;
        const resp = await fetch(apiUrl);
        if (resp.ok) {
          const data = await resp.json();
          return Response.json({ base: data.base_code||base, rates: data.rates||data.conversion_rates, updated: data.time_last_update_utc||new Date().toISOString() }, { headers: { ...cors, 'Cache-Control': 'public, max-age=3600' } });
        }
      } catch {}
      return Response.json({ base: 'ZAR', rates: { ZAR:1, USD:0.054, EUR:0.050, GBP:0.043, NGN:85, GHS:0.80 }, updated: new Date().toISOString(), source: 'fallback' }, { headers: cors });
    }

    // ── FAA Wallet ────────────────────────────────────────────────────────
    if (pathname === '/api/faa-wallet') {
      return Response.json({ wallet_id:'FAA-WALLET-001-HS', node:'GEN-ALPHA-ASIVEREIGER', assets:['ETH','BTC','USDT','XRP','BODCOIN','GRIPTO'], fiat_bridge:['Paystack','CapitecPay','Valr','Stripe'], eth_address:env.FAA_ETH_ADDRESS||null, btc_address:env.FAA_BTC_ADDRESS||null, note:'Set FAA_ETH_ADDRESS etc via wrangler secret' }, { headers: cors });
    }

    return fetch(request);
  },
};
