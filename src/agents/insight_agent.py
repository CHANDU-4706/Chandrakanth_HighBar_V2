from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
import yaml
import os
from utils.logger import logger
from utils.error_handler import safe_execute

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

    @safe_execute(default_return="Error: InsightAgent failed to generate insights.", log_context="InsightAgent.analyze", retries=3)
    def analyze(self, data_summary: str, context: str) -> str:
        """
        Analyzes the data summary to generate insights.
        """
        logger.info(f"Analyzing data for context: {context}")
        system_prompt = """You are an Insight Agent. Your goal is to interpret data summaries and find the "Why".
You will be given a context (what we are looking for) and a data summary (markdown table or text).

Your output should be a list of hypotheses or insights.
Follow this reasoning structure:
1. Observation: What does the data show? (e.g., "ROAS dropped by 20% on Tuesday")
2. Analysis: What correlates with this? (e.g., "CPM increased by 40% on the same day")
3. Conclusion/Hypothesis: What is the likely cause? (e.g., "Audience saturation led to higher CPMs, driving down ROAS")

Format the output in Markdown.
"""
        response = self.llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Context: {context}\n\nData Summary:\n{data_summary}")
        ])
        return response.content
