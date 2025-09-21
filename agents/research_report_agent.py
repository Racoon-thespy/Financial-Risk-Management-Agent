from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import ResearchConfig
from utils.helpers import get_research_timestamp, ensure_directories
from typing import Dict, Any, List

class ResearchReportAgent:
    """Agent for generating academic-quality research reports"""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=ResearchConfig.GOOGLE_API_KEY,
            temperature=0.1
        )
    
    def generate_research_report(self, research_data: Dict, analysis_data: Dict, symbols: List[str]) -> Dict[str, Any]:
        """Generate comprehensive academic research report"""
        
        report_prompt = f"""
        Generate a comprehensive Financial Risk Management Research Report following academic standards.
        
        Research Data: {research_data}
        Risk Analysis: {analysis_data}
        Symbols Studied: {', '.join(symbols)}
        
        Structure the report as follows:
        
        # FINANCIAL RISK MANAGEMENT RESEARCH REPORT
        
        ## EXECUTIVE SUMMARY
        Brief overview of research objectives, methodology, and key findings
        
        ## 1. INTRODUCTION
        - Research background and motivation
        - Problem statement and objectives
        - Scope and limitations
        
        ## 2. LITERATURE REVIEW
        - Relevant financial risk management theories
        - Current market context and research
        
        ## 3. METHODOLOGY
        - Data collection approach
        - Risk assessment framework
        - Analysis techniques employed
        
        ## 4. DATA ANALYSIS AND FINDINGS
        - Descriptive statistics
        - Risk metrics and calculations
        - Comparative analysis results
        
        ## 5. RISK ASSESSMENT RESULTS
        - Individual asset risk profiles
        - Portfolio implications
        - Key risk factors identified
        
        ## 6. DISCUSSION
        - Interpretation of results
        - Practical implications
        - Theoretical contributions
        
        ## 7. RECOMMENDATIONS
        - Risk management strategies
        - Portfolio optimization suggestions
        - Future research directions
        
        ## 8. CONCLUSION
        Summary of key findings and their significance
        
        ## REFERENCES
        [Note: In actual implementation, this would include proper citations]
        
        Ensure academic rigor, clear methodology explanation, and evidence-based conclusions.
        """
        
        try:
            response = self.llm.invoke(report_prompt)
            report_content = response.content
            
            # Save the report
            ensure_directories()
            timestamp = get_research_timestamp()
            filename = f"financial_risk_research_report_{timestamp}.md"
            filepath = f"outputs/research_reports/{filename}"
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            # Create metadata
            metadata = {
                "report_title": "Financial Risk Management Research Report",
                "symbols_analyzed": symbols,
                "timestamp": timestamp,
                "filename": filename,
                "filepath": filepath,
                "analysis_period": ResearchConfig.ANALYSIS_PERIOD,
                "research_type": "Academic Financial Risk Assessment"
            }
            
            # Save metadata
            metadata_file = f"outputs/research_reports/metadata_{timestamp}.json"
            import json
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            return {
                "report_content": report_content,
                "metadata": metadata,
                "success": True
            }
            
        except Exception as e:
            return {"error": f"Report generation error: {str(e)}", "success": False}
