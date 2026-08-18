# Fruitful Portal — Staff & Operations Spec (2026-2030)

**Vision:** "Tech meets tradition." The Fruitful Portal is not just a kiosk; it is a high-tech node in a global ecosystem. Staff are "Portal Operators" and "Artisan Ambassadors."

---

## 1. Branding & Visual Identity
The branding follows the **Fruitful CI Guide v04** and the hardware specs for the **Guangzhou Welink** kiosk.

- **Primary Colors:** Mint-green (weatherproof body), Coral-red (domed cap).
- **Physical Build:** 4mm high-gloss fibreglass cylinder; illuminated "Fruitful Portal" signage topper.
- **Hardware Interface:** 32" Customer-facing window screen + 43" Internal ops screen.

---

## 2. Staff Uniforms & Apparel (2026-2030)
Staff apparel must bridge the gap between "Tech Professional" and "Local Artisan." All items are branded using the Fruitful visual identity.

| Item | Specification | Design Direction |
|---|---|---|
| **Caps** | Branded structured caps | Mint-green with white 3D embroidered "Fruitful" logo. |
| **Shirts** | Polo shirts & button-downs | "Fruitful Professional" line: high-breathability tech fabric for 2026-2030 climates. |
| **Pants / Skirts** | Tech-chinos & work skirts | Dark charcoal or slate (neutral) to allow the mint-green tops to pop. |
| **Dresses** | Branded staff dresses | Wrap-style dresses with subtle "Banimal" pattern trim for female staff. |
| **Bomber Jackets** | "VaultMesh" Bomber | Heavy-duty, weatherproof insulated jackets for early-morning shifts. Embroidered "9-second pulse" on sleeve. |
| **Scarves** | Artisan-woven scarves | Partnered with local weavers; teal and gold "Sovereign" tier patterns. |
| **Footwear** | **Vellies (Veldskoen)** | Traditional SA leather stitch-down boots. Embossed with the "Fruitful" leaf on the heel. |
| **Safety Shoes** | Steel-toe (Audit mandatory) | Required for setup/logistics phases; branded black leather. |

---

## 3. Digital Nametags & Identity
Traditional plastic tags are replaced with **Dynamic e-Ink Nametags** for the 2026-2030 window.

- **Digital Nametags:**
  - Integrated with the **base44 IAM entity**.
  - Displays: Staff Name, Role (e.g., "Ambassador"), and real-time status (e.g., "On Break" or "Tech Support").
  - QR Code on the tag allows customers to "Meet the Maker" or "Tip via Paystack."
- **Auth:** Nametags serve as NFC/RFID keys for kiosk access (replaces traditional keys).

---

## 4. Tech-Driven Operational Tools
Staff "do work" through a unified digital interface connected to the **HotStack API**.

### 4.1 Digital Connections & Hardware
- **Staff Tablets (Industrial):**
  - Handheld 10" ruggedized units.
  - Runs the **Marketplace Operator App** (base44 SDK).
  - Used for inventory audits (`SageItemRaw`), customer "Support a Local" assistance, and mobile checkout.
- **Digital Writing Pads:**
  - e-Ink tablets for "Operational Logbooks."
  - Replaces paper logs for hygiene checks, cleaning registers, and shift handovers.
  - Instant sync to the `ComplianceAudit` entity in the backend.

### 4.2 Tech-Driven Solutions (2026-2030)
- **Biometric Attendance:** 
  - Facial or fingerprint auth for shift clock-in/out (integrated with `Biometric Attendance Sys License`).
- **9-Second Pulse Monitoring:**
  - The 43" internal screen displays a live **VaultMesh Heartbeat**.
  - Alerts staff to anomalies in coffee temperature, milk levels, or connectivity before they become outages.
- **Automated Replenishment:**
  - Kiosk stock levels (monitored via IoT) trigger `SageItemRaw` procurement requests automatically when they hit the "Daily Threshold."

---

## 5. Staff "Needs to do Work" (The Daily Loop)
1. **Clock-in:** Biometric auth + Digital Nametag activation.
2. **Setup:** Hardware diagnostic via the 43" screen; verify `GreenCoffeeReceipt` moisture/SCA scores.
3. **Operations:** Manage customer "Tech Build" sessions (Baobab AI) while preparing artisan coffee/pancakes.
4. **Maintenance:** Real-time logging of cleaning via Digital Writing Pad.
5. **Logistics:** Use Fleet/Fuel cards for restocking trips; manage local cartage via BobGo/base44 shipping entities.

---

*Synthesis derived from: Fruitful CI Guide v04 · base44 OpenAPI Spec · Fruitful-Coffee Audit & Costing · Welink Hardware Spec.*
