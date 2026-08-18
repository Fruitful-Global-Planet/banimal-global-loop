# Kiosk Till Spec — The 8-Line Quantity Engine

**Build date:** 15 Aug 2026 · **Owner:** Heyns · **Platform:** fruitfulinterface (TanStack Start + Supabase) → base44/Convex hooks

---

## 1. The screen (32" touch, portrait-safe)

**Dynamic Localization Engine:**
The UI renders labels and currencies based on the `portalId` (base44 IAM entity lookup).

```
┌─────────────────────────────────────┐
│  FRUITFUL [EN|JA|ES|IS|AR|TH|FR]    │
├─────────────────────────────────────┤
│ ☕ {{MENU_COFFEE_MILK}}     {{PRICE}} │
│ ☕ {{MENU_COFFEE_FROTH}}    {{PRICE}} │
│ ☕ {{MENU_COFFEE_CHOC}}     {{PRICE}} │
│ 🥤 {{MENU_SMOOTHIE_1}}      {{PRICE}} │
│ 🥤 {{MENU_SMOOTHIE_2}}      {{PRICE}} │
│ 🥤 {{MENU_SMOOTHIE_3}}      {{PRICE}} │
│ 🥞 {{MENU_PANCAKE}}   [−] 3 [+] {{TOT}} │
│                                     │
│        [ {{ORDER_LABEL}} — {{TOT}} ] │
└─────────────────────────────────────┘
```

**Global Currency Logic:**
Prices are calculated using the `FX_RATE` stored in the **Global Portal Matrix**.
- **ZA (ZAR):** R38 / R55 / R35
- **US (USD):** $2.05 / $2.97 / $1.89
- **JP (JPY):** ¥310 / ¥450 / ¥290
- **MX (MXN):** $40.00 / $57.75 / $36.75
- **IS (ISK):** 282 kr / 408 kr / 260 kr

**Rules:** 8 buttons · 1 base price per category · 1 quantity multiplier.

## 2. Order logic (the till)
...
### Cart → Paystack / Local APM
- **ZA/BW:** Paystack ZAR inline.
- **US/CA:** Stripe / PayPal USD.
- **JP/TH/MX:** Local Alternative Payment Methods (APMs) via the base44 Payment gateway.
- Webhook HMAC-SHA512 verified on all transactions.


## 3. The receipt (Option B live)

```
FRUITFUL PORTAL — PTA BUSH
Order FFL-041733 · 15 Aug 2026 09:41
────────────────────────────
The Coffee with Milk     R38
  Dispensed 348 ml — machine-verified
Green Energy (400 ml)    R55
Pancake 12-pack           R420
  (12 × R35)
────────────────────────────
TOTAL                    R513
QR → BushCoding session  ✓
```

## 4. Telemetry & the quarterly cut (McDonald's rule, automated)

- Every pour logs: `{drink, ml, price, qty, ts, portal}` → VaultMesh pulse (9s) + Convex.
- **Quarterly menu-trim report:** ACCIO agent reads sell-through per line; any line below the top-90% threshold is flagged; Heyns confirms the can; Pitaya Punch / rotation slot fills it. **Data decides, not taste.**

## 5. States & resilience

`attractor (45s idle, weather/AQI + Banimal Loop story) → browse → cart → paying → success (12s) → attractor`
- Offline: order queued locally (SQLite/localStorage), synced on reconnect to base44; payment falls back to cash → verified at close (Dept 05 cash protocol).
- Machine failure (Jura down): coffee buttons disabled, smoothies/pancakes stay live — never a dead kiosk.

## 6. Build checklist
1. Menu data model: 8 lines, 3 prices, qty flag on pancakes only.
2. Quantity stepper component with presets 1/2/5/12 + live total.
3. Jura telemetry hook → receipt `Dispensed ml` (verify X8 exposes per-pour ml with Aquazania — open question from brainstorm v1).
4. Paystack ZAR inline + HMAC webhook (reuse bushcoding payments module).
5. Order ref + receipt renderer (thermal 80mm + on-screen).
6. Offline queue + sync.
7. Quarterly trim report (Convex query → ACCIO agent).
