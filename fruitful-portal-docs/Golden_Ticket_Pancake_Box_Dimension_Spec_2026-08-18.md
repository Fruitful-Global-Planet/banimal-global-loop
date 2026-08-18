# Golden Ticket — Pancake Box Dimension Spec

**Fruitful Portal · Banimal Giving Loop™ · Golden Ticket Menu™**
**Owner:** Fruitful Shops (Pty) Ltd — © 2026. All rights reserved.
**Status:** Current spec — 18 Aug 2026 · Derived from SA pannekoek research + roll geometry

**Scope:** The **Milk Pannekoek (R15 / R75 / R150)** is the sellable product and defines all packaging. The **50% Golden Ticket pannekoek is the giving pancake (R0.75 dead cost, not sold)** — it uses the same boxes, packed 2 per slot.

---

## 1. Source of truth — the South African pannekoek

| Attribute | Value | Source |
|---|---|---|
| Pan diameter (home) | 8" = 20 cm (9" = 23 cm common) | foodleclub.com — "I used an 8" pan. If I use a 9" pan I normally get about 14 pancakes" |
| Pan diameter (retail/commercial) | 25 cm pancake pan | Tefal SA "Total Non-Stick 25cm Pancake Pan" |
| Batter | Thin, crepe-like — fills the whole pan | thecinnamonjar.com — "swirl it around to evenly distribute it to the edges" |
| Thickness | ~2–3 mm (thin crepe) | Crepe conventions (reluctantgourmet.com — thin, flexible, rolled) |
| Serving | Rolled with cinnamon sugar; ends open | thecinnamonjar.com / feastandwest.com |
| Rolled result | "Large, thinly rolled pancakes" — compacts dramatically | thebigtastybite.com |

**Design pannekoek (SA):** flat diameter **Ø = 230 mm** (9" pan), thickness **t = 2.5 mm**.

## 2. Roll sizes (the singularity)

```
MILK (100%, sellable):   L × W × H  =  210 × 28 × 28 mm   (roll length × roll Ø × roll Ø)
GOLDEN TICKET (50%, giving):         =  105 × 18 × 18 mm  (fits 2 per milk slot)
```

- Rolled length ≈ pancake diameter minus end squish (230 → 210 mm; 115 → 105 mm).
- Rolled Ø derived from crepe-area → cylinder calc + air allowance; ranges: milk Ø 25–30, GT Ø 16–20.

## 3. Unified packaging system — one box set, 100% Milk boxes

Layout: **landscape "pencil case"** — rolls lie horizontally; box height = one roll Ø, flat, never high.
Margins: +15 mm on length, Ø design gap 28 → 34 mm (absorbs ±3 mm hand-rolling variance).

| Pack | Container | Size L×W×H (mm) | Milk capacity | 50% GT capacity (2/slot) | Mixable |
|---|---|---|---|---|---|
| **1** | **Recyclable food paper packet** (no box) | **235 × 50** (flat, printed) | 1 roll | 2 rolls | yes |
| **6** | Corrugated self-lock box | Inner 225 × 204 × 34 / **outer 232 × 210 × 40** | 6 rolls | 12 rolls | yes (per slot) |
| **12** | Corrugated self-lock box | Inner 225 × 204 × 68 / **outer 232 × 210 × 74** | 12 rolls | 24 rolls | yes (per slot) |

Why it works: 2 × 50% rolls end-to-end = 105 + 105 = **210 mm = exactly the milk roll length**; GT Ø 18 mm sits freely in the 34 mm slot. One SKU set, no dead giving packaging, giving pancakes ride along in any order.

### 3.1 Single pack — recyclable food paper packet (decision, 18 Aug 2026)

The single-roll **box is dumped**. The 1-pack is a **printed, recyclable food-grade paper packet**:

- **Paper:** recyclable food-grade kraft / greaseproof (food-contact certified — FDA 21 CFR / EU food contact; greaseproof coating so syrup doesn't bleed through)
- **Size:** flat packet **235 × 50 mm** (roll 210 × 28 fits with comfort; **45 mm was flagged too tight** — a flat pouch wraps a Ø by half-perimeter, so 45 mm allows max Ø ≈ 28.6 = 0.6 mm clearance at design Ø28; 50 mm allows Ø ≤ ~31.8, absorbing ±3 mm hand-rolling variance; holds 1 milk roll or 2 GT rolls end-to-end)
- **Print:** full FRUITFUL™ branding per CI Guide — brand line, "1 PANNEKOEK", giving-loop tagline, ©/™ marks, nutritional + heating info (FDA English labeling; expiry 36pt if FBA-bound)
- **Closure:** fold-and-tuck or heat-seal; if sold online, **seal = tamper evidence** (Amazon food requirement)
- **Saves:** one box SKU + its tooling cost; packet stock is a fraction of board cost

## 4. Carton / pallet (Amazon FBA-ready)

- Shipper = **8 × 12-packs, stacked 2×2×2** → **470 × 425 × 155 mm**.
- Capacity: 96 milk rolls, or 192 giving rolls, or any mix.
- **Pallet (48"×40" = 1219 × 1016 mm): 4 shippers per layer (2×2)** — 1219/470 = 2.59 → 2; 1016/425 = 2.39 → 2 (rotated: same 2×2). **NOT 8 per layer** (corrected 18 Aug 2026).
- Stack: shipper 155 mm high → ~10 layers within Amazon's FBA pallet height limit (typically 72" incl. pallet — verify current limit) → **~40 shippers/pallet = 480 twelve-packs = 5,760 milk rolls**.

## 5. Prototype check (before ordering)

1. Roll 10 actual Milk pannekoek (and 10 of the 50% giving pannekoek).
2. Calliper the max length L and rolled Ø of each.
3. Plug in: **inner box = (L+15) × (n × Øgap) × (rows × Øgap)**, where Øgap = Ø + 6.
4. If 2 × GT end-to-end uses the full 225 mm length (bulging ends), bump inner L to 230 mm.

## 6. Sources

thecinnamonjar.com (granny Julia's pannekoek, thin crepe roll) · foodleclub.com (8–9" pan, ~14 pancakes) · Tefal SA 25cm pancake pan · thebigtastybite.com ("large, thinly rolled") · feastandwest.com · reluctantgourmet.com (crepe thickness conventions).

---
*FRUITFUL™ · Banimal Giving Loop™ · © 2026 Fruitful Shops (Pty) Ltd · github.com/fruitful-global-planet/Banimal-global-loop.git · www.banimal.co.za · fruitful.co · fruitful.planet.change@fruitful.co*
