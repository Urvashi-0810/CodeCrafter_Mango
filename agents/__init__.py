import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from agents.portfolio_agent import PortfolioAgent
from agents.market_agent import MarketDataAgent
from agents.analysis_agent import AnalysisAgent
from agents.recommendation_agent import RecommendationAgent
from agents.simulation_agent import SimulationAgent

load_dotenv()


class CollaborativeAgents:
    """Manager for all portfolio agents"""
    
    def __init__(self, api_key: str = None, model: str = "gemini-pro"):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.model = model
        
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found")
        
        genai.configure(api_key=self.api_key)
        
        # Initialize all agents
        self.portfolio_agent = PortfolioAgent(self.api_key, self.model)
        self.market_agent = MarketDataAgent(self.api_key, self.model)
        self.analysis_agent = AnalysisAgent(self.api_key, self.model)
        self.recommendation_agent = RecommendationAgent(self.api_key, self.model)
        self.simulation_agent = SimulationAgent(self.api_key, self.model)
        
        self.agents = [
            self.portfolio_agent,
            self.market_agent,
            self.analysis_agent,
            self.recommendation_agent,
            self.simulation_agent
        ]
    
    def get_agents_info(self) -> list:
        """Get information about all agents"""
        return [
            {
                "name": agent.name,
                "model": agent.model,
                "role": agent.__class__.__name__
            }
            for agent in self.agents
        ]


__all__ = [
    'PortfolioAgent',
    'MarketDataAgent',
    'AnalysisAgent',
    'RecommendationAgent',
    'SimulationAgent',
    'CollaborativeAgents'
]
