import copy
from typing import Dict, List, Any
from .analysis_tools import AnalysisTools


class SimulationTools:
    """Tools for portfolio simulation and what-if analysis"""
    
    @staticmethod
    def add_stock(portfolio: Dict[str, Any], symbol: str, quantity: int, buy_price: float, 
                  current_price: float, sector: str) -> Dict[str, Any]:
        """Add a stock to portfolio"""
        new_portfolio = copy.deepcopy(portfolio)
        
        new_stock = {
            "symbol": symbol.upper(),
            "quantity": quantity,
            "buy_price": buy_price,
            "current_price": current_price,
            "sector": sector,
            "exchange": "NSE"
        }
        
        new_portfolio["stocks"].append(new_stock)
        return new_portfolio
    
    @staticmethod
    def remove_stock(portfolio: Dict[str, Any], symbol: str) -> Dict[str, Any]:
        """Remove a stock from portfolio"""
        new_portfolio = copy.deepcopy(portfolio)
        
        new_portfolio["stocks"] = [
            s for s in new_portfolio["stocks"] 
            if s["symbol"].upper() != symbol.upper()
        ]
        
        return new_portfolio
    
    @staticmethod
    def modify_stock_quantity(portfolio: Dict[str, Any], symbol: str, new_quantity: int) -> Dict[str, Any]:
        """Modify quantity of a stock in portfolio"""
        new_portfolio = copy.deepcopy(portfolio)
        
        for stock in new_portfolio["stocks"]:
            if stock["symbol"].upper() == symbol.upper():
                stock["quantity"] = new_quantity
                break
        
        return new_portfolio
    
    @staticmethod
    def modify_stock_price(portfolio: Dict[str, Any], symbol: str, new_price: float) -> Dict[str, Any]:
        """Modify current price of a stock"""
        new_portfolio = copy.deepcopy(portfolio)
        
        for stock in new_portfolio["stocks"]:
            if stock["symbol"].upper() == symbol.upper():
                stock["current_price"] = new_price
                break
        
        return new_portfolio
    
    @staticmethod
    def add_mutual_fund(portfolio: Dict[str, Any], name: str, investment: float, 
                       category: str) -> Dict[str, Any]:
        """Add a mutual fund to portfolio"""
        new_portfolio = copy.deepcopy(portfolio)
        
        mf = {
            "name": name,
            "investment": investment,
            "current_value": investment,
            "category": category,
            "units": investment / 100  # Simplified
        }
        
        new_portfolio["mutual_funds"].append(mf)
        return new_portfolio
    
    @staticmethod
    def add_gold(portfolio: Dict[str, Any], amount: float, grams: float, 
                 price_per_gram: float) -> Dict[str, Any]:
        """Add gold to portfolio"""
        new_portfolio = copy.deepcopy(portfolio)
        
        new_portfolio["gold"] = {
            "grams": grams,
            "price_per_gram": price_per_gram,
            "investment": amount,
            "current_value": amount
        }
        
        return new_portfolio
    
    @staticmethod
    def add_bond(portfolio: Dict[str, Any], name: str, principal: float, 
                 rate: float, years: int) -> Dict[str, Any]:
        """Add a bond to portfolio"""
        new_portfolio = copy.deepcopy(portfolio)
        
        bond = {
            "name": name,
            "principal": principal,
            "rate": rate,
            "years": years,
            "current_value": principal,
            "maturity_amount": principal * (1 + rate/100) ** years
        }
        
        new_portfolio["bonds"].append(bond)
        return new_portfolio
    
    @staticmethod
    def change_risk_level(portfolio: Dict[str, Any], risk_level: str) -> Dict[str, Any]:
        """Modify portfolio risk level by adjusting allocation"""
        new_portfolio = copy.deepcopy(portfolio)
        
        # Risk levels: conservative, moderate, aggressive
        allocation_mapping = {
            "conservative": {"stocks": 30, "bonds": 40, "gold": 20, "mf": 10},
            "moderate": {"stocks": 50, "bonds": 25, "gold": 15, "mf": 10},
            "aggressive": {"stocks": 70, "bonds": 10, "gold": 10, "mf": 10}
        }
        
        if risk_level not in allocation_mapping:
            return new_portfolio
        
        target_allocation = allocation_mapping[risk_level]
        current_value = AnalysisTools.calculate_current_value(new_portfolio)
        
        # This is simplified - in reality would need rebalancing logic
        new_portfolio["risk_level"] = risk_level
        new_portfolio["target_allocation"] = target_allocation
        
        return new_portfolio
    
    @staticmethod
    def simulate_returns(portfolio: Dict[str, Any], years: int, annual_return_rate: float) -> Dict[str, Any]:
        """Simulate expected returns over time"""
        current_value = AnalysisTools.calculate_current_value(portfolio)
        
        projected_values = []
        
        for year in range(1, years + 1):
            projected_value = current_value * ((1 + annual_return_rate/100) ** year)
            gain = projected_value - current_value
            gain_percentage = 0.0 if current_value == 0 else (gain / current_value * 100)
            projected_values.append({
                "year": year,
                "projected_value": round(projected_value, 2),
                "gain": round(gain, 2),
                "gain_percentage": round(gain_percentage, 2)
            })
        
        return {
            "current_value": current_value,
            "annual_return_rate": annual_return_rate,
            "years": years,
            "projections": projected_values,
            "final_projected_value": projected_values[-1]["projected_value"] if projected_values else current_value
        }
    
    @staticmethod
    def compare_portfolios(original: Dict[str, Any], modified: Dict[str, Any]) -> Dict[str, Any]:
        """Compare original portfolio with modified portfolio"""
        original_analysis = AnalysisTools.generate_analysis_report(original)
        modified_analysis = AnalysisTools.generate_analysis_report(modified)
        
        differences = {
            "total_investment": {
                "original": original_analysis["total_investment"],
                "modified": modified_analysis["total_investment"],
                "change": round(modified_analysis["total_investment"] - original_analysis["total_investment"], 2)
            },
            "current_value": {
                "original": original_analysis["current_value"],
                "modified": modified_analysis["current_value"],
                "change": round(modified_analysis["current_value"] - original_analysis["current_value"], 2)
            },
            "profit_loss": {
                "original": original_analysis["profit_loss"],
                "modified": modified_analysis["profit_loss"],
                "change_amount": round(
                    modified_analysis["profit_loss"]["amount"] - original_analysis["profit_loss"]["amount"], 2
                )
            },
            "risk_score": {
                "original": original_analysis["risk_score"],
                "modified": modified_analysis["risk_score"],
                "change": round(modified_analysis["risk_score"] - original_analysis["risk_score"], 2)
            },
            "diversification_score": {
                "original": original_analysis["diversification_score"],
                "modified": modified_analysis["diversification_score"],
                "change": round(modified_analysis["diversification_score"] - original_analysis["diversification_score"], 2)
            },
            "health_score": {
                "original": original_analysis["health_score"]["score"],
                "modified": modified_analysis["health_score"]["score"],
                "change": round(
                    modified_analysis["health_score"]["score"] - original_analysis["health_score"]["score"], 2
                )
            }
        }
        
        comparison = {
            "original": original_analysis,
            "modified": modified_analysis,
            "differences": differences
        }
        
        # Add improvements after building comparison
        comparison["improvements"] = SimulationTools.identify_improvements(comparison)
        
        return comparison
    
    @staticmethod
    def identify_improvements(comparison: Dict[str, Any]) -> List[str]:
        """Identify improvements in modified portfolio"""
        improvements = []
        
        differences = comparison.get("differences", {})
        
        # Check diversification improvement
        if differences.get("diversification_score", {}).get("change", 0) > 0:
            improvements.append("✓ Better diversification")
        
        # Check risk reduction
        if differences.get("risk_score", {}).get("change", 0) < 0:
            improvements.append("✓ Lower risk")
        
        # Check profit improvement
        if differences.get("profit_loss", {}).get("change_amount", 0) > 0:
            improvements.append("✓ Higher profit potential")
        
        # Check health score improvement
        if differences.get("health_score", {}).get("change", 0) > 0:
            improvements.append("✓ Better portfolio health")
        
        return improvements if improvements else ["= No significant changes"]
    
    @staticmethod
    def rebalance_portfolio(portfolio: Dict[str, Any], target_allocation: Dict[str, float]) -> Dict[str, Any]:
        """Rebalance portfolio to achieve target allocation"""
        new_portfolio = copy.deepcopy(portfolio)
        current_value = AnalysisTools.calculate_current_value(new_portfolio)
        
        rebalancing_actions = []
        
        # Calculate target values for each asset class
        for asset_class, target_percent in target_allocation.items():
            target_value = current_value * (target_percent / 100)
            
            if asset_class == "stocks":
                current_stock_value = sum(
                    s.get("quantity", 0) * s.get("current_price", s.get("buy_price", 0))
                    for s in new_portfolio.get("stocks", [])
                )
                action = "buy" if current_stock_value < target_value else "sell"
                amount = abs(target_value - current_stock_value)
                
                rebalancing_actions.append({
                    "asset_class": asset_class,
                    "action": action,
                    "amount": round(amount, 2)
                })
        
        new_portfolio["rebalancing_actions"] = rebalancing_actions
        
        return new_portfolio
