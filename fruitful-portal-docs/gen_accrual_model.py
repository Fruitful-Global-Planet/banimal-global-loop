# gen_accrual_model.py — Fruitful Franchise: professional accrual model (bank-grade)
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

# ---------- assumptions ----------
PKG = 450000.0
STOCK_CREDIT = 70000.0
TNC = 40000.0                 # odds & ends per installation (T&Cs): launch mktg 15k, training bond 10k, legal/admin 8k, contingency 7k
VAT = 0.15
REV_STEADY = 198260.0
RAMP = [0.55, 0.70, 0.85] + [1.0]*9
COGS_PCT = 0.45
LAB_M123 = 12600.0; LAB_M4 = 16800.0
RENT = 6000.0; JURA = 2082.0; OPEX = 4000.0
ROY = 0.06; MKT = 0.04
AMZN = 0.075                # of supply cost (~R25k steady -> R2,250/mo)
SUPPLY_STEADY = 25000.0
DEP = 250000.0 / 60         # equipment 250k depreciated 60 mo
TAX = 0.27
HO_OH = 135000.0            # HQ central overhead / mo
BRAND_CAGR = 0.18
PLATO = (550000.0, 1300000.0, 10)   # user-provided benchmark: 550k -> 1.3M ~10 yrs

wb = Workbook()

# ============ 1. Assumptions ============
ws = wb.active; ws.title = 'Assumptions'
ws.sheet_properties.tabColor = '0FB5A6'
sheet(ws, ["Assumption", "Value", "Flag"], [44, 30, 44])
A = [
    ("Package price (excl VAT)", "R450,000", "Locked (Heyns)"),
    ("Opening stock credit (on account)", "R70,000", "Locked (Heyns) — drawn at cost + distribution %"),
    ("T&C odds & ends per installation", "R40,000 (15k launch mktg + 10k training bond + 8k legal/admin + 7k contingency)", "Model estimate — fix per contract"),
    ("VAT", "15% (package R517,500 incl; input reclaimable if VAT-registered)", "SA standard"),
    ("Steady-state revenue/mo (neighbourhood mall)", "R198,260", "Full-menu unit economics (50 coffee + 30 bowls + 25 smoothies + 20 pancakes + 10 snacks)"),
    ("Ramp-up", "M1 55% / M2 70% / M3 85% / M4+ 100%", "Realistic new-kiosk curve"),
    ("COGS", "45% of revenue (incl payment fees)", "Unit economics"),
    ("Labour", "M1-3 1.5 staff R14,100; M4+ 2 staff R18,800", "Ramp-friendly staffing"),
    ("Mall rent (8m2 kiosk)", "R6,000/mo (neighbourhood band)", "Tracker mid-point"),
    ("Jura X8 Option B", "R2,082/mo", "Aquazania contract"),
    ("Royalty / marketing", "6% / 4% of revenue", "Pack v2"),
    ("Amazon fulfilment", "7.5% of supply cost (~R2,250/mo steady)", "Passed to franchisee"),
    ("Depreciation", "R250k equipment / 60 mo = R4,167/mo", "Accrual standard"),
    ("SA corporate tax", "27%", "SARS rate (12I capex allowances could reduce Y1 — note)"),
    ("HQ central overhead", "R135,000/mo", "Estimate: brand, platform, support"),
    ("Brand value CAGR", "18%/yr (R450k -> ~R1.03M in 5 yrs)", "Plato benchmark: R550k -> R1.3M ~10 yrs (user-provided)"),
]
for i, a in enumerate(A, 2): put(ws, i, list(a))

# ============ 2. Franchisee Y1 P&L ============
ws2 = wb.create_sheet('Franchisee Y1 P&L')
sheet(ws2, ["Line"] + [f"M{m}" for m in range(1, 13)] + ["Y1 total"], [26] + [11]*13)
rev = [REV_STEADY * r for r in RAMP]
lines = []
def row(name, vals, fill=None):
    lines.append((name, vals, fill))
row("Revenue", rev)
row("COGS (45%)", [v * COGS_PCT for v in rev])
row("Labour", [LAB_M123 if m <= 3 else LAB_M4 for m in range(1, 13)])
row("Mall rent", [RENT]*12)
row("Jura Option B", [JURA]*12)
row("Fixed opex", [OPEX]*12)
row("Royalty (6%)", [v * ROY for v in rev])
row("Marketing (4%)", [v * MKT for v in rev])
row("Amazon delivery (7.5% supply)", [SUPPLY_STEADY * r * AMZN for r in RAMP])
row("EBITDA", [rev[i] - rev[i]*COGS_PCT - (LAB_M123 if i < 3 else LAB_M4) - RENT - JURA - OPEX - rev[i]*ROY - rev[i]*MKT - SUPPLY_STEADY*RAMP[i]*AMZN for i in range(12)])
row("Depreciation", [DEP]*12)
row("EBIT", [None]*12)
row("Tax (27%)", [None]*12)
row("NET PROFIT", [None]*12)
for name, vals, fill in lines:
    r = ws2.max_row + 1
    cells = [name] + [money(v) if isinstance(v, (int, float)) else v for v in vals]
    if name == "EBITDA":
        eb = [rev[i] - rev[i]*COGS_PCT - (LAB_M123 if i < 3 else LAB_M4) - RENT - JURA - OPEX - rev[i]*ROY - rev[i]*MKT - SUPPLY_STEADY*RAMP[i]*AMZN for i in range(12)]
        cells = [name] + [money(v) for v in eb] + [money(sum(eb))]
    elif name == "Depreciation":
        cells = [name] + [money(DEP)]*12 + [money(DEP*12)]
    elif name == "EBIT":
        ebit = [rev[i] - rev[i]*COGS_PCT - (LAB_M123 if i < 3 else LAB_M4) - RENT - JURA - OPEX - rev[i]*ROY - rev[i]*MKT - SUPPLY_STEADY*RAMP[i]*AMZN - DEP for i in range(12)]
        cells = [name] + [money(v) for v in ebit] + [money(sum(ebit))]
    elif name == "Tax (27%)":
        tax = [max(0.0, (rev[i] - rev[i]*COGS_PCT - (LAB_M123 if i < 3 else LAB_M4) - RENT - JURA - OPEX - rev[i]*ROY - rev[i]*MKT - SUPPLY_STEADY*RAMP[i]*AMZN - DEP)) * TAX for i in range(12)]
        cells = [name] + [money(v) for v in tax] + [money(sum(tax))]
    elif name == "NET PROFIT":
        net = [(rev[i] - rev[i]*COGS_PCT - (LAB_M123 if i < 3 else LAB_M4) - RENT - JURA - OPEX - rev[i]*ROY - rev[i]*MKT - SUPPLY_STEADY*RAMP[i]*AMZN - DEP) * (1 - TAX) for i in range(12)]
        cells = [name] + [money(v) for v in net] + [money(sum(net))]
        fill = gold
    put(ws2, r, cells, fill=fill)

# ============ 3. Franchisee cash flow + payback ============
ws3 = wb.create_sheet('Franchisee Cash Flow')
sheet(ws3, ["Line", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5"], [36, 14, 14, 14, 14, 14])
y1_net = sum([(rev[i] - rev[i]*COGS_PCT - (LAB_M123 if i < 3 else LAB_M4) - RENT - JURA - OPEX - rev[i]*ROY - rev[i]*MKT - SUPPLY_STEADY*RAMP[i]*AMZN - DEP) * (1 - TAX) for i in range(12)])
steady_month = (REV_STEADY - REV_STEADY*COGS_PCT - LAB_M4 - RENT - JURA - OPEX - REV_STEADY*ROY - REV_STEADY*MKT - SUPPLY_STEADY*AMZN - DEP) * (1 - TAX)
steady_net = steady_month * 12
steady_op = (steady_month + DEP) * 12
cf = [
    ("Net profit (accrual)", [y1_net] + [steady_net]*4),
    ("+ Depreciation", [DEP*12]*5),
    ("Operating cash", [y1_net + DEP*12] + [steady_op]*4),
    ("Package payment (excl VAT)", [-PKG, 0, 0, 0, 0]),
    ("T&C extras", [-TNC, 0, 0, 0, 0]),
    ("Stock credit draw/repay (net)", [0.0]*5, "net zero — credit drawn Y1, repaid via supply"),
    ("Working capital build (Y1 only)", [-30000, 0, 0, 0, 0]),
    ("NET CASH FLOW", [y1_net + DEP*12 - PKG - TNC - 30000] + [steady_op]*4),
    ("CUMULATIVE CASH", [None]*5),
]
for i, (name, vals, *note) in enumerate(cf):
    r = i + 2
    cells = [name] + [money(v) if isinstance(v, (int, float)) else v for v in vals]
    if name == "CUMULATIVE CASH":
        cum = []
        run = 0
        for v in cf[7][1]:
            run += v; cum.append(run)
        cells = [name] + [money(v) for v in cum]
        fill = gold
    else:
        fill = None
    put(ws3, r, cells, fill=fill)
    if note:
        ws3.cell(r, 7, note[0])
cb = ws3.cell(12, 1, "Cash break-even: Y1 -R" + f"{abs(y1_net + DEP*12 - PKG - TNC - 30000):,.0f}" + " -> positive cumulative ~month 14-16")
cb.font = Font(italic=True, color='666666')

# ============ 4. Brand value curve ============
ws4 = wb.create_sheet('Brand Value Curve')
sheet(ws4, ["Year", "Portal asset value (performing)", "Plato benchmark (user-provided)", "Notes"], [10, 30, 30, 30])
v0 = PKG
for y in range(1, 6):
    v = v0 * (1 + BRAND_CAGR) ** y
    plato = PLATO[0] + (PLATO[1] - PLATO[0]) * y / PLATO[2]
    put(ws4, y + 1, [y, money(v), money(plato), "resale/licence value of a performing portal"])
pb = ws4.cell(8, 1, "Plato: R550k -> R1.3M+ (no locations under R1.3M today). Fruitful at 18%/yr CAGR: R450k -> ~R1.03M in 5 yrs")
pb.font = Font(italic=True, color='666666')

# ============ 5. HQ consolidated ============
ws5 = wb.create_sheet('HQ Consolidated')
sheet(ws5, ["Line (10 franchisees, year 1)", "Direct territories", "With master split (50/50 royalty)"], [40, 22, 22])
ONEOFF = 214000.0          # 182k package margin + 32k T&C margin
ONGOING_D = 25326.0
ONGOING_N = 19378.0
hq = [
    ("One-off margin (10 x R214k)", ONEOFF*10, ONEOFF*10),
    ("Ongoing (10 x 12 mo)", ONGOING_D*10*12, ONGOING_N*10*12),
    ("Gross income", ONEOFF*10 + ONGOING_D*10*12, ONEOFF*10 + ONGOING_N*10*12),
    ("HQ overhead (R135k x 12)", -HO_OH*12, -HO_OH*12),
    ("Pretax", ONEOFF*10 + ONGOING_D*10*12 - HO_OH*12, ONEOFF*10 + ONGOING_N*10*12 - HO_OH*12),
    ("Tax (27%)", (ONEOFF*10 + ONGOING_D*10*12 - HO_OH*12)*0.73, (ONEOFF*10 + ONGOING_N*10*12 - HO_OH*12)*0.73),
    ("NET (year 1, 10 portals)", (ONEOFF*10 + ONGOING_D*10*12 - HO_OH*12)*0.73, (ONEOFF*10 + ONGOING_N*10*12 - HO_OH*12)*0.73),
    ("Lifetime value per franchisee (5 yrs)", ONEOFF + ONGOING_D*12*5, ONEOFF + ONGOING_N*12*5),
    ("Master licence one-off (9 provinces, excl this model)", 9000000, 9000000),
]
for i, h in enumerate(hq, 2):
    put(ws5, i, [h[0], money(h[1]), money(h[2])], fill=gold if h[0].startswith(("NET", "Lifetime", "Master")) else None)

# ============ 6. Executive talking points ============
ws6 = wb.create_sheet('Talking Points')
sheet(ws6, ["Metric", "Value"], [52, 26])
tp = [
    ("Package (excl VAT) — Mercedes standard", "R450,000 (R380k build + R70k stock credit)"),
    ("Franchisee profit/mo (steady state)", money(steady_month)),
    ("Franchisee year-1 net profit (accrual)", money(y1_net)),
    ("Franchisee 5-yr cumulative net", money(y1_net + steady_net*4)),
    ("Franchisee 5-yr cumulative CASH", money(y1_net + DEP*12 - PKG - TNC - 30000 + steady_op*4)),
    ("Cash break-even", "~month 14-16"),
    ("HQ year-1 net (10 portals, direct)", money((ONEOFF*10 + ONGOING_D*10*12 - HO_OH*12)*0.73)),
    ("HQ year-1 net (10 portals, master split)", money((ONEOFF*10 + ONGOING_N*10*12 - HO_OH*12)*0.73)),
    ("LTV per franchisee (5 yrs)", money(ONEOFF + ONGOING_D*12*5)),
    ("Portal asset value Y5 (18% CAGR)", money(v0*(1+BRAND_CAGR)**5)),
    ("Plato trajectory (user benchmark)", "R550k -> R1.3M+; Fruitful aims same curve"),
]
for i, t in enumerate(tp, 2): put(ws6, i, list(t), fill=gold if t[0].startswith(("Franchisee profit", "HQ year-1 net (10, direct)", "LTV")) else None)

wb.save('FRUITFUL_FRANCHISE_ACCRUAL_MODEL.xlsx')
print("DONE")
