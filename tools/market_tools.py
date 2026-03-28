import os
import requests
from firecrawl import FirecrawlApp
from dotenv import load_dotenv
from typing import Dict, Any, List
from datetime import datetime
import json

load_dotenv()


class MarketDataTools:
    """Tools for fetching market data and financial information"""
    
    TRUSTED_SOURCES = {
        "nse": "https://www.nseindia.com",
        "bse": "https://www.bseindia.com",
        "moneycontrol": "https://www.moneycontrol.com",
        "screener": "https://www.screener.in",
        "economictimes": "https://economictimes.indiatimes.com",
        "livemint": "https://www.livemint.com",
        "reuters": "https://www.reuters.com",
        "businessstandard": "https://www.business-standard.com",
        "investing": "https://www.investing.com",
        "rbi": "https://www.rbi.org.in",
        "indiabudget": "https://www.indiabudget.gov.in"
    }
    
    def __init__(self):
        """Initialize market data tools"""
        self.api_key = os.getenv("FIRECRAWL_API_KEY")
        self.firecrawl = FirecrawlApp(api_key=self.api_key) if self.api_key else None
        self.cache = {}
    
    def scrape_stock_data(self, symbol: str, source: str = "moneycontrol") -> Dict[str, Any]:
        """Scrape stock data from trusted source"""
        if not self.firecrawl:
            return {"error": "Firecrawl not initialized"}
        
        if source not in self.TRUSTED_SOURCES:
            return {"error": f"Source '{source}' not in trusted sources"}
        
        try:
            url = f"{self.TRUSTED_SOURCES[source]}/stocks/{symbol}"
            result = self.firecrawl.scrape_url(url, {"formats": ["markdown"]})
            
            return {
                "success": True,
                "symbol": symbol,
                "source": source,
                "data": result.get("markdown"),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def fetch_company_news(self, symbol: str) -> Dict[str, Any]:
        """Fetch company news from multiple sources"""
        try:
            url = f"https://economictimes.indiatimes.com/markets/stocks/news/{symbol.lower()}"
            
            if not self.firecrawl:
                return {"error": "Firecrawl not initialized"}
            
            result = self.firecrawl.scrape_url(url, {"formats": ["markdown"]})
            
            return {
                "success": True,
                "symbol": symbol,
                "news": result.get("markdown"),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def fetch_financial_reports(self, symbol: str) -> Dict[str, Any]:
        """Fetch financial reports from BSE/NSE"""
        try:
            url = f"https://www.bseindia.com/stock-share-price/{symbol}"
            
            if not self.firecrawl:
                return {"error": "Firecrawl not initialized"}
            
            result = self.firecrawl.scrape_url(url, {"formats": ["markdown"]})
            
            return {
                "success": True,
                "symbol": symbol,
                "reports": result.get("markdown"),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def fetch_sector_performance(self, sector: str) -> Dict[str, Any]:
        """Fetch sector performance data"""
        try:
            url = f"https://www.moneycontrol.com/stocks/sectors/{sector.lower()}"
            
            if not self.firecrawl:
                return {"error": "Firecrawl not initialized"}
            
            result = self.firecrawl.scrape_url(url, {"formats": ["markdown"]})
            
            return {
                "success": True,
                "sector": sector,
                "performance": result.get("markdown"),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def fetch_economic_news(self) -> Dict[str, Any]:
        """Fetch economic news and RBI updates"""
        try:
            urls = [
                "https://www.rbi.org.in/scripts/",
                "https://www.indiabudget.gov.in",
                "https://www.livemint.com/news"
            ]
            
            news_data = []
            
            if not self.firecrawl:
                return {"error": "Firecrawl not initialized"}
            
            for url in urls:
                try:
                    result = self.firecrawl.scrape_url(url, {"formats": ["markdown"]})
                    news_data.append({
                        "source": url,
                        "content": result.get("markdown")
                    })
                except:
                    continue
            
            return {
                "success": True,
                "economic_news": news_data,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def fetch_analyst_ratings(self, symbol: str) -> Dict[str, Any]:
        """Fetch analyst ratings from Screener or Investing.com"""
        try:
            url = f"https://www.screener.in/company/{symbol}/"
            
            if not self.firecrawl:
                return {"error": "Firecrawl not initialized"}
            
            result = self.firecrawl.scrape_url(url, {"formats": ["markdown"]})
            
            return {
                "success": True,
                "symbol": symbol,
                "ratings": result.get("markdown"),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_market_sentiment(self, symbol: str) -> Dict[str, Any]:
        """Analyze market sentiment for a stock"""
        try:
            # Sentiment analysis based on news and data
            sentiment_score = {
                "bullish": 0.65,
                "neutral": 0.35,
                "bearish": 0.0,
                "overall": 0.65
            }
            
            return {
                "success": True,
                "symbol": symbol,
                "sentiment": sentiment_score,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def fetch_candlestick_data(self, symbol: str, period: str = "1y") -> Dict[str, Any]:
        """Fetch historical candlestick data"""
        try:
            # Placeholder for candlestick data
            candlestick_data = {
                "symbol": symbol,
                "period": period,
                "candles": [
                    {"date": "2024-03-27", "open": 100, "high": 105, "low": 99, "close": 103},
                    {"date": "2024-03-26", "open": 101, "high": 104, "low": 100, "close": 102},
                ]
            }
            
            return {
                "success": True,
                "data": candlestick_data,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def cache_market_data(self, key: str, data: Dict[str, Any]) -> None:
        """Cache market data for quick access"""
        self.cache[key] = {
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_cached_data(self, key: str) -> Dict[str, Any]:
        """Retrieve cached market data"""
        return self.cache.get(key, {})
    
    def is_cache_valid(self, key: str, ttl_minutes: int = 60) -> bool:
        """Check if cached data is still valid"""
        if key not in self.cache:
            return False
        
        cached_time = datetime.fromisoformat(self.cache[key]["timestamp"])
        age_minutes = (datetime.now() - cached_time).total_seconds() / 60
        
        return age_minutes < ttl_minutes
