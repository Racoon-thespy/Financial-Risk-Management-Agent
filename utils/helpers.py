import os
import json
import pandas as pd
import streamlit as st
from datetime import datetime
from typing import Dict, Any, List

def ensure_directories():
    """Create necessary output directories"""
    dirs = ["outputs/research_reports", "outputs/datasets", "outputs/visualizations"]
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)

def save_research_data(data: Dict[Any, Any], filename: str) -> str:
    """Save research data with timestamp and return full file path"""
    ensure_directories()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"outputs/datasets/{timestamp}_{filename}"
    
    if isinstance(data, pd.DataFrame):
        filepath = filepath + ".csv"
        data.to_csv(filepath, index=False)
    else:
        filepath = filepath + ".json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
    
    return filepath

def get_research_timestamp() -> str:
    """Get timestamp for research outputs"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def display_research_data(data: Dict[Any, Any], title: str = "Research Data"):
    """Optional Streamlit display for quick inspection"""
    try:
        st.subheader(title)
        if isinstance(data, pd.DataFrame):
            st.dataframe(data)
        else:
            st.json(data)
    except Exception:
        # Streamlit not available or not running in UI context
        pass

def log_error(message: str):
    """Append error logs to a file with timestamp"""
    ensure_directories()
    log_file = "outputs/research_reports/error_log.txt"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat()}] {message}\n")
