import sys
import os
from flask import Flask, jsonify, request
from config import config, FLASK_ENV, Config
from agents import CollaborativeAgents

# Ensure proper path handling
sys.path.insert(0, os.path.dirname(__file__))

def create_app():
    """Flask application factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config.get(FLASK_ENV, "development"))
    
    # Initialize collaborative agents manager
    try:
        agents_manager = CollaborativeAgents(
            api_key=Config.GOOGLE_API_KEY,
            model=Config.GEMINI_MODEL
        )
        app.agents_manager = agents_manager
    except ValueError as e:
        print(f"Error: {e}")
        app.agents_manager = None
    
    # ============ HEALTH & SYSTEM ENDPOINTS ============
    
    @app.route("/health", methods=["GET"])
    def health():
        """Health check endpoint"""
        return jsonify({
            "status": "healthy",
            "llm": "Gemini",
            "agents": len(app.agents_manager.agents) if app.agents_manager else 0
        }), 200
    
    @app.route("/agents", methods=["GET"])
    def get_agents():
        """Get information about all agents"""
        if not app.agents_manager:
            return jsonify({"error": "Agents not initialized"}), 500
        
        agents_info = app.agents_manager.get_agents_info()
        return jsonify({
            "agents": agents_info,
            "total_agents": len(agents_info)
        }), 200
    
    # ============ PORTFOLIO AGENT ENDPOINTS ============
    
    @app.route("/portfolio/parse", methods=["POST"])
    def parse_portfolio():
        """Parse portfolio from file upload"""
        if not app.agents_manager:
            return jsonify({"error": "Agents not initialized"}), 500
        
        data = request.get_json()
        
        if not data or "file_path" not in data or "file_type" not in data:
            return jsonify({"error": "Missing 'file_path' or 'file_type'"}), 400
        
        try:
            result = app.agents_manager.portfolio_agent.parse_portfolio_input(
                data["file_path"],
                data["file_type"]
            )
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/portfolio/format", methods=["POST"])
    def format_portfolio():
        """Format parsed data into structured portfolio"""
        if not app.agents_manager:
            return jsonify({"error": "Agents not initialized"}), 500
        
        data = request.get_json()
        
        if not data or "portfolio_data" not in data:
            return jsonify({"error": "Missing 'portfolio_data'"}), 400
        
        try:
            result = app.agents_manager.portfolio_agent.format_portfolio(data["portfolio_data"])
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/portfolio/classify", methods=["POST"])
    def classify_holdings():
        """Classify holdings by sector"""
        if not app.agents_manager:
            return jsonify({"error": "Agents not initialized"}), 500
        
        data = request.get_json()
        
        if not data or "holdings" not in data:
            return jsonify({"error": "Missing 'holdings' list"}), 400
        
        try:
            result = app.agents_manager.portfolio_agent.classify_holdings(data["holdings"])
            return jsonify({
                "success": True,
                "sector_classification": result
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # ============ MARKET DATA AGENT ENDPOINTS ============
    
    @app.route("/market/stock/<symbol>", methods=["GET"])
    def get_stock_data(symbol):
        """Fetch stock data"""
        if not app.agents_manager:
            return jsonify({"error": "Agents not initialized"}), 500
        
        source = request.args.get("source", "moneycontrol")
        
        try:
            result = app.agents_manager.market_agent.fetch_stock_data(symbol, source)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/market/news/<symbol>", methods=["GET"])
    def get_stock_news(symbol):
        """Fetch stock news"""
        if not app.agents_manager:
            return jsonify({"error": "Agents not initialized"}), 500
        
        try:
            result = app.agents_manager.market_agent.fetch_news(symbol)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/market/financial-reports/<symbol>", methods=["GET"])
    def get_financial_reports(symbol):
        """Fetch financial reports"""
        if not app.agents_manager:
            return jsonify({"error": "Agents not initialized"}), 500
        
        try:
            result = app.agents_manager.market_agent.fetch_financial_reports(symbol)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/market/sector/<sector>", methods=["GET"])
    def get_sector_performance(sector):
        """Fetch sector performance"""
        if not app.agents_manager:
            return jsonify({"error": "Agents not initialized"}), 500
        
        try:
            result = app.agents_manager.market_agent.fetch_sector_performance(sector)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/market/economic-news", methods=["GET"])
    def get_economic_news():
        """Fetch economic news and RBI updates"""
        if not app.agents_manager:
            return jsonify({"error": "Agents not initialized"}), 500
        
        try:
            result = app.agents_manager.market_agent.fetch_economic_news()
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/market/analyst-ratings/<symbol>", methods=["GET"])
    def get_analyst_ratings(symbol):
        """Fetch analyst ratings"""
        if not app.agents_manager:
            return jsonify({"error": "Agents not initialized"}), 500
        
        try:
            result = app.agents_manager.market_agent.fetch_analyst_ratings(symbol)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/market/sentiment/<symbol>", methods=["GET"])
    def get_market_sentiment(symbol):
        """Get market sentiment analysis"""
        if not app.agents_manager:
            return jsonify({"error": "Agents not initialized"}), 500
        
        try:
            result = app.agents_manager.market_agent.get_market_sentiment(symbol)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/market/historical/<symbol>", methods=["GET"])
    def get_historical_data(symbol):
        """Fetch historical candlestick data"""
        if not app.agents_manager:
            return jsonify({"error": "Agents not initialized"}), 500
        
        period = request.args.get("period", "1y")
        
        try:
            result = app.agents_manager.market_agent.fetch_historical_data(symbol, period)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # ============ ANALYSIS AGENT ENDPOINTS ============
    
    @app.route("/analysis/portfolio", methods=["POST"])
    def analyze_portfolio():
        """Analyze portfolio and generate metrics"""
        if not app.agents_manager:
            return jsonify({"error": "Agents not initialized"}), 500
        
        data = request.get_json()
        
        if not data or "portfolio" not in data:
            return jsonify({"error": "Missing 'portfolio' data"}), 400
        
        try:
            analysis = app.agents_manager.analysis_agent.analyze_portfolio(data["portfolio"])
            return jsonify({
                "success": True,
                "analysis": analysis
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/analysis/metrics", methods=["POST"])
    def calculate_metrics():
        """Calculate portfolio metrics"""
        if not app.agents_manager:
            return jsonify({"error": "Agents not initialized"}), 500
        
        data = request.get_json()
        
        if not data or "portfolio" not in data:
            return jsonify({"error": "Missing 'portfolio' data"}), 400
        
        try:
            metrics = app.agents_manager.analysis_agent.calculate_metrics(data["portfolio"])
            return jsonify({
                "success": True,
                "metrics": metrics
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/analysis/explain", methods=["POST"])
    def explain_analysis():
        """Get LLM explanation of analysis"""
        if not app.agents_manager:
            return jsonify({"error": "Agents not initialized"}), 500
        
        data = request.get_json()
        
        if not data or "analysis" not in data:
            return jsonify({"error": "Missing 'analysis' data"}), 400
        
        try:
            explanation = app.agents_manager.analysis_agent.explain_analysis(data["analysis"])
            return jsonify({
                "success": True,
                "explanation": explanation
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # ============ RECOMMENDATION AGENT ENDPOINTS ============
    
    @app.route("/recommendations/generate", methods=["POST"])
    def generate_recommendations():
        """Generate portfolio recommendations"""
        if not app.agents_manager:
            return jsonify({"error": "Agents not initialized"}), 500
        
        data = request.get_json()
        
        if not data or "portfolio" not in data or "analysis" not in data:
            return jsonify({"error": "Missing 'portfolio' or 'analysis' data"}), 400
        
        try:
            market_data = data.get("market_data", {})
            recommendations = app.agents_manager.recommendation_agent.generate_recommendations(
                data["portfolio"],
                market_data,
                data["analysis"]
            )
            return jsonify({
                "success": True,
                "recommendations": recommendations
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/recommendations/risk-profile", methods=["POST"])
    def assess_risk_profile():
        """Assess if portfolio matches risk profile"""
        if not app.agents_manager:
            return jsonify({"error": "Agents not initialized"}), 500
        
        data = request.get_json()
        
        if not data or "portfolio" not in data or "risk_tolerance" not in data:
            return jsonify({"error": "Missing 'portfolio' or 'risk_tolerance'"}), 400
        
        try:
            result = app.agents_manager.recommendation_agent.assess_risk_profile(
                data["portfolio"],
                data["risk_tolerance"]
            )
            return jsonify({
                "success": True,
                "assessment": result
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # ============ SIMULATION AGENT ENDPOINTS ============
    
    @app.route("/simulation/modify", methods=["POST"])
    def modify_portfolio():
        """Modify portfolio with what-if changes"""
        if not app.agents_manager:
            return jsonify({"error": "Agents not initialized"}), 500
        
        data = request.get_json()
        
        if not data or "portfolio" not in data or "modification" not in data:
            return jsonify({"error": "Missing 'portfolio' or 'modification'"}), 400
        
        try:
            modified = app.agents_manager.simulation_agent.modify_portfolio(
                data["portfolio"],
                data["modification"]
            )
            return jsonify({
                "success": True,
                "modified_portfolio": modified
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/simulation/returns", methods=["POST"])
    def simulate_returns():
        """Simulate portfolio returns over time"""
        if not app.agents_manager:
            return jsonify({"error": "Agents not initialized"}), 500
        
        data = request.get_json()
        
        if not data or "portfolio" not in data or "years" not in data or "annual_return" not in data:
            return jsonify({"error": "Missing 'portfolio', 'years', or 'annual_return'"}), 400
        
        try:
            projections = app.agents_manager.simulation_agent.simulate_returns(
                data["portfolio"],
                data["years"],
                data["annual_return"]
            )
            return jsonify({
                "success": True,
                "projections": projections
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/simulation/compare", methods=["POST"])
    def compare_portfolios():
        """Compare original and modified portfolios"""
        if not app.agents_manager:
            return jsonify({"error": "Agents not initialized"}), 500
        
        data = request.get_json()
        
        if not data or "original" not in data or "modified" not in data:
            return jsonify({"error": "Missing 'original' or 'modified' portfolio"}), 400
        
        try:
            comparison = app.agents_manager.simulation_agent.compare_portfolios(
                data["original"],
                data["modified"]
            )
            return jsonify({
                "success": True,
                "comparison": comparison
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/simulation/explain-comparison", methods=["POST"])
    def explain_comparison():
        """Get LLM explanation of portfolio comparison"""
        if not app.agents_manager:
            return jsonify({"error": "Agents not initialized"}), 500
        
        data = request.get_json()
        
        if not data or "comparison" not in data:
            return jsonify({"error": "Missing 'comparison' data"}), 400
        
        try:
            explanation = app.agents_manager.simulation_agent.explain_comparison(data["comparison"])
            return jsonify({
                "success": True,
                "explanation": explanation
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
