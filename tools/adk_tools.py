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

    # CSV parser often returns {"success": True, "data": {...portfolio...}}
    if isinstance(portfolio.get("data"), dict):
        return portfolio["data"]

    # Formatter may return {"success": True, "portfolio": {...portfolio...}}
    if isinstance(portfolio.get("portfolio"), dict):
        return portfolio["portfolio"]

    # Some agents output holdings instead of stocks.
    if isinstance(portfolio.get("holdings"), list) and "stocks" not in portfolio:
        normalized = dict(portfolio)
        normalized["stocks"] = portfolio.get("holdings", [])
        return normalized

    return portfolio

# ========== Analysis Functions ==========
def calculate_portfolio_metrics(portfolio: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate key portfolio metrics."""
    # print(f"Calculating portfolio metrics for portfolio: {portfolio}")
    portfolio = _normalize_portfolio_payload(portfolio)
    return {
        "total_investment": AnalysisTools.calculate_total_investment(portfolio),
        "current_value": AnalysisTools.calculate_current_value(portfolio),
        "profit_loss": AnalysisTools.calculate_profit_loss(portfolio),
        "sector_allocation": AnalysisTools.calculate_sector_allocation(portfolio),
        "asset_allocation": AnalysisTools.calculate_asset_allocation(portfolio),
        "risk_score": AnalysisTools.calculate_risk_score(portfolio),
        "diversification_score": AnalysisTools.calculate_diversification_score(portfolio),
        "concentration_risk": AnalysisTools.calculate_concentration_risk(portfolio),
        "health_score": AnalysisTools.calculate_portfolio_health_score(portfolio)
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
        "symbol": symbol,
        "stock_data": market_tools.scrape_stock_data(symbol),
        "news": market_tools.fetch_company_news(symbol),
        "sentiment": market_tools.get_market_sentiment(symbol),
        "analyst_ratings": market_tools.fetch_analyst_ratings(symbol)
    }
    
    print(f"[MARKET] Complete market data fetch finished for {symbol}")
    return result

def force_market_analysis(symbol: str) -> Dict[str, Any]:
    """
    FORCE market analysis execution - bypasses LLM decision-making.
    This method directly calls all market tools without relying on agent.
    """
    print(f"\n[FORCE-ANALYSIS] Starting forced market analysis for: {symbol}\n")
    
    market_tools = MarketDataTools()
    
    # Step 1: Validate symbol
    if not symbol or not isinstance(symbol, str) or len(symbol.strip()) == 0:
        print(f"[FORCE-ANALYSIS] Invalid symbol: {symbol}")
        return {"error": "Invalid stock symbol", "symbol": symbol}
    
    symbol = symbol.upper().strip()
    print(f"[FORCE-ANALYSIS] Symbol after normalization: {symbol}")
    
    # Step 2: Check if symbol is in SYMBOL_MAP
    from tools.market_tools import SYMBOL_MAP
    if symbol not in SYMBOL_MAP:
        print(f"[FORCE-ANALYSIS] Symbol {symbol} not in SYMBOL_MAP")
        print(f"[FORCE-ANALYSIS] Available symbols: {list(SYMBOL_MAP.keys())}")
        return {
            "error": f"Symbol '{symbol}' not supported",
            "symbol": symbol,
            "available_symbols": list(SYMBOL_MAP.keys())
        }
    
    print(f"[FORCE-ANALYSIS] Symbol validation passed, proceeding with market data fetch")
    
    # Step 3: Fetch all market data directly
    print(f"[FORCE-ANALYSIS] Step 1: Calling scrape_stock_data()")
    stock_data = market_tools.scrape_stock_data(symbol)
    print(f"[FORCE-ANALYSIS] scrape_stock_data() returned: {type(stock_data)}")
    if stock_data.get("success"):
        print(f"[FORCE-ANALYSIS] Stock data preview:\n{stock_data.get('data', '')[:300]}\n")
    else:
        print(f"[FORCE-ANALYSIS] Stock data ERROR: {stock_data.get('error')}")
    
    print(f"[FORCE-ANALYSIS] Step 2: Calling fetch_company_news()")
    news = market_tools.fetch_company_news(symbol)
    print(f"[FORCE-ANALYSIS] fetch_company_news() returned: {type(news)}")
    if news.get("success"):
        print(f"[FORCE-ANALYSIS] News preview:\n{news.get('news', '')[:300]}\n")
    else:
        print(f"[FORCE-ANALYSIS] News ERROR: {news.get('error')}")
    
    print(f"[FORCE-ANALYSIS] Step 3: Calling get_market_sentiment()")
    sentiment = market_tools.get_market_sentiment(symbol)
    print(f"[FORCE-ANALYSIS] Sentiment returned: {sentiment}")
    
    print(f"[FORCE-ANALYSIS] Step 4: Calling fetch_analyst_ratings()")
    ratings = market_tools.fetch_analyst_ratings(symbol)
    print(f"[FORCE-ANALYSIS] fetch_analyst_ratings() returned: {type(ratings)}")
    if ratings.get("success"):
        print(f"[FORCE-ANALYSIS] Ratings preview:\n{ratings.get('ratings', '')[:300]}\n")
    else:
        print(f"[FORCE-ANALYSIS] Ratings ERROR: {ratings.get('error')}")
    
    # Step 4: Compile results with raw data in report
    print(f"[FORCE-ANALYSIS] Compiling final report...")
    
    # Create comprehensive report including all raw data
    report_text = f"""
================================================================================
                    MARKET ANALYSIS REPORT FOR {symbol}
================================================================================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

--------------------------------------------------------------------------------
1. STOCK PRICE & TECHNICAL DATA
--------------------------------------------------------------------------------
Status: {"✅ SUCCESS" if stock_data.get('success') else "❌ FAILED"}
Source: Moneycontrol
URL: {stock_data.get('url', 'N/A')}

Data Preview:
{stock_data.get('data', 'No data available')[:1000]}

Full Data Length: {stock_data.get('data_length', 0)} characters

--------------------------------------------------------------------------------
2. COMPANY NEWS
--------------------------------------------------------------------------------
Status: {"✅ SUCCESS" if news.get('success') else "❌ FAILED"}
Source: Economic Times

News Content:
{news.get('news', 'No news available')[:1000]}

--------------------------------------------------------------------------------
3. MARKET SENTIMENT
--------------------------------------------------------------------------------
Sentiment Analysis:
{json.dumps(sentiment, indent=2)}

--------------------------------------------------------------------------------
4. ANALYST RATINGS
--------------------------------------------------------------------------------
Status: {"✅ SUCCESS" if ratings.get('success') else "❌ FAILED"}
Source: Screener

Ratings Content:
{ratings.get('ratings', 'No ratings available')[:1000]}

================================================================================
END OF REPORT
================================================================================
"""
    
    result = {
        "success": True,
        "symbol": symbol,
        "analysis_type": "forced_market_analysis",
        "report": report_text,
        "raw_data": {
            "stock_data": stock_data,
            "news": news,
            "sentiment": sentiment,
            "analyst_ratings": ratings
        },
        "timestamp": datetime.now().isoformat()
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
