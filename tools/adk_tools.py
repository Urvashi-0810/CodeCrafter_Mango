# tools/adk_tools.py

import json
from typing import Dict, Any, List

# Import existing tool classes
from tools.analysis_tools import AnalysisTools
from tools.market_tools import MarketDataTools
from tools.portfolio_tools import PortfolioParsingTools
from tools.simulation_tools import SimulationTools

# ========== Analysis Functions ==========
def calculate_portfolio_metrics(portfolio: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate key portfolio metrics."""
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
    return AnalysisTools.generate_analysis_report(portfolio)

# ========== Market Functions ==========
def fetch_complete_market_data(symbol: str) -> Dict[str, Any]:
    """Fetch stock data, news, sentiment, and analyst ratings."""
    market_tools = MarketDataTools()
    print(f"Fetching market data for {symbol}...")
    return {
        "stock_data": market_tools.scrape_stock_data(symbol),
        "news": market_tools.fetch_company_news(symbol),
        "sentiment": market_tools.get_market_sentiment(symbol),
        "analyst_ratings": market_tools.fetch_analyst_ratings(symbol)
    }

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
    return SimulationTools.simulate_returns(portfolio, years, annual_return)

def add_stock_to_portfolio(portfolio: Dict[str, Any], symbol: str, quantity: int,
                           buy_price: float, current_price: float, sector: str) -> Dict[str, Any]:
    """Add a stock to the portfolio (simulation)."""
    return SimulationTools.add_stock(portfolio, symbol, quantity, buy_price, current_price, sector)
