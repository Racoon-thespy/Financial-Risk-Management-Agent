import numpy as np
import pandas as pd
from scipy import stats
import json
from datetime import datetime
from langchain.tools import Tool
from typing import List, Dict, Any
from config.settings import ResearchConfig

class RiskCalculator:
    @staticmethod
    def calculate_value_at_risk(returns: List[float], confidence_levels: List[float] = None) -> Dict[str, float]:
        """Calculate Value at Risk (VaR) and CVaR for research"""
        if confidence_levels is None:
            confidence_levels = ResearchConfig.CONFIDENCE_LEVELS
        
        if len(returns) == 0:
            return {"error": "No returns provided for VaR calculation"}
        
        returns_array = np.array(returns)
        var_results = {}
        
        for confidence in confidence_levels:
            var_historical = np.percentile(returns_array, (1 - confidence) * 100)
            mean_return = np.mean(returns_array)
            std_return = np.std(returns_array)
            var_parametric = mean_return + std_return * stats.norm.ppf(1 - confidence)
            
            # Conditional VaR (Expected Shortfall)
            cvar = returns_array[returns_array <= var_historical].mean()
            
            var_results[f"VaR_{int(confidence*100)}%_historical"] = round(var_historical, 6)
            var_results[f"VaR_{int(confidence*100)}%_parametric"] = round(var_parametric, 6)
            var_results[f"CVaR_{int(confidence*100)}%"] = round(cvar, 6)
        
        return var_results
    
    @staticmethod
    def calculate_portfolio_metrics(weights: List[float], returns_matrix: np.ndarray) -> Dict[str, float]:
        """Calculate portfolio risk metrics for research"""
        try:
            if len(weights) == 0 or returns_matrix.size == 0:
                return {"error": "Weights or returns matrix missing for portfolio calculation"}
            
            weights = np.array(weights)
            portfolio_returns = np.dot(returns_matrix, weights)
            
            portfolio_volatility = np.std(portfolio_returns) * np.sqrt(252)
            portfolio_return = np.mean(portfolio_returns) * 252
            
            excess_return = portfolio_return - ResearchConfig.RISK_FREE_RATE
            sharpe_ratio = excess_return / portfolio_volatility if portfolio_volatility > 0 else 0
            
            return {
                "portfolio_return_annualized": round(portfolio_return, 4),
                "portfolio_volatility_annualized": round(portfolio_volatility, 4),
                "sharpe_ratio": round(sharpe_ratio, 4),
                "number_of_assets": len(weights),
                "timestamp": __import__("datetime").datetime.now().isoformat()
            }
        
        except Exception as e:
            return {"error": str(e)}

def create_risk_calculator_tool():
    def risk_wrapper(input_str: str) -> str:
        try:
            data = json.loads(input_str)
            calculation_type = data.get("calculation_type")
            
            if calculation_type == "VaR":
                result = RiskCalculator.calculate_value_at_risk(data.get("returns", []))
            elif calculation_type == "portfolio":
                result = RiskCalculator.calculate_portfolio_metrics(
                    data.get("weights", []), 
                    np.array(data.get("returns_matrix", []))
                )
            else:
                result = {"error": "Unknown calculation type"}
            
            return json.dumps(result, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)
    
    return Tool(
        name="risk_calculator",
        description=(
            "Perform advanced financial risk calculations (VaR, CVaR, portfolio metrics). "
            "Input: JSON with calculation_type ('VaR' or 'portfolio'), returns, and/or weights."
        ),
        func=risk_wrapper
    )
