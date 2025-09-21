import yfinance as yf
import pandas as pd
import numpy as np
import json
from langchain.tools import Tool
from typing import Dict, Any, List
from config.settings import ResearchConfig

class FinancialDataTool:
    @staticmethod
    def fetch_stock_data(symbols: List[str]) -> Dict[str, Any]:
        """Fetch comprehensive stock data for research"""
        research_data = {}
        
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                
                # Get historical data
                hist_data = ticker.history(period=ResearchConfig.ANALYSIS_PERIOD)
                info = ticker.info
                
                if hist_data.empty:
                    research_data[symbol] = {"error": f"No data available for {symbol}"}
                    continue
                
                # Calculate research metrics
                returns = hist_data['Close'].pct_change().dropna()
                
                research_data[symbol] = {
                    "basic_info": {
                        "company_name": info.get('longName', symbol),
                        "sector": info.get('sector', 'Unknown'),
                        "market_cap": info.get('marketCap', 'N/A'),
                        "current_price": round(hist_data['Close'].iloc[-1], 2)
                    },
                    "risk_metrics": {
                        "daily_volatility": round(returns.std(), 6),
                        "annualized_volatility": round(returns.std() * np.sqrt(252), 4),
                        "beta": info.get('beta', 'N/A'),
                        "sharpe_ratio": FinancialDataTool._calculate_sharpe_ratio(returns),
                        "max_drawdown": FinancialDataTool._calculate_max_drawdown(hist_data['Close'])
                    },
                    "performance_metrics": {
                        "total_return_2y": round(((hist_data['Close'].iloc[-1] / hist_data['Close'].iloc[0]) - 1) * 100, 2),
                        "avg_daily_return": round(returns.mean(), 6),
                        "avg_volume": int(hist_data['Volume'].mean()),
                        "price_range_52w": {
                            "high": round(hist_data['Close'].max(), 2),
                            "low": round(hist_data['Close'].min(), 2)
                        }
                    },
                    "statistical_data": {
                        "skewness": round(returns.skew(), 4),
                        "kurtosis": round(returns.kurtosis(), 4),
                        "data_points": len(hist_data),
                        "analysis_period": ResearchConfig.ANALYSIS_PERIOD
                    }
                }
                
            except Exception as e:
                research_data[symbol] = {"error": f"Error fetching data for {symbol}: {str(e)}"}
        
        return research_data
    
    @staticmethod
    def _calculate_sharpe_ratio(returns: pd.Series) -> float:
        """Calculate Sharpe ratio for research"""
        if len(returns) == 0:
            return 0.0
        
        excess_returns = returns - (ResearchConfig.RISK_FREE_RATE / 252)  # Daily risk-free rate
        if excess_returns.std() == 0:
            return 0.0
        
        sharpe = (excess_returns.mean() / excess_returns.std()) * np.sqrt(252)
        return round(sharpe, 4)
    
    @staticmethod
    def _calculate_max_drawdown(prices: pd.Series) -> float:
        """Calculate maximum drawdown"""
        peak = prices.cummax()
        drawdown = (prices - peak) / peak
        max_drawdown = drawdown.min()
        return round(max_drawdown, 4)

def create_financial_data_tool():
    def financial_data_wrapper(symbols_str: str) -> str:
        symbols = [s.strip().upper() for s in symbols_str.split(',')]
        data = FinancialDataTool.fetch_stock_data(symbols)
        return json.dumps(data, indent=2)  # LLM-friendly JSON output
    
    return Tool(
        name="financial_data_research",
        description=(
            "Fetch financial and risk metrics for given stock symbols. "
            "Input: comma-separated stock symbols (e.g. 'AAPL, MSFT, TSLA'). "
            "Output: JSON with company info, risk metrics, performance metrics, and statistical data."
        ),
        func=financial_data_wrapper
    )
