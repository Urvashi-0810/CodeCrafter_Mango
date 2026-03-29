# tools/adk_tools.py

import json
import re
from typing import Dict, Any, List
from datetime import datetime

# Import existing tool classes
from tools.analysis_tools import AnalysisTools
from tools.market_tools import MarketDataTools
from tools.portfolio_tools import PortfolioParsingTools
from tools.simulation_tools import SimulationTools


def _normalize_portfolio_payload(portfolio: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize common wrapper formats to the canonical portfolio schema."""
    if not isinstance(portfolio, dict):
        return {}
    if isinstance(portfolio.get("data"), dict):
        return portfolio["data"]
    if isinstance(portfolio.get("portfolio"), dict):
        return portfolio["portfolio"]
    if isinstance(portfolio.get("holdings"), list) and "stocks" not in portfolio:
        normalized = dict(portfolio)
        normalized["stocks"] = portfolio.get("holdings", [])
        return normalized
    return portfolio


# ========== Analysis Functions ==========
def calculate_portfolio_metrics(portfolio: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate key portfolio metrics."""
    portfolio = _normalize_portfolio_payload(portfolio)
    return {
        "total_investment":    AnalysisTools.calculate_total_investment(portfolio),
        "current_value":       AnalysisTools.calculate_current_value(portfolio),
        "profit_loss":         AnalysisTools.calculate_profit_loss(portfolio),
        "sector_allocation":   AnalysisTools.calculate_sector_allocation(portfolio),
        "asset_allocation":    AnalysisTools.calculate_asset_allocation(portfolio),
        "risk_score":          AnalysisTools.calculate_risk_score(portfolio),
        "diversification_score": AnalysisTools.calculate_diversification_score(portfolio),
        "concentration_risk":  AnalysisTools.calculate_concentration_risk(portfolio),
        "health_score":        AnalysisTools.calculate_portfolio_health_score(portfolio)
    }

def generate_analysis_report(portfolio: Dict[str, Any]) -> Dict[str, Any]:
    """Generate comprehensive analysis report."""
    portfolio = _normalize_portfolio_payload(portfolio)
    return AnalysisTools.generate_analysis_report(portfolio)


# ========== Market Functions ==========
def fetch_complete_market_data(symbol: str) -> Dict[str, Any]:
    """Fetch stock data, news, sentiment, and analyst ratings."""
    market_tools = MarketDataTools()
    print(f"[MARKET] Fetching complete market data for {symbol}...")
    result = {
        "symbol":          symbol,
        "stock_data":      market_tools.scrape_stock_data(symbol),
        "news":            market_tools.fetch_company_news(symbol),
        "sentiment":       market_tools.get_market_sentiment(symbol),
        "analyst_ratings": market_tools.fetch_analyst_ratings(symbol)
    }
    print(f"[MARKET] Complete market data fetch finished for {symbol}")
    return result

def force_market_analysis(symbol: str) -> Dict[str, Any]:
    """
    FORCE market analysis execution - bypasses LLM decision-making.
    Runs scrape_stock_data, fetch_company_news, and fetch_analyst_ratings
    in PARALLEL via fetch_all_parallel() instead of sequentially.
    """
    import time
    t_total = time.perf_counter()

    print(f"\n[FORCE-ANALYSIS] Starting forced market analysis for: {symbol}\n")

    market_tools = MarketDataTools()

    if not symbol or not isinstance(symbol, str) or len(symbol.strip()) == 0:
        print(f"[FORCE-ANALYSIS] Invalid symbol: {symbol}")
        return {"error": "Invalid stock symbol", "symbol": symbol}

    symbol = symbol.upper().strip()
    print(f"[FORCE-ANALYSIS] Symbol after normalization: {symbol}")

    from tools.market_tools import SYMBOL_MAP
    if symbol not in SYMBOL_MAP:
        print(f"[FORCE-ANALYSIS] Symbol {symbol} not in SYMBOL_MAP")
        print(f"[FORCE-ANALYSIS] Available symbols: {list(SYMBOL_MAP.keys())}")
        return {
            "error":             f"Symbol '{symbol}' not supported",
            "symbol":            symbol,
            "available_symbols": list(SYMBOL_MAP.keys()),
        }

    print(f"[FORCE-ANALYSIS] Symbol validation passed")

    # ── Step 1–3: All requests fired in parallel ─────────────────────────────
    print(f"\n[TIMING] ── Step 1-3 (parallel) start ──")
    t1       = time.perf_counter()
    parallel = market_tools.fetch_all_parallel(symbol)
    print(f"[TIMING] ── Step 1-3 (parallel) done  → {(time.perf_counter()-t1)*1000:.0f} ms ──\n")

    stock_data      = parallel["stock_data"]
    news            = parallel["news"]
    analyst_ratings = parallel["analyst_ratings"]

    # ── Step 4: Sentiment (no network call, instant) ─────────────────────────
    print(f"[TIMING] ── Step 4 (sentiment) start ──")
    t4        = time.perf_counter()
    sentiment = market_tools.get_market_sentiment(symbol)
    print(f"[TIMING] ── Step 4 (sentiment) done  → {(time.perf_counter()-t4)*1000:.0f} ms ──\n")

    # ── Log individual results ───────────────────────────────────────────────
    if stock_data.get("success"):
        print(f"[FORCE-ANALYSIS] stock_data preview:\n{stock_data}\n")
    else:
        print(f"[FORCE-ANALYSIS] stock_data ERROR: {stock_data.get('error')}")

    if news.get("success"):
        print(f"[FORCE-ANALYSIS] news preview:\n{news.get('news', '')[:300]}\n")
    else:
        print(f"[FORCE-ANALYSIS] news ERROR: {news.get('error')}")

    if analyst_ratings.get("success"):
        print(f"[FORCE-ANALYSIS] ratings preview:\n{analyst_ratings.get('ratings', '')[:300]}\n")
    else:
        print(f"[FORCE-ANALYSIS] ratings ERROR: {analyst_ratings.get('error')}")

    # stock_data["data"] is a dict (NSE JSON) or a string (MC markdown fallback).
    # Safely serialise either.
    _raw_data = stock_data.get("data", {})
    stock_preview = (
        json.dumps(_raw_data, indent=2)
        if isinstance(_raw_data, dict)
        else str(_raw_data)
    )[:1000]

    news_preview = str(news.get("news", ""))[:1000]

    # ── Build report ─────────────────────────────────────────────────────────
    report_text = f"""
================================================================================
                    MARKET ANALYSIS REPORT FOR {symbol}
================================================================================
Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Fetch mode: PARALLEL (NSE API primary, Firecrawl fallback)
Price source: {parallel.get('price_source', 'N/A')}
Wall-clock: {parallel.get('elapsed_ms', 'N/A')} ms

--------------------------------------------------------------------------------
1. STOCK PRICE & TECHNICAL DATA
--------------------------------------------------------------------------------
Status : {"✅ SUCCESS" if stock_data.get('success') else "❌ FAILED"}
Source : {stock_data.get('source', 'N/A')}
URL    : {stock_data.get('url', 'N/A')}
Time   : {stock_data.get('elapsed_ms', 'N/A')} ms

Data Preview:
{stock_preview}

--------------------------------------------------------------------------------
2. COMPANY NEWS
--------------------------------------------------------------------------------
Status : {"✅ SUCCESS" if news.get('success') else "❌ FAILED"}
Source : Economic Times
Time   : {news.get('elapsed_ms', 'N/A')} ms

News Content:
{news_preview}

--------------------------------------------------------------------------------
3. MARKET SENTIMENT
--------------------------------------------------------------------------------
Sentiment Analysis:
{json.dumps(sentiment, indent=2)}

--------------------------------------------------------------------------------
4. ANALYST RATINGS
--------------------------------------------------------------------------------
Status : {"✅ SUCCESS" if analyst_ratings.get('success') else "❌ FAILED"}
Source : Screener
Time   : {analyst_ratings.get('elapsed_ms', 'N/A')} ms

Ratings Content:
{analyst_ratings.get('ratings', 'No ratings available')[:1000]}

================================================================================
END OF REPORT
================================================================================
"""

    total_elapsed = (time.perf_counter() - t_total) * 1000
    print(f"[TIMING] ── force_market_analysis TOTAL → {total_elapsed:.0f} ms ──\n")

    result = {
        "success":       True,
        "symbol":        symbol,
        "analysis_type": "forced_market_analysis",
        "report":        report_text,
        "raw_data": {
            "stock_data":      stock_data,
            "news":            news,
            "sentiment":       sentiment,
            "analyst_ratings": analyst_ratings,
        },
        "timing": {
            "parallel_ms": parallel.get("elapsed_ms"),
            "total_ms":    round(total_elapsed, 1),
        },
        "timestamp": datetime.now().isoformat(),
    }

    print(f"[FORCE-ANALYSIS] Analysis complete for {symbol}")
    print(f"[FORCE-ANALYSIS] Result keys: {list(result.keys())}")
    print(f"[FORCE-ANALYSIS] ====== END FORCED ANALYSIS ======\n")

    return result


# ========== Portfolio Functions ==========
def parse_portfolio_from_csv(file_path: str) -> Dict[str, Any]:
    """Parse portfolio from CSV file."""
    return PortfolioParsingTools.parse_csv(file_path)

def classify_holdings(holdings: List[str]) -> Dict[str, str]:
    """Classify stock symbols into sectors."""
    return PortfolioParsingTools.classify_sectors(holdings)


# ========== Simulation Functions ==========
def simulate_returns(portfolio: Dict[str, Any], years: int = 5, annual_return: float = 12.0) -> Dict[str, Any]:
    """Simulate portfolio returns over given years."""
    portfolio = _normalize_portfolio_payload(portfolio)
    return SimulationTools.simulate_returns(portfolio, years, annual_return)

def add_stock_to_portfolio(portfolio: Dict[str, Any], symbol: str, quantity: int,
                           buy_price: float, current_price: float, sector: str) -> Dict[str, Any]:
    """Add a stock to the portfolio (simulation)."""
    return SimulationTools.add_stock(portfolio, symbol, quantity, buy_price, current_price, sector)


# ========== Sector Lookup (dynamic via yfinance) ==========

_sector_cache: Dict[str, str] = {}

_SECTOR_FALLBACK = {
    "SETFGOLD":   "Gold",
    "GOLDBEES":   "Gold",
    "NIFTYBEES":  "Index ETF",
    "JUNIORBEES": "Index ETF",
    "LIQUIDBEES": "Liquid ETF",
}

_SECTOR_NORMALIZE = {
    "Financial Services":     "Banking",
    "Technology":             "IT",
    "Consumer Defensive":     "FMCG",
    "Basic Materials":        "Metals",
    "Consumer Cyclical":      "Automobile",
    "Healthcare":             "Pharma",
    "Communication Services": "Telecom",
    "Energy":                 "Energy",
    "Real Estate":            "Real Estate",
    "Industrials":            "Industrials",
    "Utilities":              "Utilities",
}

def _get_sector_for_symbol(symbol: str) -> str:
    """
    Fetch sector for a stock symbol using yfinance.
    Uses module-level cache to avoid repeated API calls.
    Falls back to _SECTOR_FALLBACK for ETFs yfinance can't resolve.
    """
    import yfinance as yf

    if symbol in _SECTOR_FALLBACK:
        return _SECTOR_FALLBACK[symbol]

    if symbol in _sector_cache:
        return _sector_cache[symbol]

    try:
        ticker = yf.Ticker(symbol + ".NS")
        info   = ticker.info
        sector = info.get("sector") or info.get("industry") or "Unknown"
        sector = _SECTOR_NORMALIZE.get(sector, sector)
    except Exception:
        sector = "Unknown"

    _sector_cache[symbol] = sector
    print(f"[SECTOR] {symbol} → {sector}")
    return sector


# ========== Risk Assessment Helpers ==========

def _calculate_concentration_label(sector_allocation: dict) -> str:
    if not sector_allocation:
        return "Highly Concentrated"
    max_pct = max(sector_allocation.values())
    if max_pct >= 60:
        return "Highly Concentrated"
    elif max_pct >= 40:
        return "Moderately Concentrated"
    else:
        return "Optimally Balanced"


def _calculate_diversification_label(num_holdings: int, num_sectors: int) -> str:
    if num_holdings >= 8 and num_sectors >= 5:
        return "Excellent"
    elif num_holdings >= 5 and num_sectors >= 3:
        return "Good"
    elif num_holdings >= 3 and num_sectors >= 2:
        return "Fair"
    else:
        return "Poor"


def _calculate_volatility_label(bullish_score: float) -> str:
    if bullish_score >= 0.65:
        return "Low-Moderate"
    elif bullish_score >= 0.45:
        return "Moderate"
    else:
        return "Moderate-High"


def _calculate_ai_status_message(sector_allocation: dict, concentration_label: str) -> str:
    if not sector_allocation:
        return "Insufficient data to assess portfolio allocation."

    max_sector = max(sector_allocation, key=sector_allocation.get)
    max_pct    = sector_allocation[max_sector]

    if concentration_label == "Highly Concentrated":
        return (
            f"Portfolio is highly concentrated in {max_sector} ({max_pct}%). "
            f"Consider diversifying across more sectors to reduce risk."
        )
    elif concentration_label == "Moderately Concentrated":
        return (
            f"{max_sector} dominates at {max_pct}% of your portfolio. "
            f"Adding exposure to 1–2 more sectors would improve balance."
        )
    else:
        return "Portfolio is currently maintaining optimal sector allocation ratios!"


def _calculate_scores(
    num_holdings: int,
    num_sectors: int,
    bullish_score: float,
    sector_allocation: dict
) -> dict:
    max_pct = max(sector_allocation.values()) if sector_allocation else 100
    diversification_score = min(num_holdings * 8 + num_sectors * 4, 100)
    concentration_penalty = max_pct * 0.5
    sentiment_penalty      = (1 - bullish_score) * 50
    risk_score = round(min(concentration_penalty + sentiment_penalty, 100), 1)
    health_score = round(diversification_score * 0.5 + bullish_score * 50, 1)
    return {
        "risk_score":            risk_score,
        "diversification_score": diversification_score,
        "health_score":          health_score
    }


# ========== OCR Parsing Helpers ==========

def _parse_portfolio_totals_from_ocr(ocr_text: str, holdings: list = None) -> dict:
    """
    Extract top-level portfolio totals from broker OCR text.

    Strategy 1 — multi-holding summary block (two values on one line):
        Invested  Current
        28,951.00 31,019.80
        P&L +2,068.80 +7.15%

    Strategy 2 — derive from parsed holdings list when the summary block
        is absent or split across lines (common with single-stock OCR).
    """
    # Strategy 1 — summary block
    inv_cur = re.search(
        r'Invested\s+Current\s*\n\s*([\d,]+\.?\d*)\s+([\d,]+\.?\d*)',
        ocr_text
    )
    if inv_cur:
        invested = float(inv_cur.group(1).replace(',', ''))
        current  = float(inv_cur.group(2).replace(',', ''))
        pl_amount, pl_pct = 0.0, 0.0
        pl = re.search(r'P&L\s+[+]?([-\d,]+\.?\d*)\s+[+]?([-\d.]+)%', ocr_text)
        if pl:
            pl_amount = float(pl.group(1).replace(',', ''))
            pl_pct    = float(pl.group(2))
        return {
            "total_invested": invested,
            "current_value":  current,
            "pl_amount":      pl_amount,
            "pl_percentage":  pl_pct
        }

    # Strategy 2 — derive from holdings
    if holdings:
        invested  = round(sum(h.get("avg_price", 0) * h.get("quantity", 0) for h in holdings), 2)
        current   = round(sum(h.get("current_value", 0) for h in holdings), 2)
        pl_amount = round(current - invested, 2)
        pl_pct    = round((pl_amount / invested * 100) if invested else 0.0, 2)
        return {
            "total_invested": invested,
            "current_value":  current,
            "pl_amount":      pl_amount,
            "pl_percentage":  pl_pct
        }

    return {"total_invested": 0.0, "current_value": 0.0, "pl_amount": 0.0, "pl_percentage": 0.0}


def _parse_holdings_from_ocr(ocr_text: str) -> list:
    """
    Parses Zerodha-style broker OCR text into individual holdings.

    Handles two real-world OCR layouts:

    Layout A (compact):
        Qty.8 © Avg. 397.00 +33.97%
        TENNIND +1,078.80
        Invested 3,176.00 LTP 531.85 (1.05%)

    Layout B (split — pct on its own line, blank line before symbol):
        Qty.8 »* Avg. 397.00
        [blank]
        +33.97%
        TENNIND +1,078.80
        Invested 3,176.00 LTP 531.85 (1.05%)

    The pattern absorbs 1-4 intermediate lines between the Qty line and the
    SYMBOL line, making it robust to pytesseract whitespace variation.
    """
    holdings = []

    pattern = re.compile(
        r'Qty[.\s]*(\d+)\s*[»©*\s]*Avg[.\s]*([\d,]+\.?\d*)'  # Qty + Avg on same line
        r'(?:[^\n]*\n){1,4}'                                    # 1-4 intermediate lines
        r'([A-Z]{3,10})\s+[+\-][\d,]+\.?\d*\n'               # SYMBOL + P&L amount
        r'Invested\s+([\d,]+\.?\d*)\s+LTP\s+([\d,]+\.?\d*)',  # Invested + LTP
        re.MULTILINE
    )

    _SKIP_SYMBOLS = {'NIFTY', 'BANK', 'NSE', 'BSE', 'BPJ', 'ETH', 'USD'}

    for m in pattern.finditer(ocr_text):
        full_block = m.group(0)
        qty        = int(m.group(1))
        avg_price  = float(m.group(2).replace(',', ''))
        symbol     = m.group(3).upper()
        invested   = float(m.group(4).replace(',', ''))
        ltp        = float(m.group(5).replace(',', ''))

        if symbol in _SKIP_SYMBOLS:
            continue

        # P&L % — search anywhere in the matched block
        pct_match = re.search(r'([+\-][\d.]+)%', full_block)
        pl_pct    = float(pct_match.group(1)) if pct_match else round(
            (ltp - avg_price) / avg_price * 100 if avg_price else 0.0, 2
        )

        cur_val   = round(qty * ltp, 2)
        pl_amount = round(cur_val - invested, 2)

        holdings.append({
            "symbol":        symbol,
            "name":          symbol,
            "sector":        "Unknown",   # filled later by _get_sector_for_symbol
            "quantity":      qty,
            "avg_price":     avg_price,
            "current_price": ltp,
            "current_value": cur_val,
            "pl_amount":     pl_amount,
            "pl_percentage": pl_pct
        })

    return holdings


def _extract_news_from_screener(ratings_markdown: str) -> tuple:
    """Pull the most recent announcement from Screener markdown."""
    ann_pattern = re.compile(
        r'-\s*\[([^\n\]]{15,}?)\n+\n+\n+\n+'
        r'(\d+[dMy]|\d+ \w+)\s*-\s*([^\]]{15,}?)\]',
        re.DOTALL
    )
    match = ann_pattern.search(ratings_markdown)
    if match:
        headline = match.group(1).strip().replace('\n', ' ')
        date_str = match.group(2).strip()
        summary  = match.group(3).strip().replace('\n', ' ')[:200]
        return headline, summary, date_str

    concall = re.search(
        r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4})\s*\n'
        r'\[Transcript\]',
        ratings_markdown
    )
    if concall:
        month = concall.group(1)
        ctx = ratings_markdown[concall.start():concall.start() + 400]
        eps_match = re.search(r'INR([\d,]+)m revenue', ctx)
        if eps_match:
            return (
                f"Q3 FY26 Earnings Call — {month}",
                f"Revenue of INR {eps_match.group(1)}m reported. See full transcript on Screener.",
                month
            )
        return f"Earnings concall transcript available — {month}", "See transcript on Screener for details.", month

    return "No recent announcements", "", ""


def _extract_financials_from_screener(ratings_markdown: str) -> dict:
    """Extract key financial metrics from Screener markdown."""
    result = {}

    mc = re.search(r'Market Cap\s*\n+₹\s*([\d,]+)', ratings_markdown)
    if mc:
        result["market_cap_cr"] = mc.group(1).replace(',', '')

    pe = re.search(r'Stock P/E\s*\n+([\d.]+)', ratings_markdown)
    if pe:
        result["pe_ratio"] = float(pe.group(1))

    roce = re.search(r'ROCE\s*\n+([\d.]+)', ratings_markdown)
    if roce:
        result["roce_pct"] = float(roce.group(1))

    roe = re.search(r'ROE\s*\n+([\d.]+)', ratings_markdown)
    if roe:
        result["roe_pct"] = float(roe.group(1))

    price = re.search(r'Current Price\s*\n+₹\s*([\d,]+)', ratings_markdown)
    if price:
        result["current_price"] = float(price.group(1).replace(',', ''))

    hl = re.search(r'High / Low\s*\n+₹\s*([\d,]+)\s*/\s*([\d,]+)', ratings_markdown)
    if hl:
        result["week52_high"] = float(hl.group(1).replace(',', ''))
        result["week52_low"]  = float(hl.group(2).replace(',', ''))

    pros_section = ratings_markdown[
        ratings_markdown.find('Pros\n'):ratings_markdown.find('Cons\n')
    ] if 'Pros' in ratings_markdown else ''
    pros = re.findall(r'- (.+?)(?=\n)', pros_section)

    cons_section = ratings_markdown[
        ratings_markdown.find('Cons\n'):ratings_markdown.find('Peer')
    ] if 'Cons' in ratings_markdown else ''
    cons = re.findall(r'\\?\*?\*?(.+?)(?=\n|$)', cons_section)

    result["pros"] = [p.strip() for p in pros if len(p.strip()) > 5][:3]
    result["cons"] = [c.strip() for c in cons if len(c.strip()) > 5][:3]

    return result


def _extract_sector_from_screener(ratings_markdown: str) -> str:
    match = re.search(
        r'Auto Components|Banking|Information Technology|FMCG|'
        r'Conglomerate|Telecom|Pharma|Energy|Real Estate|Automobile',
        ratings_markdown, re.IGNORECASE
    )
    return match.group(0).title() if match else "Unknown"


def _extract_company_name_from_screener(ratings_markdown: str) -> str:
    match = re.search(r'#\s+(.+?)\n', ratings_markdown)
    return match.group(1).strip() if match else ""


def _generate_insights_with_llm(symbol: str, sentiment: str, financials: dict, holdings_data: list) -> dict:
    """
    Use LLM to generate 4 strengths and 4 detailed recommendations.
    Returns: {"strengths": [...], "recommendations": [...]}
    """
    import google.generativeai as genai
    import os

    
    try:
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        # Build context from financials
        pe = financials.get("pe_ratio", "N/A")
        roe = financials.get("roe_pct", "N/A")
        roce = financials.get("roce_pct", "N/A")
        market_cap = financials.get("market_cap_cr", "N/A")
        pros = financials.get("pros", [])
        cons = financials.get("cons", [])
        
        prompt = f"""
You are a portfolio optimization AI.

Analyze the portfolio and generate EXACTLY one recommendation for each of the following strategies:

1. Risk Diversification
2. Portfolio Rebalancing
3. Dividend Optimization
4. Stability / Large Cap Allocation

PORTFOLIO DATA:
- Holdings: {holdings_data}
- Sector Allocation: {sector_allocation}
- Risk Level: {risk_level}
- Diversification Score: {diversification_score}
- Total Holdings Count: {len(holdings_data)}

RETURN ONLY VALID JSON:
{{
  "ai_summary": "Portfolio optimization summary",
  "recommendations": [
    {{
      "strategy": "Risk Diversification",
      "action": "add",
      "symbol": "",
      "shares": 0,
      "reason": "",
      "priority": ""
    }},
    {{
      "strategy": "Portfolio Rebalancing",
      "action": "reduce",
      "symbol": "",
      "shares": 0,
      "reason": "",
      "priority": ""
    }},
    {{
      "strategy": "Dividend Optimization",
      "action": "add",
      "symbol": "",
      "shares": 0,
      "reason": "",
      "priority": ""
    }},
    {{
      "strategy": "Stability",
      "action": "add",
      "symbol": "",
      "shares": 0,
      "reason": "",
      "priority": ""
    }}
  ]
}}

RULES:
- Fill all 4 recommendation objects
- Do not remove any object
- Each strategy must have one recommendation
- Actions must be add or reduce
- Return ONLY JSON
"""
        
        print("[INSIGHTS-LLM] Generating strengths and recommendations...")
        response = model.generate_content(prompt)
        
        if response and response.text:
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            
            parsed = json.loads(text)
            strengths = parsed.get("strengths", [])[:4]
            recommendations = parsed.get("recommendations", [])[:4]
            
            print(f"[INSIGHTS-LLM] ✓ Generated {len(strengths)} strengths and {len(recommendations)} recommendations")
            return {"strengths": strengths, "recommendations": recommendations}
    except Exception as e:
        print(f"[INSIGHTS-LLM] Error: {e}")
        return None
    
    return None


def _generate_recommendations(symbol: str, sentiment: str, swot: dict, financials: dict) -> dict:
    items      = []
    strategies = []
    strengths  = []
    areas      = []

    pe   = financials.get("pe_ratio", 0)
    roce = financials.get("roce_pct", 0)

    if roce > 15:
        strengths.append(f"Strong ROCE of {roce}% indicates efficient capital use")
    if sentiment == "Bullish":
        strengths.append("Bullish market sentiment supports near-term upside")
    strengths.extend(financials.get("pros", [])[:2])

    if pe > 50:
        areas.append(f"High P/E of {pe} — stock may be overvalued at current price")
    areas.extend(financials.get("cons", [])[:2])
    if not areas:
        areas.append("Monitor for sector-level headwinds")

    if sentiment == "Bullish" and roce > 15:
        items.append({
            "action": "add", "symbol": symbol, "shares": 5,
            "reason": "Strong fundamentals with bullish momentum",
            "strategy": "Portfolio Rebalancing", "priority": "Medium", "status": "pending"
        })
        strategies.append({
            "name": "Portfolio Rebalancing",
            "description": f"Add to {symbol} — strong ROCE and bullish sentiment",
            "priority": "Medium", "status": "pending"
        })
    elif pe > 60:
        items.append({
            "action": "reduce", "symbol": symbol, "shares": 3,
            "reason": f"P/E of {pe} is elevated — consider partial profit booking",
            "strategy": "Risk Diversification", "priority": "High", "status": "pending"
        })
        strategies.append({
            "name": "Risk Diversification",
            "description": f"Reduce {symbol} exposure — valuation stretched at P/E {pe}",
            "priority": "High", "status": "pending"
        })
    else:
        items.append({
            "action": "add", "symbol": symbol, "shares": 3,
            "reason": "Hold and monitor — balanced risk/reward profile",
            "strategy": "Dividend Optimization", "priority": "Low", "status": "pending"
        })
        strategies.append({
            "name": "Dividend Optimization",
            "description": f"Monitor {symbol} dividend payout and reinvestment",
            "priority": "Low", "status": "pending"
        })

    summary = (
        f"{symbol} shows {sentiment.lower()} sentiment with "
        f"{'strong' if roce > 15 else 'moderate'} fundamentals. "
        f"{'Consider adding on dips.' if sentiment == 'Bullish' else 'Exercise caution at current valuations.'}"
    )

    return {
        "summary":          summary,
        "items":            items,
        "strategies":       strategies,
        "strengths":        strengths if strengths else ["Sufficient data not available"],
        "areas_to_improve": areas
    }


# ========== LLM-Based OCR Parser ==========

def _parse_portfolio_with_llm(ocr_text: str) -> dict:
    """
    Use Gemini LLM to intelligently parse OCR text into structured portfolio data.
    More robust than regex — handles various OCR layouts and formats.
    """
    import os
    import google.generativeai as genai
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        prompt = f"""You are a portfolio parsing expert. Extract ALL portfolio data from this OCR text.

OCR TEXT:
{ocr_text}

EXTRACT AND RETURN VALID JSON (no markdown, pure JSON):
{{
  "portfolio_totals": {{
    "total_invested": <number or 0>,
    "current_value": <number or 0>,
    "pl_amount": <number or 0>,
    "pl_percentage": <number or 0>
  }},
  "holdings": [
    {{
      "symbol": "SYMBOL",
      "quantity": <number>,
      "avg_price": <number>,
      "current_price": <number>,
      "current_value": <number>,
      "pl_amount": <number>,
      "pl_percentage": <number>
    }}
  ]
}}

CRITICAL RULES:
1. Extract EXACT numbers from the text (no approximations)
2. Look for labels like "Invested", "Current", "P&L", "Qty", "Avg", "LTP", "Price"
3. Convert all currency strings (remove ₹, commas) to numbers
4. For each holding, calculate missing values:
   - current_value = quantity × current_price
   - pl_amount = current_value - (quantity × avg_price)
   - pl_percentage = (pl_amount / (quantity × avg_price)) × 100
5. If a value cannot be found, use 0 or null
6. Return ONLY valid JSON, no explanation"""
        
        print("[OCR-LLM] Parsing portfolio with Gemini...")
        response = model.generate_content(prompt)
        
        if response and response.text:
            # Clean response (remove markdown code blocks if present)
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            
            parsed = json.loads(text)
            totals = parsed.get("portfolio_totals", {})
            holdings = parsed.get("holdings", [])
            
            print(f"[OCR-LLM] ✓ Parsed portfolio: {len(holdings)} holding(s)")
            print(f"[OCR-LLM] Totals: Invested={totals.get('total_invested')}, Current={totals.get('current_value')}")
            
            return {
                "portfolio_totals": totals,
                "holdings": holdings
            }
    except Exception as e:
        print(f"[OCR-LLM] Error: {e}")
        print(f"[OCR-LLM] Falling back to regex parsing...")
        return None


# ========== Main Structured Data Builder ==========

def parse_raw_data_to_structured(symbol: str, raw_data: dict, ocr_text: str) -> dict:
    """
    Convert force_market_analysis raw_data + OCR text into the structured
    JSON schema the UI needs. Uses LLM for OCR parsing.
    """
    stock_data  = raw_data.get("stock_data", {})
    sentiment   = raw_data.get("sentiment", {}).get("sentiment", {})
    ratings_raw = raw_data.get("analyst_ratings", {}).get("ratings", "")

    # ── Holdings from OCR using LLM ──────────────────────────────────────────
    llm_result = _parse_portfolio_with_llm(ocr_text)
    if llm_result:
        holdings = llm_result.get("holdings", [])
        portfolio_totals = llm_result.get("portfolio_totals", {})
    else:
        # Fallback to regex if LLM fails
        print("[OCR] LLM parsing failed, falling back to regex...")
        holdings = _parse_holdings_from_ocr(ocr_text)
        portfolio_totals = _parse_portfolio_totals_from_ocr(ocr_text, holdings)
    
    print(f"[OCR] Parsed {len(holdings)} holding(s) from OCR text")

    # ── Assign sectors dynamically via yfinance ───────────────────────────────
    for h in holdings:
        h["sector"] = _get_sector_for_symbol(h["symbol"])
        if h["symbol"] == symbol:
            h["name"] = _extract_company_name_from_screener(ratings_raw) or symbol

    # ── Use portfolio totals from LLM/regex parsing ───────────────────────────
    total_invested = portfolio_totals.get("total_invested", 0)
    current_value  = portfolio_totals.get("current_value", 0)
    pl_amount      = portfolio_totals.get("pl_amount", 0)
    pl_pct         = portfolio_totals.get("pl_percentage", 0)
    print(f"[OCR] Totals — invested={total_invested}, current={current_value}, pl={pl_amount} ({pl_pct}%)")

    # ── Sector allocation from holdings ──────────────────────────────────────
    sector_map = {}
    for h in holdings:
        s = h["sector"]
        sector_map[s] = sector_map.get(s, 0) + h["quantity"] * h["current_price"]

    sector_allocation = {
        s: round(v / current_value * 100, 1) if current_value else 0
        for s, v in sector_map.items()
    }

    # ── Sentiment ─────────────────────────────────────────────────────────────
    bullish_score = sentiment.get("bullish", 0.5)
    if bullish_score >= 0.6:
        sentiment_label = "Bullish"
    elif bullish_score <= 0.4:
        sentiment_label = "Bearish"
    else:
        sentiment_label = "Neutral"

    # ── News from Screener announcements ─────────────────────────────────────
    news_headline, news_summary, news_date = _extract_news_from_screener(ratings_raw)

    # ── SWOT: prefer MoneyControl structured_data; NSE has none ──────────────
    sd = stock_data.get("structured_data", {})
    # When NSE is primary, structured_data IS the NSE fields dict directly —
    # no "swot" key.  When MC was fallback, swot is nested inside.
    swot             = sd.get("swot", {})
    technical_rating = sd.get("technical_rating") or sd.get("nse", {}).get("technical_rating", "N/A")

    # ── Key financials from Screener ──────────────────────────────────────────
    financials = _extract_financials_from_screener(ratings_raw)

    # Fill in NSE price fields when Screener doesn't have them
    if not financials.get("current_price"):
        financials["current_price"] = sd.get("last_price")
    if not financials.get("week52_high"):
        financials["week52_high"] = sd.get("week_52_high")
    if not financials.get("week52_low"):
        financials["week52_low"] = sd.get("week_52_low")

    # ── Recommendations ───────────────────────────────────────────────────────
    recommendations = _generate_recommendations(symbol, sentiment_label, {}, financials)
    
    # ── Strengths & Recommendations from LLM ──────────────────────────────────
    llm_insights = _generate_insights_with_llm(symbol, sentiment_label, financials, holdings)
    if llm_insights:
        recommendations["strengths"] = llm_insights.get("strengths", recommendations["strengths"])
        # Merge LLM recommendations with existing ones
        for rec in llm_insights.get("recommendations", [])[:2]:
            recommendations["items"].append({
                "symbol": symbol,
                "shares": 5,
                "action": rec.get("action", "hold"),
                "reason": rec.get("reason", ""),
                "strategy": "Portfolio Rebalancing",
                "priority": rec.get("priority", "Medium"),
                "status": "pending"
            })

    # ── Risk Assessment ───────────────────────────────────────────────────────
    num_holdings  = len(holdings)
    num_sectors   = len(sector_allocation)

    concentration_label   = _calculate_concentration_label(sector_allocation)
    diversification_label = _calculate_diversification_label(num_holdings, num_sectors)
    volatility_label      = _calculate_volatility_label(bullish_score)
    ai_status_message     = _calculate_ai_status_message(sector_allocation, concentration_label)
    scores                = _calculate_scores(num_holdings, num_sectors, bullish_score, sector_allocation)

    print(f"[RISK] sectors={num_sectors}, holdings={num_holdings}, "
          f"max_pct={max(sector_allocation.values(), default=0):.1f}%, "
          f"bullish={bullish_score:.2f}")
    print(f"[RISK] concentration={concentration_label}, "
          f"diversification={diversification_label}, volatility={volatility_label}")
    print(f"[RISK] scores={scores}")

    # ── Simulation (12% compound growth) ─────────────────────────────────────
    projections = []
    for yr in range(1, 6):
        pv = round(current_value * (1.12 ** yr), 2)
        projections.append({
            "year":             yr,
            "projected_value":  pv,
            "gain":             round(pv - current_value, 2),
            "gain_percentage":  round(
                (pv - current_value) / current_value * 100 if current_value else 0, 2
            )
        })

    return {
        "portfolio": {
            "total_invested": round(total_invested, 2),
            "current_value":  round(current_value, 2),
            "pl_amount":      pl_amount,
            "pl_percentage":  pl_pct,
            "stock_count":    num_holdings,
            "holdings":       holdings
        },
        "analysis": {
            "sector_allocation": sector_allocation,
            "risk_assessment": {
                "volatility":             volatility_label,
                "concentration":          concentration_label,
                "diversification_status": diversification_label,
                "ai_status_message":      ai_status_message
            },
            "risk_score":            scores["risk_score"],
            "diversification_score": scores["diversification_score"],
            "health_score":          scores["health_score"],
            "financials": financials
        },
        "recommendations": {
            "ai_summary":       recommendations["summary"],
            "items":            recommendations["items"],
            "strategies":       recommendations["strategies"],
            "strengths":        recommendations["strengths"],
            "areas_to_improve": recommendations["areas_to_improve"]
        },
        "market_data": {
            symbol: {
                "sentiment":        sentiment_label,
                "bullish_score":    bullish_score,
                "news_headline":    news_headline,
                "news_summary":     news_summary,
                "news_date":        news_date,
                "technical_rating": technical_rating
            }
        },
        "simulation": {
            "current_value":      round(current_value, 2),
            "annual_return_rate": 12,
            "projections":        projections
        }
    }