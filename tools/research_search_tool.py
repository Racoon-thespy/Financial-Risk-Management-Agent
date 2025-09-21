import requests
import json
from langchain.tools import Tool
from config.settings import ResearchConfig
from typing import List, Dict

class ResearchSearchTool:
    def __init__(self):
        self.api_key = ResearchConfig.SERPER_API_KEY
        self.base_url = "https://google.serper.dev/search"
    
    def search_financial_research(self, query: str, focus: str = "academic") -> str:
        """Search for financial research and academic sources"""
        if not self.api_key:
            return json.dumps({"error": "SERPER_API_KEY not set in environment variables"}, indent=2)
        
        try:
            research_query = f"{query} financial risk management research {focus}"
            
            payload = {"q": research_query, "num": 8, "gl": "us", "hl": "en"}
            headers = {"X-API-KEY": self.api_key, "Content-Type": "application/json"}
            
            response = requests.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            research_results = []
            
            if "organic" in data:
                for result in data["organic"][:6]:
                    research_results.append({
                        "title": result.get("title", ""),
                        "snippet": result.get("snippet", ""),
                        "source": result.get("link", ""),
                        "relevance_score": self._calculate_relevance(result, query)
                    })
            
            if not research_results:
                return json.dumps({"message": "No relevant research results found."}, indent=2)
            
            research_results.sort(key=lambda x: x["relevance_score"], reverse=True)
            
            return json.dumps({
                "query": research_query,
                "timestamp": __import__("datetime").datetime.now().isoformat(),
                "results": research_results[:5]
            }, indent=2)
        
        except Exception as e:
            return json.dumps({"error": f"Research search error: {str(e)}"}, indent=2)
    
    def _calculate_relevance(self, result: Dict, query: str) -> float:
        title = result.get("title", "").lower()
        snippet = result.get("snippet", "").lower()
        link = result.get("link", "").lower()
        
        research_keywords = [
            "study", "analysis", "research", "journal", "academic", "university", 
            "financial", "risk", "volatility", "portfolio", "investment"
        ]
        
        score = 0
        for keyword in research_keywords:
            if keyword in title:
                score += 3
            if keyword in snippet:
                score += 2
            if keyword in link:
                score += 1
        
        return score

def create_research_search_tool():
    search_tool = ResearchSearchTool()
    
    return Tool(
        name="research_search",
        description=(
            "Search for financial risk management research, academic papers, and market analysis. "
            "Returns JSON with query, timestamp, and top 5 most relevant results."
        ),
        func=search_tool.search_financial_research
    )
