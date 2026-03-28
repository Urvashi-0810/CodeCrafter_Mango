import os
import requests
from firecrawl import FirecrawlApp
from dotenv import load_dotenv
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

load_dotenv()


# ---------------------------------------------------------------------------
# Static symbol → per-source URL slug mapping.
# Add a new entry here whenever you need to support a new stock symbol.
# ---------------------------------------------------------------------------
SYMBOL_MAP: Dict[str, Dict[str, str]] = {
    "TCS": {
        "nse_slug":      "TCS/Tata-Consultancy-Services-Limited",
        "bse_slug":      "tata-consultancy-services-ltd/tcs/532540",
        "screener_slug": "TCS",
        "mc_slug":       "computers-software/tataconsultancyservices/TCS",
    },
    "INFY": {
        "nse_slug":      "INFY/Infosys-Limited",
        "bse_slug":      "infosys-ltd/infy/500209",
        "screener_slug": "INFY",
        "mc_slug":       "computers-software/infosys/IT",
    },
    "RELIANCE": {
        "nse_slug":      "RELIANCE/Reliance-Industries-Limited",
        "bse_slug":      "reliance-industries-ltd/reliance/500325",
        "screener_slug": "RELIANCE",
        "mc_slug":       "refineries/relianceindustries/RI",
    },
    "HDFCBANK": {
        "nse_slug":      "HDFCBANK/HDFC-Bank-Limited",
        "bse_slug":      "hdfc-bank-ltd/hdfcbank/500180",
        "screener_slug": "HDFCBANK",
        "mc_slug":       "banks-private-sector/hdfcbank/HDF01",
    },
    "TENNIND": {
        "nse_slug":      "TENNIND/Tenneco-Industries-Limited",
        "bse_slug":      "tenneco-industries-ltd/tennind/507685",
        "screener_slug": "TENNIND",
        "mc_slug":       "auto-ancillaries-engine-parts/tennecoindustries/TENNIND",
    },
    # ── add more symbols below ────────────────────────────────────────────
}


class MarketDataTools:
    """Tools for fetching market data and financial information."""

    print("Initializing MarketDataTools with Firecrawl integration...")

    TRUSTED_SOURCES: Dict[str, str] = {
        "nse":             "https://www.nseindia.com",
        "bse":             "https://www.bseindia.com",
        "moneycontrol":    "https://www.moneycontrol.com",
        "screener":        "https://www.screener.in",
        "economictimes":   "https://economictimes.indiatimes.com",
        "livemint":        "https://www.livemint.com",
        "reuters":         "https://www.reuters.com",
        "businessstandard":"https://www.business-standard.com",
        "investing":       "https://www.investing.com",
        "rbi":             "https://www.rbi.org.in",
        "indiabudget":     "https://www.indiabudget.gov.in",
    }

    def __init__(self):
        """Initialize market data tools."""
        self.api_key   = os.getenv("FIRECRAWL_API_KEY")
        print(f"[INIT] FIRECRAWL_API_KEY from env: {self.api_key}")
        
        if self.api_key:
            try:
                self.firecrawl = FirecrawlApp(api_key=self.api_key)
                print(f"[INIT] FirecrawlApp initialized successfully")
            except Exception as e:
                print(f"[INIT] FirecrawlApp initialization failed: {e}")
                self.firecrawl = None
        else:
            print(f"[INIT] FIRECRAWL_API_KEY not found in environment")
            self.firecrawl = None
        
        self.cache: Dict[str, Any] = {}

    # ------------------------------------------------------------------
    # URL builder (previously in StockScraper)
    # ------------------------------------------------------------------
    def build_url(self, symbol: str, source: str) -> Optional[str]:
        """
        Construct the correct stock-page URL for *symbol* on *source*.
        Returns None if the symbol is not present in SYMBOL_MAP.
        """
        symbol = symbol.upper()
        meta   = SYMBOL_MAP.get(symbol)
        if meta is None:
            return None

        base = self.TRUSTED_SOURCES[source]

        if source == "nse":
            # https://www.nseindia.com/get-quote/equity/TCS/Tata-Consultancy-Services-Limited
            return f"{base}/get-quote/equity/{meta['nse_slug']}"

        if source == "bse":
            # https://www.bseindia.com/stock-share-price/tata-consultancy-services-ltd/tcs/532540/
            return f"{base}/stock-share-price/{meta['bse_slug']}/"

        if source == "screener":
            # https://www.screener.in/company/TCS/consolidated/
            return f"{base}/company/{meta['screener_slug']}/consolidated/"

        if source == "moneycontrol":
            # https://www.moneycontrol.com/india/stockpricequote/computers-software/tataconsultancyservices/TCS
            return f"{base}/india/stockpricequote/{meta['mc_slug']}"

        return None  # unknown source

    # ------------------------------------------------------------------
    # Stock scraper (previously in StockScraper)
    # ------------------------------------------------------------------
    def scrape_stock_data(
        self, symbol: str, source: str = "moneycontrol"
    ) -> Dict[str, Any]:
        """Scrape stock data from a trusted source."""
        print(f"[SCRAPER] scrape_stock_data() called for {symbol} from {source}")
        if not self.firecrawl:
            print("[DEBUG] Firecrawl not initialized in scrape_stock_data()")
            return {"error": "Firecrawl not initialized"}

        if source not in self.TRUSTED_SOURCES:
            return {"error": f"Source '{source}' not in trusted sources"}

        symbol = symbol.upper()
        url    = self.build_url(symbol, source)
        print(f"[SCRAPER] URL built for {symbol}: {url}")

        if url is None:
            return {
                "success": False,
                "error": (
                    f"Symbol '{symbol}' not found in SYMBOL_MAP. "
                    "Please add it before scraping."
                ),
            }

        try:
            print(f"Scraping {symbol} from {source} → {url}")
            result   = self.firecrawl.scrape_url(url, {"formats": ["markdown"]})
            
            # Validate Firecrawl response
            if not result or not result.get("markdown"):
                print(f"[ERROR] Empty response from Firecrawl for {symbol}")
                return {
                    "success": False,
                    "error": "Empty response from Firecrawl",
                    "symbol": symbol,
                    "source": source,
                    "url": url
                }
            
            markdown = result.get("markdown", "")
            print(f"[SCRAPER] Scraped markdown length: {len(markdown)} characters")
            print(f"[SCRAPER] Preview (first 500 chars):\n{markdown[:500]}\n...")

            return {
                "success":   True,
                "symbol":    symbol,
                "source":    source,
                "url":       url,
                "data":      markdown,
                "data_length": len(markdown),
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            print(f"[ERROR] Exception in scrape_stock_data: {e}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": str(e)}

    # ------------------------------------------------------------------
    # Remaining original methods (unchanged)
    # ------------------------------------------------------------------
    def fetch_company_news(self, symbol: str) -> Dict[str, Any]:
        """Fetch company news from multiple sources."""
        try:
            url = f"https://economictimes.indiatimes.com/markets/stocks/news/{symbol.lower()}"

            if not self.firecrawl:
                print("[DEBUG] Firecrawl not initialized in fetch_company_news()")
                return {"error": "Firecrawl not initialized"}

            print(f"Fetching news for {symbol} from Economic Times...")
            result = self.firecrawl.scrape_url(url, {"formats": ["markdown"]})
            print(f"News results for {symbol}: {result.get('markdown')[:200]}...")
            return {
                "success":   True,
                "symbol":    symbol,
                "news":      result.get("markdown"),
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def fetch_financial_reports(self, symbol: str) -> Dict[str, Any]:
        """Fetch financial reports from BSE/NSE."""
        try:
            url = f"https://www.bseindia.com/stock-share-price/{symbol}"

            if not self.firecrawl:
                print("[DEBUG] Firecrawl not initialized in fetch_financial_reports()")
                return {"error": "Firecrawl not initialized"}

            print(f"Fetching financial reports for {symbol}...")
            result = self.firecrawl.scrape_url(url, {"formats": ["markdown"]})
            print(f"Financial reports for {symbol}: {result.get('markdown')[:200]}...")
            return {
                "success":   True,
                "symbol":    symbol,
                "reports":   result.get("markdown"),
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def fetch_sector_performance(self, sector: str) -> Dict[str, Any]:
        """Fetch sector performance data."""
        try:
            url = f"https://www.moneycontrol.com/stocks/sectors/{sector.lower()}"

            if not self.firecrawl:
                print("[DEBUG] Firecrawl not initialized in fetch_sector_performance()")
                return {"error": "Firecrawl not initialized"}

            print(f"Fetching sector performance for {sector}...")
            result = self.firecrawl.scrape_url(url, {"formats": ["markdown"]})
            print(f"Sector performance for {sector}: {result.get('markdown')[:200]}...")
            return {
                "success":     True,
                "sector":      sector,
                "performance": result.get("markdown"),
                "timestamp":   datetime.now().isoformat(),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def fetch_economic_news(self) -> Dict[str, Any]:
        """Fetch economic news and RBI updates."""
        try:
            urls = [
                "https://www.rbi.org.in/scripts/",
                "https://www.indiabudget.gov.in",
                "https://www.livemint.com/news",
            ]
            news_data = []

            if not self.firecrawl:
                print("[DEBUG] Firecrawl not initialized in fetch_economic_news()")
                return {"error": "Firecrawl not initialized"}

            print("Fetching economic news and RBI updates...")
            for url in urls:
                try:
                    result = self.firecrawl.scrape_url(url, {"formats": ["markdown"]})
                    news_data.append({"source": url, "content": result.get("markdown")})
                    print(f"Fetched news from {url}: {result.get('markdown')[:200]}...")
                except Exception:
                    continue

            return {
                "success":       True,
                "economic_news": news_data,
                "timestamp":     datetime.now().isoformat(),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def fetch_analyst_ratings(self, symbol: str) -> Dict[str, Any]:
        """Fetch analyst ratings from Screener."""
        try:
            url = f"https://www.screener.in/company/{symbol}/"

            if not self.firecrawl:
                print("[DEBUG] Firecrawl not initialized in fetch_analyst_ratings()")
                return {"error": "Firecrawl not initialized"}

            print(f"Fetching analyst ratings for {symbol}...")
            result = self.firecrawl.scrape_url(url, {"formats": ["markdown"]})
            print(f"Analyst ratings for {symbol}: {result.get('markdown')[:200]}...")
            return {
                "success":   True,
                "symbol":    symbol,
                "ratings":   result.get("markdown"),
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_market_sentiment(self, symbol: str) -> Dict[str, Any]:
        """Analyze market sentiment for a stock."""
        try:
            sentiment_score = {
                "bullish": 0.65,
                "neutral": 0.35,
                "bearish": 0.0,
                "overall": 0.65,
            }
            return {
                "success":   True,
                "symbol":    symbol,
                "sentiment": sentiment_score,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def fetch_candlestick_data(self, symbol: str, period: str = "1y") -> Dict[str, Any]:
        """Fetch historical candlestick data."""
        try:
            candlestick_data = {
                "symbol": symbol,
                "period": period,
                "candles": [
                    {"date": "2024-03-27", "open": 100, "high": 105, "low": 99,  "close": 103},
                    {"date": "2024-03-26", "open": 101, "high": 104, "low": 100, "close": 102},
                ],
            }
            return {
                "success":   True,
                "data":      candlestick_data,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def cache_market_data(self, key: str, data: Dict[str, Any]) -> None:
        """Cache market data for quick access."""
        self.cache[key] = {"data": data, "timestamp": datetime.now().isoformat()}

    def get_cached_data(self, key: str) -> Dict[str, Any]:
        """Retrieve cached market data."""
        return self.cache.get(key, {})

    def is_cache_valid(self, key: str, ttl_minutes: int = 60) -> bool:
        """Check if cached data is still valid."""
        if key not in self.cache:
            return False
        cached_time = datetime.fromisoformat(self.cache[key]["timestamp"])
        age_minutes = (datetime.now() - cached_time).total_seconds() / 60
        return age_minutes < ttl_minutes