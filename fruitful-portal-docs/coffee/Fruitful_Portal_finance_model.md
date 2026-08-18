<!-- FRUITFUL PORTAL — FINANCE MODEL -->
<div align="center">

# Fruitful_Portal_finance_model.md
### Customer Finance Engine — SP to Monthly Customer Price

**Fruitful Shops (Pty) Ltd** · Reg. 2021/121654/07 · VAT 4400302974
Director: Heyns Schoeman · Pretoria, RSA

</div>

---

## 0. Purpose

Converts the pre-finance **Selling Price (`SP`)** from `Fruitful_Portal_markup_model.md` into the **Financed Price (`FP`)** and the customer-facing **Monthly Instalment (`MI`)** / **Monthly Customer Price**, across six acquisition modes:

1. Cash sale
2. Financed sale (24 / 36 / 48 / 60-month grid)
3. Rental
4. Rent-to-own
5. Managed subscription

> **DATA RULE:** Interest rate `r`, deposit `D`, residual `R_v`, fees `F`, and all ZAR amounts are **[TBC]** until set. Formulas and grid structure are complete; cells resolve once `SP` and rate policy are supplied.

---

## 1. Position in the Formula Chain

\[
\dots \rightarrow TDC \rightarrow SP \;\Rightarrow\; \boxed{FP \rightarrow MI} \;\Rightarrow\; \text{Monthly Customer Price}
\]

---

## 2. Core Finance Variables

| Code | Variable | Definition | Value |
|------|----------|------------|-------|
| `SP` | Selling Price (pre-finance) | Output of markup model | [TBC] |
| `D` | Deposit | Up-front customer payment | [TBC] |
| `P` | Principal financed | `SP − D` (+ initiation if capitalised) | [TBC] |
| `i` | Nominal annual interest rate | Annual finance rate (NCA-compliant) | [TBC]% |
| `r` | Monthly periodic rate | `i / 12` | [TBC] |
| `n` | Term (months) | 24 / 36 / 48 / 60 | per grid |
| `F_init` | Initiation fee | Once-off finance fee | [TBC] |
| `F_admin` | Monthly admin/service fee | Recurring finance admin | [TBC] |
| `R_v` | Residual / balloon | End-of-term value (rental/RTO) | [TBC] |
| `INS_m` | Monthly insurance | Asset insurance premium | [TBC] |
| `SLA_m` | Monthly support/SLA fee | Operator support (subscription/managed) | [TBC] |

---

## 3. Mode 1 — Cash Sale

\[
\text{Cash Price} = SP \times (1 + VAT) \qquad (VAT = 15\%)
\]

No finance charge; no `m_4` risk loading (see markup decision table). Optional early-settlement / cash-discount lever `[TBC]`.

---

## 4. Mode 2 — Financed Sale (Amortising)

### 4.1 Principal

\[
P = (SP - D) + F_{init,\,capitalised}
\]

### 4.2 Monthly Instalment (standard amortisation)

\[
MI = \frac{P \cdot r (1+r)^n}{(1+r)^n - 1} + F_{admin}
\]

### 4.3 Total cost of credit

\[
TCC = (MI \times n) + D - SP, \qquad
FP = SP + TCC = (MI \times n) + D
\]

### 4.4 Finance Grid (24 / 36 / 48 / 60 months)

All cells `[TBC]` until `SP`, `r`, `D`, `F` supplied.

| Term `n` | Deposit `D` | Principal `P` | Monthly rate `r` | **Monthly Instalment `MI`** | Total repaid | `FP` (financed price) |
|----------|-------------|---------------|------------------|------------------------------|--------------|------------------------|
| 24 mo | [TBC] | [TBC] | [TBC] | **[TBC]** | [TBC] | [TBC] |
| 36 mo | [TBC] | [TBC] | [TBC] | **[TBC]** | [TBC] | [TBC] |
| 48 mo | [TBC] | [TBC] | [TBC] | **[TBC]** | [TBC] | [TBC] |
| 60 mo | [TBC] | [TBC] | [TBC] | **[TBC]** | [TBC] | [TBC] |

> Longer tenor → lower `MI`, higher `TCC`, and higher `m_4` finance-risk loading upstream (see markup decision table).

---

## 5. Mode 3 — Rental (Operating Lease)

Fruitful retains ownership; customer pays to use.

\[
MI_{rental} = \frac{SP \cdot r (1+r)^n}{(1+r)^n - 1}\Big|_{\text{less residual}} + INS_m + SLA_m
\]

With residual retained by Fruitful:

\[
MI_{rental} = \left[\frac{(SP - R_v)\, r (1+r)^n}{(1+r)^n - 1}\right] + \frac{R_v \cdot r}{1} \;(\text{financing on residual}) + INS_m + SLA_m
\]

| Variable | Value |
|----------|-------|
| Residual `R_v` retained by Fruitful | [TBC] |
| Monthly rental `MI_rental` | [TBC] |
| Includes insurance + SLA | Yes (`INS_m` + `SLA_m`) |

---

## 6. Mode 4 — Rent-to-Own

Rental during term, title transfers on final payment / option exercise.

\[
MI_{RTO} = \frac{(SP - D)\, r (1+r)^n}{(1+r)^n - 1} + F_{admin} + INS_m
\]

\[
\text{Option-to-purchase / final transfer} = R_v \;(\text{often nominal at term end})
\]

| Variable | Value |
|----------|-------|
| Deposit `D` | [TBC] |
| Monthly `MI_RTO` | [TBC] |
| Title transfer trigger | Final instalment / option fee `[TBC]` |

---

## 7. Mode 5 — Managed Subscription

Fruitful owns and operates; customer pays an all-inclusive monthly fee.

\[
MI_{sub} = \underbrace{A(SP,r,n)}_{\text{asset amortisation}} + INS_m + SLA_m + \underbrace{OPEX_m}_{\text{telemetry, maintenance, consumables backstop}}
\]

where \( A(SP,r,n) = \dfrac{SP \cdot r (1+r)^n}{(1+r)^n - 1} \).

| Component | Value |
|-----------|-------|
| Asset amortisation `A` | [TBC] |
| Insurance `INS_m` | [TBC] |
| Support/SLA `SLA_m` | [TBC] |
| Operating backstop `OPEX_m` | [TBC] |
| **Monthly subscription `MI_sub`** | **[TBC]** |

---

## 8. Monthly Customer Price Stack (Master Formula)

The full monthly amount a customer sees, by mode:

\[
\text{MonthlyCustomerPrice} = MI_{base} + F_{admin} + INS_m + SLA_m + VAT_m
\]

where:

\[
VAT_m = (MI_{base} + F_{admin} + SLA_m) \times 0.15
\]

| Stack layer | Cash | Financed | Rental | RTO | Subscription |
|-------------|------|----------|--------|-----|--------------|
| Base instalment / amortisation | — | ✔ | ✔ | ✔ | ✔ |
| Admin / service fee `F_admin` | — | ✔ | optional | ✔ | included |
| Insurance `INS_m` | optional | optional | ✔ | ✔ | ✔ |
| Support/SLA `SLA_m` | optional | optional | ✔ | optional | ✔ |
| VAT 15% | ✔ (on price) | ✔ | ✔ | ✔ | ✔ |

---

## 9. Break-Even, GPP & LTV per Portal

### 9.1 Break-even monthly turnover

The trading turnover a portal must generate to cover its monthly customer price plus running costs:

\[
T_{BE} = \frac{\text{MonthlyCustomerPrice} + OPEX_{operator}}{GM\%}
\]

where `GM%` = gross margin on goods sold (coffee/food/retail) `[TBC]`, and `OPEX_operator` = staff, consumables, utilities, rent `[TBC]`.

### 9.2 Gross Profit per Portal (GPP)

\[
GPP_{monthly} = (T_{actual} \times GM\%) - OPEX_{operator} - \text{MonthlyCustomerPrice}
\]

### 9.3 Lifetime Value per Portal (LTV)

\[
LTV = \sum_{t=1}^{N}\frac{MI_t + \text{ancillary}_t}{(1+\delta)^t} - \text{CAC} - \text{servicing cost}
\]

| Metric | Formula output | Value |
|--------|----------------|-------|
| Break-even turnover `T_BE` | per §9.1 | [TBC] |
| Gross Profit per Portal `GPP` | per §9.2 | [TBC] |
| Lifetime Value `LTV` | per §9.3 | [TBC] |
| Customer Acquisition Cost `CAC` | input | [TBC] |
| Discount rate `δ` | input | [TBC] |

---

## 10. Handoff

| Output | Feeds |
|--------|-------|
| `MI`, `FP`, MonthlyCustomerPrice | Bank application (affordability) → `Fruitful_Portal_bank_application_field_matrix.md` |
| Finance application fields | `Fruitful_Portal_data_model.md` (`finance_applications`, `pricing_plans`) |
| Deal-type selection | `Fruitful_Portal_operator_application_pack.md` |

---

<div align="center">

**Fruitful Shops (Pty) Ltd** · Reg. 2021/121654/07 · VAT 4400302974
Proudly South African — Tech meets tradition.

*All rates, deposits, residuals, fees and ZAR amounts [TBC]. Finance must comply with the National Credit Act (NCA) where applicable.*

</div>
