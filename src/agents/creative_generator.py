from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
import yaml
import os
import json
from typing import List
from src.utils.logger import logger
from src.utils.error_handler import safe_execute, AgentExecutionError
from src.schema import CreativeOutput, InsightOutput

# Load config
with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

class CreativeGenerator:
    def __init__(self):
        logger.info("Initializing CreativeGenerator")
        self.llm = ChatGroq(
            model=config["llm"]["model"],
            temperature=0.7, # Higher temp for creativity
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

    @safe_execute(default_return=None, log_context="CreativeGenerator.generate", retries=3)
    def generate(self, insights_json: str, top_ads_context: str) -> CreativeOutput:
        """
        Generates creative recommendations based on structured insights.
        """
        logger.info("Generating creative recommendations...")
        
        system_prompt = """You are a Creative Strategy Agent.
Your goal is to generate new ad creatives that directly address performance issues identified in the insights.

Input:
1. Insights (JSON list of hypotheses and evidence)
2. Top Ads Context (What is currently working/not working)

Output MUST be a valid JSON object matching this schema:
{
  "recommendations": [
    {
      "campaign_name": "Name of the campaign to target",
      "current_performance_issue": "The specific issue (e.g., 'CTR dropped 32% due to ad fatigue')",
      "suggested_headline": "A new, punchy headline",
      "suggested_message": "The primary ad text",
      "reasoning": "Why this specific change will fix the issue identified in the insight"
    }
  ]
}

CRITICAL:
- The "reasoning" must explicitly link back to the "evidence" in the insight.
- Do not generate generic advice. Be specific.
"""
        
        structured_llm = self.llm.with_structured_output(CreativeOutput)
        
        try:
            response = structured_llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Insights:\n{insights_json}\n\nTop Ads Context:\n{top_ads_context}")
            ])
            
            # Log decision
            logger.decision("CreativeGenerator", insights_json, str(response)[:100], "Generated creative recommendations")
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to generate creatives: {e}")
            raise AgentExecutionError("LLM failed to produce valid creative recommendations.")
