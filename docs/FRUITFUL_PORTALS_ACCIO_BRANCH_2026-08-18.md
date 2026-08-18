# Fruitful Portals — Accio Branch Notes (2026-08-18)

**Branch:** `Fruitful_Portals_accio`
**Author:** Accio (working for Heyns Schoeman, Fruitful Shops (Pty) Ltd)
**Repo:** https://github.com/Fruitful-Global-Planet/banimal-global-loop.git
**Status:** naming alignment + integration mapping — no destructive changes

---

## 1. Naming validation — the canonical name is **Banimal Giving Loop™**

Audit of this repo found three variants in use:

| Location | Variant found | Action |
|---|---|---|
| `README.md` title | "Banimal Global Loop" | **Kept** — this is the repository/system name (the repo is literally `banimal-global-loop`) |
| `paystack/webhook-handler.js` header | "Banimal Care Loop" | **Renamed** → "Banimal Giving Loop" |
| `src/pages/Checkout.tsx` UI copy | "Banimal's giving loop" | **Renamed** → "the Banimal Giving Loop" |
| `src/components/CharitableGiving.tsx` | "giving" (component name) | Kept (internal identifier) |

Per the validated IP register (`Golden_Ticket_Asset_Naming_IP_Register.md`) and CI Guide MASTER, the **public-facing, legally-registered-eligible mark is "Banimal Giving Loop™"** — "Care Loop" is retired for customer-facing use. The repo name `banimal-global-loop` is retained as the system/repository identifier.

## 2. Sales → Delivery → Payment flow (as deployed)

```
Customer on banimal.co.za / {brand}.seedwave.faa.zone
   │ 1. Browse catalog (catalog/products.json → src/pages/Shop.tsx)
   ▼
Cart → Checkout (src/pages/Checkout.tsx)
   │ 2. Delivery selected (BobGo — src/components/BobGoDelivery.tsx; free SA shipping)
   ▼
Paystack payment (ZAR; Card / Apple Pay / EFT — workers/banimal-applepay-verify, workers/applepay)
   │ 3. Webhook: paystack/webhook-handler.js (charge.success, signature-verified)
   ▼
Back-office loop:
   ├── Zoho Invoice (billing record)
   ├── Zoho CRM (customer record)
   ├── Zoho Campaigns (welcome / nurture)
   └── Zeptomail (order confirmation via vault@faa.zone)
   │
   ▼
Fulfilment (BobGo logistics; 15.01% of every order → Banimal Giving Loop)
```

**Deployment:** Vercel (storefront, `vercel.json`), Cloudflare Workers (`workers/banimal-router`, `workers/seedwave-router`), GitHub Actions CI/CD (`.github/workflows/`), mirror to `heyns1000`.

## 3. banimal.co.za — live site research summary (18 Aug 2026)

- **What it is:** Live Banimal storefront (Vite/React SPA, served via Vercel). Domain pair: `banimal.faa.zone` + `banimal.co.za`.
- **Products:** 100% cotton babygrows (envelope-neck, 4 colours: Sand/Charcoal/Cloud/Stone, R307.75) and bibs (bandana + round, R145.69). SKUs follow `babygrow-{colour}-{size}` and `bib-{type}-{print}` naming (e.g. `babygrow-beige-0-3`, `bib-bandana-animal-sketch`).
- **The Roleplay™ concept:** two animals, one playful name — Bat+Fox=BOX, Bear+Owl=BOWL, Wolf+Hare=WHARE, Swan+Lamb=SLAMB.
- **Signature Art:** licensed high-res downloads by **samfox_illustrate™ (Samantha Ford)** — First Eye (R259.29), Rainbow Madiba (R226.88), Dream Big (R194.47), Space Explorer (R226.88). © Samantha Ford. All rights reserved. (Licensing/royalty terms live on /art.)
- **Commerce:** Paystack (encrypted), free SA shipping, newsletter signup, returns & refund policy page.
- **Motif:** "If you don't like the fruits you are growing, change the seeds." — Fruitful Planet Change.

## 4. Scope guardrails honoured

- **Marketplace ZIP (`Fruitful Marketplace_Claude_design_to_Accio.zip`) untouched** — per user instruction, the core packaging idea stays unrevealed; nothing modified.
- All changes on this branch are additive or copy-standardisation; no data/catalog/pricing altered.
- `catalog/products.json` contains Alibaba supplier references marked **INTERNAL USE ONLY** — not exposed in any public interface (verified).

## 5. Next step

User to supply the backend repo: `https://github.com/Fruitful-Global-Planet/bushcoding.git` → integrate as the Fruitful Portals backend, follow the same branch + naming protocol.

---
*Fruitful Shops (Pty) Ltd · © 2026 · FRUITFUL™ · Banimal Giving Loop™ · github.com/fruitful-global-planet/Banimal-global-loop.git · www.banimal.co.za · fruitful.co · fruitful.planet.change@fruitful.co*
