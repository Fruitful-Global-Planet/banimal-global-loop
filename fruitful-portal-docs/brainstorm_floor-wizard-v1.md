# BRAINSTORM — The Floor Wizard (zero-waste automated floor)
## The creepy-crawly principle, applied to the Fruitful Portal base

**Date:** 15 Aug 2026 · **Owner:** Heyns · **Status:** Concept — engineering deep-dive required
**Companion:** FRUITFUL_MASTER_BOQ_CANONICAL.xlsx (Dept 06 lines to be voided)

---

## 1. The vision (your words, engineered)

The portal sits on **embedded industrial wheels** (it's movable — that's the advantage). The floor base carries **hundreds of micro-vents**. Underneath: a **suction system like a creepy crawly** — a fixed central vacuum that activates **based on weather conditions AND till output**, sucking the "noise" — crumbs, dust, drips, spill film — away. The floor surface is **sealed like a non-stick pan**: wipe and done, no mop, no bucket, no broom, no chemicals.

**The beauty of the triggers:** both are already in our stack.
- **Weather** → API Ninjas weather/airquality (verified live, per-portal, cached 6h)
- **Till output** → order_items telemetry already flowing to VaultMesh/Convex

The Floor Wizard doesn't need new data infrastructure — it's a new *actuator* on existing signals.

## 2. Engineering reality check (the honest part — why "deep deep research")

**R1 — Suctioning liquids is NOT like suctioning crumbs.** A fan that pulls milk/coffee into a motor dies fast. Real design: **two-path separation** —
- **Dry path:** crumbs/dust → cyclone → fine filter (like a central vacuum)
- **Wet path:** spills/liquid → **sump + small pump** → sealed collection cartridge (emptied weekly, like the creepy crawly's filter bag)
The vents can't be "hundreds of holes to nowhere" — they feed a **plenum plinth** under a grate, with a wet sensor array that routes liquid to the sump.

**R2 — "Non-stick pan" vs "anti-slip floor" is the classic commercial-floor fight.** PTFE-like slickness on a floor = slip liability (SANS/Health Dept will fail you). The answer from real coating tech: **seamless sealed surfaces with anti-slip additive** (Floor Shield / Tile SlipShield / nano-ceramic treatments — verified products exist). "Wipe and done" comes from the surface being *sealed and non-porous*, not from being slippery. Spec: seamless polymer flooring, anti-slip additive, food-grade, chemical-resistant. Non-stick pan is the *experience*; anti-slip sealed is the *engineering*.

**R3 — Noise.** A vacuum running in a mall at 70dB is a problem. Mitigation: runs in **off-peak windows** (triggered cycles, not continuous), sound-insulated plenum, run after close for the deep cycle. Mall hours: deep clean at 09:30 and 14:00 (quiet traffic), plus triggered mini-cycles.

**R4 — Compliance is a feature, not a hurdle.** Health Dept requires *documented* cleaning. The Floor Wizard **auto-logs every cycle** (time, trigger, duration, volume collected) to the `ComplianceAudit` entity — the logbook writes itself. That's a competitive advantage, not an admin cost.

**R5 — Power & redundancy.** Vacuum draws ~1-2kW peak. Existing 1KVA UPS covers the till, not the wizard — add a 2.5KVA UPS or run wizard on mains with UPS only for the controller. If the wizard dies: the floor is still sealed (wipe-and-done manual fallback) — the BOQ keeps a **minimal spill kit** (spill wipes, spray, cloths — ~60% of Dept 06 lines still voided).

## 3. System architecture (concept)

```
                     ┌───────────────────────────────┐
 weather (API Ninjas)│  TRIGGER ENGINE (VaultMesh)    │ till output (order_items)
 ───────────────────>│  rain?  → entrance-ring cycle  │<────────────────────
                     │  peak?  → post-peak mini-cycle │
                     │  22:00  → deep clean cycle     │
                     └──────────────┬────────────────┘
                                    │ activate
             ┌──────────────────────▼──────────────────────┐
             │  FLOOR PLINTH (under the 8m² kiosk footprint)│
             │  micro-vents ──> plenum ──> wet sensor array  │
             │        │ dry path: cyclone → fine filter      │
             │        └ wet path: sump → pump → cartridge    │
             └──────────────────────────────────────────────┘
                     sealed anti-slip polymer floor, wipe-and-done
```

## 4. Trigger matrix

| Trigger | Condition | Cycle | Duration |
|---|---|---|---|
| Rain (weather API) | precipitation > 0.5mm/h | entrance-ring suction | 3 min |
| Mud/footfall (weather + hour) | rain + peak hour | full-floor mini-cycle | 5 min |
| Till output | > 60 orders/2h | post-peak mini-cycle | 5 min |
| Crumbs (pancake prep) | > 20 pancake orders/2h | prep-zone suction | 3 min |
| Spill detected | wet sensor trip | sump pull + ring suction | 2 min |
| Close of day | 22:00 (or close) | deep clean + dry cycle | 15 min |
| Weekly | Sunday close | full cartridge service + filter change | 30 min |

## 5. BOQ impact (the noise that gets VOIDED)

| Voided (Dept 06 / canonical BOQ) | Saved est./mo | Kept (minimal) |
|---|---|---|
| Mop + mop heads + bucket/wringer | R300 | Spill kit pouch + wipes |
| Broom + dustpan + hand brushes | R250 | Surface spray + microfibre (counters) |
| Floor cleaners, degreaser bulk, bucket colour set | R600 | Sanitiser + test strips (compliance) |
| Tea towels (floor duty share) | R150 | — |
| **Added:** Floor Wizard unit (plinth+suction+sump) | — | CAPEX est. R45k–R90k (to be quoted) |
| **Added:** sealed anti-slip floor upgrade | — | CAPEX est. R15k–R25k per portal |

**Net:** ~R1,300/mo recurring removed + zero floor-labour hours per day + auto compliance logs. Payback on the wizard CAPEX (~R60–115k) ≈ 5–8 years at R1,300/mo — **honest flag: the economics stand on labour-hours saved and compliance value, not the small consumables saving.** The real case is the franchise model: "the floor cleans itself" is a sellable line in the R450k package and the zero-waste story.

## 6. Compliance mapping (auto-logbook)

Every cycle writes: `{cycle_id, trigger, start, end, volume_collected_ml, filter_ok, sump_ok}` → `ComplianceAudit` → quarterly H&S report generated (same report engine as VaultMesh). Health inspector sees a perfect, uneditable logbook.

## 7. MVP path (build honest)

- **Phase 1 (ship now):** sealed anti-slip floor upgrade + **docked robot scrubber** (off-the-shelf compact unit, e.g. ~40cm robotic floor scrubber) — triggers from weather+till via the trigger engine; robot docks in the plinth, auto-charges. Cost ~R25–40k. Gets the story, the logs, and the labour saving TODAY.
- **Phase 2 (the wizard):** vented plinth + central suction + sump — custom build with an industrial vacuum OEM (SA or CN). This is the R45–90k CAPEX, needs prototype + mall-site validation (noise, dust load, vent silting).

## 8. Open questions / risks
1. Vents silting with pancake flour/dust — filter service interval? (Prototype test.)
2. Mall floor load: does the plinth add weight beyond the kiosk spec? (Welink base load rating.)
3. Noise acceptance clause in mall lease? (Cycle windows must be contract-compatible.)
4. Wet sump disposal: cartridge is food-waste-adjacent — waste-stream classification.
5. Warranty: custom suction system vs. the Welink structure — who owns the integration?
6. Insurance: automated cleaning ≠ no staff supervision — staff still wipe counters (Dept 06 surface lines stay).

---

## 9. BONUS — The Mop-Sole (staff as the walking wiper)

**The idea (Heyns):** staff wear shoes that *look normal* — but the soles are the mops. Every step is a wipe.

**It's not fantasy — the tech exists at three levels:**
| Level | Reality | Grounding |
|---|---|---|
| **Passive (ship-ready)** | Microfiber slip-on "mop slippers" / cleanroom-style overshoes — fabric soles pick up dust & crumbs as you walk | Real consumer + industrial products (microfiber mop slippers; fleece cleanroom overshoes are standard in pharma/electronics) |
| **Active (prototyped)** | Vacuum slippers — micro-suction intake in the sole, dust collected in a heel chamber | Vacuum-slipper prototypes tested successfully on dust pickup |
| **Smart (concept)** | Motorized rotating sole that self-cleans at a dock | Documented smart-shoe concept (micro DC drive) |

**Fruitful's version — the distributed creepy crawly:**
- **Soles = replaceable microfiber "pads"** clipped onto a normal-looking, food-grade, closed-toe, anti-slip shoe (the pad is the mop; the shoe stays compliant).
- **Every step = a continuous wipe.** Staff movement covers the 8m² footprint with zero dedicated cleaning time — the floor film and crumbs never settle long enough to need a mop.
- **The plinth becomes the wash dock:** at shift end (or break), staff step onto the dock → pad wash/dry cycle runs with the wizard's sump → pads come back clean. The vented floor handles *wet spills*; the soles handle the *ongoing film* — complementary layers, no overlap.
- **NFC-tagged pads:** each pad has a tag; the dock logs "Pad 3 — 14:02 wash, 4,200 steps" → `ComplianceAudit` auto-writes the floor-hygiene logbook. The health inspector sees step-count cleaning data. That's the story.

**Honest risks:**
1. **Slip safety is the boss:** wet-zone walking with fabric soles = liability. Pad material must be anti-slip certified (the same SANS conflict as the floor — solved with patterned grip, not hope).
2. **Pad wear + laundry economics:** pad life, wash cycles, replacement cost per portal/mo — must beat the ~R1,300/mo floor consumables it replaces (est. pad set R120–200, 2 sets/portal, swap weekly — in the right ballpark).
3. **"Looks normal" constraint:** the pad clips under the toe/heel only, hidden by the shoe profile — design brief for the shoe OEM (pair with the Vellies supplier — the brand makes it work: *the Vellies that mop*).
4. **Pad hygiene between swaps:** pads are food-adjacent — wash dock + spares required, no "wet pad overnight" (bacteria).

**The one-liner:** *"The floor cleans itself, and the staff clean it as they walk — the shoes are the mops, the receipts are the logbook."* — the fifth zero: zero cleaning time.

---

*The floor that cleans itself, triggered by the rain and the register. Zero waste of matter, time and attention — the fourth zero.*
