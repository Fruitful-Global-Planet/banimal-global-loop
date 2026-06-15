# Banimal Global Loop

> **Banimal Care Loop** — commerce, invoicing, Zoho CRM/Campaigns integration, Paystack, and Cloudflare Workers automation for `banimal.faa.zone` & `banimal.co.za`

---

## Overview

This repository is the central automation and integration hub for **Banimal** — a premium baby and toddler product brand under **Fruitful Global Planet** (Fruitful Shops Pty Ltd, South Africa).

The Care Loop connects:
- Storefront (`banimal.faa.zone` / `banimal.co.za`)
- Zoho CRM + Zoho Campaigns (marketing automation)
- Zoho Invoice (billing)
- Paystack (payment gateway — ZAR)
- Cloudflare Workers (edge routing, API proxying)
- Internal product catalog (private SKU references)
- Zeptomail / vault@faa.zone (transactional email)

---

## Repository Structure

```
banimal-global-loop/
├── .github/
│   └── workflows/
│       └── deploy.yml          # CI/CD: deploy Worker + notify Zoho
├── workers/
│   └── banimal-router/
│       └── index.js            # Cloudflare Worker: routing + API proxy
├── zoho/
│   ├── crm-webhooks.md         # Zoho CRM webhook endpoints
│   ├── campaigns-templates/    # Email campaign HTML templates
│   └── invoice-config.md       # Invoice automation config
├── catalog/
│   └── products.json           # Internal product catalog (private SKUs)
├── paystack/
│   └── webhook-handler.js      # Paystack webhook processor
├── docs/
│   ├── ARCHITECTURE.md         # System architecture diagram
│   ├── ZOHO-SSO.md             # Zoho SSO / single sign-in guide
│   └── DOMAIN-DNS.md           # DNS and Cloudflare setup reference
└── README.md
```

---

## Domains

| Domain | Status | Purpose |
|--------|--------|---------|
| `banimal.faa.zone` | Active (Cloudflare + Vercel) | Primary storefront |
| `banimal.co.za` | Transition (DNS align needed) | SA-facing domain |
| `vault@faa.zone` | Active (Zeptomail) | Transactional email |

---

## Integration Flow

```
Customer Order (Paystack)
        │
        ▼
Cloudflare Worker (banimal-router)
        │
        ├──► Zoho Invoice (auto-generate invoice)
        │
        ├──► Zoho CRM (create/update contact + deal)
        │
        └──► Zoho Campaigns (trigger welcome / order sequence)
                │
                └──► Zeptomail → vault@faa.zone (transactional email)
```

---

## Product Catalog

Product SKUs are maintained privately in `catalog/products.json`. The initial catalog includes the **GS-K8** premium stroller model. Alibaba supplier references are stored internally and are NOT exposed in any public-facing interface.

---

## Zoho Setup (Single Sign-On Strategy)

To minimize login friction across Zoho CRM, Campaigns, Invoice, and Mail:

1. Use **Zoho One** as the unified suite (single org login)
2. Primary admin: `vault@faa.zone`
3. Alias: `admin@admin.faa.zone` (Zoho Mail)
4. Enable **Zoho SSO** via Zoho Directory for org members
5. See `docs/ZOHO-SSO.md` for step-by-step

---

## GitHub Enterprise Trial

This repo is hosted under the **Fruitful-Global-Planet** org on GitHub Enterprise Cloud trial (27 days remaining as of setup). Actions, Advanced Security, and Internal visibility are all active.

---

## Getting Started

```bash
git clone https://github.com/Fruitful-Global-Planet/banimal-global-loop.git
cd banimal-global-loop
```

See `docs/ARCHITECTURE.md` for the full system diagram.

---

*Part of Fruitful Global Planet · Fruitful Shops (Pty) Ltd · South Africa*
*Ubuntu! Simunye!*
