import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from tools.analysis_tools import AnalysisTools

load_dotenv()


class RecommendationAgent:
    """Main AI advisor agent for portfolio recommendations"""
    
    def __init__(self, api_key: str = None, model: str = "gemini-pro"):
        self.name = "Recommendation Agent"
        self.model = model
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.model_instance = genai.GenerativeModel(
            model_name=model,
            system_instruction="""You are an expert investment advisor. Based on portfolio analysis, market data, 
            and sentiment, provide specific and actionable portfolio recommendations. Consider risk profile, 
            diversification, sector performance, and regulations."""
        )
        self.analysis_tools = AnalysisTools()
    
    def generate_recommendations(self, portfolio: dict, market_data: dict, analysis: dict) -> str:
        """Generate portfolio recommendations based on analysis and market data"""
        prompt = f"""
Based on this portfolio analysis and market data, provide specific recommendations:
Portfolio Analysis: {analysis}
Market Data Summary: {market_data}

Provide recommendations on:
1. Stocks to add, remove, or reduce exposure
2. Sector diversification improvements
3. Mutual fund allocation
4. Gold and bond allocation
5. Risk reduction strategies
6. Buy/sell timing suggestions
"""
        response = self.model_instance.generate_content(prompt)
        return response.text
    
    def assess_risk_profile(self, portfolio: dict, user_risk_tolerance: str) -> dict:
        """Assess if portfolio matches user's risk profile"""
        analysis = self.analysis_tools.generate_analysis_report(portfolio)
        portfolio_risk = analysis["risk_score"]
        
        risk_mapping = {
            "conservative": {"min": 0, "max": 30},
            "moderate": {"min": 30, "max": 60},
            "aggressive": {"min": 60, "max": 100}
        }
        
        tolerance_range = risk_mapping.get(user_risk_tolerance, {"min": 30, "max": 60})
        
        is_aligned = tolerance_range["min"] <= portfolio_risk <= tolerance_range["max"]
        
        return {
            "user_risk_tolerance": user_risk_tolerance,
            "portfolio_risk_score": portfolio_risk,
            "aligned": is_aligned,
            "adjustment_needed": "" if is_aligned else f"Risk level should be adjusted to {tolerance_range}"
        }
