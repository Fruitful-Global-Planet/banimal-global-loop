# gen_priced_boq.py — Consolidated FACTUAL BOQ (priced, sourced, same metrics as financial models)
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

FONT = 'Arial'
thin = Side(style='thin', color='BFBFBF')
border = Border(left=thin, right=thin, top=thin, bottom=thin)
hfont = Font(name=FONT, size=11, bold=True, color='FFFFFF')
hfill = PatternFill('solid', start_color='0FB5A6')
bfill = PatternFill('solid', start_color='F2F2F2')
gold = PatternFill('solid', start_color='FFF2CC')

def sheet(ws, headers, widths):
    for j, h in enumerate(headers, 1):
        c = ws.cell(1, j, h); c.font = hfont; c.fill = hfill
        c.alignment = Alignment(horizontal='center', vertical='center'); c.border = border
    for j, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.freeze_panes = 'A2'

def put(ws, r, vals, hl=False):
    for j, v in enumerate(vals, 1):
        c = ws.cell(r, j, v); c.border = border
        if r % 2 == 1: c.fill = bfill
        if hl: c.fill = gold
        c.alignment = Alignment(wrap_text=True, vertical='top')

wb = Workbook()

# ============ Sheet: Read Me ============
ws = wb.active; ws.title = 'Read Me & Metrics'
ws.sheet_properties.tabColor = '0FB5A6'
sheet(ws, ["Metric / Rule", "Value", "Source"], [34, 40, 34])
notes = [
    ("Currency base", "ZAR ex VAT (primary). USD where sourced. FX: R18.45/USD (Aug 2026)", "ACCIO intake §7"),
    ("Baseline volume", "50 cups/day per kiosk (1,500 cups/mo)", "Unit economics model"),
    ("Bean usage", "18 g/cup, R348/kg ex VAT (R1,392/4kg Aquazania)", "Aquazania email + shop R400.20 incl VAT"),
    ("Blended sell price", "R45 incl VAT / R39.13 ex VAT per cup (market-anchored)", "Starbucks SA R51, vida R48, Seattle R28-38, Plato R48"),
    ("Pricing status", "Only VERIFIED prices filled. Blank = quote required (marked TBD)", "—"),
    ("Aquazania shop prices", "Retail listed prices (aquazaniashop.co.za) — confirm wholesale/net invoice with Kedibone", "aquazaniashop.co.za"),
    ("Alibaba prices", "Listed USD per unit/MOQ from product_supplier_search (Aug 2026)", "Alibaba.com"),
    ("Freight", "Afristar Est. 108923: LCL Guangzhou-JHB 5.5cbm/260kg R44,473.92 excl VAT", "Afristar quote"),
    ("Kiosk hardware", "Welink Invoice WL20260401C: $3,500/unit x 9 = $31,500", "Welink proforma"),
    ("VAT", "All SA contracts +15% VAT on top of ex VAT figures", "—"),
]
for i, n in enumerate(notes, 2): put(ws, i, list(n))

# ============ Sheet: Hardware & Setup ============
ws2 = wb.create_sheet('Hardware & Setup')
sheet(ws2, ["Item", "Spec", "Unit", "Price (ex VAT)", "FX/ZAR", "Qty", "Total", "Source"], [30, 30, 10, 16, 14, 8, 16, 34])
hw = [
    ("Welink fibreglass kiosk", "4mm FRP, 2.05m roof/1.81m base/2.63m, dual-screen, lighted logo", "unit", "$3,500.00", "R64,575/unit", 9, "R581,175", "Invoice WL20260401C (Gary, WeLink)"),
    ("Espresso machine (Alibaba, alt to rental)", "Semi-auto 2-group Itop (15-yr supplier)", "unit", "$1,389-1,638", "R25,627-30,220", 0, "—", "alibaba.com/product-detail/...1600985026861"),
    ("Espresso machine (Alibaba budget)", "Chashimi 2-group", "unit", "$938", "R17,300", 0, "—", "alibaba.com ...1600873174410"),
    ("Super-auto (Alibaba, staffless route)", "Jetinno JL29B bean-to-cup", "unit", "$742-834", "R13,690-15,390", 0, "—", "alibaba.com ...1601036097245"),
    ("Burr grinder (Alibaba)", "64mm flat burr Jiaozuo Forward", "unit", "$178", "R3,284", 0, "—", "alibaba.com ...1601827533136"),
    ("Water filtration (Alibaba)", "Aicksn C4-400", "unit", "$50-55", "R922-1,015", 0, "—", "alibaba.com ...1600617250239"),
    ("LCL freight (kiosk shipment)", "Guangzhou-JHB via Durban, 5.5cbm/260kg", "shipment", "R44,473.92", "excl VAT", 1, "R44,473.92", "Afristar Est. 108923 (valid 14 May 2026)"),
    ("Startup kit per portal", "Coffee+food equip, refrigeration, IT/POS, security, packaging, PPE, compliance (see 18-dept BOQ)", "portal", "R168,000-305,000", "excl kiosk", 1, "R168k-305k", "Master BOQ intake (Dept estimates)"),
]
for i, h in enumerate(hw, 2): put(ws2, i, list(h))

# ============ Sheet: Aquaspresso Contract ============
ws3 = wb.create_sheet('Aquaspresso Contract')
sheet(ws3, ["Option", "Rental R/mo (ex VAT)", "Term", "Commitment", "Total R/mo", "Includes", "Source"], [30, 16, 10, 34, 14, 20, 34])
aq = [
    ("Jura X8 Option A (RECOMMENDED start)", "1,690", "36 mo", "None — buy beans as required", "1,690 + beans", "Machine + service", "Kedibone Matloga email 15 Aug 2026"),
    ("Jura X8 Option B (bundled)", "690", "36 mo", "4kg beans/mo @ R1,392", "2,082", "Machine + service + beans", "Kedibone email"),
    ("Nestle Alegria 860 vending", "590", "12 mo", "Product to value R1,500 once-off", "590 + product", "Machine + service", "Kedibone email"),
    ("Bravilor Novo filter", "99", "12 mo", "Filter coffee as required", "99 + filter", "Machine + service", "Kedibone email"),
    ("Jura promo (14 Aug)", "0", "contract", "Sign-up by 14 Aug", "—", "Free Milk Cool Control + R500 cleaning pack", "Kedibone email — ASK TO EXTEND"),
    ("Beans (bundle rate)", "—", "—", "R1,392 / 4kg = R348/kg ex VAT", "R348/kg", "—", "Aquazania contract rate"),
]
for i, a in enumerate(aq, 2): put(ws3, i, list(a))

# ============ Sheet: Alibaba Coffee Equipment ============
ws4 = wb.create_sheet('Alibaba Coffee Equipment')
sheet(ws4, ["Category", "Product", "Price (USD)", "MOQ", "Supplier (Est/Badge/Rating)", "URL (product id)"], [18, 44, 16, 10, 32, 34])
al = [
    ("Espresso", "Professional Single Double Group Semi Automatic", "938", "5pcs", "Chashimi (7y, Verified, 4.4)", "1600873174410"),
    ("Espresso", "Semi Automatic 2 Group Commercial Italian", "1,389-1,638", "1pc", "Itop (15y, Verified, 4.4)", "1600985026861"),
    ("Espresso", "Smart Semi-Automatic Portable 2 Groups", "1,499-1,580", "1 set", "Truwin (9y, Verified, 4.8)", "1601314213526"),
    ("Espresso", "Two Groups Semi-automatic", "1,300-1,750", "2pcs", "Gemilai (15y, Verified, 4.5)", "62518229527"),
    ("Super-auto", "Jetinno JL29B Super Automatic Bean to Cup", "742-834", "24 sets", "Jetinno (10y, Verified, 5.0)", "1601036097245"),
    ("Super-auto", "Dr GT2 Smart Bean to Cup", "1,044-2,088", "1pc", "Dazheng (9y, Verified, 4.9)", "1601256340410"),
    ("Super-auto", "7\" Touch Screen Bean to Cup", "410-485", "1pc", "Shunxin (3y, 4.7)", "1601484489996"),
    ("Compact", "Commercial Espresso w/ Built-in Grinder 20 Bar", "181-262", "1 unit", "Kinghigher (3y, Verified, 4.9)", "1601721384433"),
    ("Compact", "Touch Screen Built-in Grinder", "740", "1 pack", "Angsheng (1y, Verified, 5.0)", "1601822724354"),
    ("Grinder", "64mm Stainless Flat Burr Programmable", "178", "1 set", "Jiaozuo Forward (6y, Verified, 4.3)", "1601827533136"),
    ("Grinder", "90mm Flat Burr with Tamper, Touch", "910", "1pc", "Perfex (10y, Verified, 4.7)", "1601105733606"),
    ("Filtration", "Aicksn C4-400 Water Filtration System", "50-55", "2 sets", "Aicksn (7y, Verified, 5.0)", "1600617250239"),
    ("Filtration", "4-Stage Coffee/Ice/Boiler Purifier", "138-168", "2pcs", "Xilin (3y, 4.9)", "1601216827081"),
]
for i, a in enumerate(al, 2):
    put(ws4, i, [a[0], a[1], a[2], a[3], a[4], f"alibaba.com/product-detail/{a[5]}.html"])

# ============ Sheet: Consumables (priced) ============
ws5 = wb.create_sheet('Consumables (priced)')
sheet(ws5, ["Item", "Unit", "Price ex VAT", "Usage @50 cups/day", "Monthly cost", "Source"], [34, 12, 14, 26, 14, 36])
con = [
    ("Aquazania beans (contract rate)", "kg", "R348.00", "27 kg/mo (18g/cup)", "R9,396.00", "Aquazania R1,392/4kg"),
    ("Whole milk (Dewfresh)", "6x1L", "R132.25", "~135 L/mo (150ml x 75% cups)", "R2,970.56", "aquazaniashop.co.za"),
    ("Oat milk (Milklab)", "8x1L", "R458.85", "standby stock", "TBD", "aquazaniashop.co.za"),
    ("Almond milk (Milklab)", "8x1L", "R458.85", "standby stock", "TBD", "aquazaniashop.co.za"),
    ("Sugar sachets (Huletts)", "1,000", "R338.10", "~1,500/mo (1/cup)", "R507.15", "aquazaniashop.co.za"),
    ("Jura Cleaning Tablets", "box of 6", "R287.50", "~6/mo (daily backflush)", "R287.50", "aquazaniashop.co.za"),
    ("Jura Milk Cleaner 90g", "unit", "R270.25", "1/mo", "R270.25", "aquazaniashop.co.za"),
    ("Jura Descaling Tablets", "3x3 pack", "R333.50", "quarterly", "R111.17", "aquazaniashop.co.za"),
    ("Jura CLARIS Blue filter", "unit", "R310.50", "~1/mo", "R310.50", "aquazaniashop.co.za"),
    ("Aqua Supreme filter coffee", "20x60g", "R517.50", "batch-brew add-on", "TBD", "aquazaniashop.co.za"),
    ("Vending milk 4kg", "unit", "R943.00", "Alegria route only", "TBD", "aquazaniashop.co.za"),
    ("Alegria Hot Chocolate 3kg", "unit", "R789.54", "Alegria route only", "TBD", "aquazaniashop.co.za"),
    ("Fresh fruit & veg (bowls/smoothies)", "month", "market", "daily/weekly (Tshwane+Freshpro)", "R8,000-12,000 (est)", "Tshwane Market / Freshpro / Nasci"),
]
for i, c in enumerate(con, 2): put(ws5, i, list(c))

# ============ Sheet: Fruit & Veg + ZW Coffee ============
ws6 = wb.create_sheet('FruitVeg + ZW Coffee')
sheet(ws6, ["Category", "Supplier", "Location", "Key terms", "Price", "Contact", "Source URL"], [14, 26, 24, 30, 18, 26, 30])
fv = [
    ("Fruit & Veg", "Tshwane Market (primary)", "450 President Burgers St, Pretoria West", "No minimum; buyer's tag R10; daily market prices", "cheapest in Gauteng; mango R23-26/kg", "012 358 2302 / 012 358 2398", "noordvaal.co.za/tshwane-market"),
    ("Fruit & Veg", "Freshpro Market (daily top-ups)", "JHB, serves PTA", "No minimum; R30 delivery, free >R400; WhatsApp order", "daily list", "WhatsApp 067 540 6264; PTA 083 303 2836", "facebook.com/Freshpromarket"),
    ("Fruit & Veg", "Nasci Produce (prepped)", "240 Vonkprop, Samcor, Pretoria", "Small accounts; daily pricelist; prepped produce", "daily list", "+27 82 258 4572; nasciproduce@gmail.com", "nasciproduce.co.za"),
    ("Fruit & Veg", "De Farmer (backup, online)", "Gauteng online", "R300 min; free delivery", "online prices", "+27 78 714 4383", "defarmer.co.za"),
    ("ZW Coffee", "Victoria Falls Coffee Co (TOP)", "Metcalfe Rd, Victoria Falls", "Roasts in VF; 250g/1kg; wholesale on enquiry", "~USD 22-28/kg (R130-400/bag)", "vicfallscoffee@icloud.com", "victoriafallscoffee.com"),
    ("ZW Coffee", "Loretta's Coffee (backup)", "539 Reynard Rd, Victoria Falls", "Roasts Chipinge/Chimanimani/Vumba; local delivery", "quote via IG", "IG @lorettascoffeeandsmoothie", "cuisinenoir.com (Jul 2025)"),
    ("ZW Coffee", "House of Legends (Harare consolidator)", "Kudu Corner, Harare", "Roasted wholesale; freight to VF", "quote", "+263 77 233 3769 (Sarah)", "facebook.com/HouseOfLegendsZim"),
]
for i, f in enumerate(fv, 2): put(ws6, i, list(f))

# ============ Sheet: 18-Dept BOQ (priced) ============
src = load_workbook('Fruitful_Portal_Master_BOQ_18Dept.xlsx')['Master BOQ - 18 Depts']
ws7 = wb.create_sheet('18-Dept BOQ (Priced)')
sheet(ws7, ["Dept", "Item", "Spec", "Freq", "Agent", "Unit Price (ex VAT)", "Source / Status"], [8, 42, 42, 12, 8, 18, 34])
price_map = {
    "Espresso beans": ("R348.00/kg", "Aquazania R1,392/4kg"),
    "Filter coffee ground": ("R25.88/sachet", "Aqua Supreme R517.50/20"),
    "Whole milk": ("R22.04/L", "Dewfresh R132.25/6L"),
    "Skim milk": ("R22.04/L", "Dewfresh R132.25/6L"),
    "Oat milk": ("R57.36/L", "Milklab R458.85/8L"),
    "Almond milk": ("R57.36/L", "Milklab R458.85/8L"),
    "Machine cleaner tablets": ("R47.92/tablet", "Jura R287.50/6"),
    "Milk frother cleaner": ("R270.25/unit", "Jura shop"),
    "Descaling solution": ("R333.50/pack", "Jura shop"),
    "White sugar sachets branded": ("R0.34 each", "Huletts R338.10/1000"),
    "Raw cane sugar sachets": ("R0.34 each", "Huletts R338.10/1000"),
    "Brown sugar sachets": ("R0.34 each", "Huletts R338.10/1000"),
    "Sweetener sachets": ("R0.34 each", "Huletts R338.10/1000"),
    "Stevia sachets": ("R0.34 each", "Huletts R338.10/1000"),
    "Vanilla sugar sachets": ("R0.34 each", "Huletts R338.10/1000"),
    "Espresso machine": ("RENTAL R690/mo (B)", "Aquaspresso Jura X8"),
    "Espresso grinder": ("incl. X8 super-auto", "Aquaspresso route"),
    "Water filtration": ("incl. X8", "Aquaspresso route"),
    "Pancake tongs": ("R60-120 est", "Quote required"),
}
r = 2
for row in src.iter_rows(min_row=2, values_only=True):
    dept, item, spec, freq, agent = row[0], row[1], row[2], row[3], row[4]
    price, source = "", ""
    for key, val in price_map.items():
        if key.lower() in str(item).lower():
            price, source = val
            break
    if not source:
        source = "Quote required"
    put(ws7, r, [dept, item, spec, freq, agent, price, source])
    r += 1

# ============ Sheet: Supplier Register ============
ws8 = wb.create_sheet('Supplier Register')
sheet(ws8, ["Supplier", "Role", "Contact", "Key terms", "Status"], [34, 26, 34, 30, 16])
sup = [
    ("Guangzhou Welink (Gary)", "Kiosk hardware", "Via Alibaba / WL20260401C", "$3,500/unit x 9; 25-day lead", "Ordered"),
    ("Aquazania / Aquaspresso (Kedibone)", "Coffee machines rental + beans + cleaning", "kedibonema@aquaspresso.co.za; 010 591 9240; 068 392 4549 WhatsApp", "Jura X8 R690-1,690/mo; beans R348/kg", "Proposal in hand"),
    ("Afristar Freight", "LCL freight Guangzhou-JHB", "Est. No. 108923", "R44,473.92 excl VAT (5.5cbm)", "Quote received"),
    ("Tshwane Market", "Fresh fruit & veg (bulk weekly)", "012 358 2302", "No minimum; buyer's tag R10", "Ready"),
    ("Freshpro Market", "Fruit & veg daily top-ups", "WhatsApp 067 540 6264", "No min; R30 delivery, free >R400", "Ready"),
    ("Nasci Produce", "Prepped produce", "+27 82 258 4572", "Daily pricelist; small accounts", "Ready"),
    ("Victoria Falls Coffee Co", "ZW coffee (P-008)", "vicfallscoffee@icloud.com", "~USD 22-28/kg; wholesale enquiry", "Ready to contact"),
    ("House of Legends (Harare)", "ZW backup/consolidation", "+263 77 233 3769 (Sarah)", "Roasted wholesale + freight", "Backup"),
    ("Grand Maghandlela", "Fedora hats + paintings", "+27 72 414 0117", "~50 hats/mo; 247 sold", "Restock agreement Task C"),
    ("Fantastico SA", "Coffee trading pack (certified supply)", "per Coffee Trading Pack doc", "SCA 80+ / moisture 9-12%", "Per Fruitful-Coffee pack"),
]
for i, s in enumerate(sup, 2): put(ws8, i, list(s))

# ============ Sheet: OPEX per Kiosk ============
ws9 = wb.create_sheet('OPEX per Kiosk')
sheet(ws9, ["Line", "Monthly R (ex VAT)", "Annual R", "Basis", "Status"], [34, 18, 16, 30, 12])
opex = [
    ("Jura X8 Option B rental", "690.00", "8,280.00", "Aquazania contract", "Factual"),
    ("Beans (27kg @ R348)", "9,396.00", "112,752.00", "50 cups/day baseline", "Factual"),
    ("Milk (135L @ R22.04)", "2,970.56", "35,646.72", "Dewfresh shop price", "Factual"),
    ("Sugar sachets (1,500)", "507.15", "6,085.80", "Huletts shop price", "Factual"),
    ("Jura cleaning pack (tabs+milk+descale avg)", "668.92", "8,027.04", "Jura shop prices", "Factual"),
    ("CLARIS Blue filter", "310.50", "3,726.00", "Jura shop price", "Factual"),
    ("Packaging (est R5.10/cup)", "7,650.00", "91,800.00", "wholesale estimate", "Estimate"),
    ("Payment fees (3%)", "1,760.87", "21,130.44", "Paystack on R58,696 rev", "Estimate"),
    ("Labour (2 staff + mgr share)", "18,800.00", "225,600.00", "R7,500 x2 +12% + R2,000", "Estimate"),
    ("Fixed opex (utilities/cleaning/insurance)", "4,000.00", "48,000.00", "estimate", "Estimate"),
    ("TOTAL", "46,754.00", "561,048.00", "", "—"),
    ("Revenue (1,500 cups @ R39.13)", "58,695.00", "704,340.00", "blended R45 incl VAT", "Market-anchored"),
    ("PROFIT", "11,941.00", "143,292.00", "20.3% margin", "—"),
]
for i, o in enumerate(opex, 2): put(ws9, i, list(o), hl=(o[0] in ("TOTAL", "PROFIT")))

wb.save('FRUITFUL_MASTER_BOQ_PRICED.xlsx')
print("DONE")
