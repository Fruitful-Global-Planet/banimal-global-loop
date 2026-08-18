<!-- FRUITFUL PORTAL — DOCUMENT CHECKLIST -->
<div align="center">

# Fruitful_Portal_document_checklist.md
### Master Document Checklist — Operator & Finance Application

**Fruitful Shops (Pty) Ltd** · Reg. 2021/121654/07 · VAT 4400302974
Director: Heyns Schoeman · Pretoria, RSA

</div>

---

## 0. Purpose

Every document required to onboard an operator and submit a finance application. Each row maps to the bank section (`Fruitful_Portal_bank_application_field_matrix.md`) and the backend `documents.doc_category` (`Fruitful_Portal_data_model.md`).

**Status legend:** ☐ outstanding · ☑ received · ⚠ expiring

---

## 1. Entity & Registration Documents

| ☐ | Document | doc_category | Bank section | Notes |
|---|----------|--------------|--------------|-------|
| ☐ | CIPC registration certificate (CoR 14.3) | cipc | 2 | Entity proof |
| ☐ | CIPC director/shareholder docs (CoR 14.1/15.1) | cipc | 2, 6 | Directors |
| ☐ | VAT registration certificate (VAT103) | vat_cert | 2 | If VAT-registered |
| ☐ | SARS income tax confirmation | other | 2, 9 | Tax number |
| ☐ | SARS tax clearance / good-standing PIN | other | 9 | If required by bank |
| ☐ | Business profile / company overview | other | 2 | Nature of business |

---

## 2. Director / Principal Documents

| ☐ | Document | doc_category | Bank section | Notes |
|---|----------|--------------|--------------|-------|
| ☐ | Certified ID copy (each director) | id | 6 | SA ID / passport |
| ☐ | Proof of residential address (<3 months) | other | 6 | FICA |
| ☐ | Signed personal suretyship | declaration | 6 | If bank requires |
| ☐ | Director credit-check consent | consent | 6, 8 | Signed |

---

## 3. Banking & Financial Documents

| ☐ | Document | doc_category | Bank section | Notes |
|---|----------|--------------|--------------|-------|
| ☐ | Bank confirmation letter (stamped) | bank_statement | 3 | Account verification |
| ☐ | Bank statements — 3 to 6 months | bank_statement | 3 | All accounts |
| ☐ | Annual financial statements (1–2 yrs) | financials | 9 | If trading |
| ☐ | Management accounts (recent) | financials | 9 | If available |
| ☐ | Cash-flow projection | financials | 9 | Forward-looking |
| ☐ | Existing loan/facility statements | financials | 3 | Disclose obligations |

---

## 4. Asset / Equipment Documents

| ☐ | Document | doc_category | Bank section | Notes |
|---|----------|--------------|--------------|-------|
| ☐ | Proforma invoice — Welink (WL20260325) | pi_quote | 1 | Imported stream (R130,929 landed) |
| ☐ | Fantastico SA fabrication quote | pi_quote | 1 | Local stream (R111,500 excl. VAT) |
| ☐ | Asset specification sheet | pi_quote | 1 | Dimensions/material |
| ☐ | Delivery / installation confirmation | other | 1 | Site address |

---

## 5. Insurance Documents

| ☐ | Document | doc_category | Bank section | Notes |
|---|----------|--------------|--------------|-------|
| ☐ | Asset insurance policy/schedule | insurance | 4 | Sum insured ≥ asset value |
| ☐ | Public liability insurance | insurance | 4 | Trading cover |
| ☐ | Bank interested-party endorsement | insurance | 4 | Bank noted on policy |

---

## 6. Site & Landlord Documents

| ☐ | Document | doc_category | Bank section | Notes |
|---|----------|--------------|--------------|-------|
| ☐ | Signed lease agreement | lease | 5 | Term & rent |
| ☐ | Landlord consent for portal placement | lease | 5 | Site consent |
| ☐ | Municipal trading permit | permit | 5 | Location-specific |
| ☐ | Site/utilities confirmation | other | 5 | Power & water |

---

## 7. Compliance & Legal Documents

| ☐ | Document | doc_category | Bank section | Notes |
|---|----------|--------------|--------------|-------|
| ☐ | Fire safety certificate | other | 5 | Per site |
| ☐ | Food handler medical clearance | other | — | If food/coffee |
| ☐ | Health & Safety Act compliance register | other | — | Operational |
| ☐ | COIDA / Workmen's Comp registration | other | — | If employing |
| ☐ | Hazardous substances / MSDS register | other | — | Cleaning chemicals |

---

## 8. Consents & Declarations

| ☐ | Document | doc_category | Bank section | Notes |
|---|----------|--------------|--------------|-------|
| ☐ | Credit-check consent (signed) | consent | 8 | NCA |
| ☐ | POPIA data-processing consent | consent | 8 | Data privacy |
| ☐ | Declaration of accuracy (signed) | declaration | 8 | Application truth |
| ☐ | Source-of-funds / deposit declaration | declaration | 8 | Deposit origin |
| ☐ | FICA verification pack | other | 8 | ID + address |
| ☐ | NDA / confidentiality acknowledgement | declaration | — | Fruitful Holdings Master NDA / Addendum A |
| ☐ | Operator terms acceptance | declaration | — | Fruitful-internal |

---

## 9. Supporting / Fruitful-Internal

| ☐ | Document | doc_category | Bank section | Notes |
|---|----------|--------------|--------------|-------|
| ☐ | Fruitful Portal business plan | other | 9 | Projections |
| ☐ | Break-even / affordability worksheet | financials | 9 | Finance model §9 |
| ☐ | Trade / bank / supplier references | other | 7 | Reference letters |
| ☐ | Package & variant selection sheet | other | — | Commercial model |

---

## 10. Completeness Gate

| Gate | Requirement |
|------|-------------|
| **Bank submission gate** | All ☑ in Sections 1–6, 8 (bank-mandatory rows) |
| **Fruitful onboarding gate** | Bank gate + Section 9 + NDA acknowledgement |
| **Funding gate** | Bank approval + signed contract (`contracts` entity) |

---

<div align="center">

**Fruitful Shops (Pty) Ltd** · Reg. 2021/121654/07 · VAT 4400302974
Proudly South African — Tech meets tradition.

*Categories bind to `Fruitful_Portal_data_model.md` (`documents.doc_category`). Sections map to `Fruitful_Portal_bank_application_field_matrix.md`.*

</div>
