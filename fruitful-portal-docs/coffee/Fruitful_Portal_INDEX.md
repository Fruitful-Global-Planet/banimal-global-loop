<!-- FRUITFUL PORTAL — MASTER INDEX -->
<div align="center">

# Fruitful_Portal_INDEX.md
### Master Index — Fruitful Portal Deliverable Pack

**Fruitful Shops (Pty) Ltd** · Reg. 2021/121654/07 · VAT 4400302974
**Fruitful Holdings (Pty) Ltd** · Reg. 2020/038051/07 (IP / Master NDA)
Director: Heyns Schoeman · Pretoria, RSA

*"Tech meets tradition."*

</div>

---

## 0. Pack Overview

A 10-file commercial, costing, finance and onboarding system for the **Fruitful Portal** — a cylindrical, branded, self-service kiosk supporting artisan coffee, food and curated retail. All files share the `Fruitful_Portal_` prefix and are linked by a single formula chain.

**Formula chain:**
\[
FC \rightarrow CIF \rightarrow LC \rightarrow TDC \rightarrow SP \rightarrow FP \rightarrow MI \rightarrow \text{MonthlyCustomerPrice}
\]

**Known cost anchors:** Imported landed `LC` = **R130,929** (Welink PI WL20260325) · Local shell = **R111,500 excl. VAT** (Fantastico SA). All other monetary values **[TBC]**.

---

## 1. File Index

| # | File | One-line description |
|---|------|----------------------|
| 1 | **Fruitful_Portal_commercial_model.md** | Product definition, 6 commercial layers, variant ladder, and the Package 1–5 product ladder with pricing logic. |
| 2 | **Fruitful_Portal_costing_model.md** | Full cost variable dictionary and FC→CIF→LC→TDC build-up for imported (Welink) and local (Fantastico) streams. |
| 3 | **Fruitful_Portal_finance_model.md** | Cash, financed (24/36/48/60-month grid), rental, rent-to-own and subscription modes; monthly price stack; break-even, GPP and LTV. |
| 4 | **Fruitful_Portal_markup_model.md** | The 5 markup layers with ranges and a decision-logic table; the SP = TDC × markup formula with worked structure. |
| 5 | **Fruitful_Portal_bank_application_field_matrix.md** | Bank question → backend field → required document across all 9 application sections. |
| 6 | **Fruitful_Portal_operator_application_pack.md** | Complete operator onboarding form with a clear bank-mandatory vs Fruitful-internal field split. |
| 7 | **Fruitful_Portal_data_model.md** | All 10 backend entities (applicants, portal_assets, portal_sites, operators, finance_applications, contracts, documents, maintenance_logs, product_catalogues, pricing_plans) plus consent architecture. |
| 8 | **Fruitful_Portal_franchise_benchmark.md** | Fruitful Portal vs traditional franchise kiosk comparison, highlighting financeability and mobility advantages. |
| 9 | **Fruitful_Portal_document_checklist.md** | Every required document — CIPC, VAT cert, IDs, bank statements, financials, PI/quote, insurance, site consent, signed declarations. |
| 10 | **Fruitful_Portal_INDEX.md** | This master index of all 10 files. |

---

## 2. How the Files Connect

```
commercial_model ──(what to price)──> costing_model ──(TDC)──> markup_model ──(SP)──> finance_model ──(FP, MI)
        │                                   │                        │                      │
        └───────────────> data_model <──────┴────────────────────────┴──────────────────────┘
                                 │
       bank_application_field_matrix ──> operator_application_pack ──> document_checklist
                                 │
                        franchise_benchmark (positioning)
```

---

## 3. Source & Integrity Notes

| Aspect | Detail |
|--------|--------|
| Imported cost source | Guangzhou Welink Technology Co., Ltd — PI No. WL20260325 (25 Mar 2026), USD 3,800 EXW → R130,929 landed JHB; FX R16.32/USD |
| Local cost source | Fantastico SA budgetary estimate per Addendum A (FHL-NDA-ADDENDUM-A-v2) — R111,500 excl. VAT / R128,225 incl. VAT |
| Duty assumption | Blended 20% (HS 9403.20 / 8543.70), clearing-agent dependent (0–20%) |
| Unknown values | Marked **[TBC]** — never assumed or estimated |
| Entities | Trading: Fruitful Shops (Pty) Ltd · IP/NDA: Fruitful Holdings (Pty) Ltd |
| IP framework | Fruitful Holdings Master NDA + Addendum A bind both Associated Companies |

---

<div align="center">

**Fruitful Shops (Pty) Ltd** · Reg. 2021/121654/07 · VAT 4400302974
31 Laurel Valley Street, Silver Lakes Golf Estate, Pretoria, 0081
Proudly South African — Tech meets tradition.

</div>
