from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
import yaml
import os
import json
from typing import List
from src.utils.logger import logger
from src.utils.error_handler import safe_execute, AgentExecutionError
from src.schema import InsightOutput

# Load config
with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

class InsightAgent:
    def __init__(self):
        logger.info("Initializing InsightAgent")
        self.llm = ChatGroq(
            model=config["llm"]["model"],
            temperature=config["llm"]["temperature"],
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

    @safe_execute(default_return="[]", log_context="InsightAgent.analyze", retries=3)
    def analyze(self, data_summary: str, context: str) -> str:
        """
        Analyzes the data summary to generate structured insights.
        Returns a JSON string list of InsightOutput objects.
        """
        logger.info(f"Analyzing data for context: {context}")
        
        system_prompt = """You are an Insight Agent. Your goal is to interpret data summaries and find the "Why".
You will be given a context (what we are looking for) and a data summary (markdown table or text).

Your output MUST be a valid JSON list of objects matching this schema:
{
  "hypothesis": "The core hypothesis for the performance change",
  "evidence": [
    {
      "metric": "The metric that changed (e.g., 'ctr', 'cpm')",
      "delta": "The change value (e.g., '-32%', '+15%')",
      "segment": "The segment where this was observed (e.g., 'Campaign A')"
    }
  ],
  "impact": "High" | "Medium" | "Low",
  "confidence": 0.0 to 1.0,
  "reasoning": "Explanation of how the evidence supports the hypothesis"
}

CRITICAL:
1. "evidence" must be specific. Do not say "CTR dropped". Say "CTR dropped by 32%".
2. "confidence" should be based on the strength of the data.
3. Return ONLY the JSON list. No markdown formatting like ```json.
"""
        
        structured_llm = self.llm.with_structured_output(List[InsightOutput])
        
        try:
            response = structured_llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Context: {context}\n\nData Summary:\n{data_summary}")
            ])
            
            # Log decision
            logger.decision("InsightAgent", context, str(response)[:100], "Generated structured insights")
            
            # Convert back to JSON string for the pipeline
            return json.dumps([insight.model_dump() for insight in response])
            
        except Exception as e:
            logger.error(f"Failed to generate structured insights: {e}")
            raise AgentExecutionError("LLM failed to produce valid JSON insights.")
