# gen_franchise_model.py — Fruitful Portal: landed cost, repayment flywheel, franchise benchmarks,
# master licence structure, 3-option pricing, franchisee & HQ P&L
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import LineChart, Reference

FX = 18.45
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

def money(v): return f"R{v:,.0f}"

wb = Workbook()

# ============ Sheet 1: Landed Cost ============
ws = wb.active; ws.title = 'Landed Cost'
ws.sheet_properties.tabColor = '0FB5A6'
sheet(ws, ["Component", "Single unit", "Batch of 9 (per unit)", "Basis / Source"], [30, 16, 18, 44])
lc = [
    ("Kiosk FOB (Welink)", money(3500*FX), money(3500*FX), "Invoice WL20260401C: $3,500/unit x 9; FX 18.45"),
    ("LCL freight + handling (Durban route)", money(44474+12597+1440), "R25,000-35,000 (est)", "Afristar Est.108923: subtotal R44,473.92 + customs VAT R12,597 + VAT on services ~R1,440"),
    ("(Customs duty inside freight line)", "R12,920 included", "included", "Afristar line item"),
    ("TOTAL LANDED (JHB)", money(3500*FX+44474+12597+1440), "R89,575-99,575", "Single = R123,085; batch ~R95k avg"),
    ("Sample-unit variant (1pc @ $3,800)", money(3800*FX+44474+12597+1440), "—", "Invoice WL20260325"),
]
for i, l in enumerate(lc, 2): put(ws, i, list(l), hl=(l[0].startswith("TOTAL")))
c8 = ws.cell(8, 1, "User estimate ±R115k → confirmed at R123,085 single / ~R95k batch-of-9")
c8.font = Font(italic=True, color='666666')

# ============ Sheet 2: Repayment & Flywheel ============
ws2 = wb.create_sheet('Repayment & Flywheel')
sheet(ws2, ["Scenario", "Profit R/mo/portal", "Capex R", "Payback (months)", "Portals funded in 12 mo", "Portals funded in 24 mo"], [34, 16, 12, 14, 18, 18])
CAPEX = 3500*FX + 44474 + 12597 + 1440  # 123,085
MAX_P = 300  # fleet vision target cap
scen = [
    ("A. Coffee-only (50 cups/day, incl labour)", 13024, "Conservative"),
    ("B. Realistic full menu (coffee+bowls+smoothies+pancakes+snacks)", 84573, "Recommended"),
    ("C. Conservative full menu (60% of B)", 50744, "Caution"),
]
r = 2
for name, prof, tag in scen:
    months = 0; cash = 0.0; n = 1; funded = []
    for m in range(1, 25):
        cash += prof * n
        while cash >= CAPEX and n < MAX_P:
            n += 1; cash -= CAPEX
        funded.append(n)
    payback = CAPEX / prof
    put(ws2, r, [name, money(prof), money(CAPEX), f"{payback:.1f}", funded[11], funded[23]], hl=(tag == "Recommended"))
    r += 1
# flywheel table for scenario B
ws2b_start = r + 1
cf = ws2.cell(ws2b_start - 1, 1, "--- Flywheel detail (Scenario B): portals operating per month ---")
cf.font = Font(bold=True)
ws2b = ws2
prof = 84573
n = 1; cash = 0.0
series = []
for m in range(1, 25):
    cash += prof * n
    while cash >= CAPEX and n < MAX_P:
        n += 1; cash -= CAPEX
    series.append(n)
    put(ws2b, ws2b_start + m - 1, [f"Month {m}", f"{n} portal(s)", money(cash), "", "", ""])
# chart
ws2c = wb.create_sheet('Flywheel Chart')
sheet(ws2c, ["Month", "Portals operating"], [10, 16])
for i, v in enumerate(series, 1):
    ws2c.cell(i + 1, 1, i); ws2c.cell(i + 1, 2, v)
    ws2c.cell(i + 1, 1).border = border; ws2c.cell(i + 1, 2).border = border
ch = LineChart(); ch.title = "Portals funded from internal cash flow (Scenario B)"
ch.add_data(Reference(ws2c, min_col=2, min_row=1, max_row=25), titles_from_data=True)
ch.set_categories(Reference(ws2c, min_col=1, min_row=2, max_row=25))
ch.width, ch.height = 18, 10
ws2c.add_chart(ch, "D2")

# ============ Sheet 3: Franchise Benchmarks ============
ws3 = wb.create_sheet('Franchise Benchmarks')
sheet(ws3, ["Chain", "Model", "Initial fee", "Royalty (% of gross)", "Marketing fund", "Total ongoing", "Setup investment", "Source"], [22, 22, 18, 16, 14, 14, 20, 30])
fb = [
    ("McDonald's", "Traditional franchise", "$45,000 (R830k)", "4-5%", "4%", "~9%", "$525k-2.7M", "FDD / investopedia / swoopfunding 2025-26"),
    ("Starbucks", "Licensed store (no classic franchise)", "in licence cost", "6-8%", "2%", "~8-10%", "$315k-710k", "vettedbiz / economyinsights 2026"),
    ("vida e caffè (SA)", "Franchise", "R150k-300k", "~5-6%", "~4-5%", "10% gross", "R950k-1.4M", "safranchisebrands.co.za / vidaecaffe.com"),
    ("SA coffee franchise avg", "Franchise", "R100k-300k", "5%", "5%", "10% gross", "R700k-1.5M", "whichfranchise.co.za (Jan 2026)"),
    ("FASA benchmark (SA)", "Franchise", "varies", "4-8%", "2-4%", "6-12%", "varies", "industry standard range"),
    ("Fruitful Portal (PROPOSED)", "Kiosk franchise", "R25k-50k licence", "5-6%", "3-4%", "8-10%", "R145k-295k", "this model — priced below coffee-shop norm"),
]
for i, f in enumerate(fb, 2): put(ws3, i, list(f), hl=(f[0] == "Fruitful Portal (PROPOSED)"))

# ============ Sheet 4: Master Licence (provinces) ============
ws4 = wb.create_sheet('Master Licence')
sheet(ws4, ["Item", "Value", "Basis"], [44, 30, 36])
ml = [
    ("Provincial master licence fee (per province)", "R750,000 - R1,500,000", "5-10x unit franchise fee (industry standard); Gauteng premium"),
    ("SA provinces available", "9 (GP, WC, KZN, EC, MP, LP, NW, FS, NC)", "national rollout"),
    ("Master receives — initial fees", "50% of franchisee initial fee", "per franchisee opened in territory"),
    ("Master receives — ongoing", "50% of the 6% royalty = 3% of franchisee gross", "standard master/sub split"),
    ("Fruitful (franchisor) keeps", "50% of initial + 50% of royalty + 100% marketing fund + 100% hardware margin", "marketing fund is central"),
    ("Master break-even (Gauteng R1.5M, 8 franchisees)", "1.5M / (8 x 3% x 198,260) = ~3.2 yrs", "3% x R198,260 = R5,948/mo per franchisee"),
    ("Master break-even (smaller province R750k, 4 franchisees)", "750k / (4 x R5,948) = 2.6 yrs", "plus 50% of initial fees accelerates"),
    ("Fruitful one-off master revenue (all 9 provinces)", "R6.75M - R13.5M", "before any franchisee royalties"),
]
for i, m in enumerate(ml, 2): put(ws4, i, list(m))

# ============ Sheet 5: 3-Option Pricing ============
ws5 = wb.create_sheet('3-Option Pricing')
sheet(ws5, ["Option", "Upfront price (ZAR)", "What's included", "Ongoing fees", "HQ margin (batch unit)", "Best for"], [26, 18, 46, 24, 18, 26])
op = [
    ("1. Portal Unit ('Buy the Box')", "R145,000 (batch) / R165,000 (single)",
     "Kiosk landed + delivery + installation + 30-day warranty. No brand licence, no platform access.",
     "None", "R22k-42k/unit", "Independent operators / events / corporates"),
    ("2. Licensed Operator", "R195,000", "Unit (R145k) + brand licence (R25k) + training & setup (R25k). Platform + Support-a-Local access.",
     "Royalty 5% + marketing 3% = 8% gross", "~R72k/unit", "Single-site operators, semi-supervised"),
    ("3. Turnkey Franchise (RECOMMENDED)", "R295,000", "Unit (R145k) + Jura/Aquaspresso setup (R25k) + signage & POS (R35k) + initial stock (R40k) + training (R25k) + licence (R25k). Territory rights + full support.",
     "Royalty 6% + marketing 4% = 10% gross, 5-yr term", "~R100k/unit", "Committed franchisees, master-licence territories"),
]
for i, o in enumerate(op, 2): put(ws5, i, list(o), hl=(o[0].startswith("3.")))

# ============ Sheet 6: Franchisee & HQ P&L ============
ws6 = wb.create_sheet('Franchisee & HQ P&L')
sheet(ws6, ["Line", "Option 3 franchisee (R/mo)", "Option 2 licensee (R/mo)", "HQ per franchisee (R/mo)", "Basis"], [36, 18, 18, 18, 40])
REV = 198260.0
COGS = 89217.0
LAB = 18800.0; RENT = 690.0; OPX = 4000.0
fees3 = REV * 0.10
fees2 = REV * 0.08
rows6 = [
    ("Revenue (realistic full menu)", REV, REV, "—", "50 coffee + 30 bowls + 25 smoothies + 20 pancakes + 10 snacks/day"),
    ("Food COGS + packaging (~45%)", COGS, COGS, "—", "incl. packaging R5.10/cup + payment 3%"),
    ("Labour (2 staff)", LAB, LAB, "—", "R7,500 x2 + 12% on-costs + mgr share"),
    ("Jura rental", RENT, RENT, "—", "Aquazania Option B"),
    ("Fixed opex", OPX, OPX, "—", "utilities/cleaning/insurance"),
    ("Franchise fees", fees3, fees2, "—", "Option 3 = 10% gross; Option 2 = 8%"),
    ("FRANCHISEE PROFIT", REV-COGS-LAB-RENT-OPX-fees3, REV-COGS-LAB-RENT-OPX-fees2, "—", "Option 3 payback: 295k/65,727 = 4.5 mo"),
    ("HQ — initial fee margin", "—", "—", "100,000", "295k - 123k landed - 72k equip/stock (one-off)"),
    ("HQ — royalty (6%)", "—", "—", 11895.6, "Option 3 royalty"),
    ("HQ — marketing fund (4%)", "—", "—", 7930.4, "central fund — master gets none"),
    ("HQ monthly ongoing per franchisee", "—", "—", 19826.0, "royalty + marketing"),
    ("HQ 5-yr value per franchisee", "—", "—", 100000 + 19826*60, "initial margin + 60 months"),
]
for i, r6 in enumerate(rows6, 2):
    put(ws6, i, [r6[0]] + [money(v) if isinstance(v, float) else v for v in r6[1:4]] + [r6[4]], hl=(r6[0] in ("FRANCHISEE PROFIT", "HQ 5-yr value per franchisee")))

wb.save('FRUITFUL_FRANCHISE_MODEL.xlsx')
print("DONE")
