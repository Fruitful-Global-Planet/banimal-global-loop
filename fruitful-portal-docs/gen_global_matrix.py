# gen_global_matrix.py — Fruitful Portal Global Matrix: Multi-Language & Multi-Currency
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

# FX Rates (ZAR 1.00 = x units) - LIVE exchangerate-api.com 16 Aug 2026
# FX Rates (units per 1 ZAR) — LIVE from exchangerate-api.com, 16 Aug 2026 (key: ACCIO-ECOSYSTEM)
FX = {
    "ZAR": 1.00,
    "USD": 0.06178,   # live
    "JPY": 9.8371,    # live
    "BWP": 0.8817,    # live
    "MXN": 1.0513,    # live
    "ISK": 7.6005,    # live
    "EGP": 3.1040,    # live
    "THB": 2.0481,    # live
    "CAD": 0.08573,   # live
}

# Menu Translation Table (8 Lines)
MENU = {
    "en": ["The Coffee with Milk", "The Coffee with Froth", "The Coffee with Chocolate", "Green Energy", "Mango Lassi", "Power Protein", "Pancake", "Pancake 12-pack"],
    "ja": ["ミルク入りコーヒー", "泡立ちコーヒー", "チョコ入りコーヒー", "グリーンエナジー", "マンゴーラッシー", "パワープロテイン", "パンケーキ", "パンケーキ12個入り"],
    "es": ["Café con Leche", "Café con Espuma", "Café con Chocolate", "Energía Verde", "Lassi de Mango", "Proteína de Poder", "Panqueque", "Panqueques (12 unidades)"],
    "is": ["Kaffi með mjólk", "Kaffi með froðu", "Kaffi með súkkulaði", "Græn orka", "Mangó lassi", "Kraftprótein", "Pönnukaka", "Pönnukökur (12 stk)"],
    "ar": ["قهوة بالحليب", "قهوة برغوة", "قهوة بالشوكولاتة", "الطاقة الخضراء", "مانجو لاسي", "بروتين القوة", "بان كيك", "بان كيك (١٢ قطعة)"],
    "th": ["กาแฟใส่นม", "กาแฟฟองนม", "กาแฟใส่ช็อกโกแลต", "พลังงานสีเขียว", "มะม่วงลาสซี่", "พาวเวอร์โปรตีน", "แพนเค้ก", "แพนเค้ก 12 ชิ้น"],
    "fr": ["Le Café au Lait", "Le Café Mousseux", "Le Café au Chocolat", "Énergie Verte", "Lassi à la Mangue", "Protéine de Puissance", "Crêpe", "Crêpes (paquet de 12)"],
}

# Baseline Prices (ZAR)
PRICES = {
    "COFFEE": 38.00,
    "CHOCO": 38.00, # B logic: all coffee one price
    "SMOOTHIE": 55.00,
    "PANCAKE": 35.00,
    "P12": 420.00
}

wb = Workbook()

def put(ws, r, vals, fill=None):
    for j, v in enumerate(vals, 1):
        c = ws.cell(r, j, v); c.border = border
        if r % 2 == 1 and fill is None: c.fill = bfill
        if fill: c.fill = fill
        c.alignment = Alignment(wrap_text=True, vertical='top')

# ============ Sheet 1: Global Price Matrix ============
ws = wb.active; ws.title = 'Global Price Matrix'
ws.sheet_properties.tabColor = '0FB5A6'

headers = ["Portal ID", "Country", "City", "Currency", "FX (to ZAR)", "Coffee (R38 eq)", "Smoothie (R55 eq)", "Pancake (R35 eq)", "P12 (R420 eq)"]
widths = [12, 16, 16, 12, 12, 16, 16, 16, 16]

for j, h in enumerate(headers, 1):
    c = ws.cell(1, j, h); c.font = hfont; c.fill = hfill; c.border = border
    c.alignment = Alignment(horizontal='center', vertical='center')
for j, w in enumerate(widths, 1):
    ws.column_dimensions[get_column_letter(j)].width = w
ws.freeze_panes = 'A2'

PORTALS = [
    ("P-001", "South Africa", "Pretoria", "ZAR"),
    ("P-002", "USA", "New York", "USD"),
    ("P-003", "Japan", "Tokyo", "JPY"),
    ("P-004", "USA", "Texas", "USD"),
    ("P-005", "Botswana", "Gaborone", "BWP"),
    ("P-006", "Mexico", "Mexico City", "MXN"),
    ("P-007", "Iceland", "Reykjavik", "ISK"),
    ("P-008", "Zimbabwe", "Vic Falls", "USD"),
    ("P-009", "Egypt", "Cairo", "EGP"),
    ("P-010", "Thailand", "Bangkok", "THB"),
    ("P-011", "Canada", "Toronto", "CAD"),
]

def format_curr(v, curr):
    if curr == "JPY": return f"¥{round(v, -1)}"
    if curr == "USD": return f"${v:.2f}"
    if curr == "ZAR": return f"R{v:.2f}"
    if curr == "BWP": return f"P{v:.2f}"
    if curr == "MXN": return f"${v:.2f}"
    if curr == "ISK": return f"{round(v)} kr"
    if curr == "EGP": return f"EGP {v:.2f}"
    if curr == "THB": return f"฿{round(v)}"
    if curr == "CAD": return f"${v:.2f}"
    return f"{v:.2f}"

r = 2
for pid, country, city, curr in PORTALS:
    rate = FX[curr]
    vals = [pid, country, city, curr, rate, 
            format_curr(PRICES["COFFEE"] * rate, curr),
            format_curr(PRICES["SMOOTHIE"] * rate, curr),
            format_curr(PRICES["PANCAKE"] * rate, curr),
            format_curr(PRICES["P12"] * rate, curr)]
    for j, v in enumerate(vals, 1):
        c = ws.cell(r, j, v); c.border = border
        if r % 2 == 1: c.fill = bfill
    r += 1

# ============ Sheet 2: Language Matrix ============
ws2 = wb.create_sheet('Language Matrix')
ws2.sheet_properties.tabColor = 'FFC000'
headers2 = ["Language", "Milk Coffee", "Froth Coffee", "Choc Coffee", "Green Energy", "Mango Lassi", "Power Protein", "Pancake", "Pancake 12"]
for j, h in enumerate(headers2, 1):
    c = ws2.cell(1, j, h); c.font = hfont; c.fill = hfill; c.border = border
    c.alignment = Alignment(horizontal='center', vertical='center')
ws2.column_dimensions['A'].width = 15
for j in range(2, 10): ws2.column_dimensions[get_column_letter(j)].width = 25

r = 2
for lang, items in MENU.items():
    vals = [lang.upper()] + items
    for j, v in enumerate(vals, 1):
        c = ws2.cell(r, j, v); c.border = border
        if r % 2 == 1: c.fill = bfill
    r += 1

# ============ Sheet 3: Sizing & Pours (Global) ============
ws3 = wb.create_sheet('Sizing & Pours')
headers3 = ["Tier", "Height Range", "Health Context", "Volume (ml)", "Machine Verification"]
for j, h in enumerate(headers3, 1):
    c = ws3.cell(1, j, h); c.font = hfont; c.fill = hfill; c.border = border
ws3.column_dimensions['B'].width = 20
ws3.column_dimensions['C'].width = 30
ws3.column_dimensions['E'].width = 30

put(ws3, 2, ["Little Cup", "Up to 1.4 m", "Health-suggested intake", "250 ml", "Printed on receipt"], fill=gold)
put(ws3, 3, ["Standard Cup", "1.4 - 1.7 m", "Standard daily serve", "350 ml", "Printed on receipt"])
put(ws3, 4, ["Big Cup", "Over 1.7 m", "Hydration boost", "450 ml", "Printed on receipt"])

wb.save('FRUITFUL_GLOBAL_PORTAL_MATRIX.xlsx')
print("DONE")
