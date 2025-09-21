import streamlit as st
from main import FinancialRiskResearchOrchestrator
import os
import json
import time

def load_css():
    """Load custom CSS for academic appearance"""
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #1f4e79 0%, #2980b9 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .research-metrics {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #007bff;
        margin-bottom: 1rem;
    }
    .phase-indicator {
        background-color: #e3f2fd;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Financial Risk Management Research System",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    load_css()
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🎓 Financial Risk Management Research System</h1>
        <p>Academic Multi-Agent System for Financial Risk Analysis</p>
        <p><em>Final Year Research Project</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("🔧 Research Configuration")
        
        if not os.getenv("GOOGLE_API_KEY"):
            st.error("⚠️ GOOGLE_API_KEY not found in environment variables")
            st.stop()
        
        symbols_input = st.text_input("Enter Stock Symbols (comma-separated)", value="AAPL,MSFT,GOOGL")
        research_focus = st.text_area("Research Focus", value="Technology sector risk analysis with focus on market volatility and systematic risk factors")
        study_name = st.text_input("Study Name", value="Tech Sector Financial Risk Assessment")
        
        start_button = st.button("🚀 Start Research Study", type="primary")
    
    if start_button:
        symbols = [s.strip().upper() for s in symbols_input.split(",") if s.strip()]
        if not symbols:
            st.error("Please enter at least one stock symbol.")
            return
        
        orchestrator = FinancialRiskResearchOrchestrator()
        
        st.info("🔍 Starting research study... This may take a few minutes.")
        start_time = time.time()
        
        with st.spinner("Running multi-agent research process..."):
            results = orchestrator.conduct_comprehensive_study(
                symbols=symbols,
                research_focus=research_focus,
                study_name=study_name
            )
        
        if "error" in results:
            st.error(f"❌ Research study failed: {results['error']}")
            return
        
        total_time = time.time() - start_time
        st.markdown(f"""
        <div class="success-box">
        <h3>✅ Research Study Completed Successfully</h3>
        <p><strong>Study Name:</strong> {study_name}</p>
        <p><strong>Symbols:</strong> {', '.join(symbols)}</p>
        <p><strong>Duration:</strong> {total_time:.1f} seconds</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show JSON results preview
        st.subheader("📊 Study Results")
        st.json(results)
        
        # Offer download
        results_json = json.dumps(results, indent=2)
        st.download_button(
            label="📥 Download Results JSON",
            data=results_json,
            file_name=f"{results['study_metadata']['study_id']}_results.json",
            mime="application/json"
        )
        
        st.success("You can find the full academic report in the `outputs/research_reports/` folder.")

if __name__ == "__main__":
    main()
