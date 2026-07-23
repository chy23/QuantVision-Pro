import re

with open('app.js', 'r') as f:
    code = f.read()

# Add market overview logic
overview_logic = """
// Load Market Overview Ticker
async function loadMarketOverview() {
  const tickerContainer = document.getElementById('market-overview-ticker');
  if (!tickerContainer) return;
  
  // ^TWII = 加權指數, TWO.TW = 櫃買指數, ^GSPC = S&P 500, ^IXIC = NASDAQ, ^DJI = Dow Jones, ^SOX = PHLX Semiconductor
  const indices = [
    { symbol: '^TWII', name: '台股加權' },
    { symbol: 'TWO.TW', name: '櫃買指數' },
    { symbol: '^GSPC', name: 'S&P 500' },
    { symbol: '^IXIC', name: 'NASDAQ' },
    { symbol: '^DJI', name: '道瓊工業' },
    { symbol: '^SOX', name: '費城半導體' }
  ];
  
  try {
    const symbolsParam = indices.map(i => i.symbol).join(',');
    const response = await fetch(`${API_BASE}/analyze?symbols=${encodeURIComponent(symbolsParam)}`);
    if (!response.ok) throw new Error("API Failed");
    const data = await response.json();
    
    let html = '';
    indices.forEach(idx => {
      // Find data for this index
      let live = data.find(d => d.symbol === idx.symbol || d.symbol === idx.symbol.replace('.TW', ''));
      if (live && live.currentPrice !== 'N/A' && live.currentPrice !== '0.0') {
        const isPos = live.change >= 0;
        const color = isPos ? 'var(--success-color)' : 'var(--danger-color)';
        const sign = isPos ? '+' : '';
        html += `
          <div style="display: inline-block; padding: 0 1rem; border-right: 1px solid rgba(255,255,255,0.1);">
            <div style="font-size: 0.9rem; color: var(--text-secondary);">${idx.name}</div>
            <div style="font-size: 1.2rem; font-weight: bold; color: ${color};">
              ${live.currentPrice} <span style="font-size: 0.9rem;">${sign}${live.change} (${sign}${live.changePercent}%)</span>
            </div>
          </div>
        `;
      }
    });
    
    if (html) {
      tickerContainer.innerHTML = html;
    } else {
      tickerContainer.innerHTML = '<div style="color: var(--text-secondary); width: 100%; text-align: center;">暫時無法取得大盤資料</div>';
    }
  } catch (err) {
    console.error("Market overview error:", err);
    tickerContainer.innerHTML = '<div style="color: var(--danger-color); width: 100%; text-align: center;">無法連線伺服器取得大盤資料</div>';
  }
}
"""

if "function loadMarketOverview" not in code:
    code = code + "\n" + overview_logic

# Call it in DOMContentLoaded
if "loadMarketOverview();" not in code:
    # Find DOMContentLoaded event listener
    # There is a block: document.addEventListener('DOMContentLoaded', () => {
    pattern = re.compile(r"document\.addEventListener\('DOMContentLoaded',\s*\(\)\s*=>\s*\{")
    code = pattern.sub("document.addEventListener('DOMContentLoaded', () => {\n  loadMarketOverview();", code)

with open('app.js', 'w') as f:
    f.write(code)
