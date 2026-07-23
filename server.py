import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf

import urllib.request, json, ssl

# Fetch TWSE fundamental data once globally and cache it
TWSE_FUNDAMENTALS = {}
def get_twse_fundamentals():
    global TWSE_FUNDAMENTALS
    if TWSE_FUNDAMENTALS:
        return TWSE_FUNDAMENTALS
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        req = urllib.request.Request('https://openapi.twse.com.tw/v1/opendata/BWIBBU_d', headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            for item in data:
                TWSE_FUNDAMENTALS[item['Code']] = item
    except Exception as e:
        print("TWSE Fundamental Error:", e)
    return TWSE_FUNDAMENTALS

import pandas as pd
import concurrent.futures
import requests
from bs4 import BeautifulSoup
import datetime
import time

app = Flask(__name__)
CORS(app)

CORE_SYMBOLS = {
    "2330": "2330.TW",
    "2454": "2454.TW",
    "2317": "2317.TW",
    "2382": "2382.TW",
    "3481": "3481.TW",
    "2308": "2308.TW",
    "2881": "2881.TW",
    "MSFT": "MSFT",
    "NVDA": "NVDA",
    "AAPL": "AAPL",
    "GOOGL": "GOOGL",
    "AMZN": "AMZN",
    "TSLA": "TSLA",
    "ASML": "ASML",
    "7203.T": "7203.T"
}

SCREEN_SYMBOLS = [
    "AAPL", "GOOGL", "AMZN", "META", "TSLA", "AMD", "QCOM", "TSM", "AVGO", "ASML",
    "2308.TW", "2881.TW", "2882.TW", "3231.TW", "2356.TW", "2603.TW", "1519.TW", "1513.TW", "2303.TW", "3034.TW"
]

SYMBOL_NAMES = {
    "AAPL": "蘋果 (Apple)",
    "GOOGL": "谷歌 (Alphabet)",
    "AMZN": "亞馬遜 (Amazon)",
    "META": "臉書 (Meta)",
    "TSLA": "特斯拉 (Tesla)",
    "AMD": "超微 (AMD)",
    "QCOM": "高通 (Qualcomm)",
    "TSM": "台積電 ADR (TSM)",
    "AVGO": "博通 (Broadcom)",
    "ASML": "艾司摩爾 (ASML)",
    "7203.T": "豐田汽車 (Toyota)",
    "2308.TW": "台達電 (Delta)",
    "2881.TW": "富邦金 (Fubon)",
    "2882.TW": "國泰金 (Cathay)",
    "3231.TW": "緯創 (Wistron)",
    "2356.TW": "英業達 (Inventec)",
    "2603.TW": "長榮 (Evergreen)",
    "1519.TW": "華城 (Fortune)",
    "1513.TW": "中興電 (CHEM)",
    "2303.TW": "聯電 (UMC)",
    "3034.TW": "聯詠 (Novatek)"
}

def calculate_technicals(df):
    if len(df) < 30:
        return None, None
    
    # MACD
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    macd_line = ema12 - ema26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    
    # KD
    low_min = df['Low'].rolling(window=9).min()
    high_max = df['High'].rolling(window=9).max()
    rsv = (df['Close'] - low_min) / (high_max - low_min) * 100
    
    # Calculate K and D using iterative method for EMA smoothing
    k = []
    d = []
    k_prev = 50
    d_prev = 50
    for r in rsv:
        if pd.isna(r):
            k.append(50)
            d.append(50)
            continue
        k_curr = (2/3) * k_prev + (1/3) * r
        d_curr = (2/3) * d_prev + (1/3) * k_curr
        k.append(k_curr)
        d.append(d_curr)
        k_prev = k_curr
        d_prev = d_curr
        
    macd_val = round(macd_line.iloc[-1], 2)
    sig_val = round(signal_line.iloc[-1], 2)
    k_val = round(k[-1], 2)
    d_val = round(d[-1], 2)
    
    return f"MACD:{macd_val}/Sig:{sig_val}", f"K:{k_val}/D:{d_val}"

def scrape_tw_stock_realtime(symbol):
    try:
        tw_symbol = symbol.replace('.TW', '')
        url = f'https://tw.stock.yahoo.com/quote/{tw_symbol}'
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.text, 'html.parser')
        
        price_span = soup.find_all('span', class_=lambda c: c and 'Fz(32px)' in c)
        if not price_span:
            return None
        price_str = price_span[0].text.replace(',', '')
        
        change_spans = soup.find_all('span', class_=lambda c: c and 'Fz(20px)' in c)
        change_str = change_spans[0].text.replace(',', '')
        pct_str = change_spans[1].text.strip('()%')
        
        # Check if it's down (Yahoo TW uses different classes for up/down, but text might not have minus)
        # We can look at the color class: C($c-trend-down)
        is_down = 'trend-down' in price_span[0].get('class', []) or 'trend-down' in change_spans[0].get('class', [])
        
        last_price = float(price_str)
        change = float(change_str)
        if is_down:
            change = -change
            pct_str = "-" + pct_str
            
        change_percent = float(pct_str)
        
        return last_price, change, change_percent
    except Exception as e:
        print(f"Scraping error for {symbol}: {e}")
        return None

DATA_CACHE = {}
CACHE_TTL = 21600  # 6 hours

def fetch_stock_data(symbol, include_history=False):
    try:
        ticker = yf.Ticker(symbol)
        
        # Default to yfinance
        data = ticker.fast_info
        last_price = data.last_price
        prev_close = data.previous_close
        change = last_price - prev_close
        change_percent = (change / prev_close) * 100 if prev_close else 0
        
        # Override with real-time scrape for TW stocks during intraday
        if symbol.endswith('.TW'):
            scraped = scrape_tw_stock_realtime(symbol)
            if scraped:
                last_price, change, change_percent = scraped
        
        result = {
            "symbol": symbol,
            "currentPrice": round(last_price, 2),
            "change": round(change, 2),
            "changePercent": round(change_percent, 2)
        }
        
        if include_history:
            now = time.time()
            if symbol in DATA_CACHE and (now - DATA_CACHE[symbol]['timestamp']) < CACHE_TTL:
                cached = DATA_CACHE[symbol]
                result['pe'] = cached['pe']
                result['eps'] = cached['eps']
                result['roe'] = cached['roe']
                result['roa'] = cached['roa']
                result['macd'] = cached['macd']
                result['kd'] = cached['kd']
            else:
                try:
                    info = ticker.info
                    result['pe'] = round(info.get('trailingPE', 0), 2) if info.get('trailingPE') else 'N/A'
                    result['eps'] = round(info.get('trailingEps', 0), 2) if info.get('trailingEps') else 'N/A'
                    result['roe'] = round(info.get('returnOnEquity', 0) * 100, 2) if info.get('returnOnEquity') else 'N/A'
                    result['roa'] = round(info.get('returnOnAssets', 0) * 100, 2) if info.get('returnOnAssets') else 'N/A'
                except Exception as e:
                    print(f"Info fetch failed for {symbol}: {e}")
                    result['pe'] = 'N/A'
                    result['eps'] = 'N/A'
                    result['roe'] = 'N/A'
                    result['roa'] = 'N/A'
                
                try:
                    # Fetch 60 days of history for indicators
                    hist = ticker.history(period="3mo")
                    macd_str, kd_str = calculate_technicals(hist)
                    result['macd'] = macd_str or "N/A"
                    result['kd'] = kd_str or "N/A"
                except Exception as e:
                    print(f"History fetch failed for {symbol}: {e}")
                    result['macd'] = "N/A"
                    result['kd'] = "N/A"
                
                # Cache if we successfully got some data
                if result['pe'] != 'N/A' or result['macd'] != 'N/A':
                    DATA_CACHE[symbol] = {
                        'timestamp': now,
                        'pe': result['pe'],
                        'eps': result['eps'],
                        'roe': result['roe'],
                        'roa': result['roa'],
                        'macd': result['macd'],
                        'kd': result['kd']
                    }
            
        return result
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

@app.route('/api/core-stocks', methods=['GET'])
def get_core_stocks():
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_symbol = {executor.submit(fetch_stock_data, yf_sym, False): orig_sym for orig_sym, yf_sym in CORE_SYMBOLS.items()}
        for future in concurrent.futures.as_completed(future_to_symbol):
            orig_sym = future_to_symbol[future]
            data = future.result()
            if data:
                results[orig_sym] = data
    return jsonify(results)

@app.route('/api/screen', methods=['GET'])
def get_screened_stocks():
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_stock_data, sym, True) for sym in SCREEN_SYMBOLS]
        for future in concurrent.futures.as_completed(futures):
            data = future.result()
            if data:
                cp = data['currentPrice']
                # Dummy valuation logics for target and stop loss based on fundamental metrics
                target = cp * 1.20
                stop_loss = cp * 0.92  # 8% stop loss
                
                results.append({
                    "symbol": data['symbol'].replace('.TW', ''),
                    "name": SYMBOL_NAMES.get(data['symbol'], data['symbol']),
                    "currentPrice": f"{cp}",
                    "targetPrice": f"{round(target, 2)}",
                    "stopLoss": f"{round(stop_loss, 2)}",
                    "pe": data['pe'],
                    "eps": data['eps'],
                    "roe": f"{data['roe']}%" if data['roe'] != 'N/A' else 'N/A',
                    "roa": f"{data['roa']}%" if data['roa'] != 'N/A' else 'N/A',
                    "kd": data['kd'],
                    "macd": data['macd'],
                    "trend": "向上" if data['changePercent'] > 0 else "盤整" if data['changePercent'] > -1 else "向下",
                    "reason": f"今日漲跌: {data['changePercent']}%"
                })
        
        # Sort based on time of day (Taiwan daytime 06:00 - 18:00)
        current_hour = datetime.datetime.now().hour
        is_daytime = 6 <= current_hour < 18
        if is_daytime:
            # Taiwan stocks first (symbol contains digits)
            results.sort(key=lambda x: 0 if any(c.isdigit() for c in x['symbol']) else 1)
        else:
            # US stocks first (symbol is letters only)
            results.sort(key=lambda x: 0 if not any(c.isdigit() for c in x['symbol']) else 1)
            
    return jsonify(results)

import urllib.request
import ssl
import json

TWSE_CACHE = {"timestamp": 0, "data": []}

@app.route('/api/tw-category', methods=['GET'])
def get_tw_category():
    category = request.args.get('category', '')
    if not category:
        return jsonify([])
    
    tw_symbols_map = {
  "水泥工業": [
    "1101",
    "1102",
    "1103",
    "1104",
    "1108",
    "1109",
    "1110"
  ],
  "食品工業": [
    "1201",
    "1203",
    "1210",
    "1213",
    "1215",
    "1216",
    "1217",
    "1218",
    "1219",
    "1220",
    "1225",
    "1227",
    "1229",
    "1231",
    "1232",
    "1233",
    "1234",
    "1235",
    "1236",
    "1256",
    "1702",
    "1737",
    "3054",
    "7780",
    "7791"
  ],
  "塑膠工業": [
    "1301",
    "1303",
    "1304",
    "1305",
    "1307",
    "1308",
    "1309",
    "1310",
    "1312",
    "1313",
    "1314",
    "1315",
    "1321",
    "1323",
    "1324",
    "1325",
    "1326",
    "1337",
    "1340",
    "1341",
    "4306"
  ],
  "紡織纖維": [
    "1402",
    "1409",
    "1410",
    "1413",
    "1414",
    "1417",
    "1418",
    "1419",
    "1423",
    "1434",
    "1440",
    "1441",
    "1444",
    "1445",
    "1446",
    "1447",
    "1449",
    "1451",
    "1452",
    "1454",
    "1455",
    "1457",
    "1459",
    "1460",
    "1463",
    "1464",
    "1465",
    "1466",
    "1467",
    "1468",
    "1470",
    "1473",
    "1474",
    "1475",
    "1476",
    "1477",
    "4414",
    "4426",
    "4438",
    "4439",
    "4440",
    "4441"
  ],
  "電機機械": [
    "1503",
    "1504",
    "1506",
    "1513",
    "1514",
    "1515",
    "1517",
    "1519",
    "1526",
    "1527",
    "1528",
    "1529",
    "1530",
    "1531",
    "1532",
    "1535",
    "1537",
    "1538",
    "1539",
    "1540",
    "1541",
    "1558",
    "1560",
    "1583",
    "1589",
    "1590",
    "1597",
    "2049",
    "2371",
    "3167",
    "4526",
    "4532",
    "4540",
    "4552",
    "4555",
    "4560",
    "4562",
    "4564",
    "4566",
    "4571",
    "4572",
    "4576",
    "4583",
    "4590",
    "5288",
    "6606",
    "7750",
    "8222",
    "8374",
    "8996"
  ],
  "電器電纜": [
    "1603",
    "1604",
    "1605",
    "1608",
    "1609",
    "1611",
    "1612",
    "1614",
    "1615",
    "1616",
    "1617",
    "1618",
    "1623",
    "1626",
    "4930",
    "5283"
  ],
  "化學工業": [
    "1708",
    "1709",
    "1710",
    "1711",
    "1712",
    "1713",
    "1714",
    "1717",
    "1718",
    "1721",
    "1722",
    "1723",
    "1725",
    "1726",
    "1727",
    "1730",
    "1732",
    "1735",
    "1773",
    "1776",
    "4720",
    "4722",
    "4739",
    "4755",
    "4763",
    "4764",
    "4766",
    "4770"
  ],
  "玻璃陶瓷": [
    "1802",
    "1806",
    "1809",
    "1810",
    "1817"
  ],
  "造紙工業": [
    "1903",
    "1904",
    "1905",
    "1906",
    "1907",
    "1909",
    "6790"
  ],
  "鋼鐵工業": [
    "2002",
    "2006",
    "2007",
    "2008",
    "2009",
    "2010",
    "2012",
    "2013",
    "2014",
    "2015",
    "2017",
    "2020",
    "2022",
    "2023",
    "2024",
    "2025",
    "2027",
    "2028",
    "2029",
    "2030",
    "2031",
    "2032",
    "2033",
    "2034",
    "2038",
    "2069",
    "2211",
    "3004",
    "5007",
    "5538",
    "9958"
  ],
  "橡膠工業": [
    "2101",
    "2102",
    "2103",
    "2104",
    "2105",
    "2106",
    "2107",
    "2108",
    "2109",
    "2114",
    "6582"
  ],
  "汽車工業": [
    "1319",
    "1338",
    "1339",
    "1512",
    "1521",
    "1522",
    "1524",
    "1525",
    "1533",
    "1536",
    "1563",
    "1568",
    "1587",
    "2115",
    "2201",
    "2204",
    "2206",
    "2207",
    "2227",
    "2228",
    "2231",
    "2233",
    "2236",
    "2239",
    "2241",
    "2243",
    "2247",
    "2248",
    "2250",
    "2254",
    "2258",
    "2497",
    "3346",
    "3717",
    "4551",
    "4557",
    "4569",
    "4581",
    "6605",
    "6988",
    "7732",
    "7736",
    "7821"
  ],
  "建材營造業": [
    "1316",
    "1436",
    "1438",
    "1439",
    "1442",
    "1453",
    "1456",
    "1472",
    "1805",
    "1808",
    "2442",
    "2501",
    "2504",
    "2505",
    "2506",
    "2509",
    "2511",
    "2515",
    "2516",
    "2520",
    "2524",
    "2527",
    "2528",
    "2530",
    "2534",
    "2535",
    "2536",
    "2537",
    "2538",
    "2539",
    "2540",
    "2542",
    "2543",
    "2545",
    "2546",
    "2547",
    "2548",
    "2597",
    "2923",
    "3052",
    "3056",
    "3266",
    "3703",
    "5515",
    "5519",
    "5521",
    "5522",
    "5525",
    "5531",
    "5533",
    "5534",
    "5546",
    "6177",
    "9906",
    "9946"
  ],
  "航運業": [
    "2208",
    "2601",
    "2603",
    "2605",
    "2606",
    "2607",
    "2608",
    "2609",
    "2610",
    "2611",
    "2612",
    "2613",
    "2615",
    "2617",
    "2618",
    "2630",
    "2633",
    "2634",
    "2636",
    "2637",
    "2642",
    "2645",
    "2646",
    "5607",
    "5608",
    "6753",
    "6757",
    "8367"
  ],
  "觀光餐旅": [
    "2701",
    "2702",
    "2704",
    "2705",
    "2706",
    "2707",
    "2712",
    "2722",
    "2723",
    "2727",
    "2731",
    "2739",
    "2748",
    "2753",
    "5706",
    "7705",
    "7760",
    "8940",
    "9943"
  ],
  "金融保險業": [
    "2801",
    "2812",
    "2816",
    "2820",
    "2832",
    "2834",
    "2836",
    "2838",
    "2845",
    "2849",
    "2850",
    "2851",
    "2852",
    "2855",
    "2867",
    "2880",
    "2881",
    "2882",
    "2883",
    "2884",
    "2885",
    "2886",
    "2887",
    "2889",
    "2890",
    "2891",
    "2892",
    "2897",
    "5876",
    "5880",
    "6005",
    "6024"
  ],
  "貿易百貨業": [
    "2901",
    "2903",
    "2905",
    "2906",
    "2908",
    "2910",
    "2911",
    "2912",
    "2913",
    "2915",
    "2929",
    "2939",
    "2945",
    "4807",
    "5906",
    "5907",
    "8429",
    "8443"
  ],
  "其他業": [
    "1342",
    "1416",
    "1435",
    "1437",
    "1443",
    "1516",
    "2348",
    "2496",
    "2514",
    "2614",
    "2904",
    "3040",
    "5284",
    "5871",
    "6184",
    "6464",
    "6504",
    "6585",
    "6592",
    "6625",
    "6655",
    "6901",
    "6914",
    "6952",
    "6957",
    "6958",
    "8033",
    "8404",
    "8411",
    "8442",
    "8463",
    "8466",
    "8481",
    "8488",
    "9902",
    "9905",
    "9907",
    "9917",
    "9919",
    "9925",
    "9927",
    "9928",
    "9929",
    "9933",
    "9938",
    "9939",
    "9940",
    "9941",
    "9942",
    "9944",
    "9945"
  ],
  "生技醫療業": [
    "1707",
    "1720",
    "1731",
    "1733",
    "1734",
    "1752",
    "1760",
    "1762",
    "1783",
    "1786",
    "1789",
    "1795",
    "3164",
    "3705",
    "3716",
    "4104",
    "4106",
    "4108",
    "4119",
    "4133",
    "4137",
    "4142",
    "4148",
    "4155",
    "4164",
    "4169",
    "4178",
    "4190",
    "4195",
    "4736",
    "4737",
    "4746",
    "4771",
    "6431",
    "6446",
    "6472",
    "6491",
    "6534",
    "6541",
    "6550",
    "6589",
    "6598",
    "6645",
    "6657",
    "6666",
    "6782",
    "6794",
    "6796",
    "6838",
    "6861",
    "6885",
    "6918",
    "6919",
    "6931",
    "6934",
    "6936",
    "6949",
    "6955",
    "7799",
    "7803",
    "7827"
  ],
  "油電燃氣業": [
    "2616",
    "6505",
    "8926",
    "9908",
    "9918",
    "9926",
    "9931",
    "9937"
  ],
  "半導體業": [
    "2302",
    "2303",
    "2329",
    "2330",
    "2337",
    "2338",
    "2340",
    "2342",
    "2344",
    "2351",
    "2363",
    "2369",
    "2379",
    "2388",
    "2401",
    "2408",
    "2434",
    "2436",
    "2441",
    "2449",
    "2451",
    "2454",
    "2458",
    "2481",
    "3006",
    "3014",
    "3016",
    "3034",
    "3035",
    "3041",
    "3094",
    "3135",
    "3150",
    "3189",
    "3257",
    "3413",
    "3443",
    "3450",
    "3530",
    "3532",
    "3545",
    "3583",
    "3588",
    "3592",
    "3661",
    "3686",
    "3711",
    "4919",
    "4952",
    "4961",
    "4967",
    "4968",
    "5222",
    "5236",
    "5269",
    "5285",
    "5471",
    "6202",
    "6239",
    "6243",
    "6257",
    "6271",
    "6415",
    "6451",
    "6515",
    "6525",
    "6526",
    "6531",
    "6533",
    "6552",
    "6573",
    "6695",
    "6719",
    "6756",
    "6770",
    "6789",
    "6799",
    "6854",
    "6909",
    "6921",
    "6937",
    "6962",
    "7730",
    "7749",
    "7768",
    "7769",
    "7822",
    "8016",
    "8028",
    "8081",
    "8110",
    "8131",
    "8150",
    "8162",
    "8261",
    "8271"
  ],
  "電腦及週邊設備業": [
    "2301",
    "2305",
    "2324",
    "2331",
    "2352",
    "2353",
    "2356",
    "2357",
    "2362",
    "2364",
    "2365",
    "2376",
    "2377",
    "2380",
    "2382",
    "2387",
    "2395",
    "2397",
    "2399",
    "2405",
    "2417",
    "2425",
    "2432",
    "2465",
    "2495",
    "3002",
    "3005",
    "3013",
    "3017",
    "3022",
    "3046",
    "3057",
    "3060",
    "3231",
    "3416",
    "3494",
    "3515",
    "3652",
    "3701",
    "3706",
    "3712",
    "4916",
    "4938",
    "5215",
    "5258",
    "6117",
    "6128",
    "6166",
    "6206",
    "6230",
    "6235",
    "6277",
    "6414",
    "6579",
    "6591",
    "6669",
    "6831",
    "6928",
    "6933",
    "7711",
    "8114",
    "8163",
    "8210",
    "9912"
  ],
  "光電業": [
    "2323",
    "2349",
    "2374",
    "2393",
    "2406",
    "2409",
    "2426",
    "2429",
    "2438",
    "2466",
    "2486",
    "2489",
    "2491",
    "3008",
    "3019",
    "3024",
    "3031",
    "3038",
    "3049",
    "3050",
    "3051",
    "3059",
    "3149",
    "3168",
    "3356",
    "3406",
    "3437",
    "3481",
    "3504",
    "3535",
    "3543",
    "3563",
    "3576",
    "3591",
    "3622",
    "3673",
    "3714",
    "4934",
    "4935",
    "4942",
    "4949",
    "4956",
    "4960",
    "4976",
    "5234",
    "5243",
    "5244",
    "5484",
    "6116",
    "6120",
    "6164",
    "6168",
    "6176",
    "6209",
    "6225",
    "6226",
    "6278",
    "6405",
    "6443",
    "6456",
    "6477",
    "6668",
    "6706",
    "6742",
    "6916",
    "8104",
    "8105",
    "8215"
  ],
  "通信網路業": [
    "2314",
    "2321",
    "2332",
    "2345",
    "2412",
    "2419",
    "2424",
    "2439",
    "2444",
    "2450",
    "2455",
    "2485",
    "2498",
    "3025",
    "3027",
    "3045",
    "3047",
    "3062",
    "3138",
    "3311",
    "3380",
    "3419",
    "3447",
    "3596",
    "3669",
    "3694",
    "3704",
    "4904",
    "4906",
    "4977",
    "5388",
    "6136",
    "6142",
    "6152",
    "6216",
    "6285",
    "6416",
    "6426",
    "6442",
    "6674",
    "6792",
    "6863",
    "8011",
    "8045",
    "8101"
  ],
  "電子零組件業": [
    "1471",
    "1582",
    "2059",
    "2308",
    "2313",
    "2316",
    "2327",
    "2328",
    "2355",
    "2367",
    "2368",
    "2375",
    "2383",
    "2385",
    "2392",
    "2402",
    "2413",
    "2415",
    "2420",
    "2421",
    "2428",
    "2431",
    "2440",
    "2457",
    "2460",
    "2462",
    "2467",
    "2472",
    "2476",
    "2478",
    "2483",
    "2484",
    "2492",
    "2493",
    "3003",
    "3011",
    "3015",
    "3021",
    "3023",
    "3026",
    "3032",
    "3037",
    "3042",
    "3044",
    "3058",
    "3090",
    "3092",
    "3229",
    "3296",
    "3308",
    "3321",
    "3338",
    "3376",
    "3432",
    "3501",
    "3533",
    "3550",
    "3593",
    "3605",
    "3607",
    "3645",
    "3653",
    "3679",
    "3715",
    "4545",
    "4912",
    "4915",
    "4927",
    "4943",
    "4958",
    "4989",
    "4999",
    "5469",
    "6108",
    "6115",
    "6133",
    "6141",
    "6153",
    "6155",
    "6191",
    "6197",
    "6205",
    "6213",
    "6224",
    "6269",
    "6272",
    "6282",
    "6412",
    "6449",
    "6672",
    "6715",
    "6781",
    "6805",
    "6834",
    "6835",
    "6862",
    "6924",
    "7788",
    "7795",
    "8039",
    "8046",
    "8103",
    "8213",
    "8249"
  ],
  "電子通路業": [
    "2347",
    "2414",
    "2430",
    "3010",
    "3028",
    "3033",
    "3036",
    "3048",
    "3055",
    "3209",
    "3312",
    "3528",
    "3702",
    "5434",
    "6189",
    "6281",
    "6776",
    "6908",
    "8070",
    "8072",
    "8112"
  ],
  "資訊服務業": [
    "2427",
    "2453",
    "2468",
    "2471",
    "2480",
    "3029",
    "4994",
    "5203",
    "6112",
    "6183",
    "6214"
  ],
  "其他電子業": [
    "2312",
    "2317",
    "2354",
    "2359",
    "2360",
    "2373",
    "2390",
    "2404",
    "2423",
    "2433",
    "2459",
    "2461",
    "2464",
    "2474",
    "2477",
    "2482",
    "2488",
    "3018",
    "3030",
    "3043",
    "3305",
    "3518",
    "3617",
    "3665",
    "4585",
    "4588",
    "5225",
    "6139",
    "6192",
    "6196",
    "6201",
    "6215",
    "6283",
    "6409",
    "6438",
    "6558",
    "6658",
    "6691",
    "6698",
    "6722",
    "6743",
    "6830",
    "7631",
    "8021",
    "8201",
    "8499"
  ],
  "文化創意業": [],
  "農業科技業": [],
  "電子商務業": [],
  "綠能環保": [
    "2072",
    "3708",
    "4582",
    "5292",
    "6581",
    "6641",
    "6771",
    "6869",
    "6873",
    "6887",
    "6923",
    "6944",
    "6951",
    "6969",
    "6994",
    "7610",
    "7740",
    "7786",
    "7818",
    "8341",
    "8422",
    "8438",
    "8473",
    "8476",
    "9930",
    "9955"
  ],
  "數位雲端": [
    "3130",
    "6165",
    "6614",
    "6689",
    "6902",
    "6906",
    "7721",
    "7722",
    "7765",
    "7823",
    "8454",
    "8487"
  ],
  "運動休閒": [
    "1432",
    "1598",
    "1736",
    "2762",
    "4536",
    "5306",
    "6670",
    "6768",
    "6890",
    "6965",
    "8462",
    "8467",
    "8478",
    "9802",
    "9904",
    "9910",
    "9914",
    "9921"
  ],
  "居家生活": [
    "2062",
    "3557",
    "6671",
    "6754",
    "6807",
    "8464",
    "8482",
    "9911",
    "9924",
    "9934",
    "9935"
  ]
}
        
    symbols_in_category = tw_symbols_map.get(category, [])
    if not symbols_in_category:
        return jsonify([])
        
    # Fetch TWSE BWIBBU_d
    global TWSE_CACHE
    now = time.time()
    if now - TWSE_CACHE['timestamp'] > 3600 or not TWSE_CACHE['data']:
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            req = urllib.request.Request('https://openapi.twse.com.tw/v1/exchangeReport/BWIBBU_d', headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, context=ctx) as resp:
                TWSE_CACHE['data'] = json.loads(resp.read().decode('utf-8'))
                TWSE_CACHE['timestamp'] = now
        except Exception as e:
            print("Failed to fetch TWSE BWIBBU_d:", e)
            
    # Filter
    results = []
    symbol_set = set(symbols_in_category)
    
    for item in TWSE_CACHE['data']:
        if item.get('Code') in symbol_set:
            cp_str = item.get('ClosePrice', '0').replace(',', '')
            pe_str = item.get('PEratio', '0')
            yield_str = item.get('DividendYield', '0')
            
            try:
                cp = float(cp_str) if cp_str else 0
            except:
                cp = 0
            
            try:
                pe = float(pe_str) if pe_str else 0
            except:
                pe = 0
                
            if pe > 0:
                sweet_spot = cp * 0.9
                anchor = f"預估 P/E < {round(pe * 0.9, 1)} 倍"
                if pe > 40:
                    logic = f"目前本益比偏高 ({pe}倍)，建議等回檔至 {round(sweet_spot, 2)} 以下。"
                elif pe < 15:
                    logic = f"目前本益比偏低 ({pe}倍)，具備價值投資潛力。"
                else:
                    logic = f"本益比 {pe} 倍位於合理區間。建議在 {round(sweet_spot, 2)} 附近分批佈局。"
            else:
                sweet_spot = cp * 0.95
                anchor = "技術面支撐"
                logic = f"暫無本益比資訊，以技術面作為進出依據。"

            results.append({
                "symbol": item.get('Code'),
                "name": item.get('Name'),
                "type": f"{category}成分股",
                "eps": "N/A",
                "efficiency": f"殖利率 {yield_str}%",
                "valuationAnchor": anchor,
                "sweetSpot": f"{round(sweet_spot, 2)} 以下",
                "logic": logic,
                "currentPrice": f"{cp}",
                "change": 0,
                "changePercent": 0
            })
            
    return jsonify(results)

@app.route('/api/analyze', methods=['GET'])
def analyze_stocks():
    symbols = request.args.get('symbols', '')
    if not symbols:
        return jsonify([])
        
    symbol_list = [s.strip().upper() for s in symbols.split(',') if s.strip()]
    for i in range(len(symbol_list)):
        if symbol_list[i].isdigit():
            symbol_list[i] = f"{symbol_list[i]}.TW"
            
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_stock_data, sym, True) for sym in symbol_list]
        for future in concurrent.futures.as_completed(futures):
            data = future.result()
            if data:
                cp = data['currentPrice']
                pe = data['pe']
                
                if isinstance(pe, (int, float)) and pe > 0:
                    target = cp * 1.15
                    sweet_spot = cp * 0.9
                    anchor = f"預估 P/E < {round(pe * 0.9, 1)} 倍"
                    
                    if pe > 40:
                        logic = f"目前本益比偏高 ({pe}倍)，建議等回檔至 {round(sweet_spot, 2)} 以下再介入，風險較低。"
                    elif pe < 15:
                        logic = f"目前本益比偏低 ({pe}倍)，具備價值投資潛力。若基本面無惡化，低於 {round(sweet_spot, 2)} 是不錯的買點。"
                    else:
                        logic = f"本益比 {pe} 倍位於合理區間。可觀察均線支撐，建議在 {round(sweet_spot, 2)} 附近分批佈局。"
                else:
                    sweet_spot = cp * 0.95
                    anchor = "技術面支撐"
                    logic = f"暫無有效本益比資訊。建議以技術面(MACD/KD)作為進出依據，停損設 {round(sweet_spot, 2)}。"

                results.append({
                    "symbol": data['symbol'].replace('.TW', ''),
                    "name": SYMBOL_NAMES.get(data['symbol'], data['symbol']),
                    "type": "動態分析標的",
                    "eps": f"{data['eps']}",
                    "efficiency": f"ROE {data['roe']}%" if data['roe'] != 'N/A' else "N/A",
                    "valuationAnchor": anchor,
                    "sweetSpot": f"{round(sweet_spot, 2)} 以下",
                    "logic": logic,
                    "currentPrice": f"{cp}",
                    "change": data['change'],
                    "changePercent": data['changePercent']
                })
                
    return jsonify(results)


import xml.etree.ElementTree as ET

@app.route('/api/macro-news', methods=['GET'])
def get_macro_news():
    news_feeds = {
        "americas": "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=en-US&gl=US&ceid=US:en",
        "asia": "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=zh-TW&gl=TW&ceid=TW:zh-Hant",
        "events": "https://news.google.com/rss/search?q=Economy+Events+OR+Federal+Reserve&hl=en-US&gl=US&ceid=US:en"
    }
    
    results = {}
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    for category, url in news_feeds.items():
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, context=ctx, timeout=5) as resp:
                xml_data = resp.read()
                root = ET.fromstring(xml_data)
                items = []
                for item in root.findall('./channel/item')[:5]: # Top 5 news
                    title = item.find('title').text if item.find('title') is not None else ''
                    link = item.find('link').text if item.find('link') is not None else ''
                    pubDate = item.find('pubDate').text if item.find('pubDate') is not None else ''
                    items.append({"title": title, "link": link, "date": pubDate})
                results[category] = items
        except Exception as e:
            print(f"Error fetching {category} news: {e}")
            results[category] = []
            
    return jsonify(results)

@app.route('/api/macro-data', methods=['GET'])
def get_macro_data():
    try:
        with open('macro_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
