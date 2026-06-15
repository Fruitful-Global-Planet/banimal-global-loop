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

    // CORS headers for all responses
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, x-paystack-signature',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // Route: Paystack webhook proxy
    if (pathname === '/webhooks/paystack' && request.method === 'POST') {
      const body = await request.text();
      const signature = request.headers.get('x-paystack-signature');

      // Forward to internal webhook handler (or handle inline)
      const response = await fetch('https://api.banimal.faa.zone/webhooks/paystack', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-paystack-signature': signature,
          'x-forwarded-by': 'banimal-router-worker',
        },
        body,
      });

      return new Response(await response.text(), {
        status: response.status,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    // Route: Health check
    if (pathname === '/health') {
      return new Response(JSON.stringify({ status: 'ok', service: 'banimal-router', ts: Date.now() }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    // Route: Product catalog (public-safe, no supplier refs)
    if (pathname === '/api/products') {
      const products = [
        {
          sku: 'GS-K8',
          name: 'Banimal Premium Stroller GS-K8',
          price: 4999.00,
          currency: 'ZAR',
          status: 'pre-launch',
          variants: ['Midnight Black', 'Sage Green', 'Stone White'],
        }
      ];
      return new Response(JSON.stringify({ products }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    // Default: pass through to origin
    return fetch(request);
  }
};
