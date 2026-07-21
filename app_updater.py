import json

with open('tw_symbols.json', 'r') as f:
    symbols_map = json.load(f)

with open('app.js', 'r') as f:
    code = f.read()

js_dict = "const CATEGORY_MAP = " + json.dumps(symbols_map, ensure_ascii=False, indent=2) + ";"

start_marker = "  const twCategories ="
end_marker = "  if (searchBtn) {"

start_idx = code.find(start_marker)
end_idx = code.find(end_marker)

new_logic = f"""{js_dict}

  categoryFilter.addEventListener('change', async () => {{
    const category = categoryFilter.value;
    if (!category) return;
    searchInput.value = '';

    searchBtn.disabled = true;
    searchBtn.innerHTML = '<span class="loading" style="display:inline-block;">🔄</span> 載入中...';
    searchResultsSection.style.display = 'block';
    searchResultsContainer.innerHTML = '<div style="color: var(--text-secondary); grid-column: 1 / -1; text-align: center;">準備分批載入全市場深度資料...</div>';
    
    try {{
      const symbolsList = CATEGORY_MAP[category];
      if (!symbolsList || symbolsList.length === 0) {{
        searchResultsContainer.innerHTML = '<div style="color: white; grid-column: 1/-1; text-align: center;">找不到此類別的資料。</div>';
        return;
      }}
      
      searchResultsContainer.innerHTML = '';
      
      // Batch processing (Chunks of 10)
      const chunkSize = 10;
      for (let i = 0; i < symbolsList.length; i += chunkSize) {{
        const chunk = symbolsList.slice(i, i + chunkSize);
        const symbolsParam = chunk.join(',');
        
        const progressId = 'progress-' + i;
        const progressDiv = document.createElement('div');
        progressDiv.id = progressId;
        progressDiv.style = "color: #93c5fd; grid-column: 1/-1; text-align: center; padding: 10px;";
        progressDiv.innerHTML = `⏳ 正在抓取第 ${{i + 1}} 到 ${{Math.min(i + chunkSize, symbolsList.length)}} 檔股票...`;
        searchResultsContainer.appendChild(progressDiv);
        
        try {{
          // Calls the rich Yahoo API
          const response = await fetch(`${{API_BASE}}/analyze?symbols=${{encodeURIComponent(symbolsParam)}}`);
          if (response.ok) {{
            const data = await response.json();
            
            const pDiv = document.getElementById(progressId);
            if (pDiv) pDiv.remove();
            
            data.forEach(stock => {{
              const linkURL = stock.symbol.match(/^\d+/) ? `https://tw.stock.yahoo.com/quote/${{stock.symbol}}` : `https://finance.yahoo.com/quote/${{stock.symbol}}`;
              const html = `
                <div class="glass-panel stock-card fade-in">
                  <div class="stock-header">
                    <div>
                      <div class="stock-symbol"><a href="${{linkURL}}" target="_blank" style="color: inherit; text-decoration: none;">${{stock.symbol}}</a></div>
                      <div class="stock-name">${{stock.name}}</div>
                    </div>
                    <div class="text-xs px-2 py-1 rounded bg-blue-900/50 text-blue-300 border border-blue-700/50" style="font-size: 0.8rem; padding: 2px 6px; background: rgba(59,130,246,0.2); border-radius: 4px; color: #93c5fd;">
                      ${{stock.type}}
                    </div>
                  </div>
                  
                  <div class="data-row"><span class="data-label">最新即時價</span><span class="data-value ${{stock.change >= 0 ? 'positive' : 'negative'}}">${{stock.currentPrice}} (${{stock.changePercent}}%)</span></div>
                  
                  <div class="data-row">
                    <span class="data-label">預估 EPS / 效率</span>
                    <span class="data-value">${{stock.eps}} / ${{stock.efficiency}}</span>
                  </div>
                  <div class="data-row">
                    <span class="data-label">估值錨點</span>
                    <span class="data-value">${{stock.valuationAnchor}}</span>
                  </div>
                  
                  <div class="mt-2 pt-2 border-t border-gray-700/50" style="margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.1);">
                    <div class="text-sm text-gray-400">建議買入價 (甜蜜點)</div>
                    <div class="buy-price">${{stock.sweetSpot}}</div>
                  </div>
                  
                  <div class="logic-text">
                    <strong>動態邏輯：</strong> ${{stock.logic}}
                  </div>
                </div>
              `;
              searchResultsContainer.insertAdjacentHTML('beforeend', html);
            }});
          }}
        }} catch(err) {{
          console.error("Batch fetch error:", err);
        }}
      }}
      
    }} catch (err) {{
      console.error(err);
      searchResultsContainer.innerHTML = '<div style="color: white; grid-column: 1/-1; text-align: center;">伺服器連線錯誤，請稍後再試。</div>';
    }} finally {{
      searchBtn.disabled = false;
      searchBtn.innerHTML = '🔍 分析';
      
      const doneDiv = document.createElement('div');
      doneDiv.style = "color: #4ade80; grid-column: 1/-1; text-align: center; padding: 10px; font-weight: bold;";
      doneDiv.innerHTML = `✅ 全數載入完成！`;
      searchResultsContainer.appendChild(doneDiv);
    }}
  }});

"""

code = code[:start_idx] + new_logic + code[end_idx:]

with open('app.js', 'w') as f:
    f.write(code)
