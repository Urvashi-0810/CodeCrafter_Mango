import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from tools.simulation_tools import SimulationTools

load_dotenv()


class SimulationAgent:
    """Agent for portfolio simulation and what-if analysis"""
    
    def __init__(self, api_key: str = None, model: str = "gemini-pro"):
        self.name = "Simulation Agent"
        self.model = model
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.model_instance = genai.GenerativeModel(
            model_name=model,
            system_instruction="You are a portfolio simulation expert. Explain portfolio modifications and comparisons clearly."
        )
        self.simulation_tools = SimulationTools()
    
    def modify_portfolio(self, portfolio: dict, modification: dict) -> dict:
        """Apply modification to portfolio"""
        action = modification.get("action")
        
        if action == "add_stock":
            return self.simulation_tools.add_stock(
                portfolio,
                modification.get("symbol"),
                modification.get("quantity"),
                modification.get("buy_price"),
                modification.get("current_price"),
                modification.get("sector")
            )
        elif action == "remove_stock":
            return self.simulation_tools.remove_stock(portfolio, modification.get("symbol"))
        elif action == "modify_quantity":
            return self.simulation_tools.modify_stock_quantity(
                portfolio,
                modification.get("symbol"),
                modification.get("quantity")
            )
        elif action == "add_mutual_fund":
            return self.simulation_tools.add_mutual_fund(
                portfolio,
                modification.get("name"),
                modification.get("investment"),
                modification.get("category")
            )
        elif action == "add_gold":
            return self.simulation_tools.add_gold(
                portfolio,
                modification.get("amount"),
                modification.get("grams"),
                modification.get("price_per_gram")
            )
        elif action == "change_risk_level":
            return self.simulation_tools.change_risk_level(
                portfolio,
                modification.get("risk_level")
            )
        
        return portfolio
    
    def simulate_returns(self, portfolio: dict, years: int, annual_return: float) -> dict:
        """Simulate portfolio returns over time"""
        return self.simulation_tools.simulate_returns(portfolio, years, annual_return)
    
    def compare_portfolios(self, original: dict, modified: dict) -> dict:
        """Compare original and modified portfolios"""
        return self.simulation_tools.compare_portfolios(original, modified)
    
    def explain_comparison(self, comparison: dict) -> str:
        """Use LLM to explain portfolio comparison"""
        prompt = f"""
Analyze this portfolio comparison and explain the key differences and improvements:
{comparison}

Highlight the main changes, improvements, and any concerns.
"""
        response = self.model_instance.generate_content(prompt)
        return response.text
