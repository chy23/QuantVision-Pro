import json
import re

with open('tw_names.json', 'r') as f:
    names_map = json.load(f)

with open('app.js', 'r') as f:
    code = f.read()

js_dict = "const TW_NAMES = " + json.dumps(names_map, ensure_ascii=False, indent=2) + ";"

# Insert TW_NAMES after CATEGORY_MAP
if "const TW_NAMES" not in code:
    code = code.replace("const CATEGORY_MAP", js_dict + "\n\nconst CATEGORY_MAP")

# Replace ${stock.name} with ${TW_NAMES[stock.symbol] || stock.name} in categoryFilter logic
code = code.replace('<div class="stock-name">${stock.name}</div>', '<div class="stock-name">${TW_NAMES[stock.symbol] || stock.name}</div>')

with open('app.js', 'w') as f:
    f.write(code)
