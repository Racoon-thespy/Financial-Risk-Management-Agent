from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import ResearchConfig
from utils.helpers import get_research_timestamp
from typing import Dict, Any, List

class RiskAnalysisAgent:
    """Agent for quantitative risk analysis and academic assessment"""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=ResearchConfig.GOOGLE_API_KEY,
            temperature=0.1
        )
    
    def analyze_financial_risk(self, research_data: Dict[str, Any], symbols: List[str]) -> Dict[str, Any]:
        """Perform academic-level financial risk analysis"""
        
        # Optional: Summarize research_data if very large to avoid token overflow
        analysis_prompt = f"""
        As a Financial Risk Management Researcher, perform a comprehensive quantitative and qualitative risk analysis.
        
        Research Data: {research_data}
        Assets Under Study: {', '.join(symbols)}
        
        Conduct analysis on:
        
        1. QUANTITATIVE RISK ASSESSMENT:
           - Volatility analysis and trends
           - Value at Risk (VaR) interpretation
           - Beta analysis and systematic risk
           - Correlation and portfolio implications
           
        2. QUALITATIVE RISK FACTORS:
           - Market risk factors
           - Industry-specific risks
           - Economic environment impact
           - Regulatory and operational risks
           
        3. COMPARATIVE ANALYSIS:
           - Risk-return profiles comparison
           - Benchmark against market indices
           - Peer comparison within sectors
           
        4. RESEARCH FINDINGS:
           - Key insights and patterns
           - Risk mitigation opportunities
           - Academic implications
           
        Provide a structured academic analysis with clear methodology and findings.
        """
        
        try:
            # Use predict() for safer single-prompt invocation
            analysis_result = self.llm.predict(analysis_prompt)
            
            return {
                "risk_analysis": analysis_result,
                "analysis_timestamp": get_research_timestamp(),
                "methodology": "Multi-factor risk analysis with quantitative and qualitative assessment",
                "symbols_analyzed": symbols,
                "analysis_type": "Academic Financial Risk Assessment",
                "success": True
            }
            
        except Exception as e:
            return {
                "error": f"Risk analysis error: {str(e)}",
                "success": False
            }
