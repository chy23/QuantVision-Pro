import urllib.request, json, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

names = {}

# Fetch TWSE
try:
    req = urllib.request.Request('https://openapi.twse.com.tw/v1/opendata/t187ap03_L', headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        for item in data:
            names[item['公司代號']] = item['公司簡稱']
except Exception as e:
    print("TWSE Error:", e)

with open('tw_names.json', 'w', encoding='utf-8') as f:
    json.dump(names, f, ensure_ascii=False, indent=2)

print("Names saved successfully.")
