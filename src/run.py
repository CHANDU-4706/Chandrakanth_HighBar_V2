import argparse
import asyncio
import os
import json
import time
from dotenv import load_dotenv
from src.agents.planner import PlannerAgent
from src.agents.data_agent import DataAgent
from src.agents.insight_agent import InsightAgent
from src.agents.creative_generator import CreativeGenerator
from src.agents.evaluator import EvaluatorAgent
from src.utils.logger import logger, current_run_dir
from src.utils.error_handler import AgentError

# Load environment variables
load_dotenv(".env")

# Check for API Key
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    logger.critical("GROQ_API_KEY not found in environment variables. Exiting.")
    exit(1)

async def main():
    parser = argparse.ArgumentParser(description="Kasparro Agentic FB Analyst V2")
    parser.add_argument("query", type=str, help="The analysis query (e.g., 'Analyze ROAS drop')")
    args = parser.parse_args()

    query = args.query
    logger.info(f"Starting Analysis for: '{query}'")
    logger.info(f"Run Logs Directory: {current_run_dir}")

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
    
    context = {
        "query": query, 
        "data_summary": "", 
        "insights_json": "[]", 
        "top_ads": "",
        "creative_recommendations": None
    }
    
    # Step 2: Execute Plan
    for i, step in enumerate(plan.steps):
        logger.info(f"▶️ Step {i+1}: {step.step_name} ({step.agent}) - {step.description}")
        
        try:
            step_output = ""
            if step.agent == "DataAgent":
                result = data_agent.execute(step.description)
                context["data_summary"] += f"\n\n### Data Output ({step.step_name}):\n{result}"
                step_output = result
                
            elif step.agent == "InsightAgent":
                # Insight Agent now returns JSON string
                result_json = insight_agent.analyze(context["data_summary"], step.description)
                context["insights_json"] = result_json # Store raw JSON for pipeline
                
                # Parse for readable context
                try:
                    insights = json.loads(result_json)
                    readable_insights = ""
                    for insight in insights:
                        readable_insights += f"- **Hypothesis**: {insight['hypothesis']}\n"
                        readable_insights += f"  - Confidence: {insight['confidence']}\n"
                        readable_insights += f"  - Impact: {insight['impact']}\n"
                    context["insights_readable"] = readable_insights
                except:
                    context["insights_readable"] = "Failed to parse insights JSON."
                
                step_output = context["insights_readable"]
                
            elif step.agent == "CreativeGenerator":
                # For creative gen, we need top ads. Let's ask DataAgent to get them if not present.
                if not context["top_ads"]:
                    logger.info("Fetching top ads for context...")
                    top_ads = data_agent.execute("Get top 5 ads by ROAS with their creative messages")
                    context["top_ads"] = top_ads
                
                # Pass JSON insights directly
                result = creative_gen.generate(context["insights_json"], context["top_ads"])
                if result:
                    context["creative_recommendations"] = result
                    step_output = str(result.model_dump())
                else:
                    logger.warning("Creative Generator returned no results.")
            
            logger.info(f"Step {i+1} completed.")
            logger.debug(f"Step Output: {step_output[:200]}...")
            
            logger.info("Waiting 2s to respect API rate limits...")
            time.sleep(2)

        except AgentError as e:
            logger.error(f"Step {i+1} failed with AgentError: {e}")
            # Decide whether to continue or stop based on severity. For V2, we log and continue if possible, or exit.
            # For now, let's continue but mark as failed.
        except Exception as e:
            logger.error(f"Step {i+1} failed with unexpected error: {e}")

    # Step 3: Compile Report
    logger.info("Compiling Final Report...")
    
    # Parse insights for report
    insights_section = ""
    try:
        insights_data = json.loads(context["insights_json"])
        for idx, insight in enumerate(insights_data):
            insights_section += f"### Insight {idx+1}: {insight['hypothesis']}\n"
            insights_section += f"- **Confidence**: {insight['confidence']} | **Impact**: {insight['impact']}\n"
            insights_section += f"- **Reasoning**: {insight['reasoning']}\n"
            insights_section += "- **Evidence**:\n"
            for ev in insight['evidence']:
                insights_section += f"  - {ev['metric']}: {ev['delta']} (Segment: {ev.get('segment', 'N/A')})\n"
            insights_section += "\n"
    except:
        insights_section = "Could not parse insights data.\n"

    # Parse creatives for report
    creatives_section = ""
    if context["creative_recommendations"]:
        for rec in context["creative_recommendations"].recommendations:
            creatives_section += f"### Campaign: {rec.campaign_name}\n"
            creatives_section += f"- **Issue**: {rec.current_performance_issue}\n"
            creatives_section += f"- **New Headline**: {rec.suggested_headline}\n"
            creatives_section += f"- **New Message**: {rec.suggested_message}\n"
            creatives_section += f"- **Reasoning**: {rec.reasoning}\n\n"

    report = f"""# Kasparro Analysis Report (V2 High Bar)

## Query
{query}

## Data Analysis
{context['data_summary']}

## Strategic Insights
{insights_section}

## Creative Recommendations
{creatives_section}
"""

    # Step 4: Evaluate
    logger.info("Evaluator: Reviewing report...")
    eval_result = evaluator.evaluate(query, report, context["insights_json"])
    logger.info(f"Evaluator Result: {eval_result}")

    # Save Outputs
    os.makedirs("reports", exist_ok=True)
    report_path = os.path.join("reports", "report.md")
    with open(report_path, "w") as f:
        f.write(report)
    
    # Save structured data
    insights_path = os.path.join("reports", "insights.json")
    with open(insights_path, "w") as f:
        f.write(context["insights_json"])
            
    logger.info(f"✅ Analysis Complete! Report saved to {report_path}")
    logger.info(f"📄 Full execution logs available in: {current_run_dir}")

if __name__ == "__main__":
    asyncio.run(main())
