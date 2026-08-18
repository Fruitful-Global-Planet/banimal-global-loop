# gen_mall_model.py — Fruitful Portal mall deployment model (register pending re-upload)
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

FONT = 'Arial'
thin = Side(style='thin', color='BFBFBF')
border = Border(left=thin, right=thin, top=thin, bottom=thin)
hfont = Font(name=FONT, size=11, bold=True, color='FFFFFF')
hfill = PatternFill('solid', start_color='0FB5A6')
bfill = PatternFill('solid', start_color='F2F2F2')
gold = PatternFill('solid', start_color='FFF2CC')
red = PatternFill('solid', start_color='FDE9E9')

def sheet(ws, headers, widths):
    for j, h in enumerate(headers, 1):
        c = ws.cell(1, j, h); c.font = hfont; c.fill = hfill
        c.alignment = Alignment(horizontal='center', vertical='center'); c.border = border
    for j, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.freeze_panes = 'A2'

def put(ws, r, vals, hl=False, fill=None):
    for j, v in enumerate(vals, 1):
        c = ws.cell(r, j, v); c.border = border
        if r % 2 == 1: c.fill = bfill
        if hl: c.fill = gold
        if fill: c.fill = fill
        c.alignment = Alignment(wrap_text=True, vertical='top')

def money(v): return f"R{v:,.0f}"

wb = Workbook()

# ============ Sheet 1: Strategy & Advantage ============
ws = wb.active; ws.title = 'Strategy & Advantage'
ws.sheet_properties.tabColor = '0FB5A6'
sheet(ws, ["Driver", "Full shop (shopfitted)", "Fruitful Portal (kiosk)", "Advantage"], [30, 34, 34, 20])
st = [
    ("Store cost (fit-out)", "R120k-640k one-off, sunk", "R0 — the kiosk IS the store", "100% saved"),
    ("Rental (prime mall)", "R400-1,200/m2 = R16k-96k/mo", "8m2 kiosk band R4k-25k/mo", "73-90% cheaper"),
    ("Lease term", "3-5 yrs locked", "12-36 mo", "flex + exit"),
    ("Moveability", "None — fit-out lost on exit", "Relocate in 1-2 days", "optionality"),
    ("Deposit", "R32k-288k", "R8k-50k", "~85% less"),
    ("Rates/levies/utilities", "R9k-27k/mo", "R2.3k-5k/mo", "~75% less"),
    ("Risk profile", "High fixed cost, slow exit", "Low fixed cost, fast exit", "de-risk"),
    ("Model", "Fixed footprint business", "Flywheel: profit buys next portal (R123k landed)", "compounding"),
]
for i, s in enumerate(st, 2): put(ws, i, list(s), hl=(s[0] == "Model"))

# ============ Sheet 2: Rental comparison ============
ws2 = wb.create_sheet('Rental Shop vs Portal')
sheet(ws2, ["Mall tier", "Shop rent/mo (40-80m2)", "Portal rent/mo (8m2)", "Portal rates+levies", "Saving on rent", "Example band (est.)"], [22, 22, 22, 20, 14, 34])
rc = [
    ("Neighbourhood", "R16,000-32,000", "R4,000-8,000", "R800-1,500", "75%", "R500-1,000/m2 on 8m2"),
    ("Regional", "R40,000-60,000", "R8,000-16,000", "R1,500-2,000", "73-80%", "R1,000-2,000/m2 on 8m2"),
    ("Premium (Sandton/Menlyn tier)", "R70,000-96,000", "R16,000-25,000", "R2,000-3,000", "74-77%", "R2,000-3,000/m2 on 8m2"),
]
for i, c in enumerate(rc, 2): put(ws2, i, list(c))
n6 = ws2.cell(6, 1, "NOTE: mall kiosk rates vary by mall, traffic and anchor adjacency — verify per mall before negotiating (ESTIMATES)")
n6.font = Font(italic=True, color='666666')

# ============ Sheet 3: Per-mall economics ============
ws3 = wb.create_sheet('Per-Mall Economics')
sheet(ws3, ["Line", "Neighbourhood", "Regional", "Premium"], [36, 18, 18, 18])
REV = [180000, 280000, 400000]
COGS = [0.45 * v for v in REV]
LAB = [22000, 25000, 30000]
RENT = [6000, 12000, 20000]
JURA = [10086, 15784, 19482]
OPX = [4000, 5000, 6000]
prof = [REV[i]-COGS[i]-LAB[i]-RENT[i]-JURA[i]-OPX[i] for i in range(3)]
rows3 = [
    ("Revenue/mo (full menu)", REV, "coffee 80/120/170 cups/day equiv"),
    ("COGS + packaging (~45%)", COGS, "incl payment fees"),
    ("Labour (2-3 staff)", LAB, "mall shifts"),
    ("Mall rental (mid-band)", RENT, "8m2 kiosk"),
    ("Jura Option B (beans+milk+rental)", JURA, "at volume"),
    ("Fixed opex", OPX, "utilities/cleaning/insurance"),
    ("PROFIT / mo", prof, ""),
    ("Capex: landed kiosk + NUCO deploy + deposit", [207000]*3, "R123k + R60k + R24k"),
    ("Payback (months)", [f"{207000/p:.1f}" for p in prof], ""),
]
for i, r3 in enumerate(rows3, 2):
    put(ws3, i, [r3[0]] + [money(v) if isinstance(v, (int, float)) else v for v in r3[1]] + [r3[2]], hl=(r3[0] == "PROFIT / mo"))

# ============ Sheet 4: NUCO Build Co ============
ws4 = wb.create_sheet('NUCO Build Co')
sheet(ws4, ["Item", "Value", "Basis"], [44, 34, 40])
nc = [
    ("Entity", "Bush-Portal Build Co (NUCO) — in-house subsidiary of Fruitful Shops", "shopfitting + deployment arm; no external shopfitters, margin retained"),
    ("Deployment price by tier", "R55,000 / R70,000 / R85,000 (nbrhd/regional/premium)", "transport + site works + install + POS + training + commissioning + COC"),
    ("Deployment direct cost", "R38,000-58,000", "2-man crew x2 days, van, fuel, sundries"),
    ("NUCO margin per unit", "R17,000-27,000 (30-35%)", "healthy retained margin"),
    ("Fleet (start)", "2 vans + 2 x 2-man crews, PTA HQ", "scale to 4 vans at 20+ units/mo"),
    ("Throughput", "2-4 portals/week (8-16/mo)", "from PTA hub; nearest-port / Amazon DC staging"),
    ("Monthly NUCO revenue (10 units)", "R550,000-850,000", "10 x blended tier"),
    ("Monthly NUCO margin (10 units)", "R170,000-270,000", "before overhead ~R120-140k (vans/crew/fuel)"),
    ("300-portal program revenue", "R16.5M-25.5M total", "300 x R55-85k"),
    ("300-portal program margin", "R5.1M-8.1M total", "at 30-35%"),
    ("Staging nodes", "PTA HQ + nearest port (Durban) + Amazon SA DC hub", "container direct-to-node delivery"),
    ("HQ service level", "QC, staging, commissioning, fast 'first-fingers' launch", "franchisee units deployed from HQ — no drag"),
]
for i, c in enumerate(nc, 2): put(ws4, i, list(c))

# ============ Sheet 5: Mall register (PENDING) ============
ws5 = wb.create_sheet('Mall Register (PENDING)')
sheet(ws5, ["Mall / Centre", "Address", "Province", "City", "Dist from PTA (km)", "Contact email", "Tier (est.)", "Status"], [40, 44, 14, 14, 14, 36, 12, 14])
put(ws5, 2, ["FILE MISSING — re-upload f77674592.xlsx (recovery folder recup_dir.1749 is empty)", "", "", "", "", "", "", ""], fill=red)
put(ws5, 3, ["Only captured row: City Square Spar, City Sq, Langalibalele St, KwaZulu-Natal (ID 276266)", "", "", "", "", "", "", ""])
put(ws5, 5, ["Once re-uploaded: auto-classify 308 rows -> province, city, est. distance from Pretoria (Silver Lakes HQ), tier, contact", "", "", "", "", "", "", ""])

wb.save('FRUITFUL_MALL_DEPLOYMENT_MODEL.xlsx')
print("DONE")
