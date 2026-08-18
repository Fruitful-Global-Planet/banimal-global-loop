# gen_portal_optimiser.py — Fruitful Portal Optimiser, Phase 1: site selection engine (+ Ph2/3 scaffolds)
from openpyxl import load_workbook, Workbook
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

# ---------- tier economics ----------
TIER = {
    "Premium":      dict(rev=400000, rent=20000, deploy=85000, deposit=40000, jura=19482, opex=6000, rates=2500, traffic=100),
    "Regional":     dict(rev=280000, rent=12000, deploy=70000, deposit=24000, jura=15784, opex=5000, rates=1750, traffic=75),
    "Neighbourhood":dict(rev=180000, rent=6000,  deploy=55000, deposit=12000, jura=10086, opex=4000, rates=1150, traffic=50),
}
LANDED = 123085
LABOUR = 18800

def transport(km):
    if km and km <= 60: return 0
    if km and km <= 220: return 5000
    return 10000

# ---------- read register ----------
wb_src = load_workbook('FRUITFUL_MALL_REGISTER.xlsx')
ws_src = wb_src['Mall Register (ranked)']
malls = []
for row in ws_src.iter_rows(min_row=2, values_only=True):
    malls.append({"rank": row[0], "name": row[1], "addr": row[2], "prov": row[3], "city": row[4],
                  "km": row[5] if isinstance(row[5], (int, float)) else 999, "tier": row[6], "email": row[7]})

# ---------- compute economics + scores ----------
recs = []
for m in malls:
    t = TIER.get(m["tier"], TIER["Neighbourhood"])
    rev = t["rev"]
    rent = t["rent"]
    capex = LANDED + t["deploy"] + t["deposit"] + transport(m["km"])
    profit = rev - 0.45*rev - LABOUR - rent - t["jura"] - t["opex"] - t["rates"]
    payback = capex / profit
    rent_eff = rev / rent
    recs.append({**m, "rev": rev, "rent": rent, "capex": capex, "profit": profit, "payback": payback,
                 "rent_eff": rent_eff, "traffic": t["traffic"]})

# normalize 0-100
max_pb = max(r["payback"] for r in recs); min_pb = min(r["payback"] for r in recs)
max_re = max(r["rent_eff"] for r in recs); min_re = min(r["rent_eff"] for r in recs)
max_km = max(r["km"] for r in recs); min_km = min(r["km"] for r in recs)
for r in recs:
    r["s_payback"] = 100 * (max_pb - r["payback"]) / (max_pb - min_pb)
    r["s_rent"] = 100 * (r["rent_eff"] - min_re) / (max_re - min_re)
    r["s_dist"] = 100 * (max_km - r["km"]) / (max_km - min_km)
    r["s_traffic"] = float(r["traffic"])
    r["score"] = 0.30*r["s_traffic"] + 0.15*r["s_rent"] + 0.30*r["s_payback"] + 0.25*r["s_dist"]

recs.sort(key=lambda r: -r["score"])
for i, r in enumerate(recs, 1):
    r["opt_rank"] = i

wb = Workbook()
ws = wb.active; ws.title = 'Site Scores'
ws.sheet_properties.tabColor = '0FB5A6'
sheet(ws, ["Opt rank", "Rank", "Mall", "Tier", "City", "km", "Revenue/mo", "Rent/mo", "Profit/mo", "Capex", "Payback mo", "Traffic", "RentEff", "PaybackS", "DistS", "COMPOSITE"], 
      [9, 6, 34, 13, 14, 7, 12, 11, 12, 13, 10, 8, 8, 9, 8, 10])
for i, r in enumerate(recs):
    put(ws, i+2, [r["opt_rank"], r["rank"], r["name"], r["tier"], r["city"], r["km"],
                  money(r["rev"]), money(r["rent"]), money(r["profit"]), money(r["capex"]), f"{r['payback']:.1f}",
                  r["s_traffic"], f"{r['s_rent']:.0f}", f"{r['s_payback']:.0f}", f"{r['s_dist']:.0f}", f"{r['score']:.1f}"],
              fill=gold if r["opt_rank"] <= 10 else None)

ws2 = wb.create_sheet('Scoring Weights')
sheet(ws2, ["Parameter", "Value", "Notes"], [30, 12, 44])
weights = [
    ("Traffic/tier weight", 0.30, "Premium 100 / Regional 75 / Nbrhd 50 (proxy — replace with real footfall when available)"),
    ("Rent efficiency weight", 0.15, "revenue/rent, min-max normalised"),
    ("Payback weight", 0.30, "inverse payback, min-max normalised"),
    ("Distance weight", 0.25, "inverse km from PTA (NUCO transport cost)"),
    ("Landed kiosk", LANDED, "Welink batch cost incl freight/duty"),
    ("Labour (2 staff)", LABOUR, "R7,500 x2 + 12% + mgr share"),
    ("Transport bands", "R0 / R5k / R10k", "<=60km / 60-220 / 220+ (est.)"),
    ("COGS %", "45%", "food + packaging + payment"),
]
for i, w in enumerate(weights, 2):
    put(ws2, i, [w[0], w[1], w[2]])

# Phase 2 scaffold: staffing matrix
ws3 = wb.create_sheet('Ph2 Staffing (scaffold)')
sheet(ws3, ["Cups/day", "1 staff (R9,400)", "1.5 staff (R14,100)", "2 staff (R18,800)", "Optimal"], [12, 16, 16, 16, 12])
for i, cups in enumerate([30, 40, 50, 60, 75, 100]):
    cpm = cups * 30
    rev = cpm * 39.13
    var = cpm * 6.27 + cpm * 2.25 + cpm * 5.10 + rev * 0.03
    probs = []
    for lab in [9400, 14100, 18800]:
        probs.append(rev - var - lab - 690 - 4000)
    best = probs.index(max(probs))
    put(ws3, i+2, [cups] + [money(p) for p in probs] + [f"{best+1} staff"], fill=gold if cups == 50 else None)

# Phase 3 scaffold: flywheel reference
ws4 = wb.create_sheet('Ph3 Portfolio (scaffold)')
sheet(ws4, ["Item", "Value", "Source"], [40, 22, 40])
fw = [
    ("Phase 1 ranking feeds this sheet", "site order", "Opt rank column"),
    ("Capex range per portal", "R185k-278k", "landed + deploy + deposit + transport"),
    ("Profit range per portal/mo", "R56k-144k", "tier economics (own-ops, 2 staff)"),
    ("Flywheel rule", "open next portal when retained cash >= next capex", "franchise accrual model"),
    ("300-portal timeline", "per Ph3 build (Task #10)", "pending Phase 3 execution"),
]
for i, f in enumerate(fw, 2): put(ws4, i, list(f))

wb.save('FRUITFUL_PORTAL_OPTIMISER.xlsx')
print("DONE")
for r in recs[:10]:
    print(r["opt_rank"], r["name"][:34], r["tier"], r["km"], f"score {r['score']:.1f}", f"pb {r['payback']:.1f}")
