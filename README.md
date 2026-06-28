# 🍉 Banimal Global Loop — Fruitful Global Planet Backend

---

## 🧠 Banimal Memory Snapshot — Session Anchor

> When an assistant or developer context is lost, **do not re-derive the system from scratch**.  
> First read `docs/BANIMAL-MEMORY-SNAPSHOT.md` and then continue work.

This project uses a **persistent snapshot file** to preserve:
- Current payment + logistics focus (Paystack, BobGo, Zoho, Cloudflare Workers)
- Physical product assumptions for Banimal SKUs (dimensions, max weight)
ts, gateways, webhooks, or fulfilment logic, update the snapshot timestamp and sections instead of relying on assistant memory alone.


> **The central backend engine** connecting real-world physical products to 13,000+ digital brands across the `seedwave.faa.zone` ecosystem, powered by the `Fruitful-Global-Planet` organisation and mirrored through the `heyns1000` CodeNest parallel repository network.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FRUITFUL GLOBAL PLANET                          │
│              github.com/Fruitful-Global-Planet  (BACKEND)          │
│                                                                     │
│  banimal-global-loop  ◄──── core API + worker + catalog engine     │
│  payroll-mining.seedwave.faa.zone ◄─ seedwave brand template       │
│  samfox ◄───────────────────────── metrics + styling library       │
└─────────────────────┬───────────────────────────────────────────────┘
                       │  mirrors + sync
                       ▼
┌─────────────────────────────────────────────────────────────────────┐
│               heyns1000 / CodeNest  (PARALLEL MIRROR)              │
│                    github.com/heyns1000                             │
│                95 repos | 9s Ecosystem Pulse                        │
│          Fidelity: 99.9999% | Eternal Grid Active                   │
└─────────────────────┬───────────────────────────────────────────────┘
                       │  deploys to
                       ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        FRONTENDS                                    │
│                                                                     │
│  🐾 banimal.faa.zone / banimal.co.za  ─── FLAGSHIP BRAND           │
│  🌱 {brand}.seedwave.faa.zone        ─── 13,000+ BRAND STOREFRONTS │
│                                                                     │
│         Core Checkout Engine: seedwave.faa.zone/checkout           │
│         Payment: Paystack ZAR + global gateways                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Purpose

This repository is the **developer backend** for the Fruitful Global Planet commerce network. It:

1. **Connects physical real-world products** (Banimal baby/toddler range, partner brands) to digital storefronts
2. **Powers 13,000+ brand subdomains** via the `{brand}.seedwave.faa.zone` naming convention
3. **Serves as the API backbone** — Cloudflare Workers route all edge requests
4. **Automates the commerce loop** — order → invoice → CRM → fulfilment → email
5. **Mirrors to `heyns1000`** for redundancy, developer access, and the 9s Ecosystem Pulse sync

---

## 🔗 Repository Links

| Layer | Repository | Purpose |
|-------|-----------|--------|
| **Backend Org** | [Fruitful-Global-Planet](https://github.com/Fruitful-Global-Planet) | Organisation root |
| **Core Backend** | [banimal-global-loop](https://github.com/Fruitful-Global-Planet/banimal-global-loop) | This repo — API + workers + catalog |
| **Brand Template** | [payroll-mining.seedwave.faa.zone](https://github.com/Fruitful-Global-Planet/payroll-mining.seedwave.faa.zone) | Seedwave brand template (fork per brand) |
| **Metrics/Styling** | [samfox](https://github.com/Fruitful-Global-Planet/samfox) | Shared UI metrics and styling |
| **Parallel Mirror** | [heyns1000](https://github.com/heyns1000) | CodeNest personal mirror — 95 repos, 9s Pulse |

---

## 🌱 Seedwave Brand System — `{brand}.seedwave.faa.zone`

Each brand in the 13,000+ network gets:

```
{brand}.seedwave.faa.zone
  ├── /                  → Brand storefront (product listings)
  ├── /checkout          → Core seedwave checkout (shared engine)
  ├── /api               → Proxied via banimal-router Cloudflare Worker
  └── /catalog           → Product feed from banimal-global-loop/catalog
```

### How a brand goes live:
1. Fork `payroll-mining.seedwave.faa.zone` → rename to `{brand}.seedwave.faa.zone`
2. Add brand config to `catalog/brands/{brand}.json`
3. Set Cloudflare DNS CNAME: `{brand}.seedwave.faa.zone` → worker route
4. GitHub Actions auto-deploys via `.github/workflows/`
5. Paystack subaccount created for brand revenue split

---

## 🛒 Core Checkout — `seedwave.faa.zone/checkout`

The shared checkout engine handles all 13k brands:

- **Paystack** — primary ZAR payment gateway
- **Multi-brand cart** — single checkout, multiple brand items
- **Webhook processor** — `paystack/` folder in this repo
- **Invoice generation** — Zoho Invoice API
- **Order routing** — Cloudflare Worker (`workers/banimal-router/`)
- **Confirmation email** — Zeptomail via `vault@faa.zone`

---

## 🔄 Integration Flow

```
Customer lands on {brand}.seedwave.faa.zone
  │
  ▼
Adds to cart → seedwave.faa.zone/checkout
  │
  ▼
Paystack payment (ZAR / multi-currency)
  │
  ▼
Cloudflare Worker (banimal-router) receives webhook
  │
  ├──► Zoho Invoice (billing record)
  ├──► Zoho CRM (customer record)
  ├──► Zoho Campaigns (welcome/nurture sequence)
  └──► Zeptomail (order confirmation email)
```

---

## 📁 Repository Structure

```text
banimal-global-loop/
├── .github/workflows/          # CI/CD: deploy Worker + sync mirror
│   ├── deploy-worker.yml       # Cloudflare Workers deployment
│   └── sync-mirror.yml         # Sync to heyns1000 parallel mirror
├── workers/banimal-router/     # Cloudflare Worker: routing + API proxy
├── catalog/                    # Product catalog
│   ├── brands/                 # Per-brand JSON configs ({brand}.json)
│   └── products/               # SKU-level product data
├── paystack/                   # Paystack webhook processor
├── zoho/                       # CRM webhooks, campaign templates
├── docs/
│   ├── ARCHITECTURE.md         # Full system diagram
│   ├── SEEDWAVE-BRANDS.md      # Brand onboarding guide
│   ├── MIRROR-SYNC.md          # heyns1000 mirror protocol
│   └── DOMAIN-DNS.md           # Cloudflare DNS records
└── README.md                   # This file
```

---

## 🪞 Parallel Mirror — `heyns1000` CodeNest

The `heyns1000` GitHub account serves as the **parallel mirror** for:

- Developer access and personal forks
- 9s Ecosystem Pulse monitoring (95 repos, 15min scan cycle)
- Branch consolidation and conflict resolution
- Baobab Bush Portal — the public-facing developer hub

**Sync protocol:** `ecosystem-sync-monitor.yml` → scans all 95 repos every 15 minutes  
**Mirror fidelity:** 99.9999% | Eternal Grid Active

---

## 🚀 Long-Term Build Plan

### Phase 1 — Foundation (Now)
- [x] `banimal-global-loop` as core backend
- [x] `banimal.faa.zone` + `banimal.co.za` live storefronts
- [x] Paystack + Zoho + Cloudflare Workers integrated
- [x] `heyns1000` mirror active with 9s Pulse
- [ ] `docs/ARCHITECTURE.md` full diagram
- [ ] `catalog/brands/` seeded with first 10 brands

### Phase 2 — Seedwave Scale (Q3 2026)
- [ ] Brand template (`payroll-mining.seedwave.faa.zone`) production-ready
- [ ] Auto-provisioning pipeline: fork → DNS → deploy → Paystack subaccount
- [ ] 50 brands live on `{brand}.seedwave.faa.zone`
- [ ] Shared analytics dashboard (samfox metrics)

### Phase 3 — 13k Brands (2027+)
- [ ] Automated brand onboarding via API
- [ ] Multi-currency checkout (ZAR, USD, EUR, GBP)
- [ ] Physical product ↔ digital twin linking (real items ↔ catalog)
- [ ] Amazon / Takealot / PriceCheck feed integrations
- [ ] Alibaba supplier chain connections
- [ ] Quantum ledger layer for brand IP and inventory provenance

### Phase 4 — Global Ecosystem
- [ ] `fruitful.faa.zone` as the global brand discovery portal
- [ ] AI-assisted brand creation and product onboarding
- [ ] Revenue sharing smart contracts per brand
- [ ] Ubuntu/Simunye community commerce model

---

## 🔧 Getting Started (Developers)

```bash
# Clone the backend
git clone https://github.com/Fruitful-Global-Planet/banimal-global-loop.git
cd banimal-global-loop

# Deploy Cloudflare Worker
cd workers/banimal-router
npx wrangler deploy

# Add a new brand
cp catalog/brands/_template.json catalog/brands/{brand}.json
# Edit {brand}.json with brand details
# Push — GitHub Actions handles DNS + deployment
```

> See `docs/SEEDWAVE-BRANDS.md` for the full brand onboarding guide.

---

## 🌍 Live Domains

| Domain | Purpose |
|--------|--------|
| `banimal.faa.zone` | Flagship Banimal storefront |
| `banimal.co.za` | SA market domain |
| `seedwave.faa.zone` | Core checkout + brand discovery |
| `{brand}.seedwave.faa.zone` | 13k brand storefronts |
| `fruitful.faa.zone` | Fruitful Global Planet portal |
| `vault@faa.zone` | Transactional email (Zeptomail) |

---

*Part of **Fruitful Shops (Pty) Ltd** — Harvesting resilient ecosystems for global change. Ubuntu! Simunye! 🌱*

[![Mirror: heyns1000](https://img.shields.io/badge/mirror-heyns1000-blue)](https://github.com/heyns1000)
[![Org: Fruitful-Global-Planet](https://img.shields.io/badge/org-Fruitful--Global--Planet-green)](https://github.com/Fruitful-Global-Planet)
[![Checkout: seedwave.faa.zone](https://img.shields.io/badge/checkout-seedwave.faa.zone-orange)](https://seedwave.faa.zone)
