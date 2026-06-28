# 🧠 Banimal Memory Snapshot

Last updated: 2026-06-28 15:12 SAST
Repository: Fruitful-Global-Planet / banimal-global-loop

---

## 1. Purpose

This file exists so that **AI assistants and developers never need to re-derive Banimal context from scratch** after a session closes.

It is the **single source of truth** for:
- Current integration focus (Paystack, BobGo, Zoho, Cloudflare Workers).
- Banimal product physical constraints (dimensions, max weight).
- Where to reconnect in the source tree when resuming work.

Update the timestamp and sections whenever assumptions change.

---

## 2. Current integration focus

### Paystack
- Primary ZAR payment gateway for `seedwave.faa.zone/checkout` and Banimal storefronts.
- Handles: transaction initialization, webhook processing, order status, revenue split per brand.
- Live Public Key: `pk_live_6aae7ee4a532694147cb36ee56780eb49a2af5fb`
- Live Webhook URL: `https://banimal.co.za/webhooks/paystack`
- Live Callback URL: `https://www.banimal.co.za/checkout?paystack_callback=true`
- Channels: card, bank_transfer, eft, capitec_pay
- Code paths: `workers/banimal-router/index.js`, `paystack/webhook-handler.js`

### BobGo
- Logistics / fulfilment integration for Banimal products (shipping rates, labels, delivery orchestration).
- API key: `1de***353` (created 28 Jun 2026 14:12 by Heyns Schoeman)
- From postal code: `0044` (Pretoria, South Africa)
- All product parcels: weight=1kg, length=30cm, width=20cm, height=10cm (default parcel)
- Must respect the global Banimal product constraints in section 3.
- Code paths: any files named `bobgo`, `delivery`, `logistics`, `shipping`, `delivery-rates`

### Zoho + Email
- **Invoice**: Zoho Invoice API (billing records via `invoice.zoho.com/api/v3/invoices`).
- **CRM**: Zoho CRM (`zohoapis.com/crm/v2/Contacts`) for customer records and lead source tracking.
- **Campaigns**: Zoho Campaigns for welcome/nurture sequences.
- **Email**: Zoho Mail via `banimal@admin.faa.zone` (admin.faa.zone domain).
- Backoffice user: `banimal@admin.faa.zone` — Administrator role, Active, 302 Dykor Street, Pretoria 0081, Gauteng, South Africa.
- Admin email: `banimal@admin.faa.zone` — Administrator role, Active.

### Zoho API Console Clients
- FAA Vault Sync (19 Apr 2025)
- Faa_zone_admin_portal (25 May 2025)
- Seedwave_FAA_Zone_Backend (10 Jun 2025)
- HSOMNI 9000 Backend (24 Aug 2025)
- Seedwave_FAA_Zone_Backend (25 Aug 2025)
- FAA Central Backend Hub (21 Oct 2025)
- Self Client (29 Oct 2025)

### Zoho Accounts
- Account emails: `heynsschoeman@gmail.com`, `vault@faa.zone`
- Mobile numbers: +27 82 601 3980, +27 72 414 0117
- Org: Fruitful.Planet.Change

### Cloudflare Workers
- `workers/banimal-router/index.js` — Cloudflare Worker routing, Paystack, CapitecPay, giving loop, delivery, exchange rates, orders, refunds, verify.
- KV Namespace: `BANIMAL_KV` (id: `b94b5f024375483abd194d7a79538d36`)
- Routes: `banimal.co.za/api/*`, `banimal.co.za/webhooks/*`, `banimal.co.za/port/5000/*`, `banimal.co.za/assets/*`
- Compatibility: `compatibility_date: 2024-09-23`, `nodejs_compat`
- Env vars: `PAYSTACK_SECRET_KEY`, `CAPITECPAY_SECRET`, `BOBGO_API_KEY`, `BOBGO_FROM_POSTAL=0044`, `EXCHANGE_RATE_API_KEY`, `RESEND_API_KEY`, `FAA_ETH_ADDRESS`, `FAA_BTC_ADDRESS`, `FAA_USDT_ADDRESS`, `FAA_XRP_ADDRESS`

---

## 3. Product shipping assumptions (Banimal SKUs)

Global Banimal product assumptions (supplied by Heyns):
- **Length:** 30 m
- **Width:** 15 cm
- **Thickness:** 5 cm
- **Maximum weight:** 250 g (0.25 kg)

Rules:
- Any BobGo / logistics / shipping code that depends on product dimensions or weight **must use these values as defaults** unless explicitly overridden per-SKU.
- Any rate calculation, volumetric weight, packaging, or courier rule must read from a shared config using these values.
- BobGo parcel default: `weight: 1, length: 30, width: 20, height: 10` (this is the current default in the worker — verify it matches the actual product dimensions above).

If these constraints ever change, update:
1. This section (values + rationale).
2. `workers/banimal-router/index.js` — the `delivery-rates` endpoint parcel defaults.
3. Any documentation in `docs/ARCHITECTURE.md` and `docs/DOMAIN-DNS.md` that mentions sizing/weight.

---

## 4. Recovery flow after a reset

When a session closes or an assistant loses context, use this exact sequence:

1. **Read this file** (`docs/BANIMAL-MEMORY-SNAPSHOT.md`) to recover integrations + product constraints.
2. Read `README.md` for the high-level system and long-term build plan.
3. Open `workers/banimal-router/index.js` to see current routing, Paystack hookups, and APIs.
4. Open `paystack/webhook-handler.js` to see Zoho CRM + Invoice integration.
4. Open BobGo / logistics-related files (search `bobgo`, `delivery`, `shipping`) to see latest shipping logic.
4. Open `src/pages/Checkout.tsx` to see checkout flow.
5. Resume from last unfinished task.

---

## 5. Live domains

| Domain | Purpose |
|--------|--------|
| `banimal.faa.zone` | Flagship Banimal storefront |
| `banimal.co.za` | SA market domain |
| `seedwave.faa.zone` | Core checkout + brand discovery |
| `{brand}.seedwave.faa.zone` | 13k brand storefronts |
| `fruitful.faa.zone` | Fruitful Global Planet portal |
| `vault@faa.zone` | Transactional email (Zeptomail) |
| `banimal@admin.faa.zone` | Admin email (Zoho Mail)

---

## 5. Change log

- **2026-06-28 15:12 SAST** — Snapshot created after Paystack profile login, Zoho Mail login, Zoho API Console, BobGo API keys. Banimal product constraints documented: 30m × 15cm × 5cm, max 250g. Integration focus: Paystack, BobGo.

(Append one bullet per future change: date, what changed, and which files were touched.)
