# gen_mall_register.py — distance-ranked Fruitful Portal mall register from malls.xlsx
import re
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

# ---------------- parse source ----------------
wb_src = load_workbook('malls.xlsx', read_only=True)
ws_src = wb_src.active
rows = []
for row in ws_src.iter_rows(min_row=2, values_only=True):
    if not row or not row[0]:
        continue
    rows.append({"id": str(row[0]).strip(), "name": str(row[1]).strip(),
                 "addr": str(row[2] or "").strip(), "cat": str(row[3] or "").strip(),
                 "email": str(row[4] or "").strip()})

# ---------------- classify: mall vs not ----------------
ONLINE = ["online", "webstore", "applianceonline", "buyfast", "loot", "oneday", "yuppie", "zando",
          "camera", "craftand", "craftersweb", "cybercellar", "damasq", "datakey", "diligo",
          "dreamtime", "durbsinvest", "e-stolo", "elite", "futurama", "global visual", "green goods",
          "hoiti", "holsky", "hopp", "house of sofia", "hover", "how thoughtful", "immaculate",
          "indraf", "island lily", "itradepro", "jacob", "jfacs", "jozi", "kidsology", "laager",
          "linger", "little shop", "logic tech", "lushberry", "m m i", "metropolitan", "mona lisa",
          "nafcoc", "old nick", "our precious", "omniblend", "people's place", "pick", "pokeit",
          "price spy", "quirkey", "radiant", "rand outfitters", "ready steady", "red spade", "runway",
          "s a centres", "salt lifestyle", "sascootershop", "shop and ship", "shoprite properties",
          "simplicity", "simply everything", "skapie", "skinwellness", "smacs", "sunika", "sweettaboo",
          "take 2", "the beer keg", "thrupps", "towers", "trillion", "tshirt", "ubershelf", "up4grabs",
          "vapemix", "vapory", "vape king", "wackybrats", "webantics", "win a lot", "yogabox",
          "your mementos", "blucloud", "blue skye", "bribed", "cartoyz", "cayak", "chasing clouds",
          "china mall", "china mart", "cinnamon", "cobrole", "crafters factory", "dubai centre",
          "elridge", "fadhlhome", "firstshop", "greenoak", "gutsche", "hartelief", "luxury", "moffett",
          "murchison", "pan africa", "people", "sunward", "victoria lane", "vineyard", "walker drive",
          "woodmill", "spar", "kwikspar"]
MALL_HINTS = ["mall", "centre", "center", "plaza", "square", "village", "arcade", "park", "crossing",
              "lifestyle", "boulevard", "walk", "commons", "market", "parade", "junction", "meander",
              "comers", "pavilion", "waterfront"]

def classify(name):
    n = name.lower()
    if any(h in n for h in ONLINE):
        return "not_mall"
    if any(h in n for h in MALL_HINTS):
        return "mall"
    return "not_mall"

# ---------------- distance from Pretoria (Silver Lakes HQ) ----------------
CITY_KM = {
    "pretoria": 12, "menlyn": 10, "brooklyn": 12, "hatfield": 13, "arcadia": 12, "sammy marks": 15,
    "tramshed": 14, "kolonnade": 25, "wonderpark": 28, "wonder park": 28, "the grove": 12, "grove": 12,
    "woodlands": 15, "wapadrand": 14, "olympus": 12, "morleta": 10, "irene": 20, "centurion": 30,
    "elridge": 18, "grootvlei": 25, "midrand": 40, "kyalami": 45, "rivonia": 50,
    "mall of africa": 40, "fourways": 55, "bryanston": 58, "randburg": 62, "sandton": 58,
    "hyde park": 60, "nelson mandela": 60, "bedford": 66, "balfour": 65,
    "eastgate": 68, "east rand": 70, "greenstone": 65, "modderfontein": 64, "edenvale": 68,
    "elspark": 72, "boksburg": 72, "germiston": 68, "springs": 85, "kempton": 70, "boulders": 30,
    "brightwater": 60, "cresta": 62, "westgate": 75, "clearwater": 75, "roodepoort": 72,
    "princess crossing": 72, "southgate": 80, "dobsonville": 82, "jabulani": 80, "soweto": 80,
    "protea gardens": 78, "vaal": 105, "vanderbijlpark": 105, "northmead": 70, "newmarket": 72,
    "mona lisa": 70, "honeydew": 65, "randridge": 62, "duncan yard": 60, "river square": 62,
    "27 boxes": 62, "sunward park": 72, "victoria lane": 68, "waverley": 70, "the tramshed": 14,
    "hercules": 20, "vryheid": 360, "witbank": 110, "middelburg": 130, "nelspruit": 310,
    "riverside": 310, "white river": 330, "kanyamazane": 330, "malelane": 380, "kwamhlanga": 100,
    "marlothi": 340, "kwagga": 320, "belfast": 190, "central mill": 130, "polokwane": 260,
    "limpopo mall": 260, "mokopane": 210, "crossing": 210, "tzaneen": 330, "tzaneng": 330,
    "bochum": 300, "musina": 470, "savannah": 350, "thavhani": 380, "venda": 380, "gaborone": 360,
    "rustenburg": 130, "waterfall mall": 130, "village mall": 90, "magalies": 90, "mooi rivier": 180,
    "potchefstroom": 180, "flamwood": 220, "klerksdorp": 220, "sediba": 200, "moruleng": 200,
    "ventersdorp": 150, "hartbeespoort": 60, "brits": 75, "lanseria": 50, "welkom": 330,
    "fleurdal": 330, "virginia": 340, "lochlogan": 340, "bloemfontein": 450, "bothaville": 280,
    "durban": 560, "umhlanga": 570, "la lucia": 570, "westville": 560, "pinetown": 550,
    "pavilion": 560, "galleria": 580, "south coast": 620, "scottsburgh": 630, "port shepstone": 700,
    "shelly": 700, "toti": 590, "westwood": 560, "montclair": 560, "bluff": 570, "boardwalk": 570,
    "kloof village": 550, "gillespie": 560, "china mall": 560, "davenport": 560, "pearls": 570,
    "phoenix": 570, "bridge city": 540, "cascades": 520, "ballito": 520, "tiffanys": 520,
    "selgro": 480, "quarry": 480, "pietermaritzburg": 480, "howick": 460, "ezakheni": 360,
    "ladysmith": 360, "newcastle": 330, "harding": 720, "ixopo": 620, "richards bay": 600,
    "mthatha": 780, "kokstad": 650, "east london": 1020, "hemingways": 1020, "beacon bay": 1020,
    "vincent": 1020, "port elizabeth": 1050, "gqeberha": 1050, "walmer": 1050, "greenacres": 1050,
    "cleary": 1050, "fountains": 1050, "moffett": 1050, "metlife": 1050, "king's court": 1050,
    "summerstrand": 1050, "pier 14": 1050, "gardens centre": 1050, "pe": 1050, "9th avenue": 1050,
    "george": 1250, "mossel bay": 1250, "knysna": 1250, "eden meander": 1250, "bitou": 1300,
    "cape town": 1450, "canal walk": 1440, "century city": 1440, "tygervalley": 1430, "cape gate": 1430,
    "sonstraal": 1430, "brackenfell": 1420, "kraaifontein": 1420, "n1 city": 1430, "tableview": 1440,
    "longbeach": 1440, "constantia": 1460, "cape quarter": 1450, "paarl": 1430, "stellenbosch": 1400,
    "neelsie": 1400, "somerset west": 1400, "waterstone": 1410, "willowbridge": 1430, "mountain mill": 1430,
    "rembrandt": 1430, "garden": 1450, "high street": 1420, "woodstock": 1450, "sanctuary": 1450,
    "market square": 1430, "vineyard": 1430, "howard": 1450, "woodmill": 1400, "valyland": 1430,
    "i pic": 1420, "ipic": 1420, "aurora": 1420, "kenridge": 1400, "access park": 1450,
    "kimberley": 500, "diamond pavilion": 500, "north cape": 500, "upington": 800, "apian": 700,
    "kuruman": 600, "postmasburg": 700,
}
DEFAULTS = {"gauteng": 60, "kwazulu": 560, "western cape": 1450, "eastern cape": 1050, "limpopo": 260,
            "north west": 130, "free state": 330, "mpumalanga": 110, "northern cape": 500}
PROVINCE_HINTS = ["gauteng", "kwazulu", "western cape", "eastern cape", "limpopo", "north west",
                  "free state", "mpumalanga", "northern cape"]
CITY_CLEAN = {
    "gauteng": "Johannesburg/Pretoria", "kwazulu": "Durban", "western cape": "Cape Town",
    "eastern cape": "Port Elizabeth", "limpopo": "Polokwane", "north west": "Rustenburg",
    "free state": "Welkom", "mpumalanga": "Witbank", "northern cape": "Kimberley",
}

def locate(name, addr):
    hay = (name + " " + addr).lower()
    prov = None
    for p in PROVINCE_HINTS:
        if p in addr.lower():
            prov = p; break
    best_km = None; best_city = None
    for c, d in CITY_KM.items():
        if c in hay:
            if best_km is None or d < best_km:
                best_km = d; best_city = c.title()
    if best_km is None and prov:
        best_km = DEFAULTS.get(prov)
        best_city = CITY_CLEAN.get(prov)
    return prov, best_city, best_km

# ---------------- tier ----------------
PREMIUM = ["sandton", "hyde park", "nelson mandela", "mall of africa", "menlyn", "fourways", "canal walk",
           "tygervalley", "pavilion", "eastgate", "cresta", "clearwater", "la lucia", "umhlanga",
           "galleria", "willowbridge", "woodlands", "grove", "highveld", "middelburg", "river side"]
REGIONAL = ["brooklyn", "centurion", "wonder", "kolonnade", "boulders", "irene", "east rand", "westgate",
            "southgate", "vaal", "gate", "cape", "paarl", "n1", "longbeach", "hemingways", "walmer",
            "greenacres", "mthatha", "limpopo", "savannah", "thavhani", "venda", "bochum", "tzaneen",
            "jabulani", "dobsonville", "randridge", "north", "westville", "montclair", "south coast",
            "bridge city", "pietermaritzburg", "selgro", "quarry", "high street", "garden", "fountains",
            "metlife", "waterfront", "mossel", "george", "claremont"]

def tier(name, addr=""):
    n = (name + " " + addr).lower()
    if any(p in n for p in PREMIUM): return "Premium"
    if any(p in n for p in REGIONAL): return "Regional"
    return "Neighbourhood"

# ---------------- build ----------------
malls = []
for r in rows:
    kind = classify(r["name"])
    if kind != "mall":
        continue
    prov, city, km = locate(r["name"], r["addr"])
    t = tier(r["name"], r["addr"])
    malls.append({**r, "prov": prov, "city": city, "km": km, "tier": t})

malls_sorted = sorted(malls, key=lambda m: (m["km"] if m["km"] else 999))

wb = Workbook()
ws = wb.active; ws.title = 'Mall Register (ranked)'
ws.sheet_properties.tabColor = '0FB5A6'
sheet(ws, ["Rank", "Mall / Centre", "Address", "Province", "City", "km from PTA", "Tier", "Contact email", "Deployment order"], [6, 38, 40, 13, 18, 12, 13, 36, 12])
for i, m in enumerate(malls_sorted, 1):
    order = ""
    if m["km"] and m["km"] <= 60:
        order = "Wave 1 (PTA/JHB)" if m["tier"] in ("Premium", "Regional") else "Wave 1b"
    elif m["km"] and m["km"] <= 220:
        order = "Wave 2"
    elif m["km"]:
        order = "Wave 3+"
    put(ws, i + 1, [i, m["name"], m["addr"], (m["prov"] or "").title(), m["city"] or "", m["km"] if m["km"] else "?", m["tier"], m["email"], order])

ws2 = wb.create_sheet('Excluded list')
sheet(ws2, ["Name", "Address", "Reason"], [40, 40, 18])
for i, r in enumerate(rows, 2):
    if classify(r["name"]) != "mall":
        put(ws2, i, [r["name"], r["addr"], "online shop / tenant / non-centre"])

ws3 = wb.create_sheet('Summary')
sheet(ws3, ["Metric", "Value"], [40, 30])
tot = len(malls)
by_prov = {}
by_tier = {}
for m in malls:
    p = m["prov"] or "unknown"
    by_prov[p] = by_prov.get(p, 0) + 1
    by_tier[m["tier"]] = by_tier.get(m["tier"], 0) + 1
summ = [
    ("Total centres (after excluding online/tenant)", tot),
    ("Premium", by_tier.get("Premium", 0)),
    ("Regional", by_tier.get("Regional", 0)),
    ("Neighbourhood", by_tier.get("Neighbourhood", 0)),
    ("Within 60km of Pretoria (Wave 1)", sum(1 for m in malls if m["km"] and m["km"] <= 60)),
    ("60-220km (Wave 2)", sum(1 for m in malls if m["km"] and 60 < m["km"] <= 220)),
    ("220km+ (Wave 3)", sum(1 for m in malls if m["km"] and m["km"] > 220)),
]
for i, (k, v) in enumerate(summ, 2):
    put(ws3, i, [k, v])
for p, c in sorted(by_prov.items(), key=lambda x: -x[1]):
    put(ws3, ws3.max_row + 1, [f"Province: {p.title()}", c])

wb.save('FRUITFUL_MALL_REGISTER.xlsx')
print(f"malls: {len(malls)} / rows: {len(rows)}")
