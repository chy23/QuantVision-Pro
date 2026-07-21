from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf
import pandas as pd
import concurrent.futures
import requests
from bs4 import BeautifulSoup
import datetime

app = Flask(__name__)
CORS(app)

CORE_SYMBOLS = {
    "2330": "2330.TW",
    "2454": "2454.TW",
    "2317": "2317.TW",
    "2382": "2382.TW",
    "3481": "3481.TW",
    "MSFT": "MSFT",
    "NVDA": "NVDA"
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
            info = ticker.info
            result['pe'] = round(info.get('trailingPE', 0), 2) if info.get('trailingPE') else 'N/A'
            result['eps'] = round(info.get('trailingEps', 0), 2) if info.get('trailingEps') else 'N/A'
            result['roe'] = round(info.get('returnOnEquity', 0) * 100, 2) if info.get('returnOnEquity') else 'N/A'
            result['roa'] = round(info.get('returnOnAssets', 0) * 100, 2) if info.get('returnOnAssets') else 'N/A'
            
            # Fetch 60 days of history for indicators
            hist = ticker.history(period="3mo")
            macd_str, kd_str = calculate_technicals(hist)
            result['macd'] = macd_str or "N/A"
            result['kd'] = kd_str or "N/A"
            
        return result
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

@app.route('/api/core-stocks', methods=['GET'])
def get_core_stocks():
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
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
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)
