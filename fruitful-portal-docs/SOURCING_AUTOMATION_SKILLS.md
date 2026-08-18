# Fruitful Group — Automated Sourcing Agent Skills & Tasks

**Role:** Autonomous Head Buyer (AI)
**Objective:** Standardize the procurement of 300+ Fruitful Portals using high-volume franchise models (Starbucks/McDonald's/Plato).
**Backbone:** base44 SDK / HotStack API

---

## 1. Agent Skill: `global-franchise-sourcing`
The agent must possess verified capabilities in:
- **Bulk Negotiation:** MOQ-driven pricing logic for disposables (MOQ 100k+).
- **Compliance Matching:** Verifying items against SABS, NSF, and POPIA standards.
- **Logistics Orchestration:** Mapping LCL shipments from China (Welink) and local cartage (Fantastico) into the `KioskShippingEstimate` entity.
- **base44 Integration:** Directly updating `SageCostRow` and `SageItemRaw` via the base44 SDK.

## 2. Automated Task: `portal-ready-activation`
The primary task assigned to sourcing agents.

### Step 1: Smallwares & Countertop Equipment
- **Task:** Source the standardized "Fruitful Toolkit" (Stainless pitchers, thermometers, spatulas).
- **Constraint:** All metalware must be 304 Stainless Steel with Fruitful branding capability.
- **Action:** Request samples for quality verification in JHB hub.

### Step 2: Branded Disposables (The Starbucks Standard)
- **Task:** Source factories for branded serviettes, cup markers, and cup carriers.
- **Constraint:** Use biodegradable/recycled materials only (Positivity/Creative brand values).
- **Action:** Lock in 12-month supply agreements to isolate from paper cost volatility.

### Step 3: Deep Maintenance & Compliance
- **Task:** Source bio-enzymatic grease trap treatments and sanitizer test strips.
- **Constraint:** Must satisfy the `ComplianceAudit` entity fields for SA Health Dept records.
- **Action:** Secure recurring monthly delivery contracts.

### Step 4: Tech & Hardware (The HotStack Standard)
- **Task:** Source rugged tablets, e-Ink pads, and dynamic nametags.
- **Constraint:** Must be pre-loadable with the base44 Node.js SDK.
- **Action:** Verify "Tech Readiness" via the hardware questionnaire.

---

## 3. The Automation Loop (Daily)
1. **Monitor:** Agent polls `SageItemRaw` for items below "Threshold."
2. **Search:** Agent triggers Alibaba/Local Search for best price/lead-time match.
3. **Draft:** Agent drafts a Proforma/PO in the `documents` entity.
4. **Notify:** Agent alerts Head Buyer (Heyns) for final signature.
5. **Update:** Upon signature, agent triggers the `Payment` event through the base44 SDK.

---

*Authored by: Head Buyer for Fruitful Group · 15 Aug 2026*
