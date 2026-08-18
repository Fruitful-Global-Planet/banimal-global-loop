# ACCIO™ Agent Playbook — Fruitful Portal Sourcing Automation

**Watermark:** `GC7:FSP2021121654:4400302974:VM9s:BL1501:ACCIO:FAA13713`
**Companion:** `Fruitful_Portal_Master_BOQ_18Dept.xlsx` (508 line items, 18 departments)

---

## 1. Agent Map (8 sub-agents → BOQ departments)

| Agent | Department (BOQ) | Trigger | Data Source | Output |
|---|---|---|---|---|
| **A — Coffee & Beverage** | D01, D02 equip | Weekly stock threshold | SageItemRaw | PO draft + WhatsApp to roaster |
| **B — Consumables & Packaging** | D03, D04, D14 | 1st of month | Prior-month payments | Packaging PO per portal |
| **C — Cleaning, PPE & Sanitation** | D06, D07 (+D04 waste) | Monthly + failed inspection | COSHH/SDS logs | Chemical PO + compliance check |
| **D — Cash & Payments** | D05, D12, D16 | Daily close-of-day | Paystack vs float report | Discrepancy flag + revenue summary |
| **E — Food Ingredients** | D02 ingredients | Every 3 days | Fridge temp log | Perishables order + FIFO rotation |
| **F — Artisan Restock** | D04.4 + products table | Stock < 5 units | products.inStock | WhatsApp Grand/Venda + PO |
| **G — Maintenance & Compliance** | D08–D10, D12–D13, D15, D17–D18 | Monthly audit calendar | Service schedules | Certification bookings + flags |
| **H — Staff & Uniforms** | D11, D07 apparel | New hire / quarterly | base44 user entity | Uniform order + size tracking |

## 2. Master Commands

```bash
ACCIO full_audit --portal ZA --date 2026-08-15
ACCIO coffee_restock --portal ZA
ACCIO packaging_order --month 2026-08
ACCIO artisan_restock --sku CLO-001 --qty 50
ACCIO cash_reconcile --portal ZA --date 2026-08-15
ACCIO compliance_audit --portal ZA
ACCIO new_portal_activation --portal CA --open-date 2026-02-01
```

## 3. Priority Queue (from intake §10 + §6.2)

1. 🔴 **Task A — Coffee equipment** (9 kiosks, ≤40cm depth, <$1,200/unit): espresso machine + grinder + filtration + blender. → Alibaba sourcing in progress (see search results).
2. 🔴 **Task B — SA fruit & veg supplier** (Gauteng, kiosk volume). → DONE: [SA_FRUIT_VEG_SUPPLIERS.md](SA_FRUIT_VEG_SUPPLIERS.md) — Tshwane Market (primary), Freshpro, Nasci Produce.
3. 🔴 **Task C — Grand hat restock agreement** (247 sold; ~50 hats/mo capacity; WhatsApp +27 72 414 0117).
4. 🟠 **Task D — Zimbabwe coffee source** (Chipinge/Eastern Highlands, ~5kg/wk).
5. 🟠 **Task E — Packaging spec** (branded dark green #0B0F0E + gold #E8A020; pilot 1,000/size).

## 4. Startup Cost Estimate — Per Portal (excl. Welink kiosk)

| Category | Estimate ZAR |
|---|---|
| Coffee equipment | 45,000–90,000 |
| Food equipment | 25,000–40,000 |
| Refrigeration | 15,000–25,000 |
| IT & POS | 20,000–35,000 |
| Security | 15,000–25,000 |
| Packaging (first stock) | 8,000–15,000 |
| Cleaning kit | 3,000–6,000 |
| PPE & uniforms (5 staff) | 12,000–20,000 |
| Admin & office | 2,000–4,000 |
| Compliance & legal | 5,000–10,000 |
| Outdoor & kiosk | 10,000–20,000 |
| Marketing collateral | 8,000–15,000 |
| **Total** | **R168,000–R305,000** |

## 5. Commerce Guardrails
- ZAR primary; Paystack SA (HMAC-SHA512 webhook verified).
- COGS target: coffee ≤ 28–30% of R92 retail (≤ R27.60/cup).
- Core vs local_culture rule: never substitute mass-produced for artisan.
- Banimal Loop™ disclosed on all Banimal supply agreements.
- HS codes per Appendix B (coffee 0901.21, hats 6504.00, tees 6109.10, cups 4823.20).

*ACCIO™ · Fruitful Shops (Pty) Ltd · reviewed monthly by Heyns Schoeman · +27 72 414 0117*
