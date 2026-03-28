import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from tools.analysis_tools import AnalysisTools

load_dotenv()


class AnalysisAgent:
    """Agent for portfolio analysis and metrics calculation"""
    
    def __init__(self, api_key: str = None, model: str = "gemini-pro"):
        self.name = "Analysis Agent"
        self.model = model
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.model_instance = genai.GenerativeModel(
            model_name=model,
            system_instruction="You are a financial analyst. Explain portfolio metrics and insights clearly."
        )
        self.analysis_tools = AnalysisTools()
    
    def analyze_portfolio(self, portfolio: dict) -> dict:
        """Generate comprehensive portfolio analysis"""
        return self.analysis_tools.generate_analysis_report(portfolio)
    
    def calculate_metrics(self, portfolio: dict) -> dict:
        """Calculate key portfolio metrics"""
        # print(f"Calculating portfolio metrics for portfolio: {portfolio}")
        return {
            "total_investment": self.analysis_tools.calculate_total_investment(portfolio),
            "current_value": self.analysis_tools.calculate_current_value(portfolio),
            "profit_loss": self.analysis_tools.calculate_profit_loss(portfolio),
            "sector_allocation": self.analysis_tools.calculate_sector_allocation(portfolio),
            "asset_allocation": self.analysis_tools.calculate_asset_allocation(portfolio),
            "risk_score": self.analysis_tools.calculate_risk_score(portfolio),
            "diversification_score": self.analysis_tools.calculate_diversification_score(portfolio),
            "concentration_risk": self.analysis_tools.calculate_concentration_risk(portfolio),
            "health_score": self.analysis_tools.calculate_portfolio_health_score(portfolio)
        }
    
    def explain_analysis(self, analysis_report: dict) -> str:
        """Use LLM to explain analysis results"""
        prompt = f"Explain this portfolio analysis in simple terms: {analysis_report}"
        response = self.model_instance.generate_content(prompt)
        return response.text
