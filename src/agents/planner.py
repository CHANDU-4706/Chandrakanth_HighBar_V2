from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from typing import List
import yaml
import os
from src.utils.logger import logger
from src.utils.error_handler import safe_execute, AgentError

# Load config
with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

class PlanStep(BaseModel):
    step_name: str = Field(description="Name of the step")
    description: str = Field(description="Detailed description of what to do in this step")
    agent: str = Field(description="Which agent should perform this step (DataAgent, InsightAgent, CreativeGenerator)")

class Plan(BaseModel):
    steps: List[PlanStep]

class PlannerAgent:
    def __init__(self):
        logger.info("Initializing PlannerAgent")
        self.llm = ChatGroq(
            model=config["llm"]["model"],
            temperature=config["llm"]["temperature"],
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

    @safe_execute(log_context="PlannerAgent.create_plan", raise_on_error=True, retries=3)
    def create_plan(self, user_query: str) -> Plan:
        logger.info(f"Creating plan for query: {user_query}")
        with open("prompts/planner_prompt.md", "r") as f:
            system_prompt = f.read()
        
        structured_llm = self.llm.with_structured_output(Plan)
        return structured_llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_query)
        ])
