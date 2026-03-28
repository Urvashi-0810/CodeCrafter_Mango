from flask import Flask, jsonify, request
from config import config, FLASK_ENV, Config
from agents import CollaborativeAgents
import os

def create_app():
    """Flask application factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config.get(FLASK_ENV, "development"))
    
    # Initialize collaborative agents with Gemini
    try:
        agents_manager = CollaborativeAgents(
            api_key=Config.GOOGLE_API_KEY,
            model=Config.GEMINI_MODEL
        )
        app.agents_manager = agents_manager
    except ValueError as e:
        print(f"Warning: {e}")
        app.agents_manager = None
    
    # Health check endpoint
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "healthy", "llm": "Gemini"}), 200
    
    # Task execution endpoint
    @app.route("/execute", methods=["POST"])
    def execute_task():
        """Execute a task with collaborative Gemini agents"""
        if app.agents_manager is None:
            return jsonify({"error": "Agents manager not initialized. Check GOOGLE_API_KEY"}), 500
        
        data = request.get_json()
        
        if not data or "task" not in data:
            return jsonify({"error": "Missing 'task' field"}), 400
        
        task = data.get("task")
        agents_config = data.get("agents", [])
        
        try:
            # Create agents if provided
            if agents_config:
                for agent_config in agents_config:
                    app.agents_manager.create_agent(
                        name=agent_config.get("name"),
                        system_message=agent_config.get("system_message")
                    )
            else:
                # Create default agent if none specified
                app.agents_manager.create_agent(
                    name="default_agent",
                    system_message="You are a helpful AI assistant powered by Google Gemini."
                )
            
            # Run the task
            if app.agents_manager.agents:
                conversation = app.agents_manager.run_task(task)
                return jsonify({
                    "status": "success",
                    "message": "Task executed successfully",
                    "conversation": conversation
                }), 200
            else:
                return jsonify({"error": "No agents configured"}), 400
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # Agent info endpoint
    @app.route("/agents", methods=["GET"])
    def get_agents():
        """Get information about configured agents"""
        if app.agents_manager is None:
            return jsonify({"agents": [], "count": 0}), 200
        
        agents_info = [
            {
                "name": agent.name,
                "model": agent.model,
                "tools": agent.get_available_tools()
            }
            for agent in app.agents_manager.agents
        ]
        return jsonify({"agents": agents_info, "count": len(agents_info)}), 200
    
    # Web scraping endpoint
    @app.route("/scrape", methods=["POST"])
    def scrape():
        """Scrape a URL using agent's web scraping tool"""
        if app.agents_manager is None or not app.agents_manager.agents:
            return jsonify({"error": "No agents available"}), 400
        
        data = request.get_json()
        if not data or "url" not in data:
            return jsonify({"error": "Missing 'url' field"}), 400
        
        url = data.get("url")
        agent_name = data.get("agent", app.agents_manager.agents[0].name)
        
        try:
            # Find agent and scrape
            for agent in app.agents_manager.agents:
                if agent.name == agent_name:
                    result = agent.scrape_url(url)
                    return jsonify(result), 200
            
            return jsonify({"error": f"Agent '{agent_name}' not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # Website crawling endpoint
    @app.route("/crawl", methods=["POST"])
    def crawl():
        """Crawl a website using agent's web scraping tool"""
        if app.agents_manager is None or not app.agents_manager.agents:
            return jsonify({"error": "No agents available"}), 400
        
        data = request.get_json()
        if not data or "url" not in data:
            return jsonify({"error": "Missing 'url' field"}), 400
        
        url = data.get("url")
        max_depth = data.get("max_depth", 2)
        limit = data.get("limit", 10)
        agent_name = data.get("agent", app.agents_manager.agents[0].name)
        
        try:
            # Find agent and crawl
            for agent in app.agents_manager.agents:
                if agent.name == agent_name:
                    result = agent.crawl_website(url, max_depth, limit)
                    return jsonify(result), 200
            
            return jsonify({"error": f"Agent '{agent_name}' not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # Extract data endpoint
    @app.route("/extract", methods=["POST"])
    def extract():
        """Extract structured data from a URL"""
        if app.agents_manager is None or not app.agents_manager.agents:
            return jsonify({"error": "No agents available"}), 400
        
        data = request.get_json()
        if not data or "url" not in data:
            return jsonify({"error": "Missing 'url' field"}), 400
        
        url = data.get("url")
        schema = data.get("schema")
        agent_name = data.get("agent", app.agents_manager.agents[0].name)
        
        try:
            # Find agent and extract
            for agent in app.agents_manager.agents:
                if agent.name == agent_name:
                    result = agent.extract_data(url, schema)
                    return jsonify(result), 200
            
            return jsonify({"error": f"Agent '{agent_name}' not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
