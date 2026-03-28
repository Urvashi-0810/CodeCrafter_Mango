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
parse_csv_tool = FunctionTool(parse_portfolio_from_csv)
market_data_tool = FunctionTool(fetch_complete_market_data)
metrics_tool = FunctionTool(calculate_portfolio_metrics)
report_tool = FunctionTool(generate_analysis_report)
simulate_tool = FunctionTool(simulate_returns)

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
You are an expert investment advisor. You will receive three inputs: portfolio (JSON), market data (JSON), and analysis (JSON). Based on these, provide specific, actionable recommendations covering:
- Stocks to add, remove, or reduce exposure
- Sector diversification improvements
- Mutual fund / ETF allocation
- Gold and bond allocation
- Risk reduction strategies
- Buy/sell timing suggestions

Output your recommendations in clear bullet points.
""",
    tools=[]  # No tools needed; it just reads previous outputs
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
You are a financial summary expert. Combine all previous outputs (portfolio, market data, analysis, recommendations, simulation) into a concise, well‑structured final report suitable for an investor. Use clear sections and bullet points. Be professional but friendly.
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