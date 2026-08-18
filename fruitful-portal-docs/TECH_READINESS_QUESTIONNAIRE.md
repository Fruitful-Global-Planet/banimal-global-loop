# Tech Readiness Questionnaire for IT Hardware Suppliers

**Project:** Fruitful Portal (2026-2030)
**Objective:** Evaluate hardware compatibility with the HotStack API / base44 SDK ecosystem.
**Ecosystem Backbone:** `fruitfulapp.base44.app` (Node.js SDK)

---

## 1. General Connectivity & API Integration

*   **1.1 SDK Compatibility:** Does the hardware support a Node.js runtime or provide a REST API capable of receiving/sending JSON payloads to an external endpoint (`fruitfulapp.base44.app`)?
*   **1.2 base44 Integration:** Can the device be pre-configured with an `api_key` and `appId` for secure headless authentication?
*   **1.3 Offline Sync:** Does the device support local data caching and automatic re-syncing once a 5G/LTE connection is restored?
*   **1.4 Remote Management:** Does the hardware support MDM (Mobile Device Management) for remote software updates to the "Marketplace Operator App"?

---

## 2. Item Specific: Rugged 10" Staff Tablets

*   **2.1 Battery Endurance:** Can the unit provide a minimum of **12 hours of active screen-on time** under high-brightness outdoor conditions?
*   **2.2 Environmental Protection:** Is the unit rated for IP65 or higher (dust/water resistance) and drop-tested to MIL-STD-810H?
*   **2.3 Biometric Support:** Does the tablet include a front-facing camera or fingerprint reader compatible with biometric attendance software?
*   **2.4 Performance:** Minimum 8GB RAM and Octa-core processor to handle real-time inventory audits (`SageItemRaw`) without lag.

---

## 3. Item Specific: Digital e-Ink Nametags

*   **3.1 Display Specs:** Does the tag use a multi-color e-Ink display (Black/White/Red/Green) to match the Fruitful CI identity?
*   **3.2 Connectivity:** Does the tag support NFC/RFID for kiosk access control and Bluetooth/Wi-Fi for API-driven status updates?
*   **3.3 API Sync:** Can the tag display be updated dynamically via a webhook or API call from the base44 IAM entity?
*   **3.4 Power:** Is the battery life rated for 6+ months on a single charge with daily status updates?

---

## 4. Item Specific: Industrial 5G/LTE Routers

*   **4.1 Thermal Rating:** Is the router rated for high-temperature environments (up to 60°C) inside a sealed fibreglass kiosk?
*   **4.2 Antenna Support:** Does the unit support external high-gain antennas to be mounted on the kiosk's exterior plinth?
*   **4.3 Redundancy:** Does the unit support dual-SIM failover with auto-switch between providers?
*   **4.4 Security:** Does the unit support hardware-level VPN or static IP configurations for secure VaultMesh connectivity?

---

## 5. Item Specific: Digital Writing Pads (e-Ink)

*   **5.1 Sync Capability:** Can handwriting be instantly digitized and exported as PDF/JSON to the `ComplianceAudit` entity?
*   **5.2 Durability:** Is the screen surface scratch-resistant for heavy use in a high-traffic retail environment?
*   **5.3 Latency:** Is the writing latency < 25ms to provide a natural "pen-to-paper" feel for artisan ambassadors?

---

**Supplier Declaration:**
*I, the undersigned, confirm that the hardware proposed meets or exceeds the requirements stated above and is compatible with the base44 SDK for real-time data integration.*

**Signed:** __________________________ **Date:** _________________
