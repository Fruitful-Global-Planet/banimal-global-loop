# Golden Ticket — Asset Naming Convention & IP Register

**Fruitful Portal · Banimal Giving Loop™**
**Status:** v1 — 16 Aug 2026 · © 2026 Fruitful Shops (Pty) Ltd. All rights reserved.

---

## 1. File naming convention (renders & packing layouts)

**Pattern:**
```
[BRAND]-[PRODUCT]-[SKU]-[FORMAT]-[VARIANT]_v[N]
```

| Field | Allowed values | Example |
|---|---|---|
| BRAND | FRUITFUL (Fruitful) | FRUITFUL |
| PRODUCT | PANC (pannekoek) · MENU · GIFT (giving) | PANC |
| SKU | SINGLE · 6PK · 12PK · OUTER · PALLET | 12PK |
| FORMAT | DIECUT (layout net) · RENDER (3D) · PANEL (flat art) · TEMPLATE (source) · LABEL | DIECUT |
| VARIANT | A / B / C (concept) · COLR-A / COLR-B (colourway) | A |
| VERSION | _v1, _v2 | _v1 |

Example: `FRUITFUL-PANC-12PK-DIECUT-A_v1.png`

**Full asset map (first design to now):**

| # | Asset | New standard name |
|---|---|---|
| 1 | Refined 6-pack box (Banimal Giving Loop template) | `FRUITFUL-PANC-6PK-TEMPLATE-A_v1.png` |
| 2 | 12-pack carton — front panel art | `FRUITFUL-PANC-12PK-PANEL-A_v1.png` |
| 3 | Outer shipping carton (12×PANC-12) — panel art | `FRUITFUL-PANC-OUTER-PANEL-A_v1.png` |
| 4 | Single roll box — die-cut layout | `FRUITFUL-PANC-SINGLE-DIECUT-A_v1.png` |
| 5 | Single roll box — 3D render | `FRUITFUL-PANC-SINGLE-RENDER-A_v1.png` |
| 6 | 6-piece box — die-cut layout | `FRUITFUL-PANC-6PK-DIECUT-A_v1.png` |
| 7 | 6-piece box — 3D render | `FRUITFUL-PANC-6PK-RENDER-A_v1.png` |
| 8 | 12-pack case — die-cut layout | `FRUITFUL-PANC-12PK-DIECUT-A_v1.png` |
| 9 | 12-pack case — 3D render | `FRUITFUL-PANC-12PK-RENDER-A_v1.png` |
| 10 | *(pending)* Pallet stacking diagram (8 cartons / 1,152) | `FRUITFUL-PANC-PALLET-DIAGRAM-A_v1.png` |

**Folder structure (asset library):**
```
fruitful.co/assets/packaging/
├── single/   (DIECUT + RENDER)
├── 6pk/      (DIECUT + RENDER + TEMPLATE)
├── 12pk/     (DIECUT + RENDER + PANEL)
├── outer/    (PANEL + LABEL)
├── pallet/   (DIAGRAM)
└── brand/    (logo masters, CI guide)
```

## 2. Trademark register (™)

Apply ™ on first prominent use per panel/document; the ® registration status to be confirmed with the attorney before any ® is used.

| Mark | Type | Placement |
|---|---|---|
| FRUITFUL™ | wordmark | logo lockups, header brand line |
| Banimal Giving Loop™ | sub-brand | brand line on all boxes/cartons |
| Golden Ticket Menu™ | menu brand | menu boards, pitch docs |
| The Child Ticker™ | feature | ticker screens, POS |
| Buy Artisan. Create Apps. Eat Pancakes.™ | slogan | all hero surfaces |
| "Every item you buy = 1 fresh pancake to a child in need today"™ | tagline | tagline band on every panel |
| "This pack feeds N children today"™ | badge copy | 6 / 12 / 144 badges |
| The 9-Second Pulse™ | ecosystem | screens, documentation |
| FAA™ · VaultMesh™ · Seedwave™ · HotStack™ · ClaimRoot™ | ecosystem marks | as already used in the architecture docs |

**Packaging footer standard (every panel):**
```
© 2026 Fruitful Shops (Pty) Ltd. FRUITFUL™ · Banimal Giving Loop™. All rights reserved.
```

## 3. Copyright marks

| Asset | Mark |
|---|---|
| Packaging artwork (all DIECUT/RENDER/PANEL) | © 2026 Fruitful Shops (Pty) Ltd |
| CI guide & naming register (this document) | © 2026 Fruitful Shops (Pty) Ltd |
| Child-in-need illustration & motif | © 2026 Fruitful Shops (Pty) Ltd — do not reuse without licence |
| Photography (kiosk, lifestyle, coffee hero) | © 2026 Fruitful Shops (Pty) Ltd |
| Software (Banimal-global-loop repo) | see NOTICE / FPSL v1.0 in repo |

## 4. Repo & contact footer (small, detailed — for docs, packaging, and site)

```
Source:    github.com/fruitful-global-planet/Banimal-global-loop.git
Web:       www.banimal.co.za · fruitful.co
Contact:   fruitful.planet.change@fruitful.co
© 2026 Fruitful Shops (Pty) Ltd. FRUITFUL™ · Banimal Giving Loop™
```

## 5. Application rules

1. ™ appears on **first prominent use** on a panel — not repeated on every line.
2. © line is mandatory on the **footer of every panel and every document**.
3. No ® anywhere until the attorney confirms registration (pending).
4. Renders for review carry the marks; final production art re-applies them from the master files.
5. Third-party marks (Paystack, Amazon, WordPress, etc.) must never appear on Fruitful packaging.
