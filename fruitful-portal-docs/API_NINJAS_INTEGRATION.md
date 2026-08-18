# API Ninjas Integration — Fruitful Portal Network

**Status:** Key verified live (15 Aug 2026) · Free tier tested against real endpoints
**Base URL:** `https://api.api-ninjas.com/v1/` · **Auth header:** `X-Api-Key: <key>`

---

## 1. Verified free-tier capability (tested)

| Endpoint | Free tier | Example (tested live) |
|---|---|---|
| `/weather` | ✅ **lat/lon only** (city param = premium) | Pretoria: 13°C, feels 11, humidity 53%, wind 0.45 m/s, sunrise/sunset |
| `/airquality` | ✅ **lat/lon only** | Pretoria: overall AQI 95 (PM2.5 38 µg/m³) |
| `/city` | ✅ name | Pretoria: lat −25.7464, lon 28.1881, pop 741,651, Gauteng, capital |
| `/country` | ✅ name | ZA: GDP 368k, unemployment 28.5%, currency ZAR, capital Pretoria |
| `/population` | ✅ country code | ZA: 64.0M (2024), median age 28.5, urban 66.3% |
| `/countryflag` | ✅ (param `flag=`) | — |
| `/postalcode` | ❌ city/province = premium | — |
| `/zipcode` | ❌ city/state = premium | — |
| `/timezone`, `/worldtime` | ❌ premium / temporarily down | — |
| `/county` | US-only, not relevant | — |

**Pattern for all portal queries:** use **lat/lon** (from `/city`) — not city names — on free tier.

## 2. Portal network mapping (11 portals)

| Endpoint | Use case | Portal value |
|---|---|---|
| `/weather` | Kiosk screen "Today in [city]" header; menu logic (hot vs cold drinks); rain = foot-traffic staffing signal | CX + ops |
| `/airquality` | Health display on kiosk; outdoor seating decisions; premium "green" badge | CX + ESG story |
| `/city` | Portal metadata validation: lat/lon, population, capital status; distance-from-PTA calculations for the mall register | Ops + franchise planning |
| `/country` | Market intelligence per portal (GDP, unemployment, currency) — informs local pricing + master-licence territory value | Strategy |
| `/population` | Market sizing for franchise territories & mall catchment | Strategy |
| `/countryflag` | Country/portal picker UI (shop, admin, seedwave sector pages) | UI |

## 3. Existing admin tools (fruitfulinterface repo — already wired)

The kiosk admin (`src/lib/api/ninjas.functions.ts` + `ninjas.server.ts`) already uses API Ninjas for: **password generator, QR code, barcode, EU VAT validation, unemployment data, IP lookup** — key held server-side as `API_NINJAS_KEY`. This integration adds weather/airquality/city/country/population on the same key.

## 4. Quota & caching rules (free tier)

- Free tier ≈ **10,000 calls/month, 1 call/sec** (verify current limits on api-ninjas.com/pricing).
- Budget: 11 portals × 2 endpoints (weather+airquality) × hourly = **~15,840 calls/mo → exceeds free tier**. **Cache per portal for 60 min** → ~528 calls/day = ~16k/mo... still tight. Use 6-hour cache for weather → ~1,300 calls/mo. Cache `/city` and `/country` permanently (static data).

## 5. Security note

- The key was shared in chat — **do not commit it to any repo or client bundle**. Store as server env var `API_NINJAS_KEY` (matches existing `ninjas.server.ts` pattern in fruitfulinterface). If this chat is ever shared externally, rotate the key via api-ninjas.com dashboard.
- All calls must be proxied server-side (server functions / edge) — never call with the key from the kiosk browser.

## 6. Implementation steps

1. Add `API_NINJAS_KEY` to the Convex/Supabase env (bushcoding + fruitfulinterface).
2. Server function `getPortalWeather(portalCode)` → `/city` (lat/lon, cached) → `/weather` + `/airquality` (lat/lon) → cache 6h.
3. Kiosk 32" screen: weather+AQI widget from that function.
4. Admin/franchise tools: `/country` + `/population` cached per portal for market reports.
5. Mall register enrichment: `/city` to auto-fill lat/lon + distance from PTA.
