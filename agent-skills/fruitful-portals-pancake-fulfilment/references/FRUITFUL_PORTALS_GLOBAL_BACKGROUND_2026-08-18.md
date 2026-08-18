# Fruitful Portals — Global Background & Amazon Distribution Model

**Owner:** Fruitful Shops (Pty) Ltd — © 2026. All rights reserved.
**Status:** v1 — 18 Aug 2026 · Canonical background for the Fruitful Portals fulfilment task
**FRUITFUL™ · Banimal Giving Loop™ · Golden Ticket Menu™**

---

## 1. What Fruitful is

Fruitful is a **tech company** (not the Banimal store, not a craft shop). It sells subscriptions and licensing of ecosystem metadata — the chain is **sector → core brand → subnode** — and runs a "Support a Local" activation layer pairing licenses with artisan products (Banimal babygrows/bibs, Margaret/Fruitful Kids, Sam Fox Illustrates, Grand Machadlela). The **pancake line is the physical flagship** that funds the mission: every item sold triggers the Banimal Giving Loop™ — 1 fresh pancake to a child in need per item (R0.75 direct cost).

**Entities:** Fruitful Shops (Pty) Ltd — CIPC 2021/121654/07 · VAT 4400302974 · Fruitful Holdings (Pty) Ltd — CIPC 2020/038051/07 (per Addendum; NDA cover shows 2025/015799/07 — attorney to reconcile).

## 2. The Global Portals (ecosystem map)

| Portal | Role | Notes |
|---|---|---|
| **fruitful.co** | Master portal hub (confirmed DNS) | Brand identity: Teal #47B3A8 · Red #E63946 · Amber #FFB703, Inter/Fira Code |
| **www.banimal.co.za** | Live Banimal storefront | Vite/React SPA on Vercel; Paystack checkout; free SA shipping; Roleplay™ products (BOX/BOWL/WHARE/SLAMB); samfox_illustrate™ licensed art |
| **{brand}.seedwave.faa.zone** | Sub-domain storefront architecture | 13,713 brands in LicenseVault (backend); ecosystem-v2 49 sectors / 6,548 brands / 6,227 subnodes |
| **Marketplace** | Claude-designed storefront set | 16 design pages; data/ecosystem.json; banimal.json (22 products); margaret.json (12 pieces) |
| **VaultMesh / LicenseVault** | Brand licensing + vault infrastructure | 9s PulseGrid™ sync; FPSL v1.0 license; heyns1000 mirror (95+ repos) |
| **Repo** | github.com/fruitful-global-planet/Banimal-global-loop.git | Branch `Fruitful_Portals_accio` active; bushcoding.git backend pending |

**Commerce stack (live):** Order → Paystack → signature-verified webhook → Zoho Invoice + Zoho CRM + Zoho Campaigns + Zeptomail → BobGo fulfilment. 15.01% of every order → Banimal Giving Loop.

## 3. The Golden Ticket pancake line

- **Golden Ticket Menu™ (3×3+1):** 3 coffees (R40), 3 smoothies (R60), 3 pancakes, + 1 Child Ticker™ (the 10th slot is the child, not a product).
- **Milk Pannekoek (sellable):** full-size SA pannekoek (Ø 230 mm flat) — Single R15.00 · 6-box R75.00 · 12-pack R150.00. Direct costs: R3.71 / R15.66 / R44.52 (73–79% direct margin).
- **50% Golden Ticket pannekoek:** the GIVING pancake (R0.75 dead cost, not sold) — rolls at 105 × 18 × 18 mm; packs 2-per-slot in milk packaging.
- **The singularity (VIP):** one rolled milk pancake = **210 × 28 × 28 mm** (L = roll length ≈ pancake Ø − end squish; Ø = roll diameter). This single number drives ALL packaging.

## 4. Packaging system (current decisions, 18 Aug 2026)

| Pack | Container | Size (L×W×H mm) |
|---|---|---|
| 1 | **Recyclable food paper packet** (printed, greaseproof, food-grade) | flat 235 × 45 |
| 6 | Corrugated **self-lock** box (wrap sleeve slips over) | outer 232 × 210 × 40 |
| 12 | Corrugated **self-lock** box (wrap sleeve slips over) | outer 232 × 210 × 74 |
| Shipper | 8 × 12-packs, 2×2×2 | 470 × 425 × 155 |

- Layout rule: **landscape "pencil case"** — rolls lie horizontally, box height = one roll Ø, flat never high.
- 2 × 50% giving rolls end-to-end = 210 mm = exactly the milk roll length → 1 milk slot = 2 giving rolls, mixable.
- **Wrap concept:** pre-folded FRUITFUL™ brand sleeve (2 sizes: single-packet band + 6/12 box sleeve) slips over the closed container — the container closes itself, the wrap carries the brand, no side flaps needed.
- EPS moulded alternative (Isowall, 100 m from warehouse): custom moulds; slide-lid + slim-flat stock exist; densities 20/24/32 g/L (20 = cost-efficient for pancakes).

## 5. THE AMAZON DISTRIBUTION MODEL (this task's core)

**Principle: Amazon IS the supply chain.** Fruitful focuses on product + brand; Amazon does everything physical.

1. **All suppliers quote EXW (Ex Works)** — including local South African suppliers (e.g., Isowall across the street, local printers for packets/boxes). Fruitful pays the factory-gate price only; no supplier-side logistics, no incoterms beyond EXW.
2. **Amazon picks up** — inbound via Amazon Global Logistics / seller inbound placement; supplier ships to Amazon's designated pickup/inbound point (or Amazon collects), Fruitful is not the logistics operator.
3. **Amazon warehouses** — FBA (Amazon Fulfilment) and/or AWD (Amazon Warehousing & Distribution) hold inventory; storage fees apply per cubic foot/month — flat, shallow boxes (our pencil-case design) minimise storage cost.
4. **Amazon delivers (automated)** — Amazon Logistics last-mile delivery; Prime eligibility; fulfilment fee per unit applies.
5. **Amazon assembles/preps** — Amazon FBA Prep Services (bagging, labelling, boxing, bundling) and bundle/assembly programs cover "if anything needs assembly, Amazon does that" (label application, unit prep, multi-pack bundling). NOTE: complex multi-step assembly is not a core FBA service — design for prep-level assembly; verify the exact program scope with the seller account before promising complex assembly.

**Unit-economics implication:** landed cost = **EXW price + Amazon fee stack** (referral fee %, fulfilment fee/unit, monthly storage, inbound placement, optional prep/bundling). All costing must model this stack — the EXW quotes are the input; Amazon fees are the distribution layer. Verify current fee schedule (fees change annually).

**Compliance (Amazon food rules — non-negotiable):**
- Food must be **properly prepared, sealed, and packaged** to prevent spoilage/melting/damage.
- **Tamper-evident primary packaging** required (self-seal/tear-strip boxes and heat-sealed packets satisfy this).
- **FDA labeling in English**: ingredients, allergens, storage + heating instructions; **expiration date 36pt+** on the product AND the master carton.
- Packaging must withstand warehouse handling ("handling is not gentle") — corrugated E-flute min; food-grade material certification (or food-grade inner liner).
- Product stability 50–100 °F during storage.

## 6. Supplier context (intake reference)

- **Isowall (Silverton, 326 Derdepoort Rd — ~100 m from warehouse):** EPS moulded boxes — berry/cooler/cold-chain/pharma/fish/lobster/oyster; slim-flat family (Juicebar 268×120×75 ext/248×105×56 int; Collapsible 270×120×75; Box with SLIDE LID 411×310×160); densities 20/24/32 g/L; account pack = Customer Info Form (CBD) + POPI consent + T&C 2020. Contact: Steven Dry (sales rep, 18 Aug 2026 email).
- **Alibaba packaging (validated suppliers):** self-locking corrugated mailers (food-grade option, ~$0.05–0.30/pc), ear-lock cartons, self-seal adhesive tear-strip boxes, magnetic rigid boxes (230×210×40 exact match available), long slim pen-box profile for single.

## 7. Naming & documentation convention

- Files: `FRUITFUL_PORTALS_<TOPIC>_<YYYY-MM-DD>.md` · designs `FRUITFUL-[PRODUCT]-[SKU]-[FORMAT]-[VARIANT]_v[N]`
- Assets uploaded → `Assets uploaded/<YYYY-MM-DD>/` (dedup-safe; data dumps check this folder first)
- Doc family: Golden_Ticket_* (CI Guide MASTER, Pancake Box Dimension Spec, Asset Naming & IP Register, Menu, Costing 1-10, Summary, Variant Tables, Shopping Lists) in `_analysis/fruitful-portal-reqs/`
- Legal: ™ on first prominent use (Banimal Giving Loop™); **no ® until attorney confirmation**; © 2026 Fruitful Shops (Pty) Ltd footer on all assets.

---
*FRUITFUL™ · Banimal Giving Loop™ · © 2026 Fruitful Shops (Pty) Ltd · github.com/fruitful-global-planet/Banimal-global-loop.git · www.banimal.co.za · fruitful.co · fruitful.planet.change@fruitful.co*
