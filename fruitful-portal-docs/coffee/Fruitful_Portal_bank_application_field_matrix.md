<!-- FRUITFUL PORTAL — BANK APPLICATION FIELD MATRIX -->
<div align="center">

# Fruitful_Portal_bank_application_field_matrix.md
### Bank Question → Backend Field → Required Document

**Fruitful Shops (Pty) Ltd** · Reg. 2021/121654/07 · VAT 4400302974
Director: Heyns Schoeman · Pretoria, RSA

</div>

---

## 0. Purpose

Maps every typical asset-finance bank application question to (a) the **backend field** that holds the answer (from `Fruitful_Portal_data_model.md`) and (b) the **required supporting document** (from `Fruitful_Portal_document_checklist.md`). Organised into the **9 standard sections** of a finance application.

> **DATA RULE:** Field references are schema-bound. Values are runtime / [TBC].

---

## Section 1 — Equipment / Asset Being Financed

| Bank Question | Backend Field | Required Document |
|---------------|---------------|------------------|
| What is being financed? | `portal_assets.variant`, `.serial_number` | Proforma invoice / quote |
| Supplier name & details | `portal_assets.supplier` | Welink PI WL20260325 / Fantastico quote |
| Equipment cost (ex-VAT) | `portal_assets.landed_cost_lc` / `tdc` | PI (R130,929 landed) / Fantastico (R111,500) |
| New or used? | `portal_assets.build_status` | PI / quote |
| Useful life / depreciation | `portal_assets` (spec) | Spec sheet |
| Delivery / installation address | `portal_sites.address` | Site/lease document |

---

## Section 2 — Entity / Applicant Profile

| Bank Question | Backend Field | Required Document |
|---------------|---------------|------------------|
| Registered entity name | `applicants.entity_name` | CIPC registration cert |
| Company registration number | `applicants.entity_reg_number` | CIPC CoR docs |
| VAT registration number | `applicants.vat_number` | SARS VAT103 / VAT cert |
| Tax / income tax number | `operators.entity_reg_number` (tax) | SARS tax confirmation |
| Entity type | `applicants.applicant_type` | CIPC docs |
| Date of incorporation | (applicant profile) | CIPC registration cert |
| Physical & registered address | `applicants.physical_address` | Proof of address / CIPC |
| Nature of business | `operators.operator_name` (profile) | Business profile |

---

## Section 3 — Banking Details

| Bank Question | Backend Field | Required Document |
|---------------|---------------|------------------|
| Bank name & branch | `operators.banking_ref` | Bank confirmation letter |
| Account number & type | `documents` (bank confirmation) | Stamped bank letter |
| Account holder name | `operators.entity_name` | Bank confirmation |
| Bank statements (3–6 months) | `documents` (doc_category=bank_statement) | 3–6 months statements |
| Existing facilities / loans | `finance_applications` (history) | Statements / credit profile |

---

## Section 4 — Insurance

| Bank Question | Backend Field | Required Document |
|---------------|---------------|------------------|
| Asset insured? | `finance_applications.affordability_result` (flag) | Insurance policy schedule |
| Insurer & policy number | `documents` (doc_category=insurance) | Policy document |
| Sum insured = asset value? | `portal_assets.tdc` vs sum insured | Policy schedule |
| Bank noted as interested party? | `contracts` (clause) | Endorsement letter |
| Public liability cover | `documents` (insurance) | Public liability policy |

---

## Section 5 — Landlord / Site

| Bank Question | Backend Field | Required Document |
|---------------|---------------|------------------|
| Trading location secured? | `portal_sites.status` | Lease agreement |
| Landlord name & contact | `portal_sites.landlord_name` / `.landlord_contact` | Lease |
| Lease term & rent | `portal_sites.lease_ref` | Signed lease |
| Site consent for placement | `documents` (doc_category=lease/permit) | Landlord consent letter |
| Municipal trading permit | `portal_sites.trading_permit_ref` | Trading permit |

---

## Section 6 — Directors / Principals

| Bank Question | Backend Field | Required Document |
|---------------|---------------|------------------|
| Director full name(s) | `applicants.full_name` | ID document |
| Director ID number | `applicants.id_number` | SA ID / passport |
| Date of birth | `applicants.date_of_birth` | ID |
| Residential address | `applicants.physical_address` | Proof of address |
| Director contact details | `applicants.email` / `.cell` | — |
| Director surety / personal guarantee | `contracts` (surety clause) | Signed suretyship |
| Director credit consent | `finance_applications.consent_id` | Signed credit-check consent |

---

## Section 7 — References

| Bank Question | Backend Field | Required Document |
|---------------|---------------|------------------|
| Trade references | `operators` (references json) | Reference letters |
| Bank reference | `operators.banking_ref` | Bank reference letter |
| Supplier reference | `portal_assets.supplier` | Supplier confirmation |
| Existing client/landlord reference | `portal_sites.landlord_contact` | Reference contact |

---

## Section 8 — Consents & Declarations

| Bank Question | Backend Field | Required Document |
|---------------|---------------|------------------|
| Consent to credit check | `consents` (type=credit_check) | Signed consent form |
| POPIA data-processing consent | `consents` (type=data_processing) | POPIA consent |
| Declaration of accuracy | `finance_applications.status` | Signed declaration |
| Source of funds / deposit declaration | `finance_applications.deposit_d` | Declaration |
| FICA verification | `documents` (id + proof of address) | FICA pack |

---

## Section 9 — Supporting Documents (Financials)

| Bank Question | Backend Field | Required Document |
|---------------|---------------|------------------|
| Annual financial statements | `documents` (doc_category=financials) | AFS (latest 1–2 years) |
| Management accounts | `documents` (financials) | Recent management accounts |
| Cash-flow projection | `finance_applications.affordability_result` | Cash-flow forecast |
| Affordability / break-even | finance model §9 (`T_BE`, `GPP`) | Business plan / projections |
| Business plan | `documents` (other) | Fruitful Portal business plan |
| Proforma / quote | `portal_assets.supplier_invoice_ref` | Welink PI / Fantastico quote |

---

## 10. Cross-Reference Map

| Section | Primary entity | Doc checklist link |
|---------|----------------|--------------------|
| 1 Equipment | `portal_assets` | PI/quote |
| 2 Entity | `applicants` | CIPC, VAT cert |
| 3 Banking | `operators`, `documents` | Bank statements |
| 4 Insurance | `documents` | Insurance policy |
| 5 Landlord | `portal_sites` | Lease, permit |
| 6 Directors | `applicants` | IDs, suretyship |
| 7 References | `operators` | Reference letters |
| 8 Consents | `consents` | Signed declarations |
| 9 Supporting | `documents`, `finance_applications` | Financials, business plan |

---

<div align="center">

**Fruitful Shops (Pty) Ltd** · Reg. 2021/121654/07 · VAT 4400302974
Proudly South African — Tech meets tradition.

*Field names bind to `Fruitful_Portal_data_model.md`. Documents listed in `Fruitful_Portal_document_checklist.md`.*

</div>
