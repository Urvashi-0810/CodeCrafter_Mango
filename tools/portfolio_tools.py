import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Any
import io


class PortfolioParsingTools:
    """Tools for parsing portfolio data from various formats"""
    
    @staticmethod
    def parse_csv(file_path: str) -> Dict[str, Any]:
        """Parse CSV file containing portfolio data"""
        try:
            df = pd.read_csv(file_path)
            portfolio_data = {
                "stocks": [],
                "mutual_funds": [],
                "gold": [],
                "bonds": []
            }
            
            for _, row in df.iterrows():
                stock_entry = {
                    "symbol": row.get("symbol", "").upper(),
                    "quantity": int(row.get("quantity", 0)),
                    "buy_price": float(row.get("buy_price", 0)),
                    "current_price": float(row.get("current_price", 0)),
                    "sector": row.get("sector", "Unknown"),
                    "exchange": row.get("exchange", "NSE")
                }
                portfolio_data["stocks"].append(stock_entry)
            
            return {
                "success": True,
                "data": portfolio_data,
                "records_parsed": len(df)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def parse_pdf(file_path: str) -> Dict[str, Any]:
        """Parse PDF file containing portfolio data"""
        try:
            from PyPDF2 import PdfReader
            
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            
            return {
                "success": True,
                "text": text,
                "pages": len(reader.pages)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def parse_image_ocr(file_path: str) -> Dict[str, Any]:
        """Extract text from image using OCR"""
        try:
            import pytesseract
            from PIL import Image
            
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            
            return {
                "success": True,
                "text": text,
                "image_size": image.size
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def classify_sectors(holdings: List[str]) -> Dict[str, str]:
        """Classify holdings into sectors"""
        sector_mapping = {
            "INFY": "IT",
            "TCS": "IT",
            "WIPRO": "IT",
            "RELIANCE": "Energy",
            "HDFC": "Finance",
            "ICICIBANK": "Finance",
            "SBIN": "Finance",
            "BAJAJFINSV": "Finance",
            "BHARTIARTL": "Telecom",
            "JIO": "Telecom",
            "MARUTI": "Auto",
            "TATAMOTORS": "Auto",
            "ADANIGREEN": "Energy",
            "POWERGRID": "Energy",
            "ITC": "FMCG",
            "HUL": "FMCG",
            "NESTLEIND": "FMCG"
        }
        
        classified = {}
        for holding in holdings:
            symbol = holding.upper()
            classified[holding] = sector_mapping.get(symbol, "Unknown")
        
        return classified
    
    @staticmethod
    def format_portfolio(parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert parsed data into structured portfolio JSON"""
        try:
            portfolio = {
                "metadata": {
                    "created_at": pd.Timestamp.now().isoformat(),
                    "version": "1.0"
                },
                "stocks": parsed_data.get("stocks", []),
                "mutual_funds": parsed_data.get("mutual_funds", []),
                "gold": parsed_data.get("gold", {}),
                "bonds": parsed_data.get("bonds", []),
                "summary": {
                    "total_stocks": len(parsed_data.get("stocks", [])),
                    "total_mutual_funds": len(parsed_data.get("mutual_funds", [])),
                    "total_investment": sum(
                        s["quantity"] * s["buy_price"] 
                        for s in parsed_data.get("stocks", [])
                    )
                }
            }
            
            return {
                "success": True,
                "portfolio": portfolio
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
