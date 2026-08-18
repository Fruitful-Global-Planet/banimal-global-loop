<!-- FRUITFUL PORTAL — COMMERCIAL MODEL -->
<div align="center">

# Fruitful_Portal_commercial_model.md
### Product Definition · 6 Commercial Layers · Variant Ladder

**Fruitful Shops (Pty) Ltd** · Reg. 2021/121654/07 · VAT 4400302974
Director: Heyns Schoeman · Pretoria, RSA

*"Tech meets tradition."*

</div>

---

## 0. Purpose

Defines **what the Fruitful Portal is as a commercial product**, the six commercial layers that make up its value, and the Package 1–5 variant ladder with pricing logic. This is the top of the stack: it tells the costing, markup, and finance models *what* is being priced.

> **DATA RULE:** All ZAR prices are **[TBC]** and resolve from the costing → markup → finance chain. Known physical specs come from the Welink PI and Fantastico scope; everything else is structure.

---

## 1. Product Definition

| Attribute | Specification |
|-----------|---------------|
| Product | Fruitful Portal — cylindrical, branded, self-service kiosk |
| Form | Fiberglass cylinder: roof Ø 2,050 mm · bottom Ø 1,810 mm · height 2,630 mm · 4 mm fiberglass |
| Top cap | Coral-red domed fiberglass, moulded |
| Body finish | Mint-green, smooth, weatherproof |
| Apertures | 1 service/access door (lockable) · 1 display/window aperture |
| Tech (import spec) | 1× 32" TV (window) · 1× 43" TV (kiosk) · 1× stainless cabinet 800×275×700 mm |
| Infrastructure | Pre-routed electrical conduit trunking + water inlet/drain channels (ready for fit-out) |
| Branding | Fruitful logo + tagline application; illuminated signage topper |
| Base | Plinth + levelling feet (indoor/outdoor capable) |
| Concept | Self-service portal network supporting local artisans — artisan coffee, food, curated retail |
| Positioning | Proudly South African; "Tech meets tradition" |
| IP / NDA | IP held by Fruitful Holdings (Pty) Ltd (Reg. 2020/038051/07); traded by Fruitful Shops (Pty) Ltd |

---

## 2. The Six Commercial Layers

The Portal's commercial value is assembled from six layers. Each maps to cost/markup elements downstream.

| # | Commercial Layer | What the customer gets | Maps to (cost/markup) |
|---|------------------|------------------------|------------------------|
| 1 | **Physical asset** | The fabricated/imported portal shell + structure | `FC` / shell (`LC`) |
| 2 | **Technology fit-out** | Screens, POS, router, telemetry, payments | `ELEC`, `SOFT`, `PAY` |
| 3 | **Brand & trade dress** | Fruitful identity, design, "Tech meets tradition" | `BRAND` + `m_3` brand premium |
| 4 | **Deployment & commissioning** | Delivery, install, branding application, first-power | `LTM`, `COMM`, `BRAND` |
| 5 | **Finance & ownership model** | Cash / financed / rental / RTO / subscription | finance model (`FP`, `MI`) |
| 6 | **Operator support & SLA** | Onboarding, training, maintenance, supply chain, telemetry support | `m_5` operator support loading + `SLA_m` |

---

## 3. Variant Ladder (Build Tiers)

Variants differ by **how much of layers 1–6 are included**.

| Variant | Shell source | Tech fit-out | Fit-out depth | Support level | Typical mode |
|---------|--------------|--------------|---------------|---------------|--------------|
| **Lite** | Local shell (Fantastico) | Minimal (single screen, POS) | Coffee-only | Self-support | Cash / short finance |
| **Standard** | Local or import | Dual-screen + POS + telemetry | Coffee + food | Standard SLA | Financed |
| **Plus** | Import (tech-equipped) | Full (32"+43" + cabinet) | Coffee + food + retail | Enhanced SLA | Financed / RTO |
| **Managed** | Import or local | Full + redundancy (UPS, 5G, CCTV) | Full + refrigeration | Fully managed | Rental / subscription |

\[
\text{Variant Price} = SP_{variant} \;\text{(per markup model)} \;\Rightarrow\; MI_{variant}\;\text{(per finance model)}
\]

---

## 4. Package 1–5 Product Ladder

The customer-facing packaged offers, ascending in inclusivity and price.

| Pkg | Name | Includes | Ownership | Pricing logic | Price |
|-----|------|----------|-----------|---------------|-------|
| **1** | **Shell Starter** | Portal shell only (layer 1) + brand application | Customer owns | `SP = TDC_shell × (1+m_1)(1+m_3)` — floor + brand | [TBC] |
| **2** | **Trade-Ready** | Shell + core tech + basic fit-out (layers 1–4) | Customer owns | `SP` with full markup stack, finance optional | [TBC] |
| **3** | **Financed Portal** | Package 2 + finance wrap (24–60 mo) | Customer owns (on settlement) | `FP`, `MI` per finance grid; `m_4` applied | [TBC] |
| **4** | **Rent-to-Own** | Full portal, title transfers at term end | Fruitful → customer | `MI_RTO` + residual; `m_4` + `m_5` applied | [TBC] |
| **5** | **Managed Subscription** | Full portal, fully operated by Fruitful | Fruitful retains | `MI_sub` = amortisation + INS + SLA + OPEX | [TBC] |

### 4.1 Package pricing logic chain

\[
\text{Package } k:\quad TDC_k \xrightarrow{\text{markup model}} SP_k \xrightarrow{\text{finance model}} MI_k \xrightarrow{} \text{MonthlyCustomerPrice}_k
\]

- Packages **1–2** are predominantly cash/asset sales (low/no `m_4`).
- Package **3** introduces the amortising finance grid.
- Packages **4–5** carry the highest `m_4` (finance risk) and `m_5` (operator support) loadings because Fruitful retains asset and operational exposure.

---

## 5. Reference Cost Anchors (Known)

For positioning the ladder against real cost (from `Fruitful_Portal_costing_model.md`):

| Anchor | ZAR | Source |
|--------|-----|--------|
| Imported landed unit (`LC`) | R130,929 | Welink PI WL20260325 |
| Local shell, excl. VAT | R111,500 | Fantastico SA estimate |
| Local shell, incl. VAT | R128,225 | Fantastico SA estimate |
| Units 3+ (local) | −30–40% per unit | Mould amortisation (Fantastico note) |

All package selling prices remain **[TBC]** until `TDC` (with tech/fit-out layers) and markup percentages are set.

---

## 6. Handoff

| Output | Feeds |
|--------|-------|
| Variant & package definitions | `Fruitful_Portal_costing_model.md` (what to cost) |
| Package ladder | `Fruitful_Portal_markup_model.md` & `Fruitful_Portal_finance_model.md` |
| Product catalogue structure | `Fruitful_Portal_data_model.md` (`product_catalogues`, `pricing_plans`) |
| Benchmark inputs | `Fruitful_Portal_franchise_benchmark.md` |

---

<div align="center">

**Fruitful Shops (Pty) Ltd** · Reg. 2021/121654/07 · VAT 4400302974
Proudly South African — Tech meets tradition.

*Physical specs sourced from Welink PI WL20260325 and Fantastico Addendum A scope. All prices [TBC].*

</div>
