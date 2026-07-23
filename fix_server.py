import re

with open('server.py', 'r') as f:
    code = f.read()

twse_logic = """
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
"""

# Inject TWSE fundamental fetcher at the top
if "TWSE_FUNDAMENTALS =" not in code:
    code = code.replace("import yfinance as yf", "import yfinance as yf\n" + twse_logic)

# Replace the info fetching in fetch_stock_data
old_info = """                        info = ticker.info
                        pe = info.get('trailingPE', 'N/A')
                        eps = info.get('trailingEps', 'N/A')
                        roe = round(info.get('returnOnEquity', 0) * 100, 2) if info.get('returnOnEquity') else 'N/A'"""

new_info = """                        info = ticker.info
                        pe = info.get('trailingPE', 'N/A')
                        eps = info.get('trailingEps', 'N/A')
                        roe = round(info.get('returnOnEquity', 0) * 100, 2) if info.get('returnOnEquity') else 'N/A'
                        
                        # Fallback to TWSE if yfinance fails for TW stocks
                        if symbol.endswith('.TW') and (pe == 'N/A' or eps == 'N/A'):
                            code_only = symbol.replace('.TW', '')
                            twse_data = get_twse_fundamentals().get(code_only)
                            if twse_data:
                                try:
                                    pe = float(twse_data.get('PEratio', 'N/A'))
                                    # TWSE gives yield, not eps directly, but we can estimate EPS = Price / PE
                                    if pe > 0 and last_price > 0:
                                        eps = round(last_price / pe, 2)
                                except:
                                    pass"""

code = code.replace(old_info, new_info)

with open('server.py', 'w') as f:
    f.write(code)
