import argparse
import asyncio
import os
import json
from dotenv import load_dotenv
import time
from agents.planner import PlannerAgent
from agents.data_agent import DataAgent
from agents.insight_agent import InsightAgent
from agents.creative_generator import CreativeGenerator
from agents.evaluator import EvaluatorAgent
from utils.logger import logger

# Load environment variables
load_dotenv(".env")

# Check for API Key
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    logger.critical("GROQ_API_KEY not found in environment variables. Exiting.")
    exit(1)

async def main():
    parser = argparse.ArgumentParser(description="Kasparro Agentic FB Analyst")
    parser.add_argument("query", type=str, help="The analysis query (e.g., 'Analyze ROAS drop')")
    args = parser.parse_args()

    query = args.query
    logger.info(f"Starting Analysis for: '{query}'")

    try:
        # Initialize Agents
        planner = PlannerAgent()
        data_agent = DataAgent()
        insight_agent = InsightAgent()
        creative_gen = CreativeGenerator()
        evaluator = EvaluatorAgent()
    except Exception as e:
        logger.critical(f"Failed to initialize agents: {e}")
        return

    # Step 1: Plan
    logger.info("Planner: Creating execution plan...")
    try:
        plan = planner.create_plan(query)
        if not plan:
            logger.error("Planner failed to create a plan. Exiting.")
            return
        logger.info(f"Plan created with {len(plan.steps)} steps.")
    except Exception as e:
        logger.error(f"Planning failed: {e}")
        return
    
    context = {"query": query, "data_summary": "", "insights": "", "top_ads": ""}
    
    # Step 2: Execute Plan
    for i, step in enumerate(plan.steps):
        logger.info(f"▶️ Step {i+1}: {step.step_name} ({step.agent}) - {step.description}")
        
        step_output = ""
        if step.agent == "DataAgent":
            result = data_agent.execute(step.description)
            context["data_summary"] += f"\n\n### Data Output ({step.step_name}):\n{result}"
            step_output = result
            
        elif step.agent == "InsightAgent":
            result = insight_agent.analyze(context["data_summary"], step.description)
            context["insights"] += f"\n\n### Insights ({step.step_name}):\n{result}"
            step_output = result
            
        elif step.agent == "CreativeGenerator":
            # For creative gen, we need top ads. Let's ask DataAgent to get them if not present.
            if not context["top_ads"]:
                logger.info("Fetching top ads for context...")
                top_ads = data_agent.execute("Get top 5 ads by ROAS with their creative messages")
                context["top_ads"] = top_ads
            
            result = creative_gen.generate(context["insights"], context["top_ads"])
            if result:
                # Convert Pydantic model to JSON/Dict for report
                result_json = result.model_dump_json()
                context["creative_recommendations"] = result_json
                step_output = result_json
            else:
                logger.warning("Creative Generator returned no results.")
        
        logger.info(f"Step {i+1} completed.")
        logger.debug(f"Step Output: {step_output[:200]}...") # Log first 200 chars
        
        logger.info("Waiting 5s to respect API rate limits...")
        time.sleep(5)

    # Step 3: Compile Report
    logger.info("Compiling Final Report...")
    report = f"""# Kasparro Analysis Report

## Query
{query}

## Data Analysis
{context['data_summary']}

## Insights
{context['insights']}

## Creative Recommendations
"""
    if "creative_recommendations" in context:
        try:
            recs = json.loads(context["creative_recommendations"])
            if "recommendations" in recs:
                 for rec in recs["recommendations"]:
                    report += f"\n### Campaign: {rec['campaign_name']}\n"
                    report += f"- **Issue**: {rec['current_performance_issue']}\n"
                    report += f"- **New Headline**: {rec['suggested_headline']}\n"
                    report += f"- **New Message**: {rec['suggested_message']}\n"
                    report += f"- **Reasoning**: {rec['reasoning']}\n"
        except json.JSONDecodeError:
            logger.error("Failed to parse creative recommendations JSON.")

    # Step 4: Evaluate
    logger.info("Evaluator: Reviewing report...")
    eval_result = evaluator.evaluate(query, report)
    logger.info(f"Evaluator Result: {eval_result}")

    # Save Outputs
    os.makedirs("reports", exist_ok=True)
    with open("reports/report.md", "w") as f:
        f.write(report)
    
    if "creative_recommendations" in context:
        with open("reports/creatives.json", "w") as f:
            f.write(context["creative_recommendations"])

    # Save Insights JSON
    insights_data = {
        "query": query,
        "insights": context.get("insights", ""),
        "data_summary": context.get("data_summary", "")
    }
    with open("reports/insights.json", "w") as f:
        json.dump(insights_data, f, indent=2)
            
    logger.info("✅ Analysis Complete! Report saved to reports/report.md")

if __name__ == "__main__":
    asyncio.run(main())
