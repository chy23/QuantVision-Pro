import json
import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

capital_map = {}

def fetch_capital(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            for item in data:
                try:
                    cap = int(item['實收資本額'])
                    capital_map[item['公司代號']] = cap
                except:
                    pass
    except Exception as e:
        print(f"Error fetching {url}: {e}")

print("Fetching TWSE capital...")
fetch_capital('https://openapi.twse.com.tw/v1/opendata/t187ap03_L')

print("Fetching TPEx capital...")
fetch_capital('https://openapi.tpex.org.tw/v1/opendata/t187ap03_O')

# Load existing categories
with open('tw_symbols.json', 'r') as f:
    categories = json.load(f)

new_categories = {}
for cat, symbols in categories.items():
    # Sort symbols by capital descending, default to 0 if not found
    sorted_symbols = sorted(symbols, key=lambda s: capital_map.get(s, 0), reverse=True)
    # Keep only top 50
    new_categories[cat] = sorted_symbols[:50]

print(f"Processed {len(new_categories)} categories. Example: {list(new_categories.keys())[0]} has {len(list(new_categories.values())[0])} symbols.")

# Inject into app.js
with open('app.js', 'r') as f:
    code = f.read()

js_dict = "const CATEGORY_MAP = " + json.dumps(new_categories, ensure_ascii=False, indent=2) + ";"

# Replace existing CATEGORY_MAP
# Assuming the existing map starts with "const CATEGORY_MAP = {" and ends before "const TW_NAMES = {"
import re
pattern = re.compile(r"const CATEGORY_MAP = \{.*?\};", re.DOTALL)
new_code = pattern.sub(js_dict, code)

if new_code == code:
    print("Warning: Could not replace CATEGORY_MAP using regex. It might be formatted differently.")
else:
    with open('app.js', 'w') as f:
        f.write(new_code)
    print("Successfully injected top 50 CATEGORY_MAP into app.js!")
