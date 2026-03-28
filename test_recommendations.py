import requests
import json

url = "http://localhost:5000/recommendations/generate"

payload = {
    "portfolio": {
        "stocks": [
            {"symbol": "INFY", "quantity": 10, "buy_price": 1500, "current_price": 1800, "sector": "IT", "exchange": "NSE"}
        ],
        "mutual_funds": [],
        "bonds": [],
        "gold": {}
    },
    "analysis": {
        "risk_score": 65,
        "diversification_score": 22.5,
        "total_investment": 15000,
        "current_value": 18000
    },
    "market_data": {}
}

try:
    response = requests.post(url, json=payload, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
