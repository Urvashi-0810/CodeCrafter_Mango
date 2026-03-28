import numpy as np
from typing import Dict, List, Any
from datetime import datetime


class AnalysisTools:
    """Tools for portfolio analysis and metrics calculation"""
    
    @staticmethod
    def calculate_total_investment(portfolio: Dict[str, Any]) -> float:
        """Calculate total investment amount"""
        total = 0
        
        # Stocks
        for stock in portfolio.get("stocks", []):
            total += stock.get("quantity", 0) * stock.get("buy_price", 0)
        
        # Mutual funds
        for mf in portfolio.get("mutual_funds", []):
            total += mf.get("investment", 0)
        
        # Bonds
        for bond in portfolio.get("bonds", []):
            total += bond.get("principal", 0)
        
        # Gold
        gold = portfolio.get("gold", {})
        total += gold.get("investment", 0)
        
        return round(total, 2)
    
    @staticmethod
    def calculate_current_value(portfolio: Dict[str, Any]) -> float:
        """Calculate current portfolio value"""
        current_value = 0
        
        for stock in portfolio.get("stocks", []):
            current_value += stock.get("quantity", 0) * stock.get("current_price", stock.get("buy_price", 0))
        
        for mf in portfolio.get("mutual_funds", []):
            current_value += mf.get("current_value", mf.get("investment", 0))
        
        for bond in portfolio.get("bonds", []):
            current_value += bond.get("current_value", bond.get("principal", 0))
        
        gold = portfolio.get("gold", {})
        current_value += gold.get("current_value", gold.get("investment", 0))
        
        return round(current_value, 2)
    
    @staticmethod
    def calculate_profit_loss(portfolio: Dict[str, Any]) -> Dict[str, float]:
        """Calculate profit/loss"""
        total_investment = AnalysisTools.calculate_total_investment(portfolio)
        current_value = AnalysisTools.calculate_current_value(portfolio)
        
        pl_amount = current_value - total_investment
        pl_percentage = (pl_amount / total_investment * 100) if total_investment > 0 else 0
        
        return {
            "amount": round(pl_amount, 2),
            "percentage": round(pl_percentage, 2),
            "status": "gain" if pl_amount > 0 else "loss"
        }
    
    @staticmethod
    def calculate_sector_allocation(portfolio: Dict[str, Any]) -> Dict[str, float]:
        """Calculate sector-wise allocation"""
        sector_values = {}
        total_value = AnalysisTools.calculate_current_value(portfolio)
        
        for stock in portfolio.get("stocks", []):
            sector = stock.get("sector", "Unknown")
            value = stock.get("quantity", 0) * stock.get("current_price", stock.get("buy_price", 0))
            
            if sector not in sector_values:
                sector_values[sector] = 0
            sector_values[sector] += value
        
        # Convert to percentages
        allocation = {}
        for sector, value in sector_values.items():
            allocation[sector] = round((value / total_value * 100) if total_value > 0 else 0, 2)
        
        return allocation
    
    @staticmethod
    def calculate_risk_score(portfolio: Dict[str, Any]) -> float:
        """Calculate portfolio risk score (0-100)"""
        risk_score = 0
        
        # High volatility stocks = higher risk
        stock_count = len(portfolio.get("stocks", []))
        mutual_fund_count = len(portfolio.get("mutual_funds", []))
        bond_count = len(portfolio.get("bonds", []))
        gold_allocation = len(portfolio.get("gold", {}))
        
        # More stocks = higher risk
        risk_score += min(stock_count * 3, 40)
        
        # Fewer bonds and gold = higher risk
        risk_score += max(0, 30 - (bond_count + gold_allocation) * 5)
        
        # Allocation diversity
        allocation = AnalysisTools.calculate_sector_allocation(portfolio)
        if allocation:
            concentration = max(allocation.values())
            concentration_risk = min(concentration / 30 * 30, 30)
            risk_score += concentration_risk
        
        return round(min(risk_score, 100), 2)
    
    @staticmethod
    def calculate_diversification_score(portfolio: Dict[str, Any]) -> float:
        """Calculate diversification score (0-100)"""
        diversification = 0
        
        # Number of different stocks
        stock_count = len(portfolio.get("stocks", []))
        diversification += min(stock_count * 3, 25)
        
        # Sector diversity
        allocation = AnalysisTools.calculate_sector_allocation(portfolio)
        unique_sectors = len(allocation)
        diversification += min(unique_sectors * 4, 25)
        
        # Asset class diversity
        asset_classes = 0
        if len(portfolio.get("stocks", [])) > 0:
            asset_classes += 1
        if len(portfolio.get("mutual_funds", [])) > 0:
            asset_classes += 1
        if len(portfolio.get("bonds", [])) > 0:
            asset_classes += 1
        if portfolio.get("gold", {}):
            asset_classes += 1
        
        diversification += asset_classes * 12.5
        
        # Concentration risk (inverse)
        if allocation:
            max_allocation = max(allocation.values())
            concentration_reduction = max(0, 100 - max_allocation * 2)
            diversification += concentration_reduction * 0.25
        
        return round(min(diversification, 100), 2)
    
    @staticmethod
    def calculate_volatility(portfolio: Dict[str, Any]) -> float:
        """Calculate portfolio volatility"""
        # Simplified volatility calculation
        risk_score = AnalysisTools.calculate_risk_score(portfolio)
        volatility = risk_score * 0.5  # Simplified
        
        return round(volatility, 2)
    
    @staticmethod
    def calculate_concentration_risk(portfolio: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate concentration risk and identify heavily weighted positions"""
        allocation = AnalysisTools.calculate_sector_allocation(portfolio)
        current_value = AnalysisTools.calculate_current_value(portfolio)
        
        high_concentration_sectors = {
            sector: allocation for sector, allocation in allocation.items()
            if allocation > 30
        }
        
        return {
            "concentration_risk_level": "High" if high_concentration_sectors else "Normal",
            "heavily_weighted_sectors": high_concentration_sectors,
            "max_allocation": max(allocation.values()) if allocation else 0
        }
    
    @staticmethod
    def calculate_asset_allocation(portfolio: Dict[str, Any]) -> Dict[str, float]:
        """Calculate asset class allocation"""
        total_value = AnalysisTools.calculate_current_value(portfolio)
        
        stock_value = sum(s.get("quantity", 0) * s.get("current_price", s.get("buy_price", 0)) 
                         for s in portfolio.get("stocks", []))
        mf_value = sum(m.get("current_value", m.get("investment", 0)) 
                      for m in portfolio.get("mutual_funds", []))
        bond_value = sum(b.get("current_value", b.get("principal", 0)) 
                        for b in portfolio.get("bonds", []))
        gold_value = portfolio.get("gold", {}).get("current_value", 
                                                   portfolio.get("gold", {}).get("investment", 0))
        
        return {
            "stocks": round((stock_value / total_value * 100) if total_value > 0 else 0, 2),
            "mutual_funds": round((mf_value / total_value * 100) if total_value > 0 else 0, 2),
            "bonds": round((bond_value / total_value * 100) if total_value > 0 else 0, 2),
            "gold": round((gold_value / total_value * 100) if total_value > 0 else 0, 2)
        }
    
    @staticmethod
    def calculate_portfolio_health_score(portfolio: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall portfolio health score"""
        diversification = AnalysisTools.calculate_diversification_score(portfolio)
        risk = AnalysisTools.calculate_risk_score(portfolio)
        
        # Health score = high diversification and moderate risk
        health_score = (diversification * 0.6) + ((100 - abs(50 - risk)) * 0.4)
        
        health_status = "Excellent" if health_score > 75 else "Good" if health_score > 50 else "Fair" if health_score > 25 else "Poor"
        
        return {
            "score": round(health_score, 2),
            "status": health_status,
            "diversification": diversification,
            "risk": risk,
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def generate_analysis_report(portfolio: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive portfolio analysis report"""
        return {
            "timestamp": datetime.now().isoformat(),
            "total_investment": AnalysisTools.calculate_total_investment(portfolio),
            "current_value": AnalysisTools.calculate_current_value(portfolio),
            "profit_loss": AnalysisTools.calculate_profit_loss(portfolio),
            "sector_allocation": AnalysisTools.calculate_sector_allocation(portfolio),
            "asset_allocation": AnalysisTools.calculate_asset_allocation(portfolio),
            "risk_score": AnalysisTools.calculate_risk_score(portfolio),
            "diversification_score": AnalysisTools.calculate_diversification_score(portfolio),
            "volatility": AnalysisTools.calculate_volatility(portfolio),
            "concentration_risk": AnalysisTools.calculate_concentration_risk(portfolio),
            "health_score": AnalysisTools.calculate_portfolio_health_score(portfolio)
        }
