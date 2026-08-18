# gen_usd_models.py — USD versions of the corrected Fruitful financial models
# FX basis: 1 USD = 16.185472 ZAR (exchangerate-api.com, Sun 16 Aug 2026 00:02 UTC, live fetch)
# Mirrors 1:1 the corrected ZAR workbooks:
#   PANCAKE_FINANCIAL_MODEL.xlsx          (4-SKU pannekoek, manager at HQ)
#   FRUITFUL_MENU_BOQ_ENGINE.xlsx Sheet 2 (Monthly Menu P&L, labour R16,800)
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

FX = 16.185472
FONT = 'Arial'
thin = Side(style='thin', color='BFBFBF')
border = Border(left=thin, right=thin, top=thin, bottom=thin)
hfont = Font(name=FONT, size=11, bold=True, color='FFFFFF')
hfill = PatternFill('solid', start_color='0FB5A6')
bfill = PatternFill('solid', start_color='F2F2F2')
gold = PatternFill('solid', start_color='FFF2CC')
grey = Font(name=FONT, size=10, italic=True, color='666666')

def usd(v):
    if isinstance(v, str) or v is None:
        return v
    return f"${v / FX:,.2f}"

def sheet(ws, headers, widths):
    for j, h in enumerate(headers, 1):
        c = ws.cell(1, j, h); c.font = hfont; c.fill = hfill
        c.alignment = Alignment(horizontal='center', vertical='center'); c.border = border
    for j, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.freeze_panes = 'B2'

def put(ws, r, vals, fill=None):
    for j, v in enumerate(vals, 1):
        c = ws.cell(r, j, v); c.border = border
        if r % 2 == 1 and fill is None: c.fill = bfill
        if fill: c.fill = fill
        c.alignment = Alignment(wrap_text=True, vertical='top')

def fx_note(ws, r):
    c = ws.cell(r, 1, "FX basis: 1 USD = R16.1855 (exchangerate-api.com, updated Sun 16 Aug 2026 00:02 UTC). All ZAR figures converted ÷16.1855; margins, percentages and quantities unchanged.")
    c.font = grey
    c.alignment = Alignment(wrap_text=True, vertical='top')

wb = Workbook()

# ============ Sheet 1: Pannekoek 4-SKU in USD ============
ws = wb.active; ws.title = 'Pannekoek 4-SKU (USD)'
ws.sheet_properties.tabColor = '0FB5A6'
VARIANTS = [
    "Milk single 100% (boxed)", "Milk 12-pack 100% (boxed)",
    "Water 50% single (no box)", "Water 50% 12-pack (no boxes)",
]
sheet(ws, ["Line"] + VARIANTS, [40, 18, 18, 18, 18])

def row(name, zar_vals, fill=None, bold=False, usd_prefix=True):
    r = ws.max_row + 1
    vals = [name]
    for v in zar_vals:
        vals.append(usd(v) if usd_prefix else v)
    put(ws, r, vals, fill=fill)
    if bold:
        for c in range(1, 6):
            ws.cell(r, c).font = Font(name=FONT, size=11, bold=True)

# ZAR values exactly as displayed in the corrected PANCAKE_FINANCIAL_MODEL.xlsx
row("INGREDIENTS (per unit)", [2.46, 29.52, 0.75, 9.00])
row("  Cake flour", [0.45, 5.40, 0.23, 2.76])
row("  Egg", [0.44, 5.28, 0.22, 2.64])
row("  Milk (45ml) / Water", [0.99, 11.88, 0.00, 0.00])
row("  Baking powder + salt", [0.03, 0.36, 0.01, 0.12])
row("  Pan oil", [0.08, 0.96, 0.04, 0.48])
row("  Cinnamon sugar", [0.16, 1.92, 0.05, 0.60])
row("  Lemon", [0.31, 3.72, 0.16, 1.92])
row("BOX", [1.25, 15.00, 0.00, 0.00])
row("DIRECT COST", [3.71, 44.52, 0.75, 9.00], fill=gold, bold=True)
row("SELLING PRICE", [12.50, 150.00, 1.90, 22.50], bold=True)
row("DIRECT MARGIN %", ["70.3%", "70.3%", "60.5%", "60.0%"], fill=gold, usd_prefix=False)
row("SHARED & ROYALTY LAYERS", [0.00, 0.00, 0.00, 0.00])
row("  Payment fee (3%)", [0.38, 4.50, 0.06, 0.67])
row("  Royalty (6%)", [0.75, 9.00, 0.11, 1.35])
row("  Marketing fund (4%)", [0.50, 6.00, 0.08, 0.90])
row("  Labour share (R16,800 / 2,850 = R5.89 ≈ $0.36)", [5.89, 70.68, 5.89, 70.68])
row("  Fixed share (R12,082 / 2,850 = R4.24 ≈ $0.26)", [4.24, 50.88, 4.24, 50.88])
row("FULLY LOADED COST", [15.46, 185.58, 11.13, 133.48], fill=gold, bold=True)
row("Fully-loaded margin %", ["-23.7%", "-23.7%", "-485.6%", "-493.3%"], usd_prefix=False)
row("", [0, 0, 0, 0], usd_prefix=False)
row("HQ funding check (per portal/mo)", [0, 0, 0, 0], usd_prefix=False)
row("  Fee pool (10% of R122,420 menu revenue)", [12242.00, 12242.00, 12242.00, 12242.00], fill=gold)
row("  Manager cost (R10,000 / 5 portals)", [-2000.00, -2000.00, -2000.00, -2000.00])
row("  HQ net from fees", [10242.00, 10242.00, 10242.00, 10242.00], fill=gold)
fx_note(ws, ws.max_row + 1)

# ============ Sheet 2: Monthly Menu P&L per portal in USD ============
ws2 = wb.create_sheet('Menu P&L per portal (USD)')
ws2.sheet_properties.tabColor = '0FB5A6'
sheet(ws2, ["Line", "Coffee (1,500/mo)", "Smoothies (750/mo)", "Pancakes (600 units/mo)", "TOTAL"], [30, 16, 16, 16, 14])

def row2(name, zar_vals, fill=None, bold=False, as_money=True):
    r = ws2.max_row + 1
    vals = [name]
    for v in zar_vals:
        vals.append(usd(v) if as_money else v)
    put(ws2, r, vals, fill=fill)
    if bold:
        for c in range(1, 6):
            ws2.cell(r, c).font = Font(name=FONT, size=11, bold=True)

row2("Units", [1500, 750, 600, 2850], as_money=False)
row2("Revenue", [57000.00, 41250.00, 21000.00, 119250.00])
row2("Direct COGS (grains above)", [21990.00, 17550.00, 1632.00, 41172.00])
row2("COGS %", ["38.6%", "42.5%", "7.8%", "34.5%"], as_money=False)
row2("Payment fees 3%", [1710.00, 1237.50, 630.00, 3577.50])
row2("Labour (2 staff, mgr=HQ)", [8842.00, 4421.00, 3537.00, 16800.00])
row2("Mall rent + Jura + opex", ["", "", "", 12082.00])
row2("Royalty 6% + marketing 4%", ["", "", "", 11925.00])
row2("EBITDA", ["", "", "", 33693.50], fill=gold, bold=True)
row2("Depreciation + tax (27%)", ["", "", "", -12139.00])
row2("NET PROFIT / month", ["", "", "", 21554.35], fill=gold, bold=True)
note = ws2.cell(ws2.max_row + 1, 1,
    "Honest note (ZAR, unchanged): radical menu at baseline volume = thinner revenue (R119,250 ≈ $7,368 vs R198,260 full menu) but zero waste, hours-long training, and the BushCoding funnel. Levers: volume (jam study), 1.5-staff model, pancake 12-packs, BushCoding revenue.")
note.font = grey
note.alignment = Alignment(wrap_text=True, vertical='top')
fx_note(ws2, ws2.max_row + 1)

wb.save('FRUITFUL_MODELS_USD.xlsx')
print("DONE — FRUITFUL_MODELS_USD.xlsx")
print(f"FX used: 1 USD = R{FX:.6f}")
# verification printout
print("\n--- Sheet 1 key USD values ---")
for z, label in [(12.50, "Milk single selling"), (150.00, "Milk 12-pack selling"),
                 (1.90, "Water single selling"), (22.50, "Water 12-pack selling"),
                 (15.46, "Milk single FL"), (185.58, "Milk 12-pack FL"),
                 (11.13, "Water single FL"), (133.48, "Water 12-pack FL"),
                 (12242.00, "Fee pool / portal/mo"), (-2000.00, "Manager share (5 portals)"),
                 (10242.00, "HQ net from fees")]:
    print(f"{label}: R{z:,.2f} -> ${z/FX:,.2f}")
print("\n--- Sheet 2 key USD values ---")
for z, label in [(119250.00, "Revenue"), (41172.00, "Direct COGS"), (16800.00, "Labour"),
                 (12082.00, "Mall+Jura+opex"), (11925.00, "Royalty+mkt 10%"),
                 (33693.50, "EBITDA"), (21554.35, "NET PROFIT / month")]:
    print(f"{label}: R{z:,.2f} -> ${z/FX:,.2f}")
