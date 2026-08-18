# gen_pancake_model.py — CORRECTED 4-SKU pannekoek model (milk 100% / water 50%, manager is HQ)
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

def money(v): return f"R{v:.2f}"

LABOUR, FIXED = 5.89, 4.24   # menu-shared per unit; manager paid from HQ fee pool
# 4 SKUs: [ingredients_total, box_total, selling]
VARIANTS = [
    ("Milk single 100% (boxed)",      2.46, 1.25, 12.50),
    ("Milk 12-pack 100% (boxed)",     2.46*12, 1.25*12, 150.00),
    ("Water 50% single (no box)",     0.75, 0.00, 1.90),
    ("Water 50% 12-pack (no boxes)",  0.75*12, 0.00, 22.50),
]
# ingredient detail lines (single-unit basis)
DETAIL = [
    ("Cake flour", 0.45, 0.23),
    ("Egg", 0.44, 0.22),
    ("Milk (45ml) / Water", 0.99, 0.00),
    ("Baking powder + salt", 0.03, 0.01),
    ("Pan oil", 0.08, 0.04),
    ("Cinnamon sugar", 0.16, 0.05),
    ("Lemon", 0.31, 0.16),
]
MULT = [1, 12, 1, 12]

wb = Workbook()
ws = wb.active; ws.title = 'Pannekoek 4-SKU (corrected)'
ws.sheet_properties.tabColor = '0FB5A6'
headers = ["Line"] + [v[0] for v in VARIANTS]
sheet(ws, headers, [34, 18, 18, 18, 18])

def row(name, vals, fill=None, bold=False):
    r = ws.max_row + 1
    put(ws, r, [name] + [money(v) if isinstance(v, float) else v for v in vals], fill=fill)
    if bold:
        for c in range(1, 6):
            ws.cell(r, c).font = Font(name=FONT, size=11, bold=True)

ing = [v[1] for v in VARIANTS]
box = [v[2] for v in VARIANTS]
sell = [v[3] for v in VARIANTS]
direct = [ing[i] + box[i] for i in range(4)]
# fee layers, rounded half-up to 2dp (displayed values are the source of truth for FL)
pay = [0.38, 4.50, 0.06, 0.68]          # 3% of selling
roy = [0.75, 9.00, 0.11, 1.35]          # 6%
mkt = [0.50, 6.00, 0.08, 0.90]          # 4%
lab = [LABOUR * MULT[i] for i in range(4)]   # 5.89, 70.68, 5.89, 70.68
fix = [FIXED * MULT[i] for i in range(4)]    # 4.24, 50.88, 4.24, 50.88
fl = [direct[i] + pay[i] + roy[i] + mkt[i] + lab[i] + fix[i] for i in range(4)]

row("INGREDIENTS (per unit)", ing)
for name, milk_v, water_v in DETAIL:
    row(f"  {name}", [milk_v*MULT[i] if i < 2 else water_v*MULT[i] for i in range(4)])
row("BOX", box)
row("DIRECT COST", direct, fill=gold, bold=True)
row("SELLING PRICE", sell, bold=True)
row("DIRECT MARGIN %", [f"{((s-d)/s*100):.1f}%" for s, d in zip(sell, direct)], fill=gold)
row("SHARED & ROYALTY LAYERS", [0.0]*4)
row("  Payment fee (3%)", pay)
row("  Royalty (6%)", roy)
row("  Marketing fund (4%)", mkt)
row(f"  Labour share (R16,800 / 2,850 = R{LABOUR:.2f})", lab)
row(f"  Fixed share (R12,082 / 2,850 = R{FIXED:.2f})", fix)
row("FULLY LOADED COST", fl, fill=gold, bold=True)
row("Fully-loaded margin %", [f"{((s-f)/s*100):.1f}%" for s, f in zip(sell, fl)])
row("", [0]*4)
row("HQ funding check (per portal/mo)", [0]*4)
row("  Fee pool (10% of R122,420 menu revenue)", [12242.0]*4, fill=gold)
row("  Manager cost (R10,000 / 5 portals)", [-2000.0]*4)
row("  HQ net from fees", [10242.0]*4, fill=gold)

wb.save('PANCAKE_FINANCIAL_MODEL.xlsx')
print("DONE")
for i, name in enumerate([v[0] for v in VARIANTS]):
    print(f"{name}: direct {direct[i]:.2f}, sell {sell[i]:.2f}, margin {(sell[i]-direct[i])/sell[i]*100:.1f}%, FL {fl[i]:.2f}")
