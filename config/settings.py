import os
from dotenv import load_dotenv

load_dotenv()

class ResearchConfig:
    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")
    
    if not GOOGLE_API_KEY:
        raise ValueError("Missing GOOGLE_API_KEY in .env file")
    if not SERPER_API_KEY:
        raise ValueError("Missing SERPER_API_KEY in .env file")
    
    # Research Parameters
    ANALYSIS_PERIOD = "2y"  # 2 years of data for research
    RISK_FREE_RATE = 0.05   # 5% risk-free rate
    CONFIDENCE_LEVELS = [0.95, 0.99]  # 95% and 99% confidence intervals
    
    # Output settings
    OUTPUT_DIR = "outputs/research_reports"
    DATASET_DIR = "outputs/datasets"
    VISUALIZATION_DIR = "outputs/visualizations"
    
    # Ensure directories exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(DATASET_DIR, exist_ok=True)
    os.makedirs(VISUALIZATION_DIR, exist_ok=True)
