/**
 * Banimal Router — Cloudflare Worker
 * Routes requests for banimal.faa.zone and banimal.co.za
 * Proxies Paystack webhook calls securely
 * Deployed via: wrangler deploy
 */

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const { pathname } = url;

    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, x-paystack-signature, Authorization',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // ── Giving stats ──────────────────────────────────────────────────────
    if (pathname === '/api/giving/stats' && request.method === 'GET') {
      const totalZAR = parseFloat(await env.BANIMAL_KV?.get('giving:total_zar') || '0');
      const count = parseInt(await env.BANIMAL_KV?.get('giving:count') || '0');
      const lastUpdated = await env.BANIMAL_KV?.get('giving:last_updated') || null;
      return new Response(JSON.stringify({ totalZAR, count, lastUpdated, rate: 0.1501 }), {
        status: 200,
        headers: { ...corsHeaders, 'Content-Type': 'application/json', 'Cache-Control': 'public, max-age=60' },
      });
    }

    // ── Paystack webhook (charge.success, transfer.success, etc.) ──────────
    if (pathname === '/webhooks/paystack' && request.method === 'POST') {
      const rawBody = await request.text();
      let parsed = {};
      try { parsed = JSON.parse(rawBody); } catch {}

      if (parsed?.event === 'charge.success' && env.BANIMAL_KV) {
        const amountKobo = parsed.data?.amount || 0;
        const amountZAR = amountKobo / 100;
        const givingZAR = Math.round(amountZAR * 0.1501 * 100) / 100;
        const prev = parseFloat(await env.BANIMAL_KV.get('giving:total_zar') || '0');
        const count = parseInt(await env.BANIMAL_KV.get('giving:count') || '0');
        ctx.waitUntil(Promise.all([
          env.BANIMAL_KV.put('giving:total_zar', String(Math.round((prev + givingZAR) * 100) / 100)),
          env.BANIMAL_KV.put('giving:count', String(count + 1)),
          env.BANIMAL_KV.put('giving:last_updated', new Date().toISOString()),
        ]));
      }

      const signature = request.headers.get('x-paystack-signature');
      const response = await fetch('https://api.banimal.faa.zone/webhooks/paystack', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-paystack-signature': signature,
          'x-forwarded-by': 'banimal-router-worker',
        },
        body: rawBody,
      });
      return new Response(await response.text(), {
        status: response.status,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    // ── Paystack address callback ──────────────────────────────────────────
    // FIXES THE 405 ERROR at the "user details / address" step in Paystack checkout.
    // Paystack POSTs here when "Collect Address" is enabled on a payment page.
    // Required response: 200 { redirect_url: "..." }
    //
    // TO ACTIVATE: Paystack Dashboard → Payment Pages → Edit → Address callback URL:
    //   https://<your-worker-subdomain>.workers.dev/api/paystack/address-callback
    if (pathname === '/api/paystack/address-callback' && request.method === 'POST') {
      let body = {};
      try { body = await request.json(); } catch {}
      const ref = body?.reference || '';
      const addr = body?.data?.shipping_address || {};

      if (env.BANIMAL_KV && ref) {
        ctx.waitUntil(
          env.BANIMAL_KV.put(`addr:${ref}`, JSON.stringify(addr), { expirationTtl: 86400 })
        );
      }

      return new Response(JSON.stringify({
        redirect_url: `https://banimal.co.za/checkout/order-received/?paystack_ref=${encodeURIComponent(ref)}`,
      }), {
        status: 200,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    // ── Delivery rates (real BobGo API or tiered ZAR fallback) ───────────
    if (pathname === '/api/delivery/rates' && request.method === 'POST') {
      let body = {};
      try { body = await request.json(); } catch {}
      const { toPostalCode, orderValueZAR = 0 } = body;

      if (env.BOBGO_API_KEY && toPostalCode) {
        try {
          const bobgoResp = await fetch('https://api.bobgo.co.za/2010-10-01/rates', {
            method: 'POST',
            headers: {
              'Authorization': `Basic ${btoa(env.BOBGO_API_KEY + ':')}`,
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              to_address: { code: toPostalCode, country: 'ZA' },
              from_address: { code: env.BOBGO_FROM_POSTAL || '7441', country: 'ZA' },
              parcels: [{ weight: 5, length: 40, width: 30, height: 20 }],
            }),
          });
          if (bobgoResp.ok) {
            const data = await bobgoResp.json();
            const rates = (data.rates || []).map(r => ({
              service: r.service_level_name || r.service,
              price: Math.round(r.rate || r.price || 0),
              days: r.transit_days ? `${r.transit_days} business days` : 'See tracking',
            }));
            if (rates.length > 0) {
              return new Response(JSON.stringify({ rates, source: 'bobgo' }), {
                headers: { ...corsHeaders, 'Content-Type': 'application/json' },
              });
            }
          }
        } catch {}
      }

      const free = Number(orderValueZAR) >= 500;
      const rates = [
        { service: 'Standard Delivery', price: free ? 0 : 85, days: '3–5 business days' },
        { service: 'Express Delivery',  price: free ? 60 : 145, days: '1–2 business days' },
      ];
      return new Response(JSON.stringify({ rates, source: env.BOBGO_API_KEY ? 'bobgo-fallback' : 'fallback' }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    // ── Exchange rates (live or static fallback) ──────────────────────────
    if (pathname === '/api/exchange-rates') {
      const base = url.searchParams.get('base') || 'ZAR';
      try {
        const apiKey = env.EXCHANGE_RATE_API_KEY;
        const apiUrl = apiKey
          ? `https://v6.exchangerate-api.com/v6/${apiKey}/latest/${base}`
          : `https://open.er-api.com/v6/latest/${base}`;
        const resp = await fetch(apiUrl);
        if (resp.ok) {
          const data = await resp.json();
          return new Response(JSON.stringify({
            base: data.base_code || base,
            rates: data.rates || data.conversion_rates,
            updated: data.time_last_update_utc || new Date().toISOString(),
          }), {
            headers: {
              ...corsHeaders,
              'Content-Type': 'application/json',
              'Cache-Control': 'public, max-age=3600',
            },
          });
        }
      } catch {}
      return new Response(JSON.stringify({
        base: 'ZAR',
        rates: { ZAR: 1, USD: 0.054, EUR: 0.050, GBP: 0.043, NGN: 85, GHS: 0.80, XRP: 0.017, BTC: 0.00000090, ETH: 0.0000140 },
        updated: new Date().toISOString(),
        source: 'fallback',
      }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    // ── FAA Wallet / crypto payment info ──────────────────────────────────
    // Wallet ID: FAA-WALLET-001-HS  |  Fruitful Global Planet™
    // Accepted: ETH, BTC, USDT, XRP (+ BODCOIN, GRIPTO via FAA chain)
    if (pathname === '/api/faa-wallet') {
      return new Response(JSON.stringify({
        wallet_id: 'FAA-WALLET-001-HS',
        node: 'GEN-ALPHA-ASIVEREIGER',
        assets: ['ETH', 'BTC', 'USDT', 'XRP', 'BODCOIN', 'GRIPTO'],
        fiat_bridge: ['Paystack', 'Valr', 'Stripe'],
        eth_address:  env.FAA_ETH_ADDRESS  || null,
        btc_address:  env.FAA_BTC_ADDRESS  || null,
        usdt_address: env.FAA_USDT_ADDRESS || null,
        xrp_address:  env.FAA_XRP_ADDRESS  || null,
        note: 'Set env vars FAA_ETH_ADDRESS, FAA_BTC_ADDRESS, FAA_USDT_ADDRESS, FAA_XRP_ADDRESS via wrangler secret',
      }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    // ── Health check ──────────────────────────────────────────────────────
    if (pathname === '/health') {
      return new Response(JSON.stringify({
        status: 'ok',
        service: 'banimal-router',
        ts: Date.now(),
        features: [
          'paystack-webhook',
          'paystack-address-callback',
          'delivery-rates-bobgo',
          'exchange-rates',
          'faa-wallet',
          'product-catalog',
        ],
        bobgo_live:    !!env.BOBGO_API_KEY,
        exchange_live: !!env.EXCHANGE_RATE_API_KEY,
        faa_wallet_eth: !!env.FAA_ETH_ADDRESS,
      }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    // ── Product catalog ───────────────────────────────────────────────────
    if (pathname === '/api/products') {
      const products = [
        {
          sku: 'GS-K8',
          name: 'Banimal Premium Stroller GS-K8',
          price: 4999.00,
          currency: 'ZAR',
          status: 'pre-launch',
          variants: ['Midnight Black', 'Sage Green', 'Stone White'],
          paystack_link: 'https://paystack.com/buy/banimal-premium-stroller-gs-k8-ycfsaj',
        },
        {
          sku: 'TEST-R5',
          name: 'Banimal Payment Test',
          price: 5.00,
          currency: 'ZAR',
          status: 'active',
          description: 'R5 test — verifies Paystack end-to-end',
          paystack_link: env.PAYSTACK_R5_LINK || '',
        },
      ];
      return new Response(JSON.stringify({ products }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    // Default: pass through to origin
    return fetch(request);
  },
};
