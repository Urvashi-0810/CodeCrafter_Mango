# agents/adk_agents.py

import json
from google.adk.agents import Agent, SequentialAgent
from google.adk.tools import FunctionTool
from tools.adk_tools import (
    parse_portfolio_from_csv,
    fetch_complete_market_data,
    calculate_portfolio_metrics,
    generate_analysis_report,
    simulate_returns,
)

# Create tool instances
parse_csv_tool  = FunctionTool(parse_portfolio_from_csv)
market_data_tool = FunctionTool(fetch_complete_market_data)
metrics_tool    = FunctionTool(calculate_portfolio_metrics)
report_tool     = FunctionTool(generate_analysis_report)
simulate_tool   = FunctionTool(simulate_returns)

# ========== Step 1: Parse Portfolio ==========
parse_agent = Agent(
    name="parse_agent",
    model="gemini-2.5-flash",
    instruction="""
You are responsible for parsing a portfolio from user input. The user will provide either:
- a JSON object containing the portfolio structure (as `portfolio_data`), or
- a file path (as `file_path`) and file type (as `file_type`), or
- raw text extracted from an image (as `raw_text`).

If a file path is given, use the `parse_portfolio_from_csv` tool to read the CSV. Then output the parsed portfolio as a JSON string.
If `portfolio_data` is directly provided, just output it as a JSON string.
If raw text is given, you must extract the stock holdings (symbol, quantity, buy price, current price, sector) from the text. The text may be messy; use your intelligence to infer the data. Output a JSON string representing the portfolio.

Your final output must be a valid JSON string representing the portfolio. Do not include any extra text.
""",
    tools=[parse_csv_tool]
)

# ========== Step 2: Fetch Market Data ==========
market_agent = Agent(
    name="market_agent",
    model="gemini-2.5-flash",
    instruction="""
You have been given a portfolio (as a JSON string). Extract all stock symbols from the portfolio and for each symbol, call the `fetch_complete_market_data` tool. Combine the results into a single JSON object mapping symbol to market data.

Your final output must be a JSON string containing the market data for all stocks. Format: {"symbol1": {...}, "symbol2": {...}}.
""",
    tools=[market_data_tool]
)

# ========== Step 3: Analyze Portfolio ==========
analysis_agent = Agent(
    name="analysis_agent",
    model="gemini-2.5-flash",
    instruction="""
You have a portfolio (as a JSON string). Use the `calculate_portfolio_metrics` and `generate_analysis_report` tools to compute all metrics and generate a full analysis report.

Your final output must be a JSON string containing both the metrics and the report. Structure: {"metrics": {...}, "analysis": {...}}.
""",
    tools=[metrics_tool, report_tool]
)

# ========== Step 4: Generate Recommendations ==========
recommendation_agent = Agent(
    name="recommendation_agent",
    model="gemini-2.5-flash",
    instruction="""
You are an expert investment advisor. You will receive portfolio (JSON), market data (JSON), and analysis (JSON) from previous steps.

Output ONLY a valid JSON string with this exact structure, no extra text:
{
  "recommendations": [
    {
      "action": "add" | "reduce" | "remove",
      "symbol": "SYMBOL",
      "shares": 20,
      "reason": "Short reason text",
      "strategy": "Risk Diversification" | "Dividend Optimization" | "Portfolio Rebalancing" | "Tax-Loss Harvesting Opportunity" | "Sector Expansion",
      "priority": "High" | "Medium" | "Low"
    }
  ],
  "ai_summary": "One sentence overall recommendation summary",
  "strengths": ["strength 1", "strength 2"],
  "areas_to_improve": ["area 1", "area 2"]
}
""",
    tools=[]
)

# ========== Step 5: Simulate Returns ==========
simulation_agent = Agent(
    name="simulation_agent",
    model="gemini-2.5-flash",
    instruction="""
You have the portfolio (as JSON). Use the `simulate_returns` tool to project the portfolio's growth over 5 years with a 12% annual return. Output the simulation results as a JSON string.
""",
    tools=[simulate_tool]
)

# ========== Step 6: Format Final Output ==========
formatter_agent = Agent(
    name="formatter_agent",
    model="gemini-2.5-flash",
    instruction="""
You are a data formatter. Combine all previous pipeline outputs into a single structured JSON response for a financial UI.

Output ONLY valid JSON, no markdown, no extra text.

CRITICAL RULES — read before filling any field:
1. NEVER invent, assume, or hardcode values. Every field must come from the actual pipeline data.
2. INCLUDE ALL portfolio data from parse_agent: stocks, mutual_funds, gold, bonds — pass them through unchanged.
3. For risk_assessment fields (volatility, concentration, diversification_status, ai_status_message),
   copy the EXACT values from analysis_agent output. Do NOT substitute your own labels.
4. For risk_score, diversification_score, health_score — use the numeric values from analysis_agent.
   Do NOT replace them with the example numbers below.
5. The schema below uses placeholder example values only to show data types and field names.
   Replace ALL example values with real pipeline data.

Use this schema (field names are fixed; example values are placeholders only):

{
  "portfolio": {
    "total_invested": 0,
    "current_value": 0,
    "pl_amount": 0,
    "pl_percentage": 0,
    "stock_count": 0,
    "stocks": [
      {
        "symbol": "SYMBOL",
        "name": "Company Name",
        "sector": "Sector",
        "exchange": "NSE",
        "quantity": 0,
        "buy_price": 0,
        "current_price": 0,
        "avg_price": 0,
        "current_value": 0,
        "pl_amount": 0,
        "pl_percentage": 0
      }
    ],
    "mutual_funds": [],
    "gold": [],
    "bonds": [],
    "holdings": [
      {
        "symbol": "SYMBOL",
        "name": "Company Name",
        "sector": "Sector",
        "exchange": "NSE",
        "quantity": 0,
        "buy_price": 0,
        "current_price": 0,
        "avg_price": 0,
        "current_value": 0,
        "pl_amount": 0,
        "pl_percentage": 0
      }
    ]
  },
  "analysis": {
    "sector_allocation": {},
    "risk_assessment": {
      "volatility": "<COPY EXACT VALUE FROM analysis_agent — do not change>",
      "concentration": "<COPY EXACT VALUE FROM analysis_agent — do not change>",
      "diversification_status": "<COPY EXACT VALUE FROM analysis_agent — do not change>",
      "ai_status_message": "<COPY EXACT VALUE FROM analysis_agent — do not change>"
    },
    "risk_score": 0,
    "diversification_score": 0,
    "health_score": 0
  },
  "recommendations": {
    "ai_summary": "",
    "items": [
      {
        "action": "add",
        "symbol": "SYMBOL",
        "shares": 0,
        "reason": "",
        "strategy": "",
        "priority": "",
        "status": "pending"
      }
    ],
    "strategies": [
      {
        "name": "",
        "description": "",
        "priority": "",
        "status": "pending"
      }
    ],
    "strengths": [],
    "areas_to_improve": []
  },
  "simulation": {
    "current_value": 0,
    "annual_return_rate": 12,
    "projections": [
      {"year": 1, "projected_value": 0, "gain": 0, "gain_percentage": 0},
      {"year": 2, "projected_value": 0, "gain": 0, "gain_percentage": 0},
      {"year": 3, "projected_value": 0, "gain": 0, "gain_percentage": 0},
      {"year": 4, "projected_value": 0, "gain": 0, "gain_percentage": 0},
      {"year": 5, "projected_value": 0, "gain": 0, "gain_percentage": 0}
    ]
  },
  "market_data": {}
}

Data sources:
- portfolio (all fields: stocks, mutual_funds, gold, bonds) → from parse_agent (pass through all data)
- analysis       → from analysis_agent (copy risk_assessment fields verbatim)
- recommendations → from recommendation_agent
- simulation     → from simulation_agent
- market_data    → from market_agent (sentiment, news_headline, news_summary per symbol)
"""
)

# ========== Sequential Agent ==========
full_analysis_agent = SequentialAgent(
    name="full_analysis_agent",
    description="Orchestrates the complete portfolio analysis and recommendation pipeline.",
    sub_agents=[
        parse_agent,
        market_agent,
        analysis_agent,
        recommendation_agent,
        simulation_agent,
        formatter_agent,
    ]
)