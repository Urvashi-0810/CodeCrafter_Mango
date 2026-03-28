import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from tools.market_tools import MarketDataTools

load_dotenv()


class MarketDataAgent:
    """Agent for fetching market and financial data"""
    
    def __init__(self, api_key: str = None, model: str = "gemini-pro"):
        self.name = "Market Data Agent"
        self.model = model
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.model_instance = genai.GenerativeModel(
            model_name=model,
            system_instruction="You are a market research expert. Summarize financial data and market trends."
        )
        self.market_tools = MarketDataTools()
    
    def fetch_stock_data(self, symbol: str, source: str = "moneycontrol") -> dict:
        """Fetch stock data from trusted source"""
        print(f"{self.name}: Fetching stock data for {symbol} from {source}...")
        return self.market_tools.scrape_stock_data(symbol, source)
    
    def fetch_news(self, symbol: str) -> dict:
        """Fetch company news"""
        print(f"{self.name}: Fetching news for {symbol}...")
        return self.market_tools.fetch_company_news(symbol)
    
    def fetch_financial_reports(self, symbol: str) -> dict:
        """Fetch financial reports"""
        print(f"{self.name}: Fetching financial reports for {symbol}...")

        return self.market_tools.fetch_financial_reports(symbol)
    
    def fetch_sector_performance(self, sector: str) -> dict:
        """Fetch sector performance"""
        print(f"{self.name}: Fetching performance data for {sector} sector...")
        return self.market_tools.fetch_sector_performance(sector)
    
    def fetch_economic_news(self) -> dict:
        """Fetch economic and regulatory news"""
        print(f"{self.name}: Fetching economic and regulatory news...")
        return self.market_tools.fetch_economic_news()
    
    def fetch_analyst_ratings(self, symbol: str) -> dict:
        """Fetch analyst ratings"""
        print(f"{self.name}: Fetching analyst ratings for {symbol}...")
        return self.market_tools.fetch_analyst_ratings(symbol)
    
    def get_market_sentiment(self, symbol: str) -> dict:
        """Get market sentiment analysis"""
        print(f"{self.name}: Analyzing market sentiment for {symbol}...")
        return self.market_tools.get_market_sentiment(symbol)
    
    def fetch_historical_data(self, symbol: str, period: str = "1y") -> dict:
        """Fetch historical candlestick data"""
        print(f"{self.name}: Fetching historical data for {symbol}...")

        return self.market_tools.fetch_candlestick_data(symbol, period)
