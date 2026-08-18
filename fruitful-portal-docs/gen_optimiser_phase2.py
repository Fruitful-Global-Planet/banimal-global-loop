# gen_optimiser_phase2.py — extend Portal Optimiser with Phase 2 economics sheets
from openpyxl import load_workbook
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
red = PatternFill('solid', start_color='FDE9E9')

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

wb = load_workbook('FRUITFUL_PORTAL_OPTIMISER.xlsx')

# ============ Ph2 Staffing frontier ============
ws = wb.create_sheet('Ph2 Staffing Frontier')
ws.sheet_properties.tabColor = '0FB5A6'
sheet(ws, ["Cups/day", "1 staff (R8,400)", "1.5 staff (R12,600)", "2 staff (R16,800)", "Capacity limit", "OPTIMAL", "Profit at optimal"], 
      [12, 16, 16, 16, 18, 14, 16])
# economics: coffee-equivalent, nbrhd rent
RENT_N = 6000.0
def profit(cups, lab):
    cpm = cups * 30
    rev = cpm * 39.13
    var = cpm * (6.27 + 2.25 + 5.10) + rev * 0.03
    return rev - var - lab - 690 - 4000 - RENT_N
CAP = {1: 45, 1.5: 70, 2: 100}
for i, cups in enumerate([20, 30, 40, 45, 50, 60, 70, 80, 90, 100, 120], 2):
    p1, p15, p2 = profit(cups, 8400), profit(cups, 12600), profit(cups, 16800)
    best = None
    for lab, p in [(1, p1), (1.5, p15), (2, p2)]:
        if cups <= CAP[lab] and (best is None or p > best[1]):
            best = (lab, p)
    if best is None:
        best = (2, p2)  # over capacity -> 2 staff + relief
    put(ws, i, [cups, money(p1), money(p15), money(p2), f"1:≤45 · 1.5:≤70 · 2:≤100",
                f"{best[0]} staff" + (" + relief" if cups > 100 else ""), money(best[1])], fill=gold if cups == 50 else None)
f14 = ws.cell(14, 1, "Rule: cheapest staff that meets capacity. Break-even: 1 staff 19 cups/day · 1.5 staff 23 · 2 staff 28 (nbrhd rent R6k incl).")
f14.font = Font(italic=True, color='666666')

# ============ Ph2 Price sensitivity ============
ws2 = wb.create_sheet('Ph2 Price Sensitivity')
sheet(ws2, ["Line", "Price incl VAT", "Price ex VAT", "Direct cost", "Margin/unit", "Monthly qty", "Monthly contribution", "Note"], 
      [26, 14, 14, 12, 14, 12, 18, 26])
COF_D, SM_D, PAN_D = 14.66, 23.40, 8.32
rows2 = []
for p in [30, 34, 38, 42, 45, 48, 52]:
    ex = p / 1.15
    rows2.append(["Coffee (R38 anchor)", f"R{p}", money(ex), money(COF_D), money(ex-COF_D), 1500, money(1500*(ex-COF_D)),
                  "anchor" if p == 38 else ("+R" + str(p-38) + " = upside if volume holds" if p > 38 else "")])
for p in [45, 50, 55, 60, 65, 70]:
    ex = p / 1.15
    rows2.append(["Smoothie (R55 anchor)", f"R{p}", money(ex), money(SM_D), money(ex-SM_D), 750, money(750*(ex-SM_D)),
                  "anchor" if p == 55 else ""])
for p in [30, 32, 35, 38, 40, 45]:
    ex = p / 1.15
    rows2.append(["Pancake (R35 anchor)", f"R{p}", money(ex), money(PAN_D), money(ex-PAN_D), 600, money(600*(ex-PAN_D)),
                  "anchor" if p == 35 else ""])
for i, r in enumerate(rows2, 2):
    put(ws2, i, r, fill=gold if "anchor" in r[6] else None)
e2 = ws2.cell(len(rows2)+3, 1, "Elasticity warning: raising price trades volume (jam study inverse). Sensitivity shows upside ONLY if volume holds — VaultMesh will tell you which side is true.")
e2.font = Font(italic=True, color='666666')

# ============ Ph2 Menu mix ============
ws3 = wb.create_sheet('Ph2 Menu Mix')
sheet(ws3, ["P/N", "Line", "Margin/unit", "Monthly qty", "Contribution", "Cumulative %", "90% line?", "Trim status"], 
      [8, 26, 13, 12, 14, 13, 10, 14])
mix = [
    ("FFP-01", "Coffee with Milk", 23.34, 750, None),
    ("FFP-07", "Pancake unit", 26.68, 600, None),
    ("FFP-02", "Coffee with Froth", 23.34, 450, None),
    ("FFP-04", "Green Energy", 31.60, 300, None),
    ("FFP-05", "Mango Lassi", 31.60, 262, None),
    ("FFP-06", "Power Protein", 31.60, 188, None),
    ("FFP-03", "Coffee with Chocolate", 20.94, 300, None),
    ("FFP-08", "Pancake 12-pack", 320.16, 12, None),
]
tot = sum(m[2]*m[3] for m in mix)
cum = 0
for i, m in enumerate(mix, 2):
    contrib = m[2]*m[3]
    cum += contrib
    pct = cum/tot*100
    below = "BELOW" if pct > 90 and m[0] not in ("FFP-01", "FFP-04") else ("protected" if m[0] in ("FFP-01", "FFP-04") else "in 90%")
    status = "keep" if below == "in 90%" else ("protected" if below == "protected" else "trim watch")
    put(ws3, i, [m[0], m[1], money(m[2]), m[3], money(contrib), f"{pct:.1f}%", below, status],
        fill=red if below == "BELOW" else (gold if below == "protected" else None))
t3 = ws3.cell(11, 1, "Quarterly: any line below the 90% cumulative line = trim list (see VAULTMESH_MENU_TRIM_SPEC). FFP-01/04 protected.")
t3.font = Font(italic=True, color='666666')

# ============ Ph2 Rent negotiation ============
ws4 = wb.create_sheet('Ph2 Rent Negotiation')
sheet(ws4, ["Mall tier", "Current band (R/mo)", "Target ask (R/mo)", "Savings/mo", "Payback gain (per R1k saved)", "Lever"], 
      [22, 20, 16, 14, 22, 34])
ren = [
    ("Neighbourhood", "R4,000-8,000", "R4,500", "R1,500-3,500", "payback -0.4 to -1.0 mo", "kiosk adds footfall; offer base + 5% revenue share hybrid"),
    ("Regional", "R8,000-16,000", "R10,000", "R2,000-6,000", "payback -0.5 to -1.4 mo", "anchor-adjacency premium; 12-24 mo term sweetener"),
    ("Premium", "R16,000-25,000", "R18,000", "R2,000-7,000", "payback -0.4 to -1.5 mo", "movable asset = zero vacancy risk for mall; 60/40 base/revenue-share"),
]
for i, r in enumerate(ren, 2):
    put(ws4, i, list(r))
n4 = ws4.cell(6, 1, "Negotiation principle: the portal is MOBILE — the mall risks vacancy, you risk nothing. Rent-share hybrids (lower base + % of revenue) align incentives and win leases.")
n4.font = Font(italic=True, color='666666')

wb.save('FRUITFUL_PORTAL_OPTIMISER.xlsx')
print("DONE")
