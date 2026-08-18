# Fruitful Portal — Requirements & Integration Map

**Owner:** Heyns Schoeman · **Date:** 15 Aug 2026
**Ecosystem Backbone:** `fruitfulapp.base44.app` (HotStack API / base44 SDK)
**Physical Gateway:** Fruitful Portal Kiosk (2.05m Fibreglass unit from Guangzhou Welink)
**Business Verticals:** Coffee + Pancakes + Tech Build Apps

---

## 1. Authentication & SDK Implementation

The portal's interface and any backend services must use the **base44 SDK** for all entity operations.

**Configuration:**
- **App ID:** `6953a072de46207f94f2b9d2`
- **Client Implementation:**
```javascript
import { createClient } from '@base44/sdk';

const base44 = createClient({
  appId: "6953a072de46207f94f2b9d2",
  headers: {
    "api_key": "70c349707cdd4ade8f339121c9ae5b77" // Authoritative Truth API Key
  }
});
```

---

## 2. Backend Infrastructure (HotStack API)

The `FRUITFUL-openapi-spec.json` defines a massive entity registry that acts as the single source of truth for the portal's operations.

| Domain | Entity Classes | Purpose |
|---|---|---|
| **ERP / Sage** | `SageItemRaw`, `SageCostRow` | Inventory sync, item master, and raw costing data |
| **Finance** | `Payment`, `Subscription`, `BankApplication` | Transaction logging and operator financing status |
| **Ecosystem** | `Vault`, `License`, `Node` | Security grades, node metadata, and license entitlements |
| **Logistics** | `PackagingAsset`, `ShippingJob` | Branded packaging and kiosk deployment tracking |
| **Governance** | `TruthAudit`, `Anomalies` | Multi-source reconciliation (FAA vs HSOMNI vs Seedwave) |

---

## 3. Fruitful Portal Operations (Coffee & Pancakes)

The `Fruitful-Coffee` package provides the commercial engine for the physical kiosk.

### 3.1 Commercial Models
- **Markup Model:** Defines the price floor for coffee and pancake SKUs based on raw Sage costing.
- **Franchise Benchmark:** Standardized ROI and operational metrics for "Portal Operators."
- **Operator Application:** A 4-part application pack (Applicants, Commercial, Financial, Bank-Mandatory) to onboard new kiosk operators.

### 3.2 Supply Chain (Fantastico SA)
- **Coffee Trading Pack:** Authorized supply agreement for coffee beans and equipment.
- **Addendum A:** Specifies the quality and volume requirements for "Fruitful Certified" coffee.

---

## 4. Tech Build Apps (Baobab AI Integration)

The "Tech" vertical of the portal leverages the **Baobab AI engine** (from the `bushcoding` repository) to allow on-site users to build and preview apps.

- **Interface:** The 32" kiosk window runs the IDE attractor.
- **Backend:** Connected to the Convex `ai/generate` action (Claude 3.5 Sonnet).
- **Entitlement:** App building is gated by a "Fruitful Subscription" or an "Active Activation" from a coffee/pancake purchase.

---

## 5. Build Checklist for the Sample Unit

| Component | Status | Action Required |
|---|---|---|
| **Kiosk HW** | Shipping | Track arrival in JHB; verify 32"/43" screen resolutions |
| **Auth** | Ready | Embed base44 SDK with provided keys in the kiosk UI |
| **Catalog** | Seeded | Map `SageItemRaw` items to the Kiosk Browse screen |
| **Payments** | Planned | Wire Paystack ZAR (standard Fruitful pattern) to base44 `Payment` entity |
| **Operator UI** | Design | Build the "Bank Application" form using the provided field matrix |

---

*Documents mapped: FRUITFUL-openapi-spec.json · Fruitful-Coffee.zip (Franchise/Costing/Applications) · base44 SDK implementation · Fruitful Portal Vision.*
