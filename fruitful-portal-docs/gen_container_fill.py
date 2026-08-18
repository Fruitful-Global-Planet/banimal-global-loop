# gen_container_fill.py — GZ container dead-space fill model (free freight)
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
    ws.freeze_panes = 'A2'

def put(ws, r, vals, fill=None):
    for j, v in enumerate(vals, 1):
        c = ws.cell(r, j, v); c.border = border
        if r % 2 == 1 and fill is None: c.fill = bfill
        if fill: c.fill = fill
        c.alignment = Alignment(wrap_text=True, vertical='top')

def money(v): return f"R{v:,.0f}"

FX = 18.45
LCL_CBM = 58510.0 / 5.5   # R/cbm from Afristar single-unit quote

wb = Workbook()

# ============ Sheet 1: Container scenarios ============
ws = wb.active; ws.title = 'Container Scenarios'
ws.sheet_properties.tabColor = '0FB5A6'
sheet(ws, ["Scenario", "Kiosks", "Kiosk volume (cbm)", "Container", "Internal cbm", "Nominal spare", "Usable dead space (est.)", "Freight value of dead space"], 
      [30, 8, 14, 12, 12, 12, 18, 22])
sc = [
    ("Fleet batch 1 (the 9)", 9, 49.5, "40ft HC", 67.3, 17.8, 12.0, None),
    ("Fleet batch 2 (next 9)", 9, 49.5, "40ft HC", 67.3, 17.8, 12.0, None),
    ("Two batches together", 18, 99.0, "2 x 40ft HC", 134.6, 35.6, 24.0, None),
    ("Single sample unit", 1, 5.5, "20ft", 33.2, 27.7, 6.0, None),
]
for i, s in enumerate(sc, 2):
    put(ws, i, [s[0], s[1], s[2], s[3], s[4], f"{s[5]:.1f}", f"{s[6]:.1f}", money(s[6]*LCL_CBM)],
        fill=gold if s[0].startswith("Fleet batch 1") else None)
f7 = ws.cell(7, 1, f"Freight basis: LCL R58,510 / 5.5cbm = R{LCL_CBM:,.0f}/cbm (Afristar Est.108923). Dead space ships FREE — the container is already paid.")
f7.font = Font(italic=True, color='666666')

# ============ Sheet 2: Fill plan (12cbm usable) ============
ws2 = wb.create_sheet('Fill Plan (12 cbm)')
sheet(ws2, ["Item", "Supplier (sourced)", "Unit cost (USD)", "cbm", "Units/cbm (est.)", "Units loaded", "Goods value (R)", "Freight saved (R)", "Landed cost vs BOQ line"], 
      [30, 26, 14, 8, 13, 12, 14, 14, 30])
plan = [
    ("400ml PET smoothie cup", "Guangzhou Hongkai (16y, 4.5★)", 0.03, 3.0, 1200, 3600, None, None, "R3.00 est -> ~R0.75 landed"),
    ("Dome lid 98mm", "Hongkai (bundle)", 0.015, 1.0, 2500, 2500, None, None, "R2.00 est -> ~R0.40"),
    ("Wide paper straw 10mm", "Hongkai / Telling (volume)", 0.02, 1.0, 4000, 4000, None, None, "R0.40 est -> ~R0.55 (straws NOT cheaper — volume)" ),
    ("12oz branded hot cup", "Guangzhou Victory ($0.08) / Yulong ($0.03-05)", 0.06, 2.0, 1200, 2400, None, None, "R2.50 est -> ~R1.30"),
    ("Kraft pancake box (flat)", "Guangzhou Maibao / Richpack", 0.015, 1.5, 3000, 4500, None, None, "R2.50 est -> ~R0.50"),
    ("Ceramic mug 350ml (printed)", "Xiamen Rising Chance (17y Gold, 5.0★)", 0.60, 1.0, 220, 220, None, None, "mug program — free freight"),
    ("Reserve (fittings/spares)", "—", 0, 2.5, 0, 0, None, None, "kiosk spares, signage, give-away stock"),
]
tot_v, tot_g, tot_f = 0, 0, 0
for i, p in enumerate(plan, 2):
    gv = p[2] * p[5] * FX
    fs = p[4] * p[3] * LCL_CBM
    put(ws2, i, [p[0], p[1], f"${p[2]:.2f}", p[3], p[4], p[5], money(gv), money(fs), p[6]],
        fill=gold if p[0].startswith("400ml") else None)
    tot_v += gv; tot_f += fs
put(ws2, len(plan)+3, ["TOTAL (12 cbm dead space)", "", "", "12.0", "", "", money(tot_v), money(tot_f),
                       f"combined value R{tot_v+tot_f:,.0f}"], fill=gold)
cv = ws2.cell(len(plan)+4, 1, "Caveat: carton dims/units-per-carton are ESTIMATES until suppliers confirm packing lists — Hongkai/Maibao/Victory quoted on request. Volumes scale linearly with confirmed density.")
cv.font = Font(italic=True, color='666666')

# ============ Sheet 3: Freight math ============
ws3 = wb.create_sheet('Freight Math')
sheet(ws3, ["Line", "Value", "Basis"], [40, 24, 40])
fm = [
    ("LCL rate (single kiosk)", f"R{LCL_CBM:,.0f}/cbm", "Afristar Est.108923: R58,510 / 5.5cbm"),
    ("40ft HC internal volume", "67.3 cbm", "standard container spec"),
    ("9 kiosks (crated)", "~49.5 cbm", "5.5cbm each (Welink)"),
    ("Nominal spare", "17.8 cbm", "67.3 - 49.5"),
    ("Usable dead space (conservative)", "12 cbm", "cylindrical crating waste"),
    ("Freight value of dead space", money(12*LCL_CBM), "what the fill would cost as LCL"),
    ("Fill goods value (FOB)", money(tot_v), "sourced prices incl print"),
    ("TOTAL DEAD-SPACE VALUE", money(12*LCL_CBM + tot_v), "freight avoided + goods"),
    ("Cost per portal (9 kiosks)", money((12*LCL_CBM + tot_v)/9), "≈ R21.7k of free value per portal"),
]
for i, f in enumerate(fm, 2):
    put(ws3, i, list(f), fill=gold if f[0].startswith("TOTAL") else None)

wb.save('FRUITFUL_CONTAINER_FILL_MODEL.xlsx')
print("DONE")
print(f"freight value dead space: R{12*LCL_CBM:,.0f}; goods: R{tot_v:,.0f}; per portal: R{(12*LCL_CBM+tot_v)/9:,.0f}")
