import os
import google.generativeai as genai
from dotenv import load_dotenv
from tools import WebScrapingTool, TOOLS

load_dotenv()

class Agent:
    """Represents a collaborative agent using Google Gemini with tools"""
    
    def __init__(self, name: str, system_message: str, model: str = "gemini-pro", enable_tools: bool = True):
        """Initialize an agent with optional tool support"""
        self.name = name
        self.system_message = system_message
        self.model = model
        self.model_instance = genai.GenerativeModel(
            model_name=model,
            system_instruction=system_message
        )
        self.chat_history = []
        self.enable_tools = enable_tools
        self.web_scraping_tool = None
        
        # Initialize web scraping tool if enabled
        if enable_tools:
            try:
                self.web_scraping_tool = WebScrapingTool()
            except ValueError as e:
                print(f"Warning: {e}. Web scraping tool will be unavailable.")
    
    def send_message(self, message: str):
        """Send a message and get response"""
        try:
            self.chat_history.append({"role": "user", "parts": message})
            response = self.model_instance.generate_content(message)
            self.chat_history.append({"role": "assistant", "parts": response.text})
            return response.text
        except Exception as e:
            raise Exception(f"Error in agent {self.name}: {str(e)}")
    
    def scrape_url(self, url: str):
        """Use web scraping tool to fetch content from a URL"""
        if not self.web_scraping_tool:
            return {"error": "Web scraping tool not initialized"}
        
        return self.web_scraping_tool.scrape_url(url)
    
    def crawl_website(self, url: str, max_depth: int = 2, limit: int = 10):
        """Use web scraping tool to crawl a website"""
        if not self.web_scraping_tool:
            return {"error": "Web scraping tool not initialized"}
        
        return self.web_scraping_tool.crawl_url(url, max_depth, limit)
    
    def extract_data(self, url: str, schema: dict = None):
        """Use web scraping tool to extract structured data"""
        if not self.web_scraping_tool:
            return {"error": "Web scraping tool not initialized"}
        
        return self.web_scraping_tool.extract_data(url, schema)
    
    def get_available_tools(self):
        """Get list of available tools for this agent"""
        if not self.enable_tools:
            return []
        
        return list(TOOLS.keys())


class CollaborativeAgents:
    """Manages collaborative agents using Google Gemini with tool support"""
    
    def __init__(self, api_key: str = None, model: str = "gemini-pro", enable_tools: bool = True):
        """Initialize collaborative agents manager with optional tool support"""
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.model = model
        self.agents = []
        self.conversation_history = []
        self.enable_tools = enable_tools
        
        # Configure Gemini API
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
    
    def create_agent(self, name: str, system_message: str, enable_tools: bool = None):
        """Create a new collaborative agent with optional tool support"""
        use_tools = enable_tools if enable_tools is not None else self.enable_tools
        agent = Agent(
            name=name,
            system_message=system_message,
            model=self.model,
            enable_tools=use_tools
        )
        self.agents.append(agent)
        return agent
    
    def get_agent_tools(self, agent_name: str):
        """Get available tools for a specific agent"""
        for agent in self.agents:
            if agent.name == agent_name:
                return agent.get_available_tools()
        return []
    
    def run_task(self, task: str):
        """Run a task with collaborative agents"""
        if not self.agents:
            raise ValueError("No agents created. Create agents first.")
        
        self.conversation_history = []
        
        # Initialize with task message
        self.conversation_history.append({
            "role": "user",
            "content": task,
            "timestamp": "initial"
        })
        
        # Run agents in sequence
        current_message = task
        for agent in self.agents:
            response = agent.send_message(current_message)
            self.conversation_history.append({
                "role": agent.name,
                "content": response,
                "timestamp": "agent_response"
            })
            current_message = response
        
        return self.conversation_history
    
    def get_conversation_history(self):
        """Get the conversation history"""
        return self.conversation_history
