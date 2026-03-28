#!/usr/bin/env python3
"""Fix failing endpoints test"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

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
print("TESTING FIXED ENDPOINTS")
print("="*60 + "\n")

# Test 1: /analysis/explain with correct parameters
print("Test 1: /analysis/explain")
analysis_data = {
    "risk_score": 66,
    "diversification_score": 22.5,
    "total_investment": 31000,
    "current_value": 35500,
    "profit_loss": {"amount": 4500, "percentage": 14.52, "status": "gain"}
}
try:
    response = requests.post(
        f"{BASE_URL}/analysis/explain",
        json={"analysis": analysis_data},
        timeout=20
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ PASS - Got explanation\n")
    else:
        print(f"❌ FAIL - {response.text}\n")
except Exception as e:
    print(f"❌ ERROR - {e}\n")

# Test 2: /simulation/modify with correct parameters
print("Test 2: /simulation/modify")
modification = {
    "action": "add",
    "type": "stock",
    "symbol": "HDFC",
    "quantity": 5,
    "buy_price": 2700,
    "current_price": 2700,
    "sector": "Finance",
    "exchange": "NSE"
}
try:
    response = requests.post(
        f"{BASE_URL}/simulation/modify",
        json={"portfolio": test_portfolio, "modification": modification},
        timeout=20
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ PASS - Portfolio modified\n")
    else:
        print(f"❌ FAIL - {response.text}\n")
except Exception as e:
    print(f"❌ ERROR - {e}\n")

# Test 3: /simulation/returns with correct parameters
print("Test 3: /simulation/returns")
try:
    response = requests.post(
        f"{BASE_URL}/simulation/returns",
        json={
            "portfolio": test_portfolio,
            "years": 5,
            "annual_return": 0.12
        },
        timeout=20
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ PASS - Returns simulated\n")
    else:
        print(f"❌ FAIL - {response.text}\n")
except Exception as e:
    print(f"❌ ERROR - {e}\n")

# Test 4: /simulation/compare with correct parameters
# First get the modified portfolio
modified_portfolio = {
    **test_portfolio,
    "stocks": test_portfolio["stocks"] + [
        {
            "symbol": "HDFC",
            "quantity": 5,
            "buy_price": 2700,
            "current_price": 2700,
            "sector": "Finance",
            "exchange": "NSE"
        }
    ]
}

print("Test 4: /simulation/compare")
try:
    response = requests.post(
        f"{BASE_URL}/simulation/compare",
        json={
            "original": test_portfolio,
            "modified": modified_portfolio
        },
        timeout=20
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ PASS - Portfolios compared\n")
    else:
        print(f"❌ FAIL - {response.text}\n")
except Exception as e:
    print(f"❌ ERROR - {e}\n")

# Test 5: /simulation/explain-comparison
print("Test 5: /simulation/explain-comparison")
comparison_data = {
    "original_total_investment": 31000,
    "modified_total_investment": 34700,
    "original_risk": 65,
    "modified_risk": 60,
    "improvements": ["Better diversification", "Higher profit potential"]
}
try:
    response = requests.post(
        f"{BASE_URL}/simulation/explain-comparison",
        json={"comparison": comparison_data},
        timeout=20
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ PASS - Comparison explained\n")
    else:
        print(f"❌ FAIL - {response.text}\n")
except Exception as e:
    print(f"❌ ERROR - {e}\n")

print("="*60)
print("Fixed endpoints test completed!")
print("="*60)
