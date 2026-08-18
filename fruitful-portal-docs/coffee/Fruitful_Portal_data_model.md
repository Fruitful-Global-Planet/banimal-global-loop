<!-- FRUITFUL PORTAL — DATA MODEL -->
<div align="center">

# Fruitful_Portal_data_model.md
### Backend Data Model · 10 Entities · Consent Architecture

**Fruitful Shops (Pty) Ltd** · Reg. 2021/121654/07 · VAT 4400302974
Director: Heyns Schoeman · Pretoria, RSA

</div>

---

## 0. Purpose

Defines the **10 backend entities** that hold every field the Fruitful Portal platform needs — from applicant intake through finance, contracts, assets, sites, maintenance, catalogues and pricing. Field types follow a simple convention; relationships and consent architecture (POPIA-aligned) are included.

> **DATA RULE:** This is a schema specification. Concrete data values are runtime; any sample defaults are [TBC].

**Type legend:** `uuid` · `string` · `text` · `int` · `decimal` · `bool` · `date` · `datetime` · `enum{...}` · `fk→entity` · `json`

---

## 1. `applicants`

Prospective operators/buyers at intake (pre-finance).

| Field | Type | Notes |
|-------|------|-------|
| applicant_id | uuid (PK) | |
| full_name | string | |
| id_number | string | SA ID / passport |
| date_of_birth | date | |
| email | string | |
| cell | string | |
| physical_address | text | |
| entity_name | string | if applying as company |
| entity_reg_number | string | CIPC reg |
| vat_number | string | nullable |
| applicant_type | enum{individual, company, partnership} | |
| source_channel | string | lead origin |
| status | enum{new, screening, qualified, rejected, converted} | |
| consent_id | fk→consents | links consent record |
| created_at | datetime | |
| updated_at | datetime | |

---

## 2. `portal_assets`

Every physical Fruitful Portal unit.

| Field | Type | Notes |
|-------|------|-------|
| asset_id | uuid (PK) | |
| serial_number | string | unique unit ID |
| variant | enum{lite, standard, plus, managed} | from commercial model |
| stream | enum{imported, local} | Welink vs Fantastico |
| supplier | string | "Welink" / "Fantastico SA" |
| supplier_invoice_ref | string | e.g. WL20260325 |
| factory_cost_fc | decimal | `FC` |
| landed_cost_lc | decimal | `LC` |
| total_deployment_cost_tdc | decimal | `TDC` [TBC] |
| spec_roof_dia_mm | int | 2050 |
| spec_bottom_dia_mm | int | 1810 |
| spec_height_mm | int | 2630 |
| build_status | enum{ordered, in_production, in_transit, landed, fit_out, deployed, retired} | |
| current_site_id | fk→portal_sites | nullable |
| owner_entity | enum{fruitful, operator} | depends on finance mode |
| created_at | datetime | |
| updated_at | datetime | |

---

## 3. `portal_sites`

Deployment locations.

| Field | Type | Notes |
|-------|------|-------|
| site_id | uuid (PK) | |
| site_name | string | |
| address | text | |
| gps_lat | decimal | |
| gps_lng | decimal | |
| site_type | enum{mall, transit, street, campus, event, other} | |
| foot_traffic_band | enum{low, medium, high} | |
| landlord_name | string | |
| landlord_contact | string | |
| lease_ref | fk→documents | lease agreement |
| trading_permit_ref | fk→documents | municipal permit |
| utilities_available | json | power/water flags |
| status | enum{prospect, secured, live, vacated} | |
| created_at | datetime | |

---

## 4. `operators`

Confirmed operators running portals (converted applicants).

| Field | Type | Notes |
|-------|------|-------|
| operator_id | uuid (PK) | |
| applicant_id | fk→applicants | origin |
| operator_name | string | |
| entity_name | string | |
| entity_reg_number | string | |
| vat_number | string | nullable |
| primary_contact | string | |
| email | string | |
| cell | string | |
| banking_ref | fk→documents | bank confirmation |
| onboarding_status | enum{pending, training, active, suspended, exited} | |
| sla_tier | enum{self, standard, enhanced, managed} | from `m_5` level |
| assigned_assets | json[fk→portal_assets] | |
| created_at | datetime | |
| updated_at | datetime | |

---

## 5. `finance_applications`

Credit/finance requests per deal.

| Field | Type | Notes |
|-------|------|-------|
| finance_app_id | uuid (PK) | |
| applicant_id | fk→applicants | |
| asset_id | fk→portal_assets | |
| pricing_plan_id | fk→pricing_plans | |
| mode | enum{cash, financed, rental, rent_to_own, subscription} | |
| selling_price_sp | decimal | `SP` [TBC] |
| deposit_d | decimal | `D` [TBC] |
| term_months | int | 24/36/48/60 |
| interest_rate_i | decimal | `i` [TBC] |
| monthly_instalment_mi | decimal | `MI` [TBC] |
| financed_price_fp | decimal | `FP` [TBC] |
| bank_name | string | financing bank |
| bank_app_ref | string | |
| affordability_result | json | break-even / income test |
| status | enum{draft, submitted, approved, declined, funded} | |
| consent_id | fk→consents | credit-check consent |
| created_at | datetime | |

---

## 6. `contracts`

Signed agreements.

| Field | Type | Notes |
|-------|------|-------|
| contract_id | uuid (PK) | |
| operator_id | fk→operators | |
| finance_app_id | fk→finance_applications | |
| asset_id | fk→portal_assets | |
| site_id | fk→portal_sites | |
| contract_type | enum{sale, finance, rental, rto, subscription, franchise} | |
| start_date | date | |
| end_date | date | |
| residual_value_rv | decimal | nullable |
| signed_by_operator | bool | |
| signed_by_fruitful | bool | |
| nda_addendum_ref | string | FHL-NDA-ADDENDUM-A-v2 lineage |
| document_ref | fk→documents | signed PDF |
| status | enum{draft, active, completed, terminated, breached} | |
| created_at | datetime | |

---

## 7. `documents`

All uploaded/generated documents (KYC, finance, legal, compliance).

| Field | Type | Notes |
|-------|------|-------|
| document_id | uuid (PK) | |
| owner_type | enum{applicant, operator, asset, site, contract, finance_app} | |
| owner_id | uuid | polymorphic FK |
| doc_category | enum{id, cipc, vat_cert, bank_statement, financials, pi_quote, insurance, lease, permit, declaration, consent, other} | |
| doc_name | string | |
| file_url | string | secure storage |
| issued_date | date | |
| expiry_date | date | nullable |
| verified | bool | |
| verified_by | string | |
| created_at | datetime | |

---

## 8. `maintenance_logs`

Service, repair and SLA event records.

| Field | Type | Notes |
|-------|------|-------|
| log_id | uuid (PK) | |
| asset_id | fk→portal_assets | |
| operator_id | fk→operators | |
| event_type | enum{inspection, repair, part_replacement, telemetry_alert, cleaning, incident} | |
| description | text | |
| part_ref | string | nullable (spares) |
| cost | decimal | |
| sla_breach | bool | |
| reported_at | datetime | |
| resolved_at | datetime | nullable |
| technician | string | |
| status | enum{open, in_progress, resolved, escalated} | |

---

## 9. `product_catalogues`

Sellable goods per portal (coffee, food, retail) — from inventory registry.

| Field | Type | Notes |
|-------|------|-------|
| product_id | uuid (PK) | |
| sku | string | |
| name | string | e.g. "Branded Paper Cup 8oz" |
| category | enum{ingredient, packaging, hygiene, it_security, maintenance, compliance, admin, hr_ppe, logistics, retail, beverage, food} | |
| uom | string | kg/L/unit/pack |
| cost_type | enum{variable, fixed, asset, facility, tool, repair, legal, finance, admin, hr, logistics} | from registry |
| reorder_threshold | int | |
| reorder_freq | enum{daily, weekly, monthly, quarterly, semi-annual, annual, as_needed, permanent} | |
| unit_cost | decimal | [TBC] |
| sell_price | decimal | [TBC] |
| active | bool | |

---

## 10. `pricing_plans`

Reusable pricing/finance templates linking commercial → finance.

| Field | Type | Notes |
|-------|------|-------|
| pricing_plan_id | uuid (PK) | |
| plan_name | string | e.g. "Package 3 — Financed 48mo" |
| package_no | int | 1–5 (commercial model) |
| variant | enum{lite, standard, plus, managed} | |
| mode | enum{cash, financed, rental, rent_to_own, subscription} | |
| tdc_basis | decimal | `TDC` [TBC] |
| markup_m1..m5 | json | five layer percentages [TBC] |
| selling_price_sp | decimal | `SP` [TBC] |
| term_months | int | nullable |
| interest_rate_i | decimal | [TBC] |
| monthly_price | decimal | MonthlyCustomerPrice [TBC] |
| active | bool | |
| created_at | datetime | |

---

## 11. Entity Relationship Summary

```
applicants ──< finance_applications >── portal_assets ──< maintenance_logs
     │                  │                      │
     └──> operators ──< contracts >── portal_sites
                          │
                  pricing_plans ──> product_catalogues
     all ──< documents >──  all ──< consents >── (consent architecture)
```

---

## 12. Consent Architecture (POPIA-aligned)

| Field | Type | Notes |
|-------|------|-------|
| consent_id | uuid (PK) | |
| subject_id | uuid | applicant/operator |
| consent_type | enum{kyc, credit_check, marketing, data_processing, telemetry, third_party_share} | |
| purpose | text | explicit purpose statement |
| granted | bool | |
| granted_at | datetime | |
| withdrawn_at | datetime | nullable |
| legal_basis | enum{consent, contract, legal_obligation, legitimate_interest} | |
| retention_period | string | e.g. 7-year archive (per registry) |
| nda_lineage | string | Fruitful Holdings Master NDA / Addendum A |

**Principles:** purpose limitation · explicit consent for credit checks · withdrawal supported · 7-year document retention (per inventory registry) · IP/confidential data governed by Fruitful Holdings Master NDA and Addendum A.

---

<div align="center">

**Fruitful Shops (Pty) Ltd** · Reg. 2021/121654/07 · VAT 4400302974
Proudly South African — Tech meets tradition.

</div>
