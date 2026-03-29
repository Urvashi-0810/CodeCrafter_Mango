import os
import re
import time
import concurrent.futures
from firecrawl import FirecrawlApp
from dotenv import load_dotenv
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

# curl_cffi impersonates Chrome's TLS fingerprint (JA3/JA3S), which is what
# NSE's bot-detection (Cloudflare/Akamai) actually checks.  Plain `requests`
# has a distinct Python/urllib3 TLS signature that triggers 403s on NSE.
# Install: pip install curl-cffi
try:
    from curl_cffi.requests import Session as CurlSession
    _CURL_CFFI_AVAILABLE = True
except ImportError:
    import requests  # fallback — will likely 403 on NSE
    _CURL_CFFI_AVAILABLE = False
    print(
        "[WARN] curl_cffi not installed — NSE requests will use plain `requests` "
        "and may be blocked (403).  Run: pip install curl-cffi"
    )

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

# ---------------------------------------------------------------------------
# NSE API client
# NSE requires a valid browser-like session (cookies are set on the homepage
# visit) before the JSON API endpoints will respond with data instead of a
# 401 / empty body.  We keep ONE session per MarketDataTools instance and
# refresh cookies lazily when they expire (indicated by a non-200 response
# or an empty "data" key).
# ---------------------------------------------------------------------------
NSE_BASE_URL = "https://www.nseindia.com"

NSE_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept":          "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer":         "https://www.nseindia.com/",
    "Connection":      "keep-alive",
}

# Fields from the NSE JSON we surface in structured_data; extend freely.
NSE_FIELD_MAP = {
    # Top-level priceInfo keys
    "lastPrice":          "last_price",
    "open":               "open",
    "close":              "prev_close",
    "intraDayHighLow":    None,           # dict – handled specially below
    "weekHighLow":        None,           # dict – handled specially below
    "change":             "change",
    "pChange":            "change_pct",
    "totalTradedVolume":  "volume",
    "totalTradedValue":   "traded_value",
    "vmap":               "vwap",
    "ffmc":               "ff_market_cap",
    "yearHigh":           "year_high",    # sometimes top-level
    "yearLow":            "year_low",
}


# ---------------------------------------------------------------------------
# Timing helper — wraps any callable and prints elapsed ms
# ---------------------------------------------------------------------------
def _timed(label: str, fn, *args, **kwargs):
    t0 = time.perf_counter()
    try:
        result = fn(*args, **kwargs)
        elapsed = (time.perf_counter() - t0) * 1000
        print(f"[TIMING] {label} → {elapsed:.0f} ms  ✅")
        return result
    except Exception as e:
        elapsed = (time.perf_counter() - t0) * 1000
        print(f"[TIMING] {label} → {elapsed:.0f} ms  ❌ {e}")
        raise


class MarketDataTools:
    """Tools for fetching market data and financial information."""

    print("Initializing MarketDataTools with Firecrawl + NSE API integration...")

    TRUSTED_SOURCES: Dict[str, str] = {
        "nse":              "https://www.nseindia.com",
        "bse":              "https://www.bseindia.com",
        "moneycontrol":     "https://www.moneycontrol.com",
        "screener":         "https://www.screener.in",
        "economictimes":    "https://economictimes.indiatimes.com",
        "livemint":         "https://www.livemint.com",
        "reuters":          "https://www.reuters.com",
        "businessstandard": "https://www.business-standard.com",
        "investing":        "https://www.investing.com",
        "rbi":              "https://www.rbi.org.in",
        "indiabudget":      "https://www.indiabudget.gov.in",
    }

    def __init__(self):
        """Initialize market data tools."""
        # ── Firecrawl ──────────────────────────────────────────────────────
        self.api_key = os.getenv("FIRECRAWL_API_KEY")
        print(f"[INIT] FIRECRAWL_API_KEY from env: {self.api_key}")

        if self.api_key:
            try:
                self.firecrawl = FirecrawlApp(api_key=self.api_key)
                print("[INIT] FirecrawlApp initialized successfully")
            except Exception as e:
                print(f"[INIT] FirecrawlApp initialization failed: {e}")
                self.firecrawl = None
        else:
            print("[INIT] FIRECRAWL_API_KEY not found in environment")
            self.firecrawl = None

        # ── NSE session ────────────────────────────────────────────────────
        # Session is a curl_cffi.Session (Chrome TLS fingerprint) when available,
        # else a plain requests.Session (may 403 on NSE bot-detection).
        self._nse_session = None
        self._nse_session_ts: float = 0.0   # epoch seconds of last warm-up
        self._NSE_SESSION_TTL: float = 300.0  # refresh cookies every 5 min

        self.cache: Dict[str, Any] = {}

    # ------------------------------------------------------------------
    # NSE session management
    # ------------------------------------------------------------------
    def _get_nse_session(self, force_refresh: bool = False):
        """
        Return a warmed-up session with valid NSE cookies.

        Why curl_cffi?
        NSE (and its CDN — Cloudflare / Akamai) performs TLS fingerprint
        checks (JA3/JA3S).  Plain `requests` / urllib3 has a well-known
        Python TLS signature that is blocked with 403.  curl_cffi wraps
        libcurl compiled with BoringSSL and replays Chrome's exact TLS
        ClientHello, including cipher suites, extensions, and GREASE
        values — making the connection indistinguishable from a real
        Chrome browser at the network layer.

        The homepage visit sets NSE's session + nseappid cookies that
        the API endpoint requires.  We reuse the same session object for
        all subsequent calls so cookies persist automatically.
        """
        now = time.time()
        session_stale = (now - self._nse_session_ts) > self._NSE_SESSION_TTL

        if force_refresh or self._nse_session is None or session_stale:
            print(
                "[NSE] Warming up session "
                f"({'curl_cffi/Chrome' if _CURL_CFFI_AVAILABLE else 'requests (fallback)'})…"
            )
            t0 = time.perf_counter()
            try:
                if _CURL_CFFI_AVAILABLE:
                    # impersonate="chrome120" replays Chrome 120's TLS fingerprint.
                    # The session keeps cookies automatically between requests.
                    session = CurlSession(impersonate="chrome120")
                    resp = session.get(
                        NSE_BASE_URL,
                        headers=NSE_HEADERS,
                        timeout=10,
                    )
                else:
                    import requests as _req
                    session = _req.Session()
                    session.headers.update(NSE_HEADERS)
                    resp = session.get(NSE_BASE_URL, timeout=10)

                elapsed = (time.perf_counter() - t0) * 1000
                if resp.status_code == 200:
                    print(
                        f"[NSE]   Homepage → {resp.status_code} ({elapsed:.0f} ms) ✅  "
                        f"cookies: {list(session.cookies.keys())}"
                    )
                    self._nse_session = session
                    self._nse_session_ts = now
                else:
                    print(
                        f"[NSE]   Homepage → {resp.status_code} ({elapsed:.0f} ms) ⚠️  "
                        "(session may not have valid cookies)"
                    )
                    self._nse_session = session   # keep it; API call will surface the issue

            except Exception as e:
                elapsed = (time.perf_counter() - t0) * 1000
                print(f"[NSE]   Homepage warm-up exception ({elapsed:.0f} ms): {e}")
                # Best-effort: store whatever we have so the caller can try the API
                if self._nse_session is None:
                    if _CURL_CFFI_AVAILABLE:
                        self._nse_session = CurlSession(impersonate="chrome120")
                    else:
                        import requests as _req
                        self._nse_session = _req.Session()
                        self._nse_session.headers.update(NSE_HEADERS)

        return self._nse_session

    # ------------------------------------------------------------------
    # NSE API — primary data source for equity quotes
    # ------------------------------------------------------------------
    def fetch_nse_quote(
        self,
        symbol: str,
        *,
        force_session_refresh: bool = False,
    ) -> Dict[str, Any]:
        """
        Fetch a live equity quote from NSE's internal JSON API.

        Endpoint:
            GET https://www.nseindia.com/api/quote-equity?symbol=<SYMBOL>

        Returns a rich dict that includes:
            price, open, prev_close, day_high/low, 52w high/low,
            volume, traded value, VWAP, market cap, P/E, sector,
            delivery %, order book depth, and more.

        Args:
            symbol:                NSE ticker (e.g. "TENNIND", "TCS").
            force_session_refresh: Pass True to force a new cookie handshake.

        Returns:
            {
                "success":         bool,
                "symbol":          str,
                "source":          "nse_api",
                "url":             str,
                "raw":             dict,           # full NSE JSON payload
                "structured_data": dict,           # flattened, labelled fields
                "elapsed_ms":      float,
                "timestamp":       str (ISO-8601),
                # on failure:
                "error":           str,
            }
        """
        symbol = symbol.upper()
        url    = f"{NSE_BASE_URL}/api/quote-equity?symbol={symbol}"
        print(f"[NSE] fetch_nse_quote() → {url}")

        session = self._get_nse_session(force_refresh=force_session_refresh)
        t0      = time.perf_counter()

        try:
            resp    = session.get(url, headers=NSE_HEADERS, timeout=10)
            elapsed = (time.perf_counter() - t0) * 1000
            print(f"[NSE]   API response: {resp.status_code}  ({elapsed:.0f} ms)")

            # NSE returns 401 when cookies are stale — refresh once and retry.
            if resp.status_code == 401 and not force_session_refresh:
                print("[NSE]   Got 401 — refreshing session and retrying…")
                return self.fetch_nse_quote(symbol, force_session_refresh=True)

            resp.raise_for_status()

            # Guard against empty body — happens when homepage 403'd and
            # cookies were never set, so the API silently returns nothing.
            body = resp.text.strip()
            if not body:
                raise ValueError(
                    "NSE API returned an empty response body. "
                    "This usually means the homepage cookie handshake failed "
                    "(bot-detection / 403). Ensure curl_cffi is installed: "
                    "pip install curl-cffi"
                )

            raw: Dict[str, Any] = resp.json()

        except Exception as e:
            elapsed = (time.perf_counter() - t0) * 1000
            print(f"[NSE]   ❌ Request failed ({elapsed:.0f} ms): {e}")
            return {
                "success":    False,
                "symbol":     symbol,
                "source":     "nse_api",
                "url":        url,
                "error":      str(e),
                "elapsed_ms": round(elapsed, 1),
                "timestamp":  datetime.now().isoformat(),
            }

        structured = self._parse_nse_quote(raw, symbol)

        return {
            "success":         True,
            "symbol":          symbol,
            "source":          "nse_api",
            "url":             url,
            "raw":             raw,
            "structured_data": structured,
            "elapsed_ms":      round(elapsed, 1),
            "timestamp":       datetime.now().isoformat(),
        }

    def _parse_nse_quote(
        self, raw: Dict[str, Any], symbol: str
    ) -> Dict[str, Any]:
        """
        Flatten and label the NSE JSON response into a clean dict.

        NSE's quote-equity payload has this rough shape:
        {
          "info":       { companyName, industry, isin, … },
          "metadata":   { series, status, listingDate, … },
          "priceInfo":  { lastPrice, open, close, change, pChange,
                          intraDayHighLow: {min, max, value},
                          weekHighLow:     {min, max, …},
                          vmap, totalTradedVolume, totalTradedValue, … },
          "industryInfo":{ macro, sector, industry, basicIndustry },
          "securityInfo": { boardStatus, tradingStatus, … },
          "tradeInfo":  { totalTradedVolume, totalTradedValue,
                          deliveryQuantity, deliveryToTradedQuantity, … },
          "priceband":  { upperBand, lowerBand },
          "marketDeptOrderBook": {
              "totalBuyQuantity", "totalSellQuantity",
              "bid": [{price, quantity}, …],
              "ask": [{price, quantity}, …],
          }
        }
        """
        out: Dict[str, Any] = {"symbol": symbol, "source": "nse_api"}

        # ── Company / listing info ─────────────────────────────────────
        info = raw.get("info", {})
        out["company_name"]  = info.get("companyName")
        out["isin"]          = info.get("isin")
        out["series"]        = info.get("series", raw.get("metadata", {}).get("series"))
        out["listing_date"]  = raw.get("metadata", {}).get("listingDate")
        out["trading_status"]= raw.get("metadata", {}).get("status")

        # ── Industry / sector ─────────────────────────────────────────
        ind = raw.get("industryInfo", {})
        out["sector"]         = ind.get("sector")
        out["industry"]       = ind.get("industry")
        out["basic_industry"] = ind.get("basicIndustry")

        # ── Price info ────────────────────────────────────────────────
        # Field names confirmed against live NSE JSON payload (Mar 2026).
        pi = raw.get("priceInfo", {})
        out["last_price"]  = self._to_float(pi.get("lastPrice"))
        out["open"]        = self._to_float(pi.get("open"))
        # NSE returns TWO close fields:
        #   "close"         = previous trading session close (used for change calc)
        #   "previousClose" = same value but more explicitly named
        # We use previousClose when available, fall back to close.
        out["prev_close"]  = self._to_float(pi.get("previousClose") or pi.get("close"))
        out["change"]      = self._to_float(pi.get("change"))
        out["change_pct"]  = self._to_float(pi.get("pChange"))
        # VWAP key is literally "vwap" in the NSE payload (not "vmap").
        out["vwap"]        = self._to_float(pi.get("vwap"))
        # PE is in metadata as pdSymbolPe (string "NA" when not available).
        md = raw.get("metadata", {})
        pe_raw = md.get("pdSymbolPe")
        out["pe_ratio"]    = self._to_float(pe_raw) if pe_raw not in (None, "NA", "") else None

        # Intraday high/low (nested dict)
        idhl = pi.get("intraDayHighLow", {}) or {}
        out["day_high"] = self._to_float(idhl.get("max"))
        out["day_low"]  = self._to_float(idhl.get("min"))

        # 52-week high/low (nested dict)
        whl = pi.get("weekHighLow", {}) or {}
        out["week_52_high"] = self._to_float(whl.get("max"))
        out["week_52_low"]  = self._to_float(whl.get("min"))
        out["week_52_high_date"] = whl.get("maxDate")
        out["week_52_low_date"]  = whl.get("minDate")

        # Circuit breaker bands — stored in priceInfo as string fields
        out["upper_band"] = self._to_float(pi.get("upperCP"))
        out["lower_band"] = self._to_float(pi.get("lowerCP"))

        # ── Trade / volume info ───────────────────────────────────────
        # For many SME / newly listed stocks, tradeInfo is absent.
        # Fall back to preOpenMarket.totalTradedVolume when needed.
        ti  = raw.get("tradeInfo", {}) or {}
        pom = raw.get("preOpenMarket", {}) or {}
        out["volume"]       = self._to_float(
            ti.get("totalTradedVolume")
            or pi.get("totalTradedVolume")
            or pom.get("totalTradedVolume")
        )
        out["traded_value"] = self._to_float(
            ti.get("totalTradedValue") or pi.get("totalTradedValue")
        )
        out["delivery_qty"] = self._to_float(ti.get("deliveryQuantity"))
        out["delivery_pct"] = self._to_float(ti.get("deliveryToTradedQuantity"))
        out["ff_market_cap"]= self._to_float(pi.get("ffmc"))

        # ── Order book depth (top 5 bids / asks) ─────────────────────
        mdob = raw.get("marketDeptOrderBook", {}) or {}
        out["total_buy_qty"]  = self._to_float(mdob.get("totalBuyQuantity"))
        out["total_sell_qty"] = self._to_float(mdob.get("totalSellQuantity"))
        out["bids"] = [
            {"price": self._to_float(b.get("price")), "qty": self._to_float(b.get("quantity"))}
            for b in (mdob.get("bid") or [])[:5]
        ]
        out["asks"] = [
            {"price": self._to_float(a.get("price")), "qty": self._to_float(a.get("quantity"))}
            for a in (mdob.get("ask") or [])[:5]
        ]

        return out

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _to_float(self, value: Any) -> Optional[float]:
        """Convert numeric-like string values into floats safely."""
        if value is None:
            return None
        text = str(value).strip().replace(",", "")
        match = re.search(r"-?\d+(?:\.\d+)?", text)
        if not match:
            return None
        try:
            return float(match.group(0))
        except (TypeError, ValueError):
            return None

    def _extract_json_array_block(self, text: str, start_token: str) -> Optional[str]:
        """Extract a balanced JSON array string starting from a token."""
        start = text.find(start_token)
        if start == -1:
            return None

        depth = 0
        for idx in range(start, len(text)):
            ch = text[idx]
            if ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    return text[start:idx + 1]

        return None

    def _extract_stock_insights(
        self, markdown: str, symbol: str, source: str
    ) -> Dict[str, Any]:
        """Extract structured stock insights from noisy markdown."""
        insights: Dict[str, Any] = {
            "symbol":           symbol,
            "source":           source,
            "sector":           None,
            "industry":         None,
            "technical_rating": None,
            "swot":             {},
            "financials":       {},
            "financial_summary": {},
            "warnings":         [],
        }

        sector_match = re.search(r"Sector\s*:\s*\*\*([^*|\n]+)", markdown, re.IGNORECASE)
        if sector_match:
            sector = sector_match.group(1).strip().strip("[]")
            if sector and "details" not in sector.lower():
                insights["sector"] = sector

        industry_match = re.search(r"Industry\s*:\s*\*\*([^*|\n]+)", markdown, re.IGNORECASE)
        if industry_match:
            industry = industry_match.group(1).strip().strip("[]")
            if industry and "details" not in industry.lower():
                insights["industry"] = industry

        trend_match = re.search(r"Trend\s*\[([A-Z\s]+)\]", markdown)
        if trend_match:
            insights["technical_rating"] = trend_match.group(1).strip()

        swot_patterns = {
            "strengths":     r"\*\*Strengths\s*\((\d+)\)\*\*\s*_([^_]+)_",
            "weaknesses":    r"\*\*Weaknesses\s*\((\d+)\)\*\*\s*_([^_]+)_",
            "opportunities": r"\*\*Opportunities\s*\((\d+)\)\*\*\s*_([^_]+)_",
            "threats":       r"\*\*Threats\s*\((\d+)\)\*\*\s*_([^_]+)_",
        }
        for key, pattern in swot_patterns.items():
            match = re.search(pattern, markdown, re.IGNORECASE)
            if match:
                insights["swot"][key] = {
                    "count":     int(match.group(1)),
                    "highlight": match.group(2).strip(),
                }

        cleaned = (
            markdown.replace("\\\\/", "/")
            .replace("\\\\[", "[")
            .replace("\\\\]", "]")
            .replace('\\\\"', '"')
        )
        financial_block = self._extract_json_array_block(cleaned, '[{"heading":')

        if financial_block:
            try:
                financial_rows = json.loads(financial_block)
                normalized_financials: Dict[str, List[Dict[str, Any]]] = {}

                for row in financial_rows:
                    heading     = str(row.get("heading", "")).strip().lower().replace(" ", "_")
                    data_points = row.get("data", [])
                    points: List[Dict[str, Any]] = []
                    if isinstance(data_points, list):
                        for point in data_points:
                            points.append({
                                "year":            point.get("year"),
                                "value":           self._to_float(point.get("value")),
                                "formatted_value": point.get("formattedValue"),
                            })
                    if heading:
                        normalized_financials[heading] = points

                insights["financials"] = normalized_financials

                summary: Dict[str, Any] = {}
                for metric in ["revenue", "net_profit", "eps", "roe"]:
                    values = [
                        p.get("value")
                        for p in normalized_financials.get(metric, [])
                        if p.get("value") is not None
                    ]
                    if not values:
                        continue
                    summary[f"{metric}_latest"] = values[-1]
                    if len(values) >= 2 and values[0] not in (0, None):
                        summary[f"{metric}_growth_pct"] = round(
                            ((values[-1] - values[0]) / abs(values[0])) * 100, 2
                        )

                insights["financial_summary"] = summary
            except Exception as e:
                insights["warnings"].append(f"Failed to parse embedded financial JSON: {e}")
        else:
            insights["warnings"].append("No embedded financial JSON block found.")

        if "The requested URL returned error: 422" in markdown:
            insights["warnings"].append(
                "Page contains partial-content warning (HTTP 422 marker found in body)."
            )

        return insights

    # ------------------------------------------------------------------
    # URL builder (used for non-NSE sources only)
    # ------------------------------------------------------------------
    def build_url(self, symbol: str, source: str) -> Optional[str]:
        """Construct the correct stock-page URL for symbol on source."""
        symbol = symbol.upper()
        meta   = SYMBOL_MAP.get(symbol)
        if meta is None:
            return None

        base = self.TRUSTED_SOURCES[source]

        if source == "nse":
            # Legacy web-page URL — kept for reference but prefer fetch_nse_quote()
            return f"{base}/get-quote/equity/{meta['nse_slug']}"
        if source == "bse":
            return f"{base}/stock-share-price/{meta['bse_slug']}/"
        if source == "screener":
            return f"{base}/company/{meta['screener_slug']}/consolidated/"
        if source == "moneycontrol":
            return f"{base}/india/stockpricequote/{meta['mc_slug']}"

        return None

    # ------------------------------------------------------------------
    # Core parallel fetch — replaces 3 sequential Firecrawl calls
    # ------------------------------------------------------------------
    def fetch_all_parallel(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch strategy — NSE API is primary; MoneyControl is fallback only.

        Phase 1 (always, 3 concurrent):
            fetch_nse_quote       — NSE JSON API (fast, clean, structured)
            fetch_company_news    — Economic Times via Firecrawl
            fetch_analyst_ratings — Screener via Firecrawl

        Phase 2 (only when NSE fails):
            scrape_stock_data (moneycontrol) — Firecrawl fallback, runs
            sequentially after Phase 1 so we never waste a credit on the
            happy path.

        Returns:
            {
                "stock_data":    dict,   NSE structured_data or MC fallback
                "news":          dict,
                "analyst_ratings": dict,
                "nse_quote":     dict,   full raw NSE result (always present)
                "price_source":  str,    "nse_api" | "moneycontrol_fallback"
                "elapsed_ms":    float,
            }
        """
        symbol = symbol.upper()
        print(f"\n[PARALLEL] Phase 1 — 3 concurrent requests for {symbol}")
        t0 = time.perf_counter()

        def _nse():
            t = time.perf_counter()
            try:
                result = self.fetch_nse_quote(symbol)
                print(f"[TIMING]   fetch_nse_quote       → {(time.perf_counter()-t)*1000:.0f} ms ✅")
                return result
            except Exception as e:
                print(f"[TIMING]   fetch_nse_quote       → {(time.perf_counter()-t)*1000:.0f} ms ❌ {e}")
                return {"success": False, "error": str(e)}

        def _news():
            t = time.perf_counter()
            try:
                result = self.fetch_company_news(symbol)
                print(f"[TIMING]   fetch_company_news    → {(time.perf_counter()-t)*1000:.0f} ms ✅")
                return result
            except Exception as e:
                print(f"[TIMING]   fetch_company_news    → {(time.perf_counter()-t)*1000:.0f} ms ❌ {e}")
                return {"success": False, "error": str(e)}

        def _ratings():
            t = time.perf_counter()
            try:
                result = self.fetch_analyst_ratings(symbol)
                print(f"[TIMING]   fetch_analyst_ratings → {(time.perf_counter()-t)*1000:.0f} ms ✅")
                return result
            except Exception as e:
                print(f"[TIMING]   fetch_analyst_ratings → {(time.perf_counter()-t)*1000:.0f} ms ❌ {e}")
                return {"success": False, "error": str(e)}

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            f_nse     = executor.submit(_nse)
            f_news    = executor.submit(_news)
            f_ratings = executor.submit(_ratings)

            nse_quote       = f_nse.result()
            news            = f_news.result()
            analyst_ratings = f_ratings.result()

        phase1_ms = (time.perf_counter() - t0) * 1000
        print(f"[PARALLEL] Phase 1 done — {phase1_ms:.0f} ms")

        # ── Phase 2: build stock_data from NSE or fall back to MoneyControl ──
        if nse_quote.get("success"):
            nse_sd = nse_quote.get("structured_data", {})
            stock_data = {
                "success":         True,
                "symbol":          symbol,
                "source":          "nse_api",
                "structured_data": nse_sd,
                "data":            nse_quote.get("raw"),
                "elapsed_ms":      nse_quote.get("elapsed_ms"),
                "timestamp":       nse_quote.get("timestamp"),
            }
            price_source = "nse_api"
            print(
                f"[PARALLEL] ✅ NSE OK — "
                f"last_price={nse_sd.get('last_price')}, "
                f"volume={nse_sd.get('volume')}, "
                f"pe={nse_sd.get('pe_ratio')} "
                f"— skipping MoneyControl"
            )
        else:
            nse_err = nse_quote.get("error", "unknown error")
            print(
                f"[PARALLEL] ⚠️  NSE failed ({nse_err}) "
                f"— Phase 2: falling back to MoneyControl Firecrawl scrape"
            )
            t2 = time.perf_counter()
            try:
                stock_data = self.scrape_stock_data(symbol, source="moneycontrol")
                print(
                    f"[TIMING]   scrape_stock_data (MC fallback) "
                    f"→ {(time.perf_counter()-t2)*1000:.0f} ms ✅"
                )
            except Exception as e:
                print(f"[TIMING]   scrape_stock_data (MC fallback) ❌ {e}")
                stock_data = {"success": False, "error": str(e)}
            stock_data["nse_error"] = nse_err
            price_source = "moneycontrol_fallback"

        total_ms = (time.perf_counter() - t0) * 1000
        print(
            f"[PARALLEL] All done — {total_ms:.0f} ms | "
            f"price_source={price_source}\n"
        )

        return {
            "stock_data":      stock_data,
            "news":            news,
            "analyst_ratings": analyst_ratings,
            "nse_quote":       nse_quote,
            "price_source":    price_source,
            "elapsed_ms":      round(total_ms, 1),
        }

    # ------------------------------------------------------------------
    # Individual fetch methods
    # ------------------------------------------------------------------
    def scrape_stock_data(
        self, symbol: str, source: str = "moneycontrol"
    ) -> Dict[str, Any]:
        """
        Fetch stock data from a trusted source.

        For NSE:  uses the JSON API (fetch_nse_quote) — fast, structured,
                  no Firecrawl credits consumed.
        For other sources: falls back to Firecrawl markdown scraping as before.
        """
        print(f"[SCRAPER] scrape_stock_data() called for {symbol} from {source}")
        symbol = symbol.upper()

        # ── Route NSE requests to the JSON API ────────────────────────
        if source == "nse":
            return self.fetch_nse_quote(symbol)

        # ── All other sources: Firecrawl ──────────────────────────────
        if not self.firecrawl:
            print("[DEBUG] Firecrawl not initialized in scrape_stock_data()")
            return {"error": "Firecrawl not initialized"}

        if source not in self.TRUSTED_SOURCES:
            return {"error": f"Source '{source}' not in trusted sources"}

        url = self.build_url(symbol, source)
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
            print(f"[SCRAPER] → Firecrawl scrape start: {symbol} / {source}")
            t0     = time.perf_counter()
            result = self.firecrawl.scrape(url, formats=["markdown"])
            elapsed = (time.perf_counter() - t0) * 1000
            print(f"[TIMING]   firecrawl.scrape ({source}) → {elapsed:.0f} ms")

            if not result or not result.markdown:
                print(f"[ERROR] Empty response from Firecrawl for {symbol}")
                return {
                    "success": False,
                    "error":   "Empty response from Firecrawl",
                    "symbol":  symbol,
                    "source":  source,
                    "url":     url,
                }

            markdown = result.markdown
            print(f"[SCRAPER] Scraped markdown length: {len(markdown)} characters")
            print(f"[SCRAPER] Preview (first 500 chars):\n{markdown[:500]}\n...")

            t1              = time.perf_counter()
            structured_data = self._extract_stock_insights(markdown, symbol, source)
            print(f"[TIMING]   _extract_stock_insights → {(time.perf_counter()-t1)*1000:.0f} ms")
            print(f"[SCRAPER] Structured fields extracted: {list(structured_data.keys())}")

            return {
                "success":         True,
                "symbol":          symbol,
                "source":          source,
                "url":             url,
                "data":            markdown,
                "structured_data": structured_data,
                "data_length":     len(markdown),
                "elapsed_ms":      round(elapsed, 1),
                "timestamp":       datetime.now().isoformat(),
            }
        except Exception as e:
            print(f"[ERROR] Exception in scrape_stock_data: {e}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": str(e)}

    def fetch_company_news(self, symbol: str) -> Dict[str, Any]:
        """Fetch company news from Economic Times."""
        print(f"[NEWS] fetch_company_news() called for {symbol}")
        if not self.firecrawl:
            print("[DEBUG] Firecrawl not initialized in fetch_company_news()")
            return {"error": "Firecrawl not initialized"}

        url = f"https://economictimes.indiatimes.com/markets/stocks/news/{symbol.lower()}"
        try:
            print(f"[NEWS] → Firecrawl scrape start: {symbol} / economictimes")
            t0      = time.perf_counter()
            result  = self.firecrawl.scrape(url, formats=["markdown"])
            elapsed = (time.perf_counter() - t0) * 1000
            print(f"[TIMING]   firecrawl.scrape (economictimes) → {elapsed:.0f} ms")
            print(f"[NEWS] Preview: {result.markdown[:200]}...")

            return {
                "success":    True,
                "symbol":     symbol,
                "news":       result.markdown,
                "elapsed_ms": round(elapsed, 1),
                "timestamp":  datetime.now().isoformat(),
            }
        except Exception as e:
            print(f"[ERROR] Exception in fetch_company_news: {e}")
            return {"success": False, "error": str(e)}

    def fetch_analyst_ratings(self, symbol: str) -> Dict[str, Any]:
        """Fetch analyst ratings from Screener."""
        print(f"[RATINGS] fetch_analyst_ratings() called for {symbol}")
        if not self.firecrawl:
            print("[DEBUG] Firecrawl not initialized in fetch_analyst_ratings()")
            return {"error": "Firecrawl not initialized"}

        url = f"https://www.screener.in/company/{symbol}/"
        try:
            print(f"[RATINGS] → Firecrawl scrape start: {symbol} / screener")
            t0      = time.perf_counter()
            result  = self.firecrawl.scrape(url, formats=["markdown"])
            elapsed = (time.perf_counter() - t0) * 1000
            print(f"[TIMING]   firecrawl.scrape (screener) → {elapsed:.0f} ms")
            print(f"[RATINGS] Preview: {result.markdown[:200]}...")

            return {
                "success":    True,
                "symbol":     symbol,
                "ratings":    result.markdown,
                "elapsed_ms": round(elapsed, 1),
                "timestamp":  datetime.now().isoformat(),
            }
        except Exception as e:
            print(f"[ERROR] Exception in fetch_analyst_ratings: {e}")
            return {"success": False, "error": str(e)}

    def fetch_financial_reports(self, symbol: str) -> Dict[str, Any]:
        """Fetch financial reports from BSE."""
        print(f"[REPORTS] fetch_financial_reports() called for {symbol}")
        if not self.firecrawl:
            print("[DEBUG] Firecrawl not initialized in fetch_financial_reports()")
            return {"error": "Firecrawl not initialized"}

        url = f"https://www.bseindia.com/stock-share-price/{symbol}"
        try:
            t0      = time.perf_counter()
            result  = self.firecrawl.scrape(url, formats=["markdown"])
            elapsed = (time.perf_counter() - t0) * 1000
            print(f"[TIMING]   firecrawl.scrape (bse reports) → {elapsed:.0f} ms")
            print(f"[REPORTS] Preview: {result.markdown[:200]}...")

            return {
                "success":    True,
                "symbol":     symbol,
                "reports":    result.markdown,
                "elapsed_ms": round(elapsed, 1),
                "timestamp":  datetime.now().isoformat(),
            }
        except Exception as e:
            print(f"[ERROR] Exception in fetch_financial_reports: {e}")
            return {"success": False, "error": str(e)}

    def fetch_sector_performance(self, sector: str) -> Dict[str, Any]:
        """Fetch sector performance data."""
        print(f"[SECTOR] fetch_sector_performance() called for {sector}")
        if not self.firecrawl:
            print("[DEBUG] Firecrawl not initialized in fetch_sector_performance()")
            return {"error": "Firecrawl not initialized"}

        url = f"https://www.moneycontrol.com/stocks/sectors/{sector.lower()}"
        try:
            t0      = time.perf_counter()
            result  = self.firecrawl.scrape(url, formats=["markdown"])
            elapsed = (time.perf_counter() - t0) * 1000
            print(f"[TIMING]   firecrawl.scrape (sector) → {elapsed:.0f} ms")
            print(f"[SECTOR] Preview: {result.markdown[:200]}...")

            return {
                "success":     True,
                "sector":      sector,
                "performance": result.markdown,
                "elapsed_ms":  round(elapsed, 1),
                "timestamp":   datetime.now().isoformat(),
            }
        except Exception as e:
            print(f"[ERROR] Exception in fetch_sector_performance: {e}")
            return {"success": False, "error": str(e)}

    def fetch_economic_news(self) -> Dict[str, Any]:
        """Fetch economic news and RBI updates — sources run in parallel."""
        print("[ECONOMIC] fetch_economic_news() called")
        if not self.firecrawl:
            print("[DEBUG] Firecrawl not initialized in fetch_economic_news()")
            return {"error": "Firecrawl not initialized"}

        urls = [
            "https://www.rbi.org.in/scripts/",
            "https://www.indiabudget.gov.in",
            "https://www.livemint.com/news",
        ]

        t0_total = time.perf_counter()

        def _fetch_url(url):
            t = time.perf_counter()
            try:
                result  = self.firecrawl.scrape(url, formats=["markdown"])
                elapsed = (time.perf_counter() - t) * 1000
                print(f"[TIMING]   firecrawl.scrape ({url}) → {elapsed:.0f} ms ✅")
                return {"source": url, "content": result.markdown, "elapsed_ms": round(elapsed, 1)}
            except Exception as e:
                elapsed = (time.perf_counter() - t) * 1000
                print(f"[TIMING]   firecrawl.scrape ({url}) → {elapsed:.0f} ms ❌ {e}")
                return {"source": url, "content": "", "error": str(e)}

        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=len(urls)) as executor:
                news_data = list(executor.map(_fetch_url, urls))

            total_ms = (time.perf_counter() - t0_total) * 1000
            print(f"[TIMING]   fetch_economic_news total → {total_ms:.0f} ms")

            return {
                "success":       True,
                "economic_news": news_data,
                "elapsed_ms":    round(total_ms, 1),
                "timestamp":     datetime.now().isoformat(),
            }
        except Exception as e:
            print(f"[ERROR] Exception in fetch_economic_news: {e}")
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