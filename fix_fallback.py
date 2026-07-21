import re

with open('app.js', 'r') as f:
    code = f.read()

# Replace the assignment block in app.js
old_block = """      // Use dynamic data if available, fallback to hardcoded
      const eps = live ? (live.eps + ' / ' + live.efficiency) : stock.eps;
      const valuationAnchor = live ? live.valuationAnchor : stock.valuationAnchor;
      const sweetSpot = live ? live.sweetSpot : stock.sweetSpot;
      const logic = live ? live.logic : stock.logic;"""

new_block = """      // Use dynamic data ONLY if yfinance successfully fetched PE/EPS. Otherwise, fallback to curated text.
      const hasValidData = live && live.eps !== 'N/A' && live.eps !== undefined;
      const eps = hasValidData ? (live.eps + ' / ' + live.efficiency) : stock.eps;
      const valuationAnchor = hasValidData ? live.valuationAnchor : stock.valuationAnchor;
      
      // Keep the handwritten logic text if dynamic fetch fails, but calculate sweet spot using current price if possible
      let sweetSpot = stock.sweetSpot;
      let logic = stock.logic;
      
      if (hasValidData) {
        sweetSpot = live.sweetSpot;
        logic = live.logic;
      } else if (live && live.currentPrice !== 'N/A') {
        // If we only have price, at least make the sweet spot somewhat dynamic (e.g., 5% below current price for safety)
        // Or better yet, just use the curated sweet spot and logic because the user wrote them!
        sweetSpot = stock.sweetSpot;
        logic = stock.logic;
      }"""

code = code.replace(old_block, new_block)

with open('app.js', 'w') as f:
    f.write(code)
