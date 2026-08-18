# wire_ffp_skus.py — add canonical FFP menu SKUs to the priced master BOQ (D01/D02 + packaging)
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

SRC = 'FRUITFUL_MASTER_BOQ_PRICED.xlsx'
OUT = 'FRUITFUL_MASTER_BOQ_CANONICAL.xlsx'

thin = Side(style='thin', color='BFBFBF')
border = Border(left=thin, right=thin, top=thin, bottom=thin)
hfont = Font(name='Arial', size=11, bold=True, color='FFFFFF')
hfill = PatternFill('solid', start_color='0FB5A6')
gold = PatternFill('solid', start_color='FFF2CC')

# keyword -> canonical FFP part number (Mercedes rule)
FFP_MAP = [
    ("espresso beans", "FFP-01·02·03"),
    ("filter coffee ground", "NON-MENU (trim)"),
    ("whole milk", "FFP-01·02·03"),
    ("skim milk", "FFP-01·02·03"),
    ("oat milk", "FFP-01·02·03"),
    ("almond milk", "FFP-01·02·03"),
    ("soy milk", "FFP-01·02·03"),
    ("coconut milk", "FFP-04·05·06"),
    ("vanilla syrup", "NON-MENU (trim)"),
    ("caramel syrup", "NON-MENU (trim)"),
    ("hazelnut syrup", "NON-MENU (trim)"),
    ("mocha sauce", "FFP-03"),
    ("white choc sauce", "FFP-03"),
    ("cocoa powder", "FFP-03"),
    ("matcha", "NON-MENU (trim)"),
    ("cake flour", "FFP-07·08"),
    ("baking powder", "FFP-07·08"),
    ("baking soda", "FFP-07·08"),
    ("fine salt", "FFP-07·08"),
    ("castor sugar", "FFP-07·08"),
    ("brown sugar", "FFP-07·08"),
    ("eggs", "FFP-07·08"),
    ("buttermilk", "FFP-07·08"),
    ("butter", "FFP-07·08"),
    ("cooking spray", "FFP-07·08"),
    ("vanilla essence", "FFP-07·08"),
    ("cinnamon sugar", "FFP-07·08"),
    ("golden syrup", "FFP-07·08"),
    ("maple syrup", "FFP-07·08"),
    ("strawberry jam", "FFP-07·08"),
    ("apricot jam", "FFP-07·08"),
    ("lemon curd", "FFP-07·08"),
    ("condensed milk", "FFP-07·08"),
    ("chocolate hazelnut", "FFP-07·08"),
    ("whipped cream", "FFP-07·08"),
    ("icing sugar", "FFP-07·08"),
    ("dulce de leche", "FFP-07·08"),
    ("fresh mango", "FFP-05"),
    ("fresh pineapple", "FFP-04·06"),
    ("kiwi", "FFP-04·05·06"),
    ("strawberries", "FFP-04·05·06"),
    ("blueberries", "FFP-04·05·06"),
    ("raspberries", "FFP-04·05·06"),
    ("oranges navel", "NON-MENU (juice cut)"),
    ("grapefruit", "NON-MENU (juice cut)"),
    ("pomelo", "NON-MENU (juice cut)"),
    ("watermelon", "NON-MENU (bowl phase-2)"),
    ("cucumber english", "FFP-04"),
    ("fresh mint", "FFP-04"),
    ("baby spinach", "FFP-04"),
    ("green apple", "FFP-04"),
    ("fresh ginger", "FFP-04"),
    ("dragon fruit", "FFP-04·05·06 bench"),
    ("banana", "FFP-06"),
    ("lemon", "NON-MENU (juice cut)"),
    ("lime", "FFP-04·05·06"),
    ("apples red/green", "NON-MENU (juice cut)"),
    ("beetroot", "NON-MENU (juice cut)"),
    ("carrots", "NON-MENU (juice cut)"),
    ("coconut water carton", "FFP-06"),
    ("greek yogurt", "FFP-05"),
    ("almond butter", "FFP-06"),
    ("whey protein", "FFP-06"),
    ("plant protein", "FFP-06"),
    ("chia seeds", "FFP-06"),
    ("granola", "FFP-06"),
    ("shredded coconut", "FFP-06"),
    ("mixed nuts", "FFP-06"),
    ("cacao nibs", "FFP-06"),
    ("dried apricots", "NON-MENU (snack cut)"),
    ("dried mango", "NON-MENU (snack cut)"),
    ("dried cranberries", "NON-MENU (snack cut)"),
    ("rolled oats", "NON-MENU (snack cut)"),
    ("cardamom", "FFP-05"),
    ("hot cups 8oz", "FFP-01·02·03 pkg"),
    ("hot cups 12oz", "FFP-01·02·03 pkg"),
    ("hot cups 16oz", "FFP-01·02·03 pkg"),
    ("flat lids", "FFP-01·02·03 pkg"),
    ("dome lids sip-hole", "FFP-01·02·03 pkg"),
    ("splash stoppers", "FFP-01·02·03 pkg"),
    ("cup sleeves", "FFP-01·02·03 pkg"),
    ("hot take-away bags", "FFP-01·02·03 pkg"),
    ("cold cups 16oz", "FFP-04·05·06 pkg"),
    ("cold cups 24oz", "FFP-04·05·06 pkg"),
    ("dome lids cold", "FFP-04·05·06 pkg"),
    ("flat lids cold", "FFP-04·05·06 pkg"),
    ("juice cups 8oz", "NON-MENU (juice cut)"),
    ("fruit bowl 500ml", "NON-MENU (bowl phase-2)"),
    ("fruit bowl 750ml", "NON-MENU (bowl phase-2)"),
    ("smoothie bowls", "NON-MENU (bowl phase-2)"),
    ("pancake box single", "FFP-07 pkg"),
    ("pancake box double", "FFP-08 pkg"),
    ("greaseproof sheets", "FFP-07·08 pkg"),
    ("greaseproof bags", "FFP-07·08 pkg"),
    ("kraft snack bags", "FFP-07·08 pkg"),
    ("bakery tissue", "FFP-07·08 pkg"),
    ("white sugar sachets", "FFP-01·02·03 cond"),
    ("raw cane sugar", "FFP-01·02·03 cond"),
    ("brown sugar sachets", "FFP-01·02·03 cond"),
    ("sweetener sachets", "FFP-01·02·03 cond"),
    ("stevia sachets", "FFP-01·02·03 cond"),
    ("vanilla sugar sachets", "FFP-01·02·03 cond"),
    ("wooden stir sticks", "FFP-01·02·03 cond"),
    ("plastic stirrers", "FFP-01·02·03 cond"),
    ("branded serviettes", "FFP-01·02·03 cond"),
    ("drinking straws", "FFP-04·05·06 pkg"),
    ("smoothie straws wide", "FFP-04·05·06 pkg"),
]

wb = load_workbook(SRC)
ws = wb['18-Dept BOQ (Priced)']
# insert header col 8: "Menu SKU (FFP)"
ws.cell(1, 8, "Menu SKU (FFP)")
c = ws.cell(1, 8); c.font = hfont; c.fill = hfill; c.border = border
c.alignment = Alignment(horizontal='center', vertical='center')
ws.column_dimensions['H'].width = 22

def map_sku(item):
    il = str(item).lower()
    for kw, sku in FFP_MAP:
        if kw in il:
            return sku
    return ""

wired = 0
for row in ws.iter_rows(min_row=2):
    item = row[1].value
    sku = map_sku(item)
    if sku:
        row[7].value = sku
        row[7].border = border
        row[7].alignment = Alignment(wrap_text=True, vertical='top')
        row[7].fill = gold if sku.startswith("FFP") else PatternFill('solid', start_color='FDE9E9')
        wired += 1

wb.save(OUT)
print(f"wired {wired} rows -> {OUT}")
