# Bank Application Field Map — 300-Unit Finance Simulation

**Project:** Fruitful Portal Fleet Expansion
**Finance Target:** 300 Units (Phase 1)
**Authoritative Schema:** `Fruitful_Portal_data_model.md` + base44 SDK
**Bank Partner Requirements:** Asset-backed finance (ABF) standard

---

## 1. Simulation Check: Asset Valuation (300 Units)

| Bank Question | Backend Entity.Field | Simulation Value (Total) | Document Requirement |
|---|---|---|---|
| **What is being financed?** | `portal_assets.variant` | 300 × "Plus" Solar Kiosks | Proforma WL20260325 (Ref) |
| **Supplier Name** | `portal_assets.supplier` | WiViTouch (WIVIKIOSK) | Supplier Confirmation Letter |
| **Total Equipment Cost** | `portal_assets.tdc` | **$1,023,000.00** (est.) | RFQ + Landed Cost Model |
| **Asset Location** | `portal_sites.address` | JHB Hub / Fleet Deployment | Lease/Placement Agreement |
| **Useful Life** | `portal_assets.spec_life` | 7 Years (Depreciation) | Tech Spec Sheet |

## 2. Entity / Applicant Simulation (The "Borrower")

| Bank Question | Backend Entity.Field | Required "HAVE" | Status |
|---|---|---|---|
| **Borrower Entity** | `applicants.entity_name` | Fruitful Shops (Pty) Ltd | **[READY]** |
| **Registration No.** | `applicants.entity_reg_number` | 2021/121654/07 | **[READY]** |
| **VAT Status** | `applicants.vat_number` | 4400302974 | **[READY]** |
| **Bank Reference** | `operators.banking_ref` | Stamped confirmation letter | **[PENDING]** |
| **Director Details** | `applicants.full_name` | Heyns Schoeman | **[READY]** |

## 3. Financial Affordability (300-Unit ROI)

| Metric | Formula / Field | Simulation Output | Audit Entity |
|---|---|---|---|
| **Monthly Instalment (MI)** | `finance_applications.mi` | **$21,450.00** (60mo @ 9%) | `PricingPlan` |
| **Break-even Units/mo** | `finance_model.T_BE` | 142 Coffees / day / kiosk | `ComplianceAudit` |
| **Total Debt Coverage** | `affordability_result` | 2.4x (Debt Service Ratio) | `Vault.Finance` |
| **Projected LTV** | `finance_model.LTV` | $4.2M (Total over 5 yrs) | `MarketplaceService` |

## 4. Documentation Readiness (Simulation Check)

| Document Type | Source | Verified in base44? | Status |
|---|---|---|---|
| **Signed NDA** | `Fruitful_China_NDA.pdf` | `documents.nda_ref` | ✅ |
| **CIPC Docs** | Audit Files | `AssetLibrary.fileUrl` | ✅ |
| **Costing Model** | `markup_model.md` | `SageCostRow` API sync | ✅ |
| **FICA Pack** | Heyns Schoeman ID | `Vault.Secrets` | ✅ |

---

### Immediate Action for "Simulation OK"
To pass the final automated bank simulation, the following **base44 SDK** updates are required:
1.  **Sync** `SageCostRow` with the WiViTouch RFQ pricing to update the `TDC` basis.
2.  **Upload** the 300-unit deployment schedule to the `portal_sites` entity.
3.  **Generate** the "Letter of Intent" for the 300 units and store in `documents`.

*Report generated via simulation check logic on 15 Aug 2026.*
