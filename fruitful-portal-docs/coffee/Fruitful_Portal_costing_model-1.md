<!-- FRUITFUL PORTAL — COSTING MODEL -->
<div align="center">

# Fruitful_Portal_costing_model.md
### The Build-Up Cost Engine — Factory to Deploy-Ready

**Fruitful Shops (Pty) Ltd** · Reg. 2021/121654/07 · VAT 4400302974
31 Laurel Valley Street, Silver Lakes Golf Estate, Pretoria, 0081
Director: Heyns Schoeman · Cell: 081 415 9468

*"If you don't like the fruits we are growing, change the seeds."*

</div>

---

## 0. Purpose & Scope

This file is the **single source of truth for unit cost build-up** of one Fruitful Portal. It defines every cost variable, the formula chain that assembles them, and two parallel procurement streams:

- **Stream A — Imported** (Guangzhou Welink Technology Co., Ltd, PI No. WL20260325)
- **Stream B — Locally fabricated** (Fantastico SA, Addendum A scope)

> **DATA INTEGRITY RULE:** Known figures are sourced from the Welink Proforma Invoice and the Fantastico SA budgetary estimate. Every figure not in those two source documents is marked **[TBC]**. No values are assumed or estimated beyond what those documents state.

The cost chain feeds downstream into `Fruitful_Portal_markup_model.md` (markup → SP) and `Fruitful_Portal_finance_model.md` (FP → MI).

---

## 1. Variable Dictionary

Every cost variable used across the Fruitful Portal model set.

| Code | Variable | Definition | Unit |
|------|----------|------------|------|
| `FC` | Factory Cost (EXW) | Ex-Works unit price at factory gate | ZAR / USD |
| `CL` | China-side Logistics | Local transport to port + export documentation/handling | ZAR |
| `SF` | Sea Freight | Ocean freight, port-to-port (Guangzhou → Durban) | ZAR |
| `INS` | Marine Insurance | Cargo insurance, % of FOB | ZAR |
| `CIF` | Cost, Insurance & Freight | FOB + SF + INS = customs value at port | ZAR |
| `DUTY` | Customs Duty | SARS import duty, % of CIF | ZAR |
| `VAT_i` | Import VAT | 15% on (CIF + DUTY); reclaimable input credit | ZAR |
| `CLR` | Clearing & Handling | Clearing agent, port/depot handling, storage, Bill of Entry | ZAR |
| `LTM` | Local Transport (inland) | Road freight Durban → Johannesburg | ZAR |
| `STO` | Storage / Depot | Port/depot storage charges | ZAR |
| `INSL` | Inland Insurance | Inland transit insurance | ZAR [TBC] |
| `COMM` | Commissioning | Site commissioning / first-power checks | ZAR [TBC] |
| `BRAND` | Branding & Wrap | Exterior brand application (vinyl/paint/moulded) | ZAR |
| `ELEC` | Electronics Fit-out | Screens, router, UPS, CCTV, POS, network hardware | ZAR [TBC] |
| `SOFT` | Software / Licences | Cloud telemetry, VPN/static IP, POS software | ZAR [TBC] |
| `PAY` | Payments Hardware | Card terminal / Paystack-Checkout integration hardware | ZAR [TBC] |
| `FIT` | Internal Fit-out | Shelving, refrigeration, plumbing fixtures, boiler, DB board | ZAR [TBC] |
| `SPR` | Spares & Tooling | Initial spares kit, tamper-proof tooling, consumable starter | ZAR [TBC] |
| `WCB` | Working Capital Buffer | Opening stock float + cash float + first-period consumables | ZAR [TBC] |
| `CONT` | Contingency | % buffer on landing/deployment costs | ZAR |

---

## 2. Formula Chain (Master)

The canonical chain from factory gate to monthly customer price:

\[
\textbf{FC} \rightarrow \textbf{CIF} \rightarrow \textbf{LC} \rightarrow \textbf{TDC} \rightarrow \textbf{SP} \rightarrow \textbf{FP} \rightarrow \textbf{MI} \rightarrow \textbf{MonthlyCustomerPrice}
\]

### 2.1 FOB (Free On Board, Guangzhou)

\[
FOB = FC + CL
\]

### 2.2 CIF (Cost, Insurance & Freight, Durban)

\[
CIF = FOB + SF + INS = (FC + CL) + SF + INS
\]

### 2.3 SARS Import Charges

\[
DUTY = CIF \times d \quad\text{where } d = \text{duty rate (blended estimate 20\%, HS-code dependent)}
\]

\[
VAT_i = (CIF + DUTY) \times 0.15
\]

\[
\text{SARS Payable} = DUTY + VAT_i
\]

### 2.4 LC (Landed Cost, Johannesburg)

\[
LC = CIF + DUTY + VAT_i + CLR + LTM + STO + INSL + CONT
\]

> Note: `VAT_i` is shown in `LC` for cash-flow completeness but is **reclaimable** as an input-tax credit on the VAT 201 return (Fruitful Shops is VAT-registered, No. 4400302974). The **VAT-exclusive landed cost** for margin purposes excludes `VAT_i`.

### 2.5 TDC (Total Deployment Cost — Deploy-Ready)

\[
TDC = LC + COMM + BRAND + ELEC + SOFT + PAY + FIT + SPR + WCB + CONT_{deploy}
\]

### 2.6 SP (Selling Price, pre-finance) — *defined in markup model*

\[
SP = TDC \times (1 + m_{total}) \qquad \text{(see } \texttt{Fruitful\_Portal\_markup\_model.md)}
\]

### 2.7 FP (Financed Price) and MI (Monthly Instalment) — *defined in finance model*

\[
MI = \frac{FP \times r (1+r)^n}{(1+r)^n - 1} \qquad \text{(see } \texttt{Fruitful\_Portal\_finance\_model.md)}
\]

---

## 3. Stream A — Imported Unit (Welink, PI No. WL20260325)

**Source:** Guangzhou Welink Technology Co., Ltd · Invoice WL20260325 · 25 March 2026
**Spec:** Fiberglass kiosk, 4 mm; roof Ø 2,050 mm; bottom Ø 1,810 mm; height 2,630 mm; 1× stainless cabinet 800×275×700 mm; 1× 32" TV (window) + 1× 43" TV (kiosk); 1 window, 1 door.
**FX:** USD/ZAR = R16.32 (mid-rate, 17 April 2026) — *10% currency buffer advised.*

### 3.1 EXW → FOB Guangzhou

| Component | Code | USD | ZAR |
|-----------|------|-----|-----|
| Kiosk unit EXW | `FC` | 3,800 | R62,016 |
| Local China transport to port (est.) | `CL` (part) | 150 | R2,448 |
| China export documentation & handling | `CL` (part) | 100 | R1,632 |
| **FOB Guangzhou** | **FOB** | **4,050** | **R66,096** |

### 3.2 FOB → CIF Durban

| Component | Code | USD | ZAR |
|-----------|------|-----|-----|
| Sea freight Guangzhou → Durban (LCL/FCL, 1 unit, est.) | `SF` | 850 | R13,872 |
| Marine cargo insurance (1.5% of FOB) | `INS` | 61 | R996 |
| **CIF Value Durban** | **CIF** | **4,961** | **R80,964** |

### 3.3 SARS Import Duties & Taxes

> HS Code 9403.20 (metal/commercial furniture) **or** 8543.70 (electrical apparatus). Blended **20%** duty applied as conservative estimate. Actual rate 0–20% pending clearing-agent classification; if classified as 8543, duty may be 0–5%.

| Component | Code | Calculation | ZAR |
|-----------|------|-------------|-----|
| Customs Duty | `DUTY` | R80,964 × 20% | R16,193 |
| Import VAT (reclaimable) | `VAT_i` | (R80,964 + R16,193) × 15% | R14,574 |
| **Total SARS Payable** | | | **R30,767** |

### 3.4 Clearing, Handling & Inland Delivery (JHB)

| Component | Code | ZAR |
|-----------|------|-----|
| Customs clearing agent fee | `CLR` (part) | R4,500 |
| Port/depot handling & storage (Durban) | `STO` | R3,200 |
| Road freight Durban → Johannesburg | `LTM` | R5,500 |
| Documentation (Bill of Entry, etc.) | `CLR` (part) | R1,200 |
| Contingency (5%) | `CONT` | R4,798 |
| **Sub-total SA Landing Costs** | | **R19,198** |

### 3.5 LC — Total Landed Cost (Imported)

| Component | ZAR |
|-----------|-----|
| Ex-Works China unit price (`FC`) | R62,016 |
| China-side export logistics (`CL`) | R4,080 |
| Sea freight + insurance (`SF` + `INS`) | R14,868 |
| SA Customs Duty 20% (`DUTY`) | R16,193 |
| SA Import VAT 15% (`VAT_i`, reclaimable) | R14,574 |
| Clearing, handling & delivery to JHB (`CLR`+`STO`+`LTM`+`CONT`) | R19,198 |
| **`LC` — TOTAL LANDED COST (1 unit)** | **R130,929** |

> **VAT-exclusive landed cost** (for margin base) = R130,929 − R14,574 = **R116,355**.

---

## 4. Stream B — Locally Fabricated Shell (Fantastico SA)

**Source:** Fantastico SA budgetary estimate, per Addendum A (FHL-NDA-ADDENDUM-A-v2).
**Scope:** Complete branded exterior shell **only** — excludes all tech hardware, internal shopfitting, live electrical, plumbing fixtures, POS/network hardware.

### 4.1 Phase 1 Fabrication Build-Up

| Line Item | ZAR (excl. VAT) |
|-----------|-----------------|
| Shell fabrication (fiberglass moulding, structural form) | R45,000 |
| Top cap (coral-red domed fiberglass, moulded) | R12,000 |
| Exterior finish (surface prep, paint, weatherproof coating) | R8,500 |
| Brand application (logo, tagline, vinyl/painted) | R7,500 |
| Service door (lockable, hinged, finished to match) | R4,500 |
| Window/display aperture (perspex panel, frame, flush fit) | R3,500 |
| Electrical trunking channels (internal conduit routing only) | R4,000 |
| Water channel routing (inlet/drain trunking only) | R2,500 |
| Ventilation provisions (grille mounting points/openings) | R1,500 |
| Branded signage topper (illuminated housing, no electronics) | R9,000 |
| Base/plinth & levelling feet | R3,000 |
| Transport to Johannesburg (delivery, prototype unit) | R4,500 |
| Design & pattern-making consultation | R6,000 |
| **Sub-total (excl. VAT)** | **R111,500** |
| VAT 15% | R16,725 |
| **TOTAL PHASE 1 — FANTASTICO SA (incl. VAT)** | **R128,225** |

> **Notes (per source):** Budgetary estimate only — actual cost pending Egon's formal quotation. Phase 1 = 1 prototype unit. Units 3+ benefit from mould amortisation, typically **30–40% lower per unit**. Signage topper = housing only; LED/electrical handled separately. Quote separately requested on (a) mould creation for repeat production and (b) per-unit cost for batches of 5 and 10.

### 4.2 Local Stream — Shell vs. Deploy-Ready

The Fantastico figure is **shell-only**. To reach a deploy-ready local unit, add the tech/fit-out layers (§5) which Fantastico explicitly excludes.

\[
LC_{local,shell} = \text{R111,500 (excl. VAT)} \quad/\quad \text{R128,225 (incl. VAT)}
\]

\[
TDC_{local} = LC_{local,shell} + ELEC + SOFT + PAY + FIT + SPR + WCB + COMM + CONT_{deploy}
\]

---

## 5. Deploy-Ready Layers (Both Streams)

These layers convert a bare shell (or tech-equipped import) into a trading-ready portal. **All [TBC]** — to be populated from supplier quotes before finalisation.

| Layer | Code | Imported (Welink) | Local (Fantastico) | Source needed |
|-------|------|-------------------|--------------------|---------------|
| Electronics fit-out (screens, router, UPS, CCTV) | `ELEC` | *(32"+43" TV & cabinet included in import)* [TBC remainder] | [TBC] | Hardware supplier quote |
| Software / licences (telemetry, VPN, POS) | `SOFT` | [TBC] | [TBC] | SaaS pricing |
| Payments hardware (terminal / Paystack-Checkout) | `PAY` | [TBC] | [TBC] | Acquirer quote |
| Internal fit-out (shelving, refrigeration, plumbing, boiler, DB) | `FIT` | [TBC] | [TBC] | Shopfitter quote |
| Branding (where not in shell) | `BRAND` | [TBC] | *(included in R111,500)* | — |
| Spares & tooling starter kit | `SPR` | [TBC] | [TBC] | Inventory registry |
| Working-capital buffer (opening stock + float) | `WCB` | [TBC] | [TBC] | Stock plan |
| Commissioning / site setup | `COMM` | [TBC] | [TBC] | Install quote |
| Deployment contingency | `CONT_deploy` | [TBC] | [TBC] | % of TDC |

> Inventory line items feeding `SPR` / `WCB` are catalogued in the Fruitful inventory registry (ingredients, packaging, hygiene, IT/security, maintenance, compliance, admin, HR/PPE, logistics).

---

## 6. Deploy-Ready Total (TDC) — Assembly

### 6.1 Imported Stream

\[
TDC_{import} = \underbrace{R130{,}929}_{LC} + ELEC_{[TBC]} + SOFT_{[TBC]} + PAY_{[TBC]} + FIT_{[TBC]} + SPR_{[TBC]} + WCB_{[TBC]} + COMM_{[TBC]} + CONT_{[TBC]}
\]

| | Known (ZAR) | Plus [TBC] layers | TDC (import) |
|---|---|---|---|
| Landed cost | R130,929 | + ELEC, SOFT, PAY, FIT, SPR, WCB, COMM, CONT | **[TBC]** |

### 6.2 Local Stream

\[
TDC_{local} = \underbrace{R111{,}500}_{shell\,excl.\,VAT} + ELEC_{[TBC]} + SOFT_{[TBC]} + PAY_{[TBC]} + FIT_{[TBC]} + SPR_{[TBC]} + WCB_{[TBC]} + COMM_{[TBC]} + CONT_{[TBC]}
\]

| | Known (ZAR) | Plus [TBC] layers | TDC (local) |
|---|---|---|---|
| Shell (excl. VAT) | R111,500 | + ELEC, SOFT, PAY, FIT, SPR, WCB, COMM, CONT | **[TBC]** |

> **Parallel-stream rule:** Welink (import) and Fantastico (local) are **two alternative procurement streams, not additive** for a single unit. Choosing the Fantastico route makes the China import a reference/benchmark only.

---

## 7. Downstream Handoff

| Output | Feeds | Target file |
|--------|-------|-------------|
| `TDC` | Markup application → `SP` | `Fruitful_Portal_markup_model.md` |
| `SP` | Finance layering → `FP`, `MI` | `Fruitful_Portal_finance_model.md` |
| Cost variable dictionary | Backend cost fields | `Fruitful_Portal_data_model.md` |
| Known vs [TBC] split | Bank PI/quote evidence | `Fruitful_Portal_bank_application_field_matrix.md` |

---

<div align="center">

**Fruitful Shops (Pty) Ltd** · Reg. 2021/121654/07 · VAT 4400302974
Proudly South African — Tech meets tradition.

*Source documents: Welink PI No. WL20260325 (25 Mar 2026); Fantastico SA budgetary estimate per Addendum A FHL-NDA-ADDENDUM-A-v2. All other figures [TBC].*

</div>
