<!-- FRUITFUL PORTAL — OPERATOR APPLICATION PACK -->
<div align="center">

# Fruitful_Portal_operator_application_pack.md
### Operator Onboarding Form · Bank-Mandatory vs Fruitful-Internal

**Fruitful Shops (Pty) Ltd** · Reg. 2021/121654/07 · VAT 4400302974
Director: Heyns Schoeman · Pretoria, RSA

</div>

---

## 0. Purpose

The complete intake form for a prospective Fruitful Portal operator. Each field is tagged:

- **[BANK]** = bank-mandatory (also required for finance application — see `Fruitful_Portal_bank_application_field_matrix.md`)
- **[FRUITFUL]** = Fruitful-internal (operational / suitability, not required by the bank)

> **DATA RULE:** This is a blank form specification. Applicant-entered values are runtime.

---

## Part A — Applicant Identity

| # | Field | Tag | Backend field |
|---|-------|-----|---------------|
| A1 | Full legal name | **[BANK]** | `applicants.full_name` |
| A2 | ID / passport number | **[BANK]** | `applicants.id_number` |
| A3 | Date of birth | **[BANK]** | `applicants.date_of_birth` |
| A4 | Residential address | **[BANK]** | `applicants.physical_address` |
| A5 | Email | **[BANK]** | `applicants.email` |
| A6 | Cell number | **[BANK]** | `applicants.cell` |
| A7 | Preferred language | [FRUITFUL] | — |
| A8 | How did you hear about Fruitful? | [FRUITFUL] | `applicants.source_channel` |

---

## Part B — Business Entity

| # | Field | Tag | Backend field |
|---|-------|-----|---------------|
| B1 | Applying as individual or company? | **[BANK]** | `applicants.applicant_type` |
| B2 | Registered entity name | **[BANK]** | `applicants.entity_name` |
| B3 | CIPC registration number | **[BANK]** | `applicants.entity_reg_number` |
| B4 | VAT number (if registered) | **[BANK]** | `applicants.vat_number` |
| B5 | SARS income tax number | **[BANK]** | `documents` (tax) |
| B6 | Date of incorporation | **[BANK]** | applicant profile |
| B7 | Business address | **[BANK]** | `applicants.physical_address` |
| B8 | Number of existing businesses owned | [FRUITFUL] | — |

---

## Part C — Banking & Financial

| # | Field | Tag | Backend field |
|---|-------|-----|---------------|
| C1 | Bank name & branch | **[BANK]** | `operators.banking_ref` |
| C2 | Account number & type | **[BANK]** | `documents` (bank) |
| C3 | 3–6 months bank statements | **[BANK]** | `documents` (bank_statement) |
| C4 | Annual financial statements | **[BANK]** | `documents` (financials) |
| C5 | Existing loans / facilities | **[BANK]** | `finance_applications` |
| C6 | Available deposit amount | **[BANK]** | `finance_applications.deposit_d` |
| C7 | Monthly disposable income/cash | **[BANK]** | affordability |
| C8 | Estimated personal net worth | [FRUITFUL] | — |

---

## Part D — Finance Preference

| # | Field | Tag | Backend field |
|---|-------|-----|---------------|
| D1 | Acquisition mode (cash/financed/rental/RTO/subscription) | **[BANK]** | `finance_applications.mode` |
| D2 | Preferred term (24/36/48/60) | **[BANK]** | `finance_applications.term_months` |
| D3 | Package selection (1–5) | [FRUITFUL] | `pricing_plans.package_no` |
| D4 | Variant (lite/standard/plus/managed) | [FRUITFUL] | `portal_assets.variant` |

---

## Part E — Site / Location

| # | Field | Tag | Backend field |
|---|-------|-----|---------------|
| E1 | Proposed trading location | **[BANK]** | `portal_sites.address` |
| E2 | Site type (mall/transit/street/campus) | [FRUITFUL] | `portal_sites.site_type` |
| E3 | Landlord name & contact | **[BANK]** | `portal_sites.landlord_name` |
| E4 | Lease / site consent secured? | **[BANK]** | `portal_sites.lease_ref` |
| E5 | Municipal trading permit status | **[BANK]** | `portal_sites.trading_permit_ref` |
| E6 | Estimated foot traffic | [FRUITFUL] | `portal_sites.foot_traffic_band` |
| E7 | Power & water availability | [FRUITFUL] | `portal_sites.utilities_available` |

---

## Part F — Operating Experience (Fruitful-Internal)

| # | Field | Tag | Backend field |
|---|-------|-----|---------------|
| F1 | Prior retail/coffee/food experience | [FRUITFUL] | operator profile |
| F2 | Hours available to operate | [FRUITFUL] | — |
| F3 | Will you operate or employ staff? | [FRUITFUL] | — |
| F4 | Number of portals sought | [FRUITFUL] | — |
| F5 | Growth intentions (1/3/5 year) | [FRUITFUL] | — |

---

## Part G — Insurance

| # | Field | Tag | Backend field |
|---|-------|-----|---------------|
| G1 | Will asset be insured? | **[BANK]** | `documents` (insurance) |
| G2 | Insurer name / quote | **[BANK]** | `documents` (insurance) |
| G3 | Public liability cover | **[BANK]** | `documents` (insurance) |

---

## Part H — Consents & Declarations

| # | Field | Tag | Backend field |
|---|-------|-----|---------------|
| H1 | Consent to credit check | **[BANK]** | `consents` (credit_check) |
| H2 | POPIA data-processing consent | **[BANK]** | `consents` (data_processing) |
| H3 | Declaration of accuracy (signed) | **[BANK]** | `finance_applications.status` |
| H4 | Acceptance of Fruitful operator terms | [FRUITFUL] | `contracts` |
| H5 | NDA / confidentiality acknowledgement | [FRUITFUL] | `contracts.nda_addendum_ref` |
| H6 | Marketing consent (optional) | [FRUITFUL] | `consents` (marketing) |

---

## Part I — Required Attachments

(See full list in `Fruitful_Portal_document_checklist.md`.)

| # | Attachment | Tag |
|---|-----------|-----|
| I1 | Certified ID copy | **[BANK]** |
| I2 | CIPC registration documents | **[BANK]** |
| I3 | VAT registration certificate | **[BANK]** |
| I4 | 3–6 months bank statements | **[BANK]** |
| I5 | Annual financial statements | **[BANK]** |
| I6 | Proforma invoice / quote | **[BANK]** |
| I7 | Insurance quote/policy | **[BANK]** |
| I8 | Site lease / consent | **[BANK]** |
| I9 | Signed consent & declaration forms | **[BANK]** |
| I10 | Proof of address | **[BANK]** |
| I11 | Business plan / projections | [FRUITFUL] |

---

## J. Bank-Mandatory vs Fruitful-Internal — Summary Split

| Category | **[BANK]** fields | [FRUITFUL] fields |
|----------|-------------------|-------------------|
| Identity | A1–A6 | A7–A8 |
| Entity | B1–B7 | B8 |
| Banking/Financial | C1–C7 | C8 |
| Finance preference | D1–D2 | D3–D4 |
| Site | E1, E3–E5 | E2, E6–E7 |
| Experience | — | F1–F5 |
| Insurance | G1–G3 | — |
| Consents | H1–H3 | H4–H6 |
| Attachments | I1–I10 | I11 |

**Rule:** Every **[BANK]** field must be complete and evidenced before a finance application is submitted. **[FRUITFUL]** fields drive operator suitability, package/variant fit, and SLA tier — they do not block the bank submission but do gate Fruitful's approval to onboard.

---

<div align="center">

**Fruitful Shops (Pty) Ltd** · Reg. 2021/121654/07 · VAT 4400302974
Proudly South African — Tech meets tradition.

</div>
