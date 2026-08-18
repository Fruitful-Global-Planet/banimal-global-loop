---
name: fruitful-portals-pancake-fulfilment
description: >-
  Fruitful Portals pancake fulfilment & packaging task. Use this skill whenever the user references Fruitful pancake packaging, box/container sizes (single, 6-pack, 12-pack, sleeve, packet, shipper), the rolled-pancake singularity, supplier quotes (EXW), Amazon FBA distribution ("Amazon does all distribution / picks up / warehouses / delivers / assembles"), Isowall EPS moulded boxes, Golden Ticket packaging, or asks to intake-hold supplier files for the Fruitful Portals project. Also triggers on "pancake box dimensions", "moulded box", "food paper packet", "Amazon prepacked food guidelines", and packaging cost/economics for the Golden Ticket menu.
---

# Fruitful Portals — Pancake Fulfilment & Packaging

## What this task is

You support the Fruitful Portals pancake line: sizing packaging from the rolled-pancake singularity, sourcing suppliers (EXW), applying the Amazon FBA distribution model, and maintaining the Golden Ticket packaging decisions. The user is Heyns Schoeman (Fruitful Shops Pty Ltd). **This is a real operating business — be exact, cite sources, never fabricate numbers, and follow the add-only documentation rule** (never reduce or restructure approved files without explicit instruction).

## Golden rules

1. **The singularity drives everything.** One rolled milk pannekoek = **210 × 28 × 28 mm** (L = roll length ≈ pancake Ø 230 mm − end squish; W=H = roll Ø). The 50% giving pancake = **105 × 18 × 18 mm** and packs **2 per milk slot** (105+105 = 210 mm exactly). Always re-derive box sizes from these numbers, never guess.
2. **Landscape "pencil case" rule:** rolls lie horizontally; L = roll length stays constant, W = n × roll Ø, H = one roll Ø. Box must be **flat, never high**.
3. **Current packaging decisions (18 Aug 2026):** 1-pack = **recyclable food paper packet** (flat 235 × 45 mm, printed, greaseproof, food-grade) — the single box is DUMPED; 6-pack = corrugated self-lock box outer 232 × 210 × 40; 12-pack = corrugated self-lock box outer 232 × 210 × 74; shipper = 8 × 12-packs 2×2×2 → 470 × 425 × 155. Brand wrap = pre-folded FRUITFUL™ sleeve in 2 sizes that slips over the closed container (container closes itself; wrap carries the brand).
4. **Amazon is the supply chain:** all suppliers quote **EXW** (even local SA); Amazon picks up, warehouses (FBA/AWD), delivers (Amazon Logistics), and preps/assembles (FBA Prep Services/bundling). Landed cost = EXW + Amazon fee stack (referral, fulfilment/unit, storage, inbound, optional prep). Verify the current Amazon fee schedule — do not state fees from memory.
5. **Food compliance (non-negotiable):** sealed + tamper-evident primary packaging; FDA labeling in English (ingredients, allergens, storage/heating); expiration date 36pt+ on product AND master carton; food-grade material certification (or food-grade inner liner); packaging must survive warehouse handling.

## Workflow

### A. Intake mode (supplier files — "read and hold")
When the user says intake/read-and-hold (e.g., Isowall moulded box emails, supplier HTML/xlsx files, screenshots):
1. Locate the file(s) (Downloads, Desktop, attachments — check attachments first).
2. Read them fully; parse ALL data (dimensions, codes, prices, MOQ, contacts) into context.
3. **Do NOT create files or produce output** until the user asks. Hold and confirm intake in one short reply.
4. Note anything unreadable (corrupt files, sandbox-blocked temp folders) honestly and tell the user how to fix it.

### B. Sizing / dimension tasks
1. Re-derive from the singularity (§ Golden rules 1–2).
2. Present inner vs outer (board + print tolerance ≈ 3 mm/side) and the carton/shipper logic.
3. Flag rolled Ø as derived geometry — always include the 10-roll calliper prototype check formula: **inner = (L+15) × (n × Øgap) × (rows × Øgap)**, Øgap = Ø + 6.
4. Cite the source of truth: SA pannekoek are thin crepes made in 8–10" (20–25 cm) pans, rolled with cinnamon sugar.

### C. Sourcing (Alibaba / suppliers)
1. Use `product_supplier_search` (Alibaba) with tight dimension queries (e.g., `230*210*40mm`).
2. Filter for: **secure closure** (self-lock/self-seal/magnetic — NOT loose EPS lids that pop open), **food-grade option**, custom-size capability, cheap unit price (cheap pancakes).
3. Present only the best 1–2 matches per size with images, price/MOQ, and closure type. No long lists.
4. Local SA suppliers (Isowall — 100 m from warehouse; local printers) also quote EXW.

### D. Costing & economics
- Contribution-margin frame: Price − Direct Cost; EXW price is the input; Amazon fees are the distribution layer.
- Reference figures (already validated): Milk single R15.00 (direct R3.71, 75.3%), 6-box R75.00 (R15.66, 79.1%), 12-pack R150.00 (R44.52, 70.3%); giving pancake R0.75. Store: R112,500/mo turnover, R16,800 labour (14.9%), break-even ~50 cups/day.
- 15.01% of every order → Banimal Giving Loop.

## Reference files
Read when needed:
- `references/FRUITFUL_PORTALS_GLOBAL_BACKGROUND_2026-08-18.md` — full ecosystem background (portals, entities, commerce stack, packaging system, Amazon model, supplier context, naming conventions). Read this first for any task touching global context, entities, or the Amazon model.
- Canonical docs live in the workspace: `_analysis/fruitful-portal-reqs/Golden_Ticket_Pancake_Box_Dimension_Spec_2026-08-18.md`, `Golden_Ticket_CI_Guide_MASTER.md`, `Golden_Ticket_Asset_Naming_IP_Register.md`.

## Output conventions
- Files: `FRUITFUL_PORTALS_<TOPIC>_<YYYY-MM-DD>.md`; uploaded assets → `Assets uploaded/<YYYY-MM-DD>/` (dedup-safe).
- Legal marks: ™ on first prominent use (FRUITFUL™, Banimal Giving Loop™, Golden Ticket Menu™, Child Ticker™); **no ® until attorney confirms**; © 2026 Fruitful Shops (Pty) Ltd footer.
- Footer: github.com/fruitful-global-planet/Banimal-global-loop.git · www.banimal.co.za · fruitful.co · fruitful.planet.change@fruitful.co
