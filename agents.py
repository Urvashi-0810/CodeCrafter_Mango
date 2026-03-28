import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class Agent:
    """Represents a collaborative agent using Google Gemini"""
    
    def __init__(self, name: str, system_message: str, model: str = "gemini-pro"):
        """Initialize an agent"""
        self.name = name
        self.system_message = system_message
        self.model = model
        self.model_instance = genai.GenerativeModel(
            model_name=model,
            system_instruction=system_message
        )
        self.chat_history = []
    
    def send_message(self, message: str):
        """Send a message and get response"""
        try:
            self.chat_history.append({"role": "user", "parts": message})
            response = self.model_instance.generate_content(message)
            self.chat_history.append({"role": "assistant", "parts": response.text})
            return response.text
        except Exception as e:
            raise Exception(f"Error in agent {self.name}: {str(e)}")


class CollaborativeAgents:
    """Manages collaborative agents using Google Gemini"""
    
    def __init__(self, api_key: str = None, model: str = "gemini-pro"):
        """Initialize collaborative agents manager"""
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.model = model
        self.agents = []
        self.conversation_history = []
        
        # Configure Gemini API
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
    
    def create_agent(self, name: str, system_message: str):
        """Create a new collaborative agent"""
        agent = Agent(name=name, system_message=system_message, model=self.model)
        self.agents.append(agent)
        return agent
    
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
