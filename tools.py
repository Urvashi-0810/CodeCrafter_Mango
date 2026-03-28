import os
from firecrawl import FirecrawlApp
from dotenv import load_dotenv

load_dotenv()


class WebScrapingTool:
    """Web scraping tool using Firecrawl for agent use"""
    
    def __init__(self, api_key: str = None):
        """Initialize the web scraping tool"""
        self.api_key = api_key or os.getenv("FIRECRAWL_API_KEY")
        if not self.api_key:
            raise ValueError("FIRECRAWL_API_KEY not found in environment variables")
        
        self.app = FirecrawlApp(api_key=self.api_key)
    
    def scrape_url(self, url: str, markdown: bool = True):
        """
        Scrape a URL and extract content
        
        Args:
            url: The URL to scrape
            markdown: Return content as markdown (default True)
        
        Returns:
            dict: Scraped content data
        """
        try:
            result = self.app.scrape_url(url, {"formats": ["markdown" if markdown else "html"]})
            return {
                "success": True,
                "url": url,
                "content": result.get("markdown") or result.get("html"),
                "metadata": result.get("metadata", {})
            }
        except Exception as e:
            return {
                "success": False,
                "url": url,
                "error": str(e)
            }
    
    def crawl_url(self, url: str, max_depth: int = 2, limit: int = 10):
        """
        Crawl a website and extract content from multiple pages
        
        Args:
            url: The base URL to crawl
            max_depth: Maximum depth to crawl
            limit: Maximum pages to crawl
        
        Returns:
            dict: Crawl results
        """
        try:
            result = self.app.crawl_url(
                url,
                {
                    "limit": limit,
                    "maxDepth": max_depth,
                    "scrapeOptions": {"formats": ["markdown"]}
                },
                wait_until_done=True
            )
            return {
                "success": True,
                "url": url,
                "pages_crawled": len(result) if isinstance(result, list) else 1,
                "data": result
            }
        except Exception as e:
            return {
                "success": False,
                "url": url,
                "error": str(e)
            }
    
    def extract_data(self, url: str, schema: dict = None):
        """
        Extract structured data from a URL using optional schema
        
        Args:
            url: The URL to extract from
            schema: Optional schema for structured extraction
        
        Returns:
            dict: Extracted data
        """
        try:
            options = {"formats": ["markdown"]}
            if schema:
                options["jsonSchema"] = schema
            
            result = self.app.scrape_url(url, options)
            return {
                "success": True,
                "url": url,
                "data": result
            }
        except Exception as e:
            return {
                "success": False,
                "url": url,
                "error": str(e)
            }


# Tool registry for agent use
TOOLS = {
    "scrape_url": {
        "description": "Scrape a single URL and extract its content in markdown format",
        "function": lambda tool, url: tool.scrape_url(url),
        "params": ["url"]
    },
    "crawl_website": {
        "description": "Crawl a website starting from a URL up to specified depth",
        "function": lambda tool, url, max_depth=2, limit=10: tool.crawl_url(url, max_depth, limit),
        "params": ["url", "max_depth", "limit"]
    },
    "extract_data": {
        "description": "Extract structured data from a URL",
        "function": lambda tool, url, schema=None: tool.extract_data(url, schema),
        "params": ["url", "schema"]
    }
}
