# gen_review_sql.py — build the complete Fruitful review database SQL (offline; upload when network returns)
# Reads every workbook we created and emits a single PostgreSQL script.
import csv, io
from openpyxl import load_workbook

OUT = 'FRUITFUL_REVIEW_DB.sql'
S = []
def q(v):
    if v is None: return "NULL"
    return "'" + str(v).replace("'", "''") + "'"

S.append("-- =====================================================================")
S.append("-- FRUITFUL PORTAL REVIEW DATABASE (deep-dive upload package)")
S.append("-- Generated: 16 Aug 2026 · Source: all analysis workbooks")
S.append("-- Owner: Fruitful Shops (Pty) Ltd · For final review & discussion")
S.append("-- =====================================================================")
S.append("DROP SCHEMA IF EXISTS fruitful CASCADE;")
S.append("CREATE SCHEMA fruitful;")
S.append("SET search_path TO fruitful;")

# ---------- portals ----------
S.append("CREATE TABLE portals (id text PRIMARY KEY, country text, city text, currency text, fx_to_zar numeric, status text);")
portals = [
    ("P-001","South Africa","Pretoria","ZAR",1.00,"flagship"),
    ("P-002","USA","New York","USD",0.054,"open"),
    ("P-003","Japan","Tokyo","JPY",8.25,"open"),
    ("P-004","USA","Texas","USD",0.054,"open"),
    ("P-005","Botswana","Gaborone","BWP",0.72,"open"),
    ("P-006","Mexico","Mexico City","MXN",1.05,"open"),
    ("P-007","Iceland","Reykjavik","ISK",7.42,"open"),
    ("P-008","Zimbabwe","Victoria Falls","USD",0.054,"open"),
    ("P-009","Egypt","Cairo","EGP",2.65,"open"),
    ("P-010","Thailand","Bangkok","THB",1.95,"open"),
    ("P-011","Canada","Toronto","CAD",0.076,"coming_soon"),
]
for p in portals:
    S.append(f"INSERT INTO portals VALUES ({q(p[0])},{q(p[1])},{q(p[2])},{q(p[3])},{p[4]},{q(p[5])});")

# ---------- menu lines + costs ----------
S.append("CREATE TABLE menu_lines (sku text PRIMARY KEY, line_en text, price_zar numeric, direct_cost numeric, margin_pct numeric);")
MENU = [
    ("FFP-01","The Coffee with Milk",38.00,14.66,61.4),
    ("FFP-02","The Coffee with Froth",38.00,14.66,61.4),
    ("FFP-03","The Coffee with Chocolate",38.00,17.06,55.1),
    ("FFP-04","Green Energy smoothie",55.00,23.40,57.5),
    ("FFP-05","Mango Lassi smoothie",55.00,23.40,57.5),
    ("FFP-06","Power Protein smoothie",55.00,23.40,57.5),
    ("FFP-07","Pancake unit (prepacked)",35.00,8.32,76.2),
    ("FFP-08","Pancake 12-pack",420.00,99.84,76.2),
]
for m in MENU:
    S.append(f"INSERT INTO menu_lines VALUES ({q(m[0])},{q(m[1])},{m[2]},{m[3]},{m[4]});")

S.append("CREATE TABLE menu_translations (lang text, sku text, label text);")
TRANS = {
    "ja": ["ミルク入りコーヒー","泡立ちコーヒー","チョコ入りコーヒー","グリーンエナジー","マンゴーラッシー","パワープロテイン","パンケーキ","パンケーキ12個入り"],
    "es": ["Café con Leche","Café con Espuma","Café con Chocolate","Energía Verde","Lassi de Mango","Proteína de Poder","Panqueque","Panqueques (12 unidades)"],
    "is": ["Kaffi með mjólk","Kaffi með froðu","Kaffi með súkkulaði","Græn orka","Mangó lassi","Kraftprótein","Pönnukaka","Pönnukökur (12 stk)"],
    "ar": ["قهوة بالحليب","قهوة برغوة","قهوة بالشوكولاتة","الطاقة الخضراء","مانجو لاسي","بروتين القوة","بان كيك","بان كيك (١٢ قطعة)"],
    "th": ["กาแฟใส่นม","กาแฟฟองนม","กาแฟใส่ช็อกโกแลต","พลังงานสีเขียว","มะม่วงลาสซี่","พาวเวอร์โปรตีน","แพนเค้ก","แพนเค้ก 12 ชิ้น"],
    "fr": ["Le Café au Lait","Le Café Mousseux","Le Café au Chocolat","Énergie Verte","Lassi à la Mangue","Protéine de Puissance","Crêpe","Crêpes (paquet de 12)"],
}
skus = [m[0] for m in MENU]
for lang, labels in TRANS.items():
    for sku, label in zip(skus, labels):
        S.append(f"INSERT INTO menu_translations VALUES ({q(lang)},{q(sku)},{q(label)});")

# ---------- BOQ items (from canonical workbook) ----------
S.append("CREATE TABLE boq_items (dept text, item text, spec text, freq text, agent text, unit_price_zar text, source text, ffp_sku text);")
wb = load_workbook('FRUITFUL_MASTER_BOQ_CANONICAL.xlsx')
ws = wb['18-Dept BOQ (Priced)']
n_boq = 0
for row in ws.iter_rows(min_row=2, values_only=True):
    if not row or not row[0]: continue
    S.append(f"INSERT INTO boq_items VALUES ({q(row[0])},{q(row[1])},{q(row[2])},{q(row[3])},{q(row[4])},{q(row[5])},{q(row[6])},{q(row[7])});")
    n_boq += 1
print(f"BOQ items: {n_boq}")

# ---------- malls ----------
S.append("CREATE TABLE malls (rank int, name text, address text, province text, city text, km_from_pta numeric, tier text, contact_email text, wave text);")
wb = load_workbook('FRUITFUL_MALL_REGISTER.xlsx')
ws = wb['Mall Register (ranked)']
n_malls = 0
for row in ws.iter_rows(min_row=2, values_only=True):
    if not row or not row[1]: continue
    km = row[5] if isinstance(row[5], (int, float)) else None
    S.append(f"INSERT INTO malls VALUES ({row[0]},{q(row[1])},{q(row[2])},{q(row[3])},{q(row[4])},{km},{q(row[6])},{q(row[7])},{q(row[8])});")
    n_malls += 1
print(f"Malls: {n_malls}")

# ---------- deployment economics ----------
S.append("CREATE TABLE deployment_economics (rank int, mall text, tier text, est_rent_zar numeric, est_profit_zar numeric, capex_zar numeric, payback_months numeric);")
wb = load_workbook('FRUITFUL_DEPLOYMENT_TRACKER.xlsx')
ws = wb['Deployment Tracker']
n_dep = 0
for row in ws.iter_rows(min_row=2, values_only=True):
    if not row or not row[1]: continue
    def num(v):
        if isinstance(v, (int, float)): return v
        if isinstance(v, str):
            v = v.replace("R", "").replace(",", "").strip()
            try: return float(v)
            except: return None
        return None
    S.append(f"INSERT INTO deployment_economics VALUES ({row[0]},{q(row[1])},{q(row[2])},{num(row[6])},{num(row[7])},{num(row[8])},{num(row[9])});")
    n_dep += 1
print(f"Deployment rows: {n_dep}")

# ---------- container fill ----------
S.append("CREATE TABLE container_fill (item text, supplier text, unit_cost_usd numeric, cbm numeric, units_loaded int, freight_saved_zar numeric);")
CF = [
    ("400ml PET smoothie cup","Guangzhou Hongkai (16y, 4.5★)",0.03,3.0,3600,None),
    ("Dome lid 98mm","Hongkai (bundle)",0.015,1.0,2500,None),
    ("Wide paper straw 10mm","Hongkai / Telling",0.02,1.0,4000,None),
    ("12oz branded hot cup","Guangzhou Victory / Yulong",0.06,2.0,2400,None),
    ("Kraft pancake box (flat)","Guangzhou Maibao / Richpack",0.015,1.5,4500,None),
    ("Ceramic mug 350ml (printed)","Xiamen Rising Chance (17y Gold, 5.0★)",0.60,1.0,220,None),
]
LCL = 58510.0/5.5
for c in CF:
    fs = c[3] * c[4] * LCL if c[3] and c[4] else None
    S.append(f"INSERT INTO container_fill VALUES ({q(c[0])},{q(c[1])},{c[2]},{c[3]},{c[4]},{fs});")

# ---------- history log (decisions timeline) ----------
S.append("CREATE TABLE history_log (ts text, event text, detail text);")
HIST = [
    ("2026-08-15","Deep dive: bushcoding + fruitfulinterface repos","Architecture, auth findings, risk register (10 items)"),
    ("2026-08-15","China kiosk program","Welink kiosk $3,500/unit x9, Afristar freight R58,510, landed R123,085 single / R95k batch"),
    ("2026-08-15","Aquaspresso decision","Jura X8 Option B R690/mo + R1,392 beans; local rental beats import; negotiated price anchors"),
    ("2026-08-15","Market-corrected pricing","R92/cup rejected; blended R45 incl VAT (R39.13 ex) anchored to Starbucks R51/vida R48/Plato R48"),
    ("2026-08-15","Unit economics","Labour+packaging in: profit R13,024/mo @50 cups; break-even 32 cups/day (2 staff)"),
    ("2026-08-15","Master BOQ 18 departments","508 line items priced+sourced; 19 factual, rest quote-required"),
    ("2026-08-15","Franchise Pack v2","R450k Mercedes-standard (R380k build + R70k stock credit); ongoing R25,326/mo/portal; Amazon DC spine"),
    ("2026-08-15","Accrual model (bank-grade)","Franchisee Y1 net R410,999; HQ 10 portals R2.6M/yr; brand CAGR 18% -> R1.03M Y5 (Plato curve)"),
    ("2026-08-15","Radical menu (McDonald's rule)","8 lines, 3 prices, 1 multiplier; pancake R35 x n; coffee R38 flat; smoothie R55 one size"),
    ("2026-08-15","Zero-waste-of-choice doctrine","Hick's Law + jam study; BushCoding = freed attention; quarterly trim via VaultMesh"),
    ("2026-08-15","Floor Wizard + Mop-Sole","Vented self-cleaning floor (weather+till triggers); mop-sole patent disclosure FSP-MOP-001 (pending)"),
    ("2026-08-15","Mall register + tracker","117 centres ranked by distance from PTA; 16 premium/60 regional/41 nbrhd; combined profit R10.2M/mo"),
    ("2026-08-15","Portal Optimiser","Phase 1 site engine (117 scored, top-10 = Premium payback 1.6-1.7mo); Phase 2 economics (staffing/price/rent/menu)"),
    ("2026-08-16","Global matrix","11 portals, 7 languages, 9 currencies; FX + translations in DB"),
    ("2026-08-16","Container fill","GZ dead space 12cbm = R127.7k freight saved + R10.5k goods; packaging landed 25-35% of BOQ estimates"),
    ("2026-08-16","Neon upload initiated","Review DB package built; network outage at upload time — pending connection restore"),
]
for h in HIST:
    S.append(f"INSERT INTO history_log VALUES ({q(h[0])},{q(h[1])},{q(h[2])});")

# ---------- financial snapshot ----------
S.append("CREATE TABLE financial_snapshot (metric text, value_zar numeric, basis text);")
FIN = [
    ("Kiosk landed (single)", 123085, "Welink $3,500 + Afristar freight/duty"),
    ("Kiosk landed (batch of 9)", 95000, "freight per unit drops"),
    ("Portal capex in mall (nbrhd)", 190085, "landed + NUCO deploy + deposit"),
    ("Portal profit/mo (nbrhd, 2 staff)", 55914, "180k rev tier"),
    ("Portal profit/mo (regional)", 96216, "280k rev tier"),
    ("Portal profit/mo (premium)", 144518, "400k rev tier"),
    ("Franchise package", 450000, "R380k build + R70k stock credit"),
    ("Franchisee Y1 net (accrual)", 410999, "ramp 55/70/85/100%"),
    ("HQ Y1 net (10 portals, direct)", 2598158, "after overhead + tax"),
    ("LTV per franchisee (5yr)", 1733560, "one-off + ongoing"),
    ("Container dead-space value", 138158, "freight + goods per 9-kiosk container"),
]
for f in FIN:
    S.append(f"INSERT INTO financial_snapshot VALUES ({q(f[0])},{f[1]},{q(f[2])});")

# ---------- suppliers ----------
S.append("CREATE TABLE suppliers (name text, role text, contact text, terms text, status text);")
SUP = [
    ("Guangzhou Welink (Gary)","Kiosk hardware","Via Alibaba / WL20260401C","$3,500/unit x9; 25-day lead","Ordered"),
    ("Aquazania / Aquaspresso (Kedibone)","Coffee machines + beans + cleaning","kedibonema@aquaspresso.co.za; 010 591 9240","Jura X8 R690-1,690/mo; beans R348/kg","Proposal in hand"),
    ("Afristar Freight","LCL freight","Est. No. 108923","R44,473.92 excl VAT (5.5cbm)","Quote received"),
    ("Tshwane Market","Fresh fruit & veg","012 358 2302","No minimum; buyer's tag R10","Ready"),
    ("Freshpro Market","Fruit & veg daily top-ups","WhatsApp 067 540 6264","No min; R30 delivery free >R400","Ready"),
    ("Nasci Produce","Prepped produce","+27 82 258 4572","Daily pricelist","Ready"),
    ("Victoria Falls Coffee Co","ZW coffee (P-008)","vicfallscoffee@icloud.com","~USD 22-28/kg","Ready to contact"),
    ("Grand Maghandlela","Fedora hats + paintings","+27 72 414 0117","~50 hats/mo; 247 sold","Restock Task C"),
    ("Guangzhou Hongkai","Packaging cups/lids/straws","Alibaba (16y, 4.5★)","400ml PET $0.02-0.04; GZ","Quoted (agent)"),
    ("Xiamen Rising Chance","Ceramic mugs","Alibaba (17y Gold, 5.0★)","$0.55-0.65 printed, MOQ 48","Quoted (agent)"),
    ("Guangzhou Victory / Yulong","Hot cups","Alibaba","12oz $0.03-0.08","Quoted (agent)"),
    ("Guangzhou Maibao / Richpack","Pancake boxes","Alibaba","flat kraft $0.01-0.02","Quoted (agent)"),
]
for s in SUP:
    S.append(f"INSERT INTO suppliers VALUES ({q(s[0])},{q(s[1])},{q(s[2])},{q(s[3])},{q(s[4])});")

S.append("-- ===================== end =====================")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(S))
print(f"SQL written: {OUT} ({len(S)} lines)")
