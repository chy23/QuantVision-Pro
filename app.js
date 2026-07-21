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
    symbol: "2308",
    name: "台達電 (Delta)",
    type: "穩健成長型",
    eps: "18.5 元 (2026預估)",
    efficiency: "ROE 18% (電源龍頭)",
    valuationAnchor: "預估 P/E < 22 倍",
    sweetSpot: "407 元以下",
    logic: "AI電源與電動車雙引擎。具備高度定價權，本益比回落至歷史下緣22倍具長線投資價值。"
  },
  {
    symbol: "2881",
    name: "富邦金 (Fubon)",
    type: "金融/高配息型",
    eps: "8.5 元 (2026預估)",
    efficiency: "ROE 12% (壽險雙雄)",
    valuationAnchor: "股價淨值比 < 1.1 倍",
    sweetSpot: "75 元以下",
    logic: "金融股看淨值而非EPS。當市場恐慌導致淨值比(P/B)跌破1.1倍時，是最佳存股切入點。"
  },
  {
    symbol: "MSFT",
    name: "微軟 (Microsoft)",
    type: "美股/長青型",
    eps: "15.2 美元 (預估)",
    efficiency: "ROE 38% (軟體壟斷)",
    valuationAnchor: "預估 P/E < 30 倍",
    sweetSpot: "456 美元以下",
    logic: "高權值龍頭很難跌破25倍。大盤修正且P/E回落30倍上下時，是長線最安全的存股買點。"
  },
  {
    symbol: "NVDA",
    name: "輝達 (NVIDIA)",
    type: "美股/爆發型",
    eps: "4.25 美元 (預估)",
    efficiency: "ROE 52% (全球AI算力王)",
    valuationAnchor: "預估 P/E < 28 倍",
    sweetSpot: "119 美元以下",
    logic: "忌諱看歷史本益比。只要AI資本支出未衰退，獲利了結導致P/E壓縮至28倍即是強勢買進時機。"
  },
  {
    symbol: "AAPL",
    name: "蘋果 (Apple)",
    type: "美股/穩健型",
    eps: "7.8 美元 (預估)",
    efficiency: "ROE 150% (極高資本效率)",
    valuationAnchor: "預估 P/E < 25 倍",
    sweetSpot: "195 美元以下",
    logic: "現金流霸主，長期靠庫藏股推升EPS。本益比若跌回25倍，是長期持有的極佳時機。"
  },
  {
    symbol: "GOOGL",
    name: "谷歌 (Alphabet)",
    type: "美股/價值成長",
    eps: "8.2 美元 (預估)",
    efficiency: "ROE 29% (廣告霸主)",
    valuationAnchor: "預估 P/E < 20 倍",
    sweetSpot: "164 美元以下",
    logic: "科技巨頭中估值相對便宜。若因AI競爭擔憂導致P/E跌破20倍，市場往往過度悲觀。"
  },
  {
    symbol: "AMZN",
    name: "亞馬遜 (Amazon)",
    type: "美股/高周轉型",
    eps: "5.5 美元 (預估)",
    efficiency: "ROE 18% (雲端與電商)",
    valuationAnchor: "營運現金流倍數 < 15 倍",
    sweetSpot: "175 美元以下",
    logic: "不適合看本益比，應看營運現金流(OCF)倍數。當雲端(AWS)成長穩定，回檔即買點。"
  },
  {
    symbol: "TSLA",
    name: "特斯拉 (Tesla)",
    type: "美股/高波動型",
    eps: "3.2 美元 (預估)",
    efficiency: "ROE 15% (電動車與AI)",
    valuationAnchor: "預估 P/E < 45 倍",
    sweetSpot: "144 美元以下",
    logic: "估值受情緒影響極大。不應在利多噴出時追高，而是要在交車量不如預期的大跌時佈局。"
  },
  {
    symbol: "ASML",
    name: "艾司摩爾 (ASML)",
    type: "其他/壟斷型",
    eps: "24.5 歐元 (預估)",
    efficiency: "ROE 55% (EUV獨家)",
    valuationAnchor: "預估 P/E < 35 倍",
    sweetSpot: "850 歐元/美元以下",
    logic: "全球半導體命脈，具絕對定價權。只要半導體長線需求在，任何因地緣政治的非理性下殺皆是買點。"
  },
  {
    symbol: "7203.T",
    name: "豐田汽車 (Toyota)",
    type: "其他/價值型",
    eps: "385 日圓 (預估)",
    efficiency: "ROE 11% (全球車廠龍頭)",
    valuationAnchor: "預估 P/E < 8 倍",
    sweetSpot: "3080 日圓以下",
    logic: "傳統車廠估值偏低，日圓貶值受惠股。P/E跌破8倍且配息率達4%時，提供絕佳防禦與價值保護。"
  }
];

// Mock data structure kept as fallback, but we'll fetch from API
// 設定後端 API 網址 (指向 Render 雲端伺服器)
const API_BASE = 'https://quantvision-pro.onrender.com/api';

let cachedCoreStocks = null;
let cachedScreenedStocks = null;
let currentMarket = 'TW';

function getMarket(symbol) {
  if (symbol === 'ASML' || symbol.endsWith('.T')) {
    return 'OTHER';
  }
  return symbol.match(/^\d+/) ? 'TW' : 'US';
}

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
  if (!cachedCoreStocks) {
    container.innerHTML = '<div style="text-align: center; width: 100%; color: var(--text-secondary);">連線至伺服器讀取即時報價中...</div>';
    cachedCoreStocks = await fetchCoreStocksData();
  }
  
  const liveData = cachedCoreStocks;
  let html = '';
  
  const filteredStocks = coreStocks.filter(s => getMarket(s.symbol) === currentMarket);
  
  if (filteredStocks.length === 0) {
    container.innerHTML = '<div style="text-align: center; width: 100%; color: var(--text-secondary);">此市場目前無觀察清單。</div>';
    return;
  }
  
  filteredStocks.forEach(stock => {
    const live = liveData && liveData[stock.symbol];
    const linkURL = getMarket(stock.symbol) === 'TW' ? `https://tw.stock.yahoo.com/quote/${stock.symbol}` : `https://finance.yahoo.com/quote/${stock.symbol}`;
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
  
  if (!cachedScreenedStocks) {
    const loadingHtml = '<tr><td colspan="11" style="text-align: center; color: var(--text-secondary);">正在網路上抓取符合條件的股票... (因為需下載歷史股價，約需數秒)</td></tr>';
    shortTbody.innerHTML = loadingHtml;
    midTbody.innerHTML = loadingHtml;
    longTbody.innerHTML = loadingHtml;
    
    cachedScreenedStocks = await fetchScreenedStocks();
  }
  
  if (!cachedScreenedStocks || cachedScreenedStocks.length === 0) {
    shortTbody.innerHTML = '<tr><td colspan="11" style="text-align: center;">無法連線伺服器，請確認伺服器是否啟動。</td></tr>';
    midTbody.innerHTML = '<tr><td colspan="11" style="text-align: center;">無資料</td></tr>';
    longTbody.innerHTML = '<tr><td colspan="11" style="text-align: center;">無資料</td></tr>';
    return;
  }
  
  const filteredStocks = cachedScreenedStocks.filter(s => getMarket(s.symbol) === currentMarket);
  
  // For demo, we split the filtered stocks into the 3 tabs roughly
  const chunk = Math.ceil(filteredStocks.length / 3);
  const shortList = filteredStocks.slice(0, chunk);
  const midList = filteredStocks.slice(chunk, chunk * 2);
  const longList = filteredStocks.slice(chunk * 2);
  
  renderTableData('table-short', shortList);
  renderTableData('table-mid', midList);
  renderTableData('table-long', longList);
}

function renderTableData(dataId, data) {
  const tbody = document.getElementById(dataId);
  let html = '';
  
  data.forEach(item => {
    const linkURL = getMarket(item.symbol) === 'TW' ? `https://tw.stock.yahoo.com/quote/${item.symbol}` : `https://finance.yahoo.com/quote/${item.symbol}`;
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

  const marketBtns = document.querySelectorAll('.market-btn');
  marketBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      marketBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      
      currentMarket = btn.dataset.market;
      // Re-render data without re-fetching
      renderStockCards();
      loadRecommendations();
    });
  });

  const refreshBtn = document.getElementById('refresh-btn');
  if (refreshBtn) {
    refreshBtn.addEventListener('click', async () => {
      refreshBtn.innerHTML = '🔄 載入中...';
      refreshBtn.disabled = true;
      cachedCoreStocks = null;
      cachedScreenedStocks = null;
      await renderStockCards();
      await loadRecommendations();
      refreshBtn.innerHTML = '🔄 重新整理';
      refreshBtn.disabled = false;
    });
  }

  // Search Logic
  const searchBtn = document.getElementById('search-btn');
  const searchInput = document.getElementById('stock-search');
  const categoryFilter = document.getElementById('category-filter');
  const searchResultsSection = document.getElementById('search-results-section');
  const searchResultsContainer = document.getElementById('search-results-container');

const CATEGORY_MAP = {
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
};

  categoryFilter.addEventListener('change', async () => {
    const category = categoryFilter.value;
    if (!category) return;
    searchInput.value = '';

    searchBtn.disabled = true;
    searchBtn.innerHTML = '<span class="loading" style="display:inline-block;">🔄</span> 載入中...';
    searchResultsSection.style.display = 'block';
    searchResultsContainer.innerHTML = '<div style="color: var(--text-secondary); grid-column: 1 / -1; text-align: center;">準備分批載入全市場深度資料...</div>';
    
    try {
      const symbolsList = CATEGORY_MAP[category];
      if (!symbolsList || symbolsList.length === 0) {
        searchResultsContainer.innerHTML = '<div style="color: white; grid-column: 1/-1; text-align: center;">找不到此類別的資料。</div>';
        return;
      }
      
      searchResultsContainer.innerHTML = '';
      
      // Batch processing (Chunks of 10)
      const chunkSize = 10;
      for (let i = 0; i < symbolsList.length; i += chunkSize) {
        const chunk = symbolsList.slice(i, i + chunkSize);
        const symbolsParam = chunk.join(',');
        
        const progressId = 'progress-' + i;
        const progressDiv = document.createElement('div');
        progressDiv.id = progressId;
        progressDiv.style = "color: #93c5fd; grid-column: 1/-1; text-align: center; padding: 10px;";
        progressDiv.innerHTML = `⏳ 正在抓取第 ${i + 1} 到 ${Math.min(i + chunkSize, symbolsList.length)} 檔股票...`;
        searchResultsContainer.appendChild(progressDiv);
        
        try {
          // Calls the rich Yahoo API
          const response = await fetch(`${API_BASE}/analyze?symbols=${encodeURIComponent(symbolsParam)}`);
          if (response.ok) {
            const data = await response.json();
            
            const pDiv = document.getElementById(progressId);
            if (pDiv) pDiv.remove();
            
            data.forEach(stock => {
              const linkURL = stock.symbol.match(/^\d+/) ? `https://tw.stock.yahoo.com/quote/${stock.symbol}` : `https://finance.yahoo.com/quote/${stock.symbol}`;
              const html = `
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
                  
                  <div class="data-row"><span class="data-label">最新即時價</span><span class="data-value ${stock.change >= 0 ? 'positive' : 'negative'}">${stock.currentPrice} (${stock.changePercent}%)</span></div>
                  
                  <div class="data-row">
                    <span class="data-label">預估 EPS / 效率</span>
                    <span class="data-value">${stock.eps} / ${stock.efficiency}</span>
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
                    <strong>動態邏輯：</strong> ${stock.logic}
                  </div>
                </div>
              `;
              searchResultsContainer.insertAdjacentHTML('beforeend', html);
            });
          }
        } catch(err) {
          console.error("Batch fetch error:", err);
        }
      }
      
    } catch (err) {
      console.error(err);
      searchResultsContainer.innerHTML = '<div style="color: white; grid-column: 1/-1; text-align: center;">伺服器連線錯誤，請稍後再試。</div>';
    } finally {
      searchBtn.disabled = false;
      searchBtn.innerHTML = '🔍 分析';
      
      const doneDiv = document.createElement('div');
      doneDiv.style = "color: #4ade80; grid-column: 1/-1; text-align: center; padding: 10px; font-weight: bold;";
      doneDiv.innerHTML = `✅ 全數載入完成！`;
      searchResultsContainer.appendChild(doneDiv);
    }
  });

  if (searchBtn) {
    searchBtn.addEventListener('click', async () => {
      const symbols = searchInput.value.trim();
      if (!symbols) return;

      searchBtn.innerHTML = '🔄 分析中...';
      searchBtn.disabled = true;
      searchResultsSection.style.display = 'block';
      searchResultsContainer.innerHTML = '<div style="color: var(--text-secondary); grid-column: 1 / -1; text-align: center;">正在向雲端引擎請求動態分析，請稍候...</div>';

      try {
        const response = await fetch(`${API_BASE}/analyze?symbols=${encodeURIComponent(symbols)}`);
        const data = await response.json();
        
        if (data.length === 0) {
          searchResultsContainer.innerHTML = '<div style="color: var(--text-secondary); grid-column: 1 / -1; text-align: center;">找不到此代碼的資料。</div>';
        } else {
          let html = '';
          data.forEach(stock => {
            const linkURL = stock.symbol.match(/^\d+/) ? `https://tw.stock.yahoo.com/quote/${stock.symbol}` : `https://finance.yahoo.com/quote/${stock.symbol}`;
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
                
                <div class="data-row"><span class="data-label">最新即時價</span><span class="data-value ${stock.change >= 0 ? 'positive' : 'negative'}">${stock.currentPrice} (${stock.changePercent}%)</span></div>
                
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
                  <strong>動態邏輯：</strong> ${stock.logic}
                </div>
              </div>
            `;
          });
          searchResultsContainer.innerHTML = html;
        }
      } catch (err) {
        searchResultsContainer.innerHTML = '<div style="color: var(--danger-color); grid-column: 1 / -1; text-align: center;">伺服器連線錯誤，請稍後再試。</div>';
      }

      searchBtn.innerHTML = '🔍 分析';
      searchBtn.disabled = false;
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  renderStockCards();
  loadRecommendations();
  setupTabs();
});
