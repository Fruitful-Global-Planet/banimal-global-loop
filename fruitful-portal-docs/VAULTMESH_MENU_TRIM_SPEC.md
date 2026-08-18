# VaultMesh Menu-Trim Report — Specification

**Purpose:** Automate the McDonald's 90% rule. Every quarter, the data decides which of the 8 lines stays and which gets canned — not taste, not habit.
**Cadence:** Quarterly (day 1 of Jan / Apr / Jul / Oct), fully automated, human sign-off.
**Owner:** ACCIO agent (draft) → Heyns (confirm) → Convex config (apply).

---

## 1. Input telemetry (already flowing)

Every pour/order logs to VaultMesh (9s pulse) and Convex:

```typescript
order_items: {
  lineSku:   "FFP-01"…"FFP-08",   // canonical part number (Mercedes rule)
  qty,       // units (pancakes = units; coffee = cups; smoothie = cups)
  price,     // line price at time of sale (R38 / R55 / R35)
  directCost,// from the menu BOQ engine (R14.66 / R23.40 / R8.32 …)
  ts,        // ISO timestamp
  portalId,  // which portal
}
```

## 2. Quarterly ranking query (Convex aggregate)

For each `FFP-0n` over the trailing 92 days:

| Metric | Definition |
|---|---|
| **Units** | Σ qty |
| **Revenue** | Σ (qty × price) |
| **Gross margin** | Σ (qty × (price − directCost)) |
| **Margin/unit** | gross margin ÷ units |
| **Trend** | units this Q vs prior Q (Δ%) |
| **Portal reach** | distinct portalId count |

## 3. The 90% rule (the cut logic)

1. Sort all lines by **gross margin contribution, descending**.
2. Walk down the sorted list, accumulating margin until **cumulative ≥ 90% of total menu margin**.
3. Everything below that line = **TRIM LIST**.
4. Guardrails before a cut is proposed:
   - Line must be **below the 90% line AND** < 60% of the median line's margin contribution.
   - A line that is trending **+25% QoQ** is spared one quarter (traction test).
   - **FFP-01 (Coffee with Milk)** and **FFP-04 (Green Energy)** are **protected** — they are the daily-driver anchor and the health anchor; they can only be *reformulated*, never cut (same logic as McDonald's keeping the burger).
5. Output: TRIM LIST with margin at risk, replacement slot, and rationale.

## 4. Replacement slots (the rotation bench)

| Slot | Primary | Bench (designated replacement) |
|---|---|---|
| Smoothie | FFP-04 Green / FFP-05 Lassi / FFP-06 Protein | **Pitaya Punch** (already data-flagged 🆕) |
| Pancake | FFP-07 Classic | Rotating variant (chocolate → banana → savoury) |
| Coffee | FFP-01/02/03 (protected trio) | Filter/batch brew — only if data says it outsells a current line |

Bench items get 90 days, same trim rules. No bench item is ever added *alongside* — it replaces (the 8-line ceiling is absolute).

## 5. Approval flow (human sign-off, 2 clicks)

1. **ACCIO draft:** query runs → trim brief generated (see §7) → pushed to the admin console + WhatsApp summary to Heyns.
2. **Heyns reviews:** Approve / Override (with reason) in the VaultMesh admin UI.
3. **Apply:** Convex config flips `active: false` on the cut P/N, `active: true` on the bench P/N. Kiosk till rebuilds to 8 lines overnight. Menu BOQ engine re-costs.

## 6. Companion KPI panel (from brainstorm §7 — same report card)

| KPI | Target | Source |
|---|---|---|
| Order-to-pay | < 30 s | till telemetry |
| Till error rate | < 0.5% | order vs receipt diffs |
| BushCoding attach | > 15% of orders | QR scan → session |
| Close-of-day food waste | 0 | prepack model |
| Repeat rate (same portal) | > 40% | customer refs |
| Lines cut per quarter | bottom-90% | this spec |

## 7. ACCIO trim brief output (draft format)

```markdown
## VAULTMESH MENU TRIM — Q3 2026
**Portal fleet:** n portals · **Period:** 92 days
**Total menu margin:** R[x] · **90% line:** R[y]

### TRIM LIST
| P/N | Line | Units | Margin | ΔQoQ | Rationale |
|---|---|---|---|---|---|
| FFP-05 | Mango Lassi | 4,210 | R42k | -18% | below 90% line 2 quarters |

### PROTECTED (reformulate-only)
FFP-01 · FFP-04

### PROPOSED REPLACEMENT
Slot: smoothie → bench: Pitaya Punch (90-day trial)

### Next Action
1. Heyns: approve/override in VaultMesh admin (by [date])
2. Apply config → till rebuilds overnight
3. ACCIO re-costs menu BOQ engine for the new line
```

## 8. Dashboard widget (VaultMesh admin)

- Bar: margin contribution per FFP line with the 90% threshold line overlaid
- Table: TRIM LIST with approve/override buttons
- Trend sparklines: 8 lines, 8 quarters
- KPI row: the 6 KPIs from §6, live

---

*Data decides. Taste is banned. The 8-line ceiling is absolute.*
