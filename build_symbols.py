import urllib.request, json, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

INDUSTRY_MAP = {
    '01': '水泥工業', '02': '食品工業', '03': '塑膠工業', '04': '紡織纖維', '05': '電機機械',
    '06': '電器電纜', '07': '化學工業', '08': '玻璃陶瓷', '09': '造紙工業', '10': '鋼鐵工業',
    '11': '橡膠工業', '12': '汽車工業', '14': '建材營造業', '15': '航運業', '16': '觀光餐旅',
    '17': '金融保險業', '18': '貿易百貨業', '20': '其他業', '21': '化學工業', '22': '生技醫療業',
    '23': '油電燃氣業', '24': '半導體業', '25': '電腦及週邊設備業', '26': '光電業', '27': '通信網路業',
    '28': '電子零組件業', '29': '電子通路業', '30': '資訊服務業', '31': '其他電子業', '32': '文化創意業',
    '33': '農業科技業', '34': '電子商務業', '35': '綠能環保', '36': '數位雲端', '37': '運動休閒',
    '38': '居家生活'
}

result = {v: [] for v in INDUSTRY_MAP.values()}

# Fetch TWSE
try:
    req = urllib.request.Request('https://openapi.twse.com.tw/v1/opendata/t187ap03_L', headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        for item in data:
            ind_code = item.get('產業別')
            if ind_code in INDUSTRY_MAP:
                result[INDUSTRY_MAP[ind_code]].append(item['公司代號'])
except Exception as e:
    print("TWSE Error:", e)

# Fetch TPEx
try:
    req = urllib.request.Request('https://openapi.tpex.org.tw/v1/opendata/t187ap03_O', headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        for item in data:
            ind_code = item.get('產業別')
            if ind_code in INDUSTRY_MAP:
                result[INDUSTRY_MAP[ind_code]].append(item['公司代號'])
except Exception as e:
    print("TPEx Error:", e)

with open('tw_symbols.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("Symbols built successfully.")
