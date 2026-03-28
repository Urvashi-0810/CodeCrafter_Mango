import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from tools.portfolio_tools import PortfolioParsingTools

load_dotenv()


class PortfolioAgent:
    """Agent for handling portfolio input and parsing"""
    
    def __init__(self, api_key: str = None, model: str = "gemini-pro"):
        self.name = "Portfolio Agent"
        self.model = model
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.model_instance = genai.GenerativeModel(
            model_name=model,
            system_instruction="You are a portfolio parsing expert. Help users structure their investment portfolio data."
        )
        self.portfolio_tools = PortfolioParsingTools()
    
    def parse_portfolio_input(self, file_path: str, file_type: str) -> dict:
        """Parse portfolio from various file formats"""
        if file_type == "csv":
            return self.portfolio_tools.parse_csv(file_path)
        elif file_type == "pdf":
            return self.portfolio_tools.parse_pdf(file_path)
        elif file_type == "image":
            return self.portfolio_tools.parse_image_ocr(file_path)
        return {"error": f"Unsupported file type: {file_type}"}
    
    def format_portfolio(self, parsed_data: dict) -> dict:
        """Format parsed data into structured portfolio JSON"""
        return self.portfolio_tools.format_portfolio(parsed_data)
    
    def classify_holdings(self, holdings: list) -> dict:
        """Classify holdings by sector"""
        return self.portfolio_tools.classify_sectors(holdings)
