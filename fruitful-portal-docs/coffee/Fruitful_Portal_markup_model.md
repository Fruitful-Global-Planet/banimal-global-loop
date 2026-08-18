<!-- FRUITFUL PORTAL — MARKUP MODEL -->
<div align="center">

# Fruitful_Portal_markup_model.md
### The 5-Layer Markup Engine — TDC to Selling Price

**Fruitful Shops (Pty) Ltd** · Reg. 2021/121654/07 · VAT 4400302974
Director: Heyns Schoeman · Pretoria, RSA

</div>

---

## 0. Purpose

Defines how the **Total Deployment Cost (`TDC`)** from `Fruitful_Portal_costing_model.md` is converted into a **pre-finance Selling Price (`SP`)** through five stacked markup layers. Each layer has a defined purpose, a range, and a decision rule.

> **DATA RULE:** Markup percentages below are presented as **decision ranges** (policy levers). Actual percentages selected per deal are **[TBC]** until set by management. ZAR worked examples use the placeholder `TDC = [TBC]` and resolve to **[TBC]** until `TDC` is populated.

---

## 1. Position in the Formula Chain

\[
FC \rightarrow CIF \rightarrow LC \rightarrow TDC \;\Rightarrow\; \boxed{SP} \;\Rightarrow\; FP \rightarrow MI
\]

The markup model owns the `TDC → SP` step.

---

## 2. The Five Markup Layers

Each layer is a multiplier applied to the running cost base. They **compound** in sequence.

| # | Layer | Code | Purpose | Range (policy lever) |
|---|-------|------|---------|----------------------|
| 1 | Minimum Viable Margin | \(m_1\) | Covers overhead recovery + baseline profit; the floor below which no unit is sold | [TBC]% |
| 2 | Strategic Margin | \(m_2\) | Market-positioning uplift vs. competing kiosks/franchises | [TBC]% |
| 3 | Brand Premium | \(m_3\) | Charge for Fruitful trade dress, IP, design, "Tech meets tradition" positioning | [TBC]% |
| 4 | Finance Risk Loading | \(m_4\) | Buffer for credit/default risk on financed & rent-to-own deals | [TBC]% |
| 5 | Operator Support Loading | \(m_5\) | Funds onboarding, training, SLA, maintenance backstop, telemetry support | [TBC]% |

---

## 3. SP Formula

### 3.1 Compounded form (sequential layers)

\[
SP = TDC \times (1+m_1)(1+m_2)(1+m_3)(1+m_4)(1+m_5)
\]

### 3.2 Additive-margin form (single blended markup)

\[
SP = TDC \times (1 + m_{total}), \qquad
m_{total} = (1+m_1)(1+m_2)(1+m_3)(1+m_4)(1+m_5) - 1
\]

### 3.3 Gross profit on the unit sale

\[
GP_{unit} = SP - TDC, \qquad GP\%_{unit} = \frac{SP - TDC}{SP}
\]

### 3.4 Layer-by-layer running base

\[
\begin{aligned}
B_0 &= TDC \\
B_1 &= B_0 (1+m_1) \quad &\text{(min viable)}\\
B_2 &= B_1 (1+m_2) \quad &\text{(strategic)}\\
B_3 &= B_2 (1+m_3) \quad &\text{(brand premium)}\\
B_4 &= B_3 (1+m_4) \quad &\text{(finance risk)}\\
SP = B_5 &= B_4 (1+m_5) \quad &\text{(operator support)}
\end{aligned}
\]

---

## 4. Worked Example (ZAR) — Structure Only

Using `TDC = [TBC]` (from costing model). Percentages `[TBC]` per policy.

| Step | Layer | Multiplier | Running base (ZAR) |
|------|-------|------------|--------------------|
| \(B_0\) | Total Deployment Cost | — | [TBC] |
| \(B_1\) | + Minimum Viable Margin | ×(1+[TBC]%) | [TBC] |
| \(B_2\) | + Strategic Margin | ×(1+[TBC]%) | [TBC] |
| \(B_3\) | + Brand Premium | ×(1+[TBC]%) | [TBC] |
| \(B_4\) | + Finance Risk Loading | ×(1+[TBC]%) | [TBC] |
| \(B_5 = SP\) | + Operator Support Loading | ×(1+[TBC]%) | **[TBC]** |

**Reference cost anchors available now** (from costing model, for sanity-checking `TDC` once tech layers are added):

- Imported landed cost `LC` = **R130,929** (R116,355 excl. reclaimable VAT)
- Local shell (Fantastico) = **R111,500 excl. VAT** / R128,225 incl. VAT

---

## 5. Decision Logic Table

Which layers apply, and at what end of the range, by deal type:

| Deal Type | \(m_1\) Min Viable | \(m_2\) Strategic | \(m_3\) Brand | \(m_4\) Finance Risk | \(m_5\) Operator Support | Rationale |
|-----------|------|------|------|------|------|-----------|
| **Cash sale (sophisticated buyer)** | Required | Low–Mid | Mid | **Excluded** | Optional | No credit risk; buyer self-supports |
| **Cash sale (standard)** | Required | Mid | Mid–High | **Excluded** | Required | Full brand + support, no finance risk |
| **Financed 24–36 mo** | Required | Mid | High | **Low–Mid** | Required | Short tenor → lower default exposure |
| **Financed 48–60 mo** | Required | Mid | High | **Mid–High** | Required | Longer tenor → higher risk loading |
| **Rental** | Required | High | High | **High** | **High** | Fruitful retains asset risk + full support |
| **Rent-to-own** | Required | High | High | **High** | Required | Asset risk until title transfers |
| **Managed subscription** | Required | High | High | **High** | **Highest** | Fruitful operates everything; all loadings on |

**Selection rules:**

1. \(m_1\) (Minimum Viable) is **mandatory on every deal** — it is the floor.
2. \(m_4\) (Finance Risk) is **zero on cash deals**, scales with tenor on credit deals.
3. \(m_5\) (Operator Support) scales with the degree of Fruitful's ongoing involvement.
4. \(m_3\) (Brand Premium) is constant across deal types — the brand is the brand.
5. Floor guard: never quote below \(SP_{floor} = TDC \times (1+m_1)\).

---

## 6. Margin Guards & Sensitivity

\[
SP_{floor} = TDC \times (1+m_1) \qquad\text{(absolute minimum quotable price)}
\]

\[
\text{FX guard: } TDC_{adj} = TDC \times (1 + b_{fx}), \quad b_{fx} = \text{currency buffer (10\% advised on imported stream)}
\]

| Sensitivity lever | Effect on SP | Source/owner |
|-------------------|--------------|--------------|
| USD/ZAR move (import stream) | Raises `FC`→`LC`→`TDC`→`SP` | FX rate R16.32 baseline (17 Apr 2026) |
| Duty reclassification (0–20%) | Lowers `DUTY`→`LC`→`SP` | Clearing agent HS code |
| Mould amortisation (units 3+) | Lowers `TDC` (local) 30–40% | Fantastico batch quote |
| Layer % policy changes | Direct on `m_total` | Management |

---

## 7. Handoff to Finance Model

\[
SP \;\longrightarrow\; \texttt{Fruitful\_Portal\_finance\_model.md} \;\longrightarrow\; FP, \; MI
\]

The finance model adds interest/finance charges to `SP` to produce the **Financed Price (`FP`)** and **Monthly Instalment (`MI`)**.

---

<div align="center">

**Fruitful Shops (Pty) Ltd** · Reg. 2021/121654/07 · VAT 4400302974
Proudly South African — Tech meets tradition.

*All markup percentages are policy levers marked [TBC]. Cost anchors sourced from Welink PI WL20260325 and Fantastico SA estimate.*

</div>
