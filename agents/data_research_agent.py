# data_research_agent.py
from typing import List, Dict, Any
from datetime import datetime
import logging

# --- LLM / LangChain imports (try multiple paths and give helpful errors) ---
try:
    # Google Gemini via the langchain-google-genai integration
    from langchain_google_genai import ChatGoogleGenerativeAI
except Exception as e:
    raise ImportError(
        "Could not import 'langchain_google_genai'. Install with: "
        "'pip install -U langchain-google-genai'\n"
        "Original error: " + str(e)
    ) from e

# Agent imports - different LangChain releases expose agent helpers in slightly
# different submodules, so try a couple of likely locations and bubble up a clear error.
try:
    from langchain.agents import create_react_agent, AgentExecutor
except Exception:
    try:
        # alternate import paths used in some versions
        from langchain.agents.react.agent import create_react_agent
        from langchain.agents.agent import AgentExecutor
    except Exception as e:
        raise ImportError(
            "Could not import create_react_agent / AgentExecutor from langchain. "
            "Make sure 'langchain' is installed and up-to-date: "
            "'pip install -U langchain'.\nOriginal error: " + str(e)
        ) from e

# PromptTemplate import (langchain_core.prompts or fallback)
try:
    from langchain_core.prompts import PromptTemplate
except Exception:
    try:
        from langchain_core.prompts.prompt import PromptTemplate
    except Exception:
        # final fallback for older installs
        from langchain.prompts import PromptTemplate

# Your project imports (these should exist in your repo)
from config.settings import ResearchConfig
from tools.financial_data_tool import create_financial_data_tool
from tools.research_search_tool import create_research_search_tool

logger = logging.getLogger(__name__)


# Fallback timestamp util — if you move this to a shared utils module, import it instead
try:
    # if you have a shared util, prefer importing that
    from utils import get_research_timestamp  # optional
except Exception:
    def get_research_timestamp() -> str:
        """Fallback timestamp generator (YYYYmmdd_HHMMSS)."""
        return datetime.now().strftime("%Y%m%d_%H%M%S")


class DataResearchAgent:
    """Agent responsible for comprehensive financial data research."""

    def __init__(self, model_name: str = "gemini-2.5-flash", temperature: float = 0.1):
        # instantiate the Gemini chat model via langchain-google-genai
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=ResearchConfig.GOOGLE_API_KEY,
            temperature=temperature,
        )

        # create tools (these factory functions should return LangChain BaseTool objects)
        self.tools = [
            create_financial_data_tool(),
            create_research_search_tool()
        ]

        # prompt template - keep it explicit about the expected input variables
        template = """
You are a Financial Research Analyst conducting academic-level research on financial risk management.

Available tools:
{tools}

Tool names: {tool_names}

Research Query: {input}

IMPORTANT: Only respond with a single tool call in strict JSON format:
{{"tool": "<tool_name>", "tool_input": "<input_string>"}}
Do not include any explanations or additional text.

Thought: {agent_scratchpad}
"""

        # from_template helper is commonly available
        try:
            self.prompt = PromptTemplate.from_template(template)
        except Exception:
            # fallback constructor
            self.prompt = PromptTemplate(template=template, input_variables=["input", "tools", "tool_names", "agent_scratchpad"])

        # create a ReAct agent and executor
        # create_react_agent(llm, tools, prompt) is a common pattern in LangChain docs
        self.agent = create_react_agent(self.llm, self.tools, self.prompt)

        # AgentExecutor wraps the agent + tools and runs iterations until finish
        self.executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            max_iterations=6,
            return_intermediate_steps=True,
            handle_parsing_errors=True,
        )

    def conduct_research(self, symbols: List[str], research_focus: str = "") -> Dict[str, Any]:
        """Conduct comprehensive financial research.

        Returns:
            A dict with keys: research_output, intermediate_steps, symbols_analyzed, research_timestamp
            or an error dict: {"error": "..."}
        """
        query = f"""
Conduct comprehensive financial risk research for: {', '.join(symbols)}

Research Focus: {research_focus}

Required analysis:
1. Fetch detailed financial data and risk metrics for each symbol
2. Search for recent market research and analysis
3. Identify key risk factors and market conditions
4. Gather relevant academic or industry research

Provide structured research findings.
"""

        try:
            # AgentExecutor historically exposes `invoke` and/or `run`. handle both.
            if hasattr(self.executor, "invoke"):
                result = self.executor.invoke({"input": query})
            elif hasattr(self.executor, "run"):
                raw = self.executor.run(query)
                # normalize to a dict with 'output'
                if isinstance(raw, dict):
                    result = raw
                else:
                    result = {"input": query, "output": raw}
            else:
                raise RuntimeError("AgentExecutor has neither 'invoke' nor 'run' methods in this installation.")

            # normalize result
            output = result.get("output") if isinstance(result, dict) else str(result)
            intermediate_steps = result.get("intermediate_steps", []) if isinstance(result, dict) else []

            return {
                "research_output": output,
                "intermediate_steps": intermediate_steps,
                "symbols_analyzed": symbols,
                "research_timestamp": get_research_timestamp(),
            }

        except Exception as e:
            logger.exception("Research agent failed")
            return {"error": f"Research error: {str(e)}"}
