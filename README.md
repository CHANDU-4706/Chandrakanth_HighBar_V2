# Kasparro Agentic FB Analyst (V2 High Bar)

A production-grade multi-agent system for analyzing Facebook Ads performance, generating strategic insights, and creating targeted creative recommendations.

## 🚀 Key Features (V2)

- **Tight Production Pipeline**: Data -> Insight -> Creative workflow where every recommendation is directly linked to a diagnosed issue.
- **Strict Schema Governance**: Pydantic-based validation ensures data integrity before processing.
- **Statistical Validation**: Automated checks for confidence scores, evidence strength, and data quality.
- **Robust Error Handling**: Custom exception hierarchy and structured logging for full traceability.
- **Observability**: Run-specific log folders with detailed decision logs for every agent action.

## 🛠️ Architecture

The system follows a linear orchestration pattern with specialized agents:

1.  **Planner Agent**: Decomposes the user query into executable steps.
2.  **Data Agent**: Executes Pandas operations on the dataset with strict schema validation.
3.  **Insight Agent**: Analyzes data summaries to generate structured JSON insights with confidence scores.
4.  **Creative Generator**: Consumes structured insights to propose specific ad creatives (Headline + Message).
5.  **Evaluator Agent**: Validates the final report for statistical rigor and relevance.

## 📦 Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up Environment Variables**:
    Create a `.env` file in the root directory:
    ```env
    GROQ_API_KEY=your_groq_api_key_here
    ```

## 🏃‍♂️ How to Run

Run the analysis with a natural language query:

```bash
python src/run.py "Analyze why ROAS dropped last week and suggest creative fixes"
```

### Outputs
- **Report**: `reports/report.md` (Final readable report)
- **Insights**: `reports/insights.json` (Structured data)
- **Logs**: `logs/run_YYYYMMDD_HHMMSS/app.json` (Full execution trace)

## 🔧 How to Modify: 

- **Schema**: Edit `src/schema.py` to change input validation or output structures.
- **Agents**:
    - `src/agents/data_agent.py`: Data processing logic.
    - `src/agents/insight_agent.py`: Insight generation prompts.
    - `src/agents/creative_generator.py`: Creative strategy prompts.
- **Configuration**: Adjust thresholds and model settings in `config/config.yaml`.

## 🧪 Testing

Run the unit tests to verify schema validation and evaluator logic:

```bash
pytest tests/
```

## 📂 Project Structure

```
├── config/             # Configuration files
├── data/               # Dataset files
├── logs/               # Run-specific logs
├── reports/            # Generated reports
├── src/
│   ├── agents/         # Agent implementations
│   ├── utils/          # Shared utilities (logger, error_handler, validators)
│   ├── run.py          # Main entry point
│   └── schema.py       # Pydantic models
├── tests/              # Unit tests
├── .env                # Secrets
└── requirements.txt    # Dependencies
```
