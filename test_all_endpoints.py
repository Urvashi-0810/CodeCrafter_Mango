#!/usr/bin/env python3
"""Comprehensive test suite for portfolio advisory API endpoints"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5000"
RESULTS = []

def test_endpoint(method, endpoint, payload=None, description=""):
    """Test an endpoint and record results"""
    url = f"{BASE_URL}{endpoint}"
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=30)
        else:
            response = requests.post(url, json=payload, timeout=30)
        
        status = "✅ PASS" if response.status_code in [200, 201] else "❌ FAIL"
        result = {
            "time": timestamp,
            "endpoint": endpoint,
            "method": method,
            "status_code": response.status_code,
            "status": status,
            "description": description
        }
        
        # Try to get response preview
        try:
            resp_json = response.json()
            if isinstance(resp_json, dict) and "success" in resp_json:
                result["success"] = resp_json.get("success")
            # Check for error
            if "error" in resp_json:
                result["error"] = resp_json["error"]
        except:
            pass
        
        RESULTS.append(result)
        print(f"{status} [{response.status_code}] {description}\n   {endpoint}\n")
        
    except Exception as e:
        result = {
            "time": timestamp,
            "endpoint": endpoint,
            "method": method,
            "status": "❌ ERROR",
            "error": str(e),
            "description": description
        }
        RESULTS.append(result)
        print(f"❌ ERROR {description}\n   {endpoint}\n   Error: {e}\n")

# Test portfolio
test_portfolio = {
    "stocks": [
        {
            "symbol": "INFY",
            "quantity": 10,
            "buy_price": 1500,
            "current_price": 1800,
            "sector": "IT",
            "exchange": "NSE"
        },
        {
            "symbol": "TCS",
            "quantity": 5,
            "buy_price": 3200,
            "current_price": 3500,
            "sector": "IT",
            "exchange": "NSE"
        }
    ],
    "mutual_funds": [],
    "bonds": [],
    "gold": {}
}

print("\n" + "="*60)
print("PORTFOLIO ADVISORY API - COMPREHENSIVE TEST SUITE")
print("="*60 + "\n")

# ========== SYSTEM ENDPOINTS ==========
print("[ SYSTEM ENDPOINTS ]\n")
test_endpoint("GET", "/health", description="Health Check")
test_endpoint("GET", "/agents", description="List All Agents")

# ========== PORTFOLIO ENDPOINTS ==========
print("\n[ PORTFOLIO ENDPOINTS ]\n")
test_endpoint("POST", "/portfolio/classify", 
              {"holdings": ["INFY", "TCS", "HDFC", "RELIANCE", "BHARTIARTL"]},
              "Classify Holdings")

test_endpoint("POST", "/portfolio/format",
              {"portfolio_data": test_portfolio},
              "Format Portfolio Data")

# ========== MARKET ENDPOINTS ==========
print("\n[ MARKET ENDPOINTS ]\n")
test_endpoint("GET", "/market/stock/INFY", description="Fetch Stock Data (INFY)")
test_endpoint("GET", "/market/stock/TCS", description="Fetch Stock Data (TCS)")
test_endpoint("GET", "/market/news/INFY", description="Fetch Market News (INFY)")
test_endpoint("GET", "/market/sentiment/INFY", description="Market Sentiment (INFY)")
test_endpoint("GET", "/market/sentiment/TCS", description="Market Sentiment (TCS)")

# ========== ANALYSIS ENDPOINTS ==========
print("\n[ ANALYSIS ENDPOINTS ]\n")
test_endpoint("POST", "/analysis/metrics",
              {"portfolio": test_portfolio},
              "Calculate Portfolio Metrics")

test_endpoint("POST", "/analysis/explain",
              {"portfolio": test_portfolio, "aspect": "risk"},
              "Explain Analysis Aspect")

# ========== RECOMMENDATION ENDPOINTS ==========
print("\n[ RECOMMENDATION ENDPOINTS ]\n")
test_endpoint("POST", "/recommendations/risk-profile",
              {"portfolio": test_portfolio, "risk_tolerance": "moderate"},
              "Assess Risk Profile")

test_endpoint("POST", "/recommendations/generate",
              {
                  "portfolio": test_portfolio,
                  "analysis": {
                      "risk_score": 66,
                      "diversification_score": 22.5,
                      "total_investment": 31000,
                      "current_value": 35500
                  },
                  "market_data": {}
              },
              "Generate Recommendations")

# ========== SIMULATION ENDPOINTS ==========
print("\n[ SIMULATION ENDPOINTS ]\n")
test_endpoint("POST", "/simulation/modify",
              {"portfolio": test_portfolio, "modifications": [{"action": "add", "type": "stock", "symbol": "HDFC", "quantity": 5, "price": 2700}]},
              "Modify Portfolio")

test_endpoint("POST", "/simulation/compare",
              {
                  "original_portfolio": test_portfolio,
                  "modified_portfolio": {
                      **test_portfolio,
                      "stocks": test_portfolio["stocks"] + [{"symbol": "HDFC", "quantity": 5, "buy_price": 2700, "current_price": 2700, "sector": "Finance", "exchange": "NSE"}]
                  }
              },
              "Compare Portfolios")

test_endpoint("POST", "/simulation/returns",
              {"portfolio": test_portfolio, "scenarios": [{"name": "bull", "market_change": 0.20}, {"name": "bear", "market_change": -0.15}]},
              "Simulate Returns")

test_endpoint("POST", "/simulation/explain",
              {"original_portfolio": test_portfolio, "modified_portfolio": test_portfolio, "explanation": "no changes"},
              "Explain Simulation")

# ========== SUMMARY REPORT ==========
print("\n" + "="*60)
print("TEST SUMMARY")
print("="*60 + "\n")

total_tests = len(RESULTS)
passed = sum(1 for r in RESULTS if "✅" in r.get("status", ""))
failed = sum(1 for r in RESULTS if "❌" in r.get("status", ""))

print(f"Total Tests: {total_tests}")
print(f"Passed: {passed} ✅")
print(f"Failed: {failed} ❌")
print(f"Success Rate: {(passed/total_tests*100):.1f}%\n")

if failed > 0:
    print("Failed Tests:")
    for r in RESULTS:
        if "❌" in r.get("status", ""):
            print(f"  - {r['endpoint']} ({r.get('error', r.get('status_code', 'Unknown'))})")
    print()

print("Test Results Saved to: test_results.json")
with open("test_results.json", "w") as f:
    json.dump(RESULTS, f, indent=2)

print("\n✅ Test suite completed!\n")
