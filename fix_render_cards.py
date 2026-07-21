import re

with open('app.js', 'r') as f:
    code = f.read()

start_marker = "async function renderStockCards() {"
end_marker = "async function loadRecommendations() {"

start_idx = code.find(start_marker)
end_idx = code.find(end_marker)

new_logic = """async function renderStockCards() {
  const container = document.getElementById('core-stocks-container');
  
  const filteredStocks = coreStocks.filter(s => getMarket(s.symbol) === currentMarket);
  
  if (filteredStocks.length === 0) {
    container.innerHTML = '<div style="text-align: center; width: 100%; color: var(--text-secondary);">此市場目前無觀察清單。</div>';
    return;
  }
  
  container.innerHTML = '<div style="text-align: center; width: 100%; color: var(--text-secondary);"><span class="loading" style="display:inline-block;">🔄</span> 正在連線雲端引擎獲取動態估值...</div>';
  
  try {
    const symbols = filteredStocks.map(s => s.symbol).join(',');
    const response = await fetch(`${API_BASE}/analyze?symbols=${encodeURIComponent(symbols)}`);
    if (!response.ok) throw new Error("API Request Failed");
    const dynamicDataList = await response.json();
    
    // Convert array to dictionary keyed by symbol
    const dynamicData = {};
    dynamicDataList.forEach(item => {
      // API might return '2330.TW' or '2330', so we handle both
      const cleanSym = item.symbol.replace('.TW', '');
      dynamicData[cleanSym] = item;
    });

    let html = '';
    filteredStocks.forEach(stock => {
      const live = dynamicData[stock.symbol];
      const linkURL = getMarket(stock.symbol) === 'TW' ? `https://tw.stock.yahoo.com/quote/${stock.symbol}` : `https://finance.yahoo.com/quote/${stock.symbol}`;
      
      const livePriceHTML = live 
        ? `<div class="data-row"><span class="data-label">最新即時價</span><span class="data-value ${live.change >= 0 ? 'positive' : 'negative'}"><a href="${linkURL}" target="_blank" style="color: inherit; text-decoration: none;">${live.currentPrice} (${live.changePercent}%)</a></span></div>`
        : `<div class="data-row"><span class="data-label">最新即時價</span><span class="data-value text-secondary">無法取得</span></div>`;

      // Use dynamic data if available, fallback to hardcoded
      const eps = live ? (live.eps + ' / ' + live.efficiency) : stock.eps;
      const valuationAnchor = live ? live.valuationAnchor : stock.valuationAnchor;
      const sweetSpot = live ? live.sweetSpot : stock.sweetSpot;
      const logic = live ? live.logic : stock.logic;

      html += `
        <div class="glass-panel stock-card fade-in">
          <div class="stock-header">
            <div>
              <div class="stock-symbol"><a href="${linkURL}" target="_blank" style="color: inherit; text-decoration: none;">${stock.symbol}</a></div>
              <div class="stock-name">${stock.name}</div>
            </div>
            <div class="text-xs px-2 py-1 rounded bg-blue-900/50 text-blue-300 border border-blue-700/50" style="font-size: 0.8rem; padding: 2px 6px; background: rgba(59,130,246,0.2); border-radius: 4px; color: #93c5fd;">
              ${stock.type}
            </div>
          </div>
          
          ${livePriceHTML}
          
          <div class="data-row">
            <span class="data-label">預估 EPS / 效率</span>
            <span class="data-value">${eps}</span>
          </div>
          <div class="data-row">
            <span class="data-label">估值錨點</span>
            <span class="data-value">${valuationAnchor}</span>
          </div>
          
          <div class="mt-2 pt-2 border-t border-gray-700/50" style="margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.1);">
            <div class="text-sm text-gray-400">建議買入價 (甜蜜點)</div>
            <div class="buy-price">${sweetSpot}</div>
          </div>
          
          <div class="logic-text">
            <strong>動態邏輯：</strong> ${logic}
          </div>
        </div>
      `;
    });
    
    container.innerHTML = html;
  } catch(err) {
    console.error(err);
    container.innerHTML = '<div style="text-align: center; width: 100%; color: var(--danger-color);">無法連線伺服器，請確認伺服器是否正常運作。</div>';
  }
}

"""

code = code[:start_idx] + new_logic + code[end_idx:]

with open('app.js', 'w') as f:
    f.write(code)
