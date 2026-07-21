const coreStocks = [
  {
    symbol: "2330",
    name: "台積電 (TSMC)",
    type: "高成長型",
    eps: "105 元 (2026預估)",
    efficiency: "ROE 36% (極高/無負債)",
    valuationAnchor: "預估 P/E < 22 倍",
    sweetSpot: "2,310 元以下",
    logic: "長期高賺錢效率、常因政治恐慌被打折。ROE維持30%以上，本益比回落22倍即黃金買點。"
  },
  {
    symbol: "2454",
    name: "聯發科 (MediaTek)",
    type: "輕資產/爆發型",
    eps: "66.55 元 (2026預估)",
    efficiency: "ROE 28% (輕資產回報)",
    valuationAnchor: "預估 P/E < 25 倍",
    sweetSpot: "1,663 元以下",
    logic: "IC設計景氣好轉本益比可上修30倍。庫存去化且動能轉強，回拉至25倍時適合分批買進爆發空間。"
  },
  {
    symbol: "2317",
    name: "鴻海 (Hon Hai)",
    type: "重資產/高槓桿型",
    eps: "17.68 元 (2026預估)",
    efficiency: "ROE 14% (高財務槓桿)",
    valuationAnchor: "預估 P/E < 13 倍",
    sweetSpot: "230 元以下",
    logic: "AI伺服器機櫃放量獲得重新估值。三率走升且回檔至13倍時，兼具價值與成長。"
  },
  {
    symbol: "2382",
    name: "廣達 (Quanta)",
    type: "高週轉/重資產型",
    eps: "23.82 元 (2026預估)",
    efficiency: "ROE 20% (高週轉效率)",
    valuationAnchor: "預估 P/E < 14 倍",
    sweetSpot: "333 元以下",
    logic: "伺服器組裝本益比介於代工與品牌間。短期遞延引發回檔時，只要大方向不變，14倍即是良機。"
  },
  {
    symbol: "3481",
    name: "群創 (Innolux)",
    type: "強景氣循環型",
    eps: "景氣低谷經常為負數",
    efficiency: "景氣波動大（看淨值）",
    valuationAnchor: "股價淨值比 < 0.7 倍",
    sweetSpot: "17.8 元以下",
    logic: "不能等EPS變好才買。要在EPS虧損、利空不跌，且股價遠低於淨值(P/B<0.7)的絕望期買進。"
  },
  {
    symbol: "MSFT",
    name: "微軟 (Microsoft)",
    type: "美股/長青型",
    eps: "15.2 美元 (近四季預估)",
    efficiency: "ROE 38% (軟體壟斷)",
    valuationAnchor: "預估 P/E < 30 倍",
    sweetSpot: "456 美元以下",
    logic: "高權值龍頭很難跌破25倍。大盤修正且P/E回落30倍上下時，是長線最安全的存股買點。"
  },
  {
    symbol: "NVDA",
    name: "輝達 (NVIDIA)",
    type: "美股/爆發型",
    eps: "4.25 美元 (26/27預估)",
    efficiency: "ROE 52% (全球AI算力王)",
    valuationAnchor: "預估 P/E < 28 倍",
    sweetSpot: "119 美元以下",
    logic: "忌諱看歷史本益比。只要AI資本支出未衰退，獲利了結導致P/E壓縮至28倍即是強勢買進時機。"
  }
];

// Mock data structure kept as fallback, but we'll fetch from API
const hostname = window.location.hostname || '127.0.0.1';
const API_BASE = `http://${hostname}:5001/api`;

async function fetchCoreStocksData() {
  try {
    const response = await fetch(`${API_BASE}/core-stocks`, { cache: 'no-store' });
    return await response.json();
  } catch (e) {
    console.error("Failed to fetch core stocks:", e);
    return null;
  }
}

async function fetchScreenedStocks() {
  try {
    const response = await fetch(`${API_BASE}/screen`, { cache: 'no-store' });
    return await response.json();
  } catch (e) {
    console.error("Failed to fetch screened stocks:", e);
    return [];
  }
}

async function renderStockCards() {
  const container = document.getElementById('core-stocks-container');
  container.innerHTML = '<div style="text-align: center; width: 100%; color: var(--text-secondary);">連線至伺服器讀取即時報價中...</div>';
  
  const liveData = await fetchCoreStocksData();
  
  let html = '';
  
  coreStocks.forEach(stock => {
    const live = liveData && liveData[stock.symbol];
    const linkURL = stock.symbol.match(/^\d+$/) ? `https://tw.stock.yahoo.com/quote/${stock.symbol}` : `https://finance.yahoo.com/quote/${stock.symbol}`;
    const livePriceHTML = live 
      ? `<div class="data-row"><span class="data-label">最新即時價</span><span class="data-value ${live.change >= 0 ? 'positive' : 'negative'}"><a href="${linkURL}" target="_blank" style="color: inherit; text-decoration: none;">${live.currentPrice} (${live.changePercent}%)</a></span></div>`
      : `<div class="data-row"><span class="data-label">最新即時價</span><span class="data-value text-secondary">無法取得</span></div>`;

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
          <span class="data-label">預估 EPS</span>
          <span class="data-value">${stock.eps}</span>
        </div>
        <div class="data-row">
          <span class="data-label">估值錨點</span>
          <span class="data-value">${stock.valuationAnchor}</span>
        </div>
        
        <div class="mt-2 pt-2 border-t border-gray-700/50" style="margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.1);">
          <div class="text-sm text-gray-400">建議買入價 (甜蜜點)</div>
          <div class="buy-price">${stock.sweetSpot}</div>
        </div>
        
        <div class="logic-text">
          <strong>指標邏輯：</strong> ${stock.logic}
        </div>
      </div>
    `;
  });
  
  container.innerHTML = html;
}

async function loadRecommendations() {
  const shortTbody = document.getElementById('table-short');
  const midTbody = document.getElementById('table-mid');
  const longTbody = document.getElementById('table-long');
  
  const loadingHtml = '<tr><td colspan="11" style="text-align: center; color: var(--text-secondary);">正在網路上抓取符合條件的 20 支股票... (因為需下載歷史股價，約需數秒)</td></tr>';
  shortTbody.innerHTML = loadingHtml;
  midTbody.innerHTML = loadingHtml;
  longTbody.innerHTML = loadingHtml;
  
  const screenedStocks = await fetchScreenedStocks();
  
  if (screenedStocks.length === 0) {
    shortTbody.innerHTML = '<tr><td colspan="6" style="text-align: center;">無法連線伺服器，請確認 python server.py 是否啟動。</td></tr>';
    return;
  }
  
  // For demo, we split the 20 stocks into the 3 tabs roughly
  const shortList = screenedStocks.slice(0, 7);
  const midList = screenedStocks.slice(7, 14);
  const longList = screenedStocks.slice(14, 20);
  
  renderTableData('table-short', shortList);
  renderTableData('table-mid', midList);
  renderTableData('table-long', longList);
}

function renderTableData(dataId, data) {
  const tbody = document.getElementById(dataId);
  let html = '';
  
  data.forEach(item => {
    const linkURL = item.symbol.match(/^\d+$/) ? `https://tw.stock.yahoo.com/quote/${item.symbol}` : `https://finance.yahoo.com/quote/${item.symbol}`;
    html += `
      <tr>
        <td><strong><a href="${linkURL}" target="_blank" style="color: inherit; text-decoration: underline;">${item.symbol}</a></strong><br/><span style="font-size: 0.85rem; color: var(--text-secondary);">${item.name}</span></td>
        <td><a href="${linkURL}" target="_blank" style="color: inherit; text-decoration: none;">${item.currentPrice}</a></td>
        <td class="positive" style="font-weight: 600;">${item.targetPrice}</td>
        <td class="negative" style="font-weight: 600;">${item.stopLoss}</td>
        <td style="color: ${item.pe !== 'N/A' && item.pe < 20 ? 'var(--success-color)' : 'inherit'};">${item.pe}</td>
        <td>${item.eps}</td>
        <td style="color: ${item.roe !== 'N/A' && parseFloat(item.roe) > 15 ? 'var(--success-color)' : 'inherit'};">${item.roe}</td>
        <td>${item.roa}</td>
        <td>${item.kd}</td>
        <td>${item.macd}</td>
        <td style="font-size: 0.85rem; color: var(--text-secondary);">${item.reason}</td>
      </tr>
    `;
  });
  
  tbody.innerHTML = html;
}

function setupTabs() {
  const tabs = document.querySelectorAll('.tab-btn');
  const contents = document.querySelectorAll('.tab-content');
  
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      // Remove active class from all tabs and contents
      tabs.forEach(t => t.classList.remove('active'));
      contents.forEach(c => c.classList.remove('active'));
      
      // Add active class to clicked tab and corresponding content
      tab.classList.add('active');
      document.getElementById(`content-${tab.dataset.target}`).classList.add('active');
    });
  });
}

document.addEventListener('DOMContentLoaded', () => {
  renderStockCards();
  loadRecommendations();
  setupTabs();
});
