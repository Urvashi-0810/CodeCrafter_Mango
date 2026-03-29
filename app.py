import sys
import os
import json
import asyncio
import tempfile
import uuid
import re
from contextlib import aclosing
from google.adk.sessions import InMemorySessionService
import traceback
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
from config import config, FLASK_ENV, Config
from flask_cors import CORS
from agents.adk_agents import full_analysis_agent
from google.adk import Runner
from google.genai import types
from tools.adk_tools import force_market_analysis, parse_raw_data_to_structured
from tools.market_tools import SYMBOL_MAP

sys.path.insert(0, os.path.dirname(__file__))

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_app():
    app = Flask(__name__)
    app.config.from_object(config.get(FLASK_ENV, "development"))

    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "healthy", "llm": "Gemini"}), 200

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

            # ========== VALIDATE & EXTRACT STOCK SYMBOL ==========
            print("[STEP] Extracting stock symbol from OCR text...")

            symbol_patterns = [
                r'\b([A-Z]{2,}IND)\b',
                r'\b([A-Z]{2,})\b(?=\n.*(?:Invested|P&L|Holdings))',
                r'(?:^|\n)([A-Z]{2,})(?:\s+.*)?(?:Invested|Holdings|Current)',
            ]

            detected_symbol = None
            for pattern in symbol_patterns:
                match = re.search(pattern, extracted_text, re.MULTILINE)
                if match:
                    candidate = match.group(1).upper().strip()
                    if candidate in SYMBOL_MAP:
                        detected_symbol = candidate
                        print(f"[INFO] Detected stock symbol from OCR: {detected_symbol}")
                        break
                    else:
                        print(f"[DEBUG] Found candidate '{candidate}' but not in SYMBOL_MAP")

            if detected_symbol:
                print(f"\n[INFO] ===== SYMBOL VALIDATION PASSED =====")
                print(f"[INFO] Symbol: {detected_symbol}")
                print(f"[INFO] Calling force_market_analysis directly (bypassing LLM)...")
                print(f"[INFO] =====================================\n")

                try:
                    market_analysis = force_market_analysis(detected_symbol)

                    if market_analysis.get("success"):
                        final_report = market_analysis.get("report", "")
                        structured_data = parse_raw_data_to_structured(
                            symbol=detected_symbol,
                            raw_data=market_analysis.get("raw_data", {}),
                            ocr_text=extracted_text
                        )
                        print("[SUCCESS] Forced market analysis completed successfully")
                    else:
                        final_report = f"Analysis failed: {market_analysis.get('error', 'Unknown error')}"
                        structured_data = None

                    return jsonify({
                        "success": True,
                        "ocr_text": extracted_text,
                        "detected_symbol": detected_symbol,
                        "analysis_type": "forced_market_analysis",
                        "report": final_report,
                        "data": structured_data,        # ← structured for UI
                        "timestamp": market_analysis.get("timestamp", "")
                    }), 200

                except Exception as e:
                    print(f"[ERROR] forced_market_analysis failed: {e}")
                    print(traceback.format_exc())
                    # Fall through to ADK pipeline as backup

            else:
                print(f"[WARNING] No valid stock symbol detected in OCR text")
                print(f"[WARNING] Available symbols: {list(SYMBOL_MAP.keys())}")
                print(f"[INFO] Proceeding with ADK pipeline for generic analysis")

            # ========== FALLBACK: ADK PIPELINE ==========
            print("[STEP] Preparing input for ADK pipeline...")
            input_data = {"raw_text": extracted_text}
            user_input = json.dumps(input_data)

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
                function_calls_made = []

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
                                for part in event.content.parts:
                                    if hasattr(part, 'text') and part.text:
                                        print("[ASYNC] Received text chunk")
                                        final_report += part.text
                                    elif hasattr(part, 'function_call') and part.function_call:
                                        print(f"[ASYNC] Received function_call: {part.function_call.name}")
                                        function_calls_made.append({
                                            "name": part.function_call.name,
                                            "args": getattr(part.function_call, 'args', {})
                                        })

                        if function_calls_made:
                            print(f"[ASYNC] Function calls captured: {len(function_calls_made)}")
                            for fc in function_calls_made:
                                print(f"  - {fc['name']}: {fc['args']}")

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

            # Try to parse structured JSON from formatter_agent output
            structured_data = None
            try:
                clean = final_report.strip()
                clean = re.sub(r'^```json\s*', '', clean)
                clean = re.sub(r'^```\s*', '', clean)
                clean = re.sub(r'\s*```$', '', clean)
                structured_data = json.loads(clean)
            except Exception:
                structured_data = None

            print("[STEP] Sending response to client...")
            return jsonify({
                "success": True,
                "ocr_text": extracted_text,
                "report": final_report,       # raw text fallback
                "data": structured_data       # structured fields for UI
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

            print("========== [full-analysis-image] REQUEST END ==========\n")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)