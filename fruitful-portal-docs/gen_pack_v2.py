# gen_pack_v2.py — Franchise Pack v2: R450k Mercedes-standard package, Amazon DC supply spine
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
green = PatternFill('solid', start_color='E2F0D9')

def sheet(ws, headers, widths):
    for j, h in enumerate(headers, 1):
        c = ws.cell(1, j, h); c.font = hfont; c.fill = hfill
        c.alignment = Alignment(horizontal='center', vertical='center'); c.border = border
    for j, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.freeze_panes = 'A2'

def put(ws, r, vals, fill=None):
    for j, v in enumerate(vals, 1):
        c = ws.cell(r, j, v); c.border = border
        if r % 2 == 1 and fill is None: c.fill = bfill
        if fill: c.fill = fill
        c.alignment = Alignment(wrap_text=True, vertical='top')

def money(v): return f"R{v:,.0f}"

wb = Workbook()

# ============ Sheet 1: Package (Mercedes standard) ============
ws = wb.active; ws.title = 'Package R450k'
ws.sheet_properties.tabColor = '0FB5A6'
sheet(ws, ["Component (identical for EVERY portal)", "R (excl VAT)", "Notes"], [46, 14, 44])
pkg = [
    ("Kiosk landed (batch avg)", 110000, "Welink $3,500 x 9 batch; freight + duty + VAT"),
    ("NUCO deployment + shopfitting", 70000, "in-house build company; install + COC + commissioning"),
    ("Signage + lighted logo + branding", 25000, "CI Guide v04 compliant"),
    ("POS + tablet + 5G router + UPS", 35000, "base44 SDK pre-loaded"),
    ("Coffee equipment setup (Jura X8)", 25000, "Aquazania rental initiation + first-year tablets"),
    ("Training + certification (2 staff)", 25000, "barista + ops + Banimal Loop protocol"),
    ("Platform/tech setup", 15000, "Convex, AI terminal, weather/AQ widget, seedwave"),
    ("Brand licence + franchise fee", 30000, "5-yr licence included"),
    ("Commissioning + contingency", 15000, "pre-launch QC, first-week support"),
    ("SUBTOTAL BUILD & LICENCE", 350000, ""),
    ("Opening stock credit (on franchisee account)", 70000, "drawn at supplier cost + distribution %; repaid via sales"),
    ("TOTAL PACKAGE (excl VAT)", 450000, "single standard — no options, no half measures"),
]
for i, p in enumerate(pkg, 2):
    put(ws, i, [p[0], money(p[1]), p[2]], fill=gold if p[0].startswith(("SUBTOTAL", "TOTAL")) else None)

# ============ Sheet 2: HQ margin ============
ws2 = wb.create_sheet('HQ Margin per Portal')
sheet(ws2, ["Line", "R (excl VAT)", "Basis"], [40, 16, 44])
hm = [
    ("Package revenue", 450000, "per portal, excl VAT"),
    ("Build direct cost (kiosk+deploy+signage+POS+setup+training+platform)", -226000, "kiosk 110k + deploy 45k + signage 15k + POS 28k + Jura 18k + training 12k + platform 5k + comm 8k (est.)"),
    ("Stock credit cost (goods at cost ~60%)", -42000, "R70k credit x 60% cost ratio"),
    ("ONE-OFF GROSS MARGIN per portal", 450000-226000-42000, "≈40%"),
    ("Ongoing — royalty (6% of franchisee revenue)", 11896, "franchisee realistic revenue R198,260/mo"),
    ("Ongoing — marketing fund (4%)", 7930, "central fund"),
    ("Ongoing — distribution margin (20% on supply R25k)", 5000, "all BOQ items bought at supplier cost +20%"),
    ("Ongoing — supplier rebates (2%)", 500, "Aquazania/Jura/packaging volume rebates"),
    ("ONGOING GROSS per portal / month", 11896+7930+5000+500, "direct-territory (no master split)"),
    ("Master-territory net (50% royalty to master)", 11896+7930+5000+500-5948, "royalty split 50/50 with provincial master"),
]
for i, h in enumerate(hm, 2):
    put(ws2, i, [h[0], money(h[1]) if isinstance(h[1], (int, float)) else h[1], h[2]],
        fill=gold if h[0].startswith(("ONE-OFF", "ONGOING")) else None)

# ============ Sheet 3: Amazon fulfilment ============
ws3 = wb.create_sheet('Amazon Fulfilment')
sheet(ws3, ["Line", "Value", "Basis"], [40, 22, 40])
am = [
    ("Model", "Amazon DC as national supply spine", "suppliers deliver to Amazon DC; Amazon handles nationwide last-mile"),
    ("Listing", "Complete BOQ at supplier cost", "cups, lids, beans, hats, cleaning — every SKU listed"),
    ("Amazon fulfilment fee (delivery)", "5-10% of order value", "use 7.5% mid-point; passed to franchisee as delivery line"),
    ("Typical monthly supply per portal (supplier cost)", "R25,000", "beans 9.4k + milk 3.0k + packaging 7.7k + cleaning 1.0k + sugar 0.5k + sundries"),
    ("Franchisee pays (cost +20% distribution)", "R30,000", "HQ margin R5,000/mo/portal"),
    ("Amazon fee on R30,000 shipped", "R2,250", "7.5% — charged to franchisee as delivery"),
    ("HQ admin cost (Amazon fee processing)", "~1%", "R300/mo/portal"),
    ("Cash flow", "Amazon payouts to Fruitful", "weekly/monthly settlement; no Fruitful warehousing"),
    ("Scale benefit", "no national fleet needed for consumables", "NUCO fleet reserved for deployments only"),
]
for i, a in enumerate(am, 2): put(ws3, i, list(a))

# ============ Sheet 4: Franchisee economics ============
ws4 = wb.create_sheet('Franchisee Economics')
sheet(ws4, ["Line", "R/mo", "Basis"], [36, 14, 44])
fr = [
    ("Investment (package)", "R450,000 once", "incl R70k stock credit"),
    ("Revenue (realistic full menu, neighbourhood mall)", 198260, "coffee 50 + bowls 30 + smoothies 25 + pancakes 20 + snacks 10/day"),
    ("Supply COGS (via Fruitful at +20%)", -30000, "beans+milk+packaging+cleaning+sugar"),
    ("Other food COGS + payment fees", -59217, "bowls/smoothie ingredients + payment 3%"),
    ("Labour (2 staff)", -18800, "R7,500 x2 + 12% + mgr share"),
    ("Mall rent (neighbourhood)", -6000, "8m2 kiosk"),
    ("Jura Option B", -2082, "rental + 4kg beans bundled"),
    ("Fixed opex", -4000, "utilities/cleaning/insurance"),
    ("Royalty 6%", -11896, "of revenue"),
    ("Marketing 4%", -7930, "central fund"),
    ("Amazon delivery pass-through", -2250, "on supply"),
    ("PROFIT / month", 198260-30000-59217-18800-6000-2082-4000-11896-7930-2250, ""),
    ("Payback on R450k", "%.1f months" % (450000 / (198260-30000-59217-18800-6000-2082-4000-11896-7930-2250)), "before master-licence territory fee"),
]
for i, f in enumerate(fr, 2):
    put(ws4, i, [f[0], money(f[1]) if isinstance(f[1], (int, float)) else f[1], f[2]],
        fill=gold if f[0] == "PROFIT / month" else None)

# ============ Sheet 5: Fleet income ============
ws5 = wb.create_sheet('Fleet Income (HQ)')
sheet(ws5, ["Portals", "One-off margin", "Ongoing/mo (direct)", "Ongoing/mo (net of master)", "Annual ongoing (net)"], [12, 18, 22, 24, 20])
ONEOFF = 182000
ONGOING = 25326
NET = 19378
for i, n in enumerate([10, 50, 117, 300], 2):
    put(ws5, i, [n, money(ONEOFF*n), money(ONGOING*n), money(NET*n), money(NET*n*12)])

wb.save('FRUITFUL_FRANCHISE_PACK_V2.xlsx')
print("DONE")
