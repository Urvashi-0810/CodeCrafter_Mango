import sys
import os
import json
import asyncio
import tempfile
import uuid
from contextlib import aclosing
from google.adk.sessions import InMemorySessionService
import traceback
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
from config import config, FLASK_ENV, Config
from agents import CollaborativeAgents
from agents.adk_agents import full_analysis_agent
from google.adk import Runner
from google.genai import types

# Ensure proper path handling
sys.path.insert(0, os.path.dirname(__file__))

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        print(f"Error initializing agents: {e}")
        app.agents_manager = None

    # ============ UNIFIED ANALYSIS ENDPOINTS ============

    @app.route("/full-analysis", methods=["POST"])
    def full_analysis():
        """Run the complete analysis pipeline using Google ADK (JSON input)."""
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data"}), 400

        user_input = json.dumps(data)  # Pass the whole input as JSON

        try:
            # Create session service and runner
            session_service = InMemorySessionService()
            runner = Runner(agent=full_analysis_agent, session_service=session_service)

            # Generate unique session and user IDs
            session_id = str(uuid.uuid4())
            user_id = "user_123"  # You can make this dynamic if needed

            # Run the agent
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                runner.run_async(
                    user_id=user_id,
                    session_id=session_id,
                    new_message=user_input
                )
            )
            final_report = result.final_response

            return jsonify({
                "success": True,
                "report": final_report
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/full-analysis-image", methods=["POST"])
    def full_analysis_image():
        print("\n========== [full-analysis-image] NEW REQUEST ==========")

        if 'image' not in request.files:
            print("[ERROR] No image file in request")
            return jsonify({"error": "No image file provided"}), 400

        file = request.files['image']
        print(f"[INFO] Uploaded filename: {file.filename}")

        if file.filename == '':
            print("[ERROR] Empty filename")
            return jsonify({"error": "Empty filename"}), 400

        if not allowed_file(file.filename):
            print(f"[ERROR] Invalid file type: {file.filename}")
            return jsonify({
                "error": f"File type not allowed. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            }), 400

        filepath = None

        try:
            # Save temporarily
            print("[STEP] Saving file temporarily...")
            filename = secure_filename(file.filename)
            temp_dir = tempfile.gettempdir()
            os.makedirs(temp_dir, exist_ok=True)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            filepath = os.path.join(temp_dir, unique_filename)

            print(f"[INFO] Temp filepath: {filepath}")
            file.save(filepath)
            print("[SUCCESS] File saved")

            # Perform OCR
            print("[STEP] Opening image for OCR...")
            with Image.open(filepath) as image:
                print("[STEP] Running pytesseract OCR...")
                extracted_text = pytesseract.image_to_string(image)

            print("[SUCCESS] OCR completed")
            print(f"[INFO] Extracted text length: {len(extracted_text)}")
            print(f"[INFO] Extracted text preview:\n{extracted_text[:300]}")

            # Wrap OCR text
            print("[STEP] Preparing input for ADK pipeline...")
            input_data = {"raw_text": extracted_text}
            user_input = json.dumps(input_data)

            # Create session service and runner
            print("[STEP] Creating session service...")
            session_service = InMemorySessionService()

            print("[STEP] Creating Runner...")
            runner = Runner(
                app_name="codecrafter_mango",
                agent=full_analysis_agent,
                session_service=session_service
            )

            async def run_adk_pipeline(payload: str) -> str:
                print("[ASYNC] Starting ADK pipeline")

                user_id = "user_123"
                print("[ASYNC] Creating session...")
                session = await session_service.create_session(
                    app_name="codecrafter_mango",
                    user_id=user_id
                )

                print(f"[ASYNC] Session created: {session.id}")

                content = types.Content(role="user", parts=[types.Part(text=payload)])
                final_report = ""

                try:
                    print("[ASYNC] Starting runner.run_async()")

                    async with aclosing(
                        runner.run_async(
                            user_id=session.user_id,
                            session_id=session.id,
                            new_message=content
                        )
                    ) as events:

                        print("[ASYNC] Listening for events...")

                        async for event in events:
                            print("[ASYNC] Event received")

                            if event.content and event.content.parts:
                                text = "".join(part.text or "" for part in event.content.parts)
                                if text:
                                    print("[ASYNC] Received text chunk")
                                    final_report = text

                except Exception as e:
                    print("[ASYNC ERROR]", e)
                    print(traceback.format_exc())

                finally:
                    print("[ASYNC] Closing runner...")
                    await runner.close()
                    print("[ASYNC] Runner closed")

                print("[ASYNC] Returning final report")
                return final_report

            print("[STEP] Creating new event loop...")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            print("[STEP] Running ADK pipeline...")
            final_report = loop.run_until_complete(run_adk_pipeline(user_input))

            print("[STEP] Closing event loop...")
            loop.close()

            print("[SUCCESS] Runner completed")
            print(f"[INFO] Final report length: {len(final_report)} characters")

            print("[STEP] Sending response to client...")
            return jsonify({
                "success": True,
                "ocr_text": extracted_text,
                "report": final_report
            }), 200

        except Exception as e:
            print("[ERROR] Exception occurred:")
            print(e)
            print(traceback.format_exc())
            return jsonify({"error": str(e)}), 500

        finally:
            print("[STEP] Cleaning up temp file...")
            if filepath and os.path.exists(filepath):
                try:
                    os.remove(filepath)
                    print(f"[SUCCESS] Temp file deleted: {filepath}")
                except OSError as cleanup_error:
                    print(f"[ERROR] Temp cleanup failed: {cleanup_error}")

            print("========== [full-analysis-image] REQUEST END ==========\n")   # ============ HEALTH & SYSTEM ENDPOINTS ============

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
            return jsonify({"success": True, "analysis": analysis}), 200
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
            return jsonify({"success": True, "metrics": metrics}), 200
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
            return jsonify({"success": True, "explanation": explanation}), 200
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
            return jsonify({"success": True, "recommendations": recommendations}), 200
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
            return jsonify({"success": True, "assessment": result}), 200
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
            return jsonify({"success": True, "modified_portfolio": modified}), 200
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
            return jsonify({"success": True, "projections": projections}), 200
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
            return jsonify({"success": True, "comparison": comparison}), 200
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
            return jsonify({"success": True, "explanation": explanation}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)