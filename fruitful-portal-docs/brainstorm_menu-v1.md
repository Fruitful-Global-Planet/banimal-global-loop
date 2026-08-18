# BRAINSTORM — The Radical Menu (v1)
## The McDonald Brothers' 90% Rule, applied to a zero-waste, movable Fruitful Portal

**Date:** 15 Aug 2026 · **Owner:** Heyns · **Status:** Baseline for build

---

## 1. The Lesson (why we cut)

- Pre-Ray-Kroc McDonald's: the brothers had a full menu, then **cut it to the ~90% of sales** — burgers, chips, milkshakes. Everything else canned. That single decision is why the system scaled.
- Fruitful Portal = zero-waste model, tiny footprint (mug-spec kiosk, ~3.3 m²), and physically movable. **Every SKU we keep must earn its shelf space.**
- We are NOT Starbucks (87,000 drink combinations). We are NOT Plato's price trap (Small R38 / Medium R40 / **Large R67** — a 76% jump for ~40% more liquid is a joke customers feel).

**The Fruitful rule:** 3 hot drinks · 3 smoothies · 1 pancake (2 sizes). Total 8 lines. If it doesn't make the top-90%, it's gone — reviewed quarterly, like the brothers.

## 2. The Menu (baseline, layman's terms, no S/M/L/Grande)

### ☕ Coffee — the milk trio, ONE price (data: cappuccino = world #1 across 24 countries; flat white = SA favourite; latte = 2025's most-buzzed; mocha = the sweet tier)

| # | Name (what it is) | Base | Price |
|---|---|---|---|
| 1 | **The Coffee with Milk** *(flat white/latte merged — the daily driver)* | espresso + milk | **R38** |
| 2 | **The Coffee with Froth** *(cappuccino)* | espresso + milk + foam | **R38** |
| 3 | **The Coffee with Chocolate** *(mocha)* | espresso + milk + cocoa | **R38** |

**One price for every coffee — R38 flat, any size (Option A or B).** The size is earned, the pour is proven; the price never changes. No black coffee, no americanos, no syrups, no matcha, no cold brew, no frappe — the fluff is canned.

### 🥤 Smoothies — the top 3, ONE price, ONE size (data-flagged in our own kiosk terminal + category norms)

| # | Name | Why it stays | Price |
|---|---|---|---|
| 1 | **Green Energy** 🌿 | detox/daily-health anchor | **R55** |
| 2 | **Mango Lassi** | mass appeal, low ingredient risk | **R55** |
| 3 | **Power Protein** 💪 | premium ticket, gym crowd | **R55** |

**One price for every smoothie — R55 flat. One size only (fixed 400 ml).** No upsell tiers, no "large" trap. (Pitaya Punch sits as the designated replacement for any line that underperforms at the 90-day cut.)

### 🥞 Pancakes — ONE unit, billed by quantity (×)

| Units | Pieces | Price |
|---|---|---|
| **1** | 1 piece, boxed | **R35** |
| **2** | 2 pieces, boxed | **R70** |
| **5** | 5 pieces, boxed | **R175** |
| **12** | 12 pieces, boxed | **R420** |

**One unit = R35, billed × quantity. Want 2, 5, 12 — you're billed R35 × n.** No tiers, no combo maths, no "double" price class — the customer counts, the till multiplies. The 12-unit box is the natural prepack for the Amazon-DC catalog (movable, zero-waste, consistent portion). One recipe baseline (cinnamon-sugar classic); a rotating variant can replace a loser, never add.

**Total baseline: 8 SKUs.** Bowls and juices are Phase-2 candidates — they re-enter only on data, not nostalgia.

## 3. Sizing — the two options (no nonsense, no Grande)

### Option A — "Stand Against the Wall" (your height IS your size)
A simple height chart at the portal (old-school wall measure):
- **Up to 1.4 m** → Little Cup · 250 ml *(health-suggested intake for smaller bodies)*
- **1.4 – 1.7 m** → Standard Cup · 350 ml
- **Over 1.7 m** → Big Cup · 450 ml

Factual, grounded, layman's terms. The cup you get is *earned by your length*, guided by intake-health suggestion. No menu confusion, no 6-tier size board — one line on the menu: *"Your height is your size. Measure yourself at the wall."*

### Option B — "The Pour We Prove" (machine-verified volume)
One cup for everyone, one price — but **the receipt prints the machine's dispensed volume**:
> The Coffee with Milk — R38 · **Dispensed: 348 ml (machine-verified)**

The Jura/Aquazania machine + VaultMesh telemetry records actual ml dispensed per pour (the same data feeds the 9-second pulse). No under-pour, no "large" premium — **the receipt is the evidence, and the data is already ours** (base44/Convex hookup).

**Recommended: run BOTH.** Option A is the front-of-house story ("the size you earn"), Option B is the trust layer ("the pour we prove") — together they kill the Grande-premium game and fit the tech-meets-tradition brand.

## 4. Why this wins (the mechanics)

1. **Zero-waste:** prepacked pancakes = no close-of-day food waste; height sizing = no dumped "grande" pours; verified pours = no giveaway shrinkage.
2. **Movable + Amazon-DC compatible:** 8 SKUs fit a crate; all consumables listable at supplier cost on Amazon (delivery 5–10% national) — the menu IS the BOQ subset.
3. **Speed:** 3 drink buttons on the kiosk UI, 1 pancake button, 2 size toggles. Training = hours, not weeks. Fits the Jura X8's one-touch strengths.
4. **Margins:** R38 flat coffee at ~R7–9 all-in cup cost = 76%+ margin, priced BELOW Plato's medium with zero size-shaming optics.
5. **Data-ready:** every pour already telemetry; quarterly top-90% cut is automated (VaultMesh/Convex report → ACCIO agent trims the menu).

## 5. Open questions (for the build team)
1. Confirm the Jura X8 can output **exact dispensed ml per drink** into the receipt pipeline (Option B dependency) — verify with Aquazania.
2. Height-chart placement: printed on the kiosk panel vs. digital on the 32" screen? (Digital = updates free, ties to the weather/AQI widget.)
3. Pancake packaging supplier: prepacked box in the Amazon-DC catalog (kraft, branded, R35/R60 pricing verified against cost).
4. Kids' sizing: under-1.4m cup at 250ml — confirm health-suggestion wording is factual, not medical advice (compliance note for the legal pack).

---

*The McDonald brothers cut to 90% of sales and built a system. Fruitful cuts to 8 lines and builds a movable, zero-waste, data-proven network.*
