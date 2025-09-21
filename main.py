from agents.data_research_agent import DataResearchAgent
from agents.risk_analysis_agent import RiskAnalysisAgent
from agents.research_report_agent import ResearchReportAgent
from utils.helpers import ensure_directories, save_research_data, get_research_timestamp, log_error
from typing import List, Dict, Any
import time

class FinancialRiskResearchOrchestrator:
    """Main orchestrator for the Financial Risk Management Research System"""
    
    def __init__(self):
        print("🔬 Initializing Financial Risk Management Research System...")
        self.data_research_agent = DataResearchAgent()
        self.risk_analysis_agent = RiskAnalysisAgent()
        self.research_report_agent = ResearchReportAgent()
        ensure_directories()
        print("✅ Research system initialized successfully!")
    
    def conduct_comprehensive_study(self, 
                                  symbols: List[str], 
                                  research_focus: str = "",
                                  study_name: str = "Financial Risk Analysis") -> Dict[str, Any]:
        study_id = get_research_timestamp()
        total_start = time.time()
        
        print(f"\n📊 Starting Research Study: {study_name}")
        print(f"🏷️  Study ID: {study_id}")
        print(f"🎯 Symbols: {', '.join(symbols)}")
        print(f"🔍 Focus: {research_focus}")
        print("="*60)
        
        study_results = {
            "study_metadata": {
                "study_id": study_id,
                "study_name": study_name,
                "symbols": symbols,
                "research_focus": research_focus,
                "start_time": study_id
            }
        }
        
        try:
            # Phase 1: Data Research
            print("📚 Phase 1: Conducting comprehensive data research...")
            start_time = time.time()
            
            research_results = self.data_research_agent.conduct_research(
                symbols=symbols, 
                research_focus=research_focus
            )
            
            if "error" in research_results:
                return {"error": f"Research phase failed: {research_results['error']}"}
            
            study_results["data_research"] = research_results
            print(f"✅ Phase 1 completed in {time.time() - start_time:.1f} seconds")
            
            data_path = save_research_data(research_results, f"research_data_{study_id}.json")
            study_results["data_research_path"] = data_path
            print(f"💾 Data saved: {data_path}")
            
            # Phase 2: Risk Analysis
            print("\n🧮 Phase 2: Performing quantitative risk analysis...")
            start_time = time.time()
            
            analysis_results = self.risk_analysis_agent.analyze_financial_risk(
                research_data=research_results,
                symbols=symbols
            )
            
            if "error" in analysis_results:
                return {"error": f"Analysis phase failed: {analysis_results['error']}"}
            
            study_results["risk_analysis"] = analysis_results
            print(f"✅ Phase 2 completed in {time.time() - start_time:.1f} seconds")
            
            # Phase 3: Research Report
            print("\n📝 Phase 3: Generating academic research report...")
            start_time = time.time()
            
            report_results = self.research_report_agent.generate_research_report(
                research_data=research_results,
                analysis_data=analysis_results,
                symbols=symbols
            )
            
            if not report_results.get("success", False):
                return {"error": f"Report generation failed: {report_results.get('error', 'Unknown error')}"}
            
            study_results["research_report"] = report_results
            print(f"✅ Phase 3 completed in {time.time() - start_time:.1f} seconds")
            
            complete_path = save_research_data(study_results, f"complete_study_{study_id}.json")
            print(f"💾 Complete study saved: {complete_path}")
            
            print("\n" + "="*60)
            print("🎉 RESEARCH STUDY COMPLETED SUCCESSFULLY!")
            print(f"📁 Report saved: {report_results['metadata']['filepath']}")
            print(f"⏱️ Total Study Duration: {time.time() - total_start:.1f} seconds")
            print("="*60)
            
            return study_results
            
        except Exception as e:
            error_msg = f"Research study failed: {str(e)}"
            log_error(error_msg)
            print(f"❌ {error_msg}")
            return {"error": error_msg}

    def get_study_summary(self, study_results: Dict[str, Any]) -> str:
        ...
