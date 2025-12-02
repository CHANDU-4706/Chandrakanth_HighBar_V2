import pytest
import pandas as pd
import json
from datetime import datetime
from src.utils.validators import validate_schema
from src.utils.error_handler import SchemaValidationError
from src.agents.evaluator import EvaluatorAgent

# --- Schema Validation Tests ---

def test_schema_validation_pass():
    data = {
        "date": [datetime.now()],
        "campaign_name": ["Test Campaign"],
        "adset_name": ["Test AdSet"],
        "impressions": [1000],
        "clicks": [100],
        "spend": [50.0],
        "roas": [2.5],
        "ctr": [10.0]
    }
    df = pd.DataFrame(data)
    assert validate_schema(df) is True

def test_schema_validation_fail_missing_column():
    data = {
        "date": [datetime.now()],
        # Missing campaign_name
        "adset_name": ["Test AdSet"],
        "impressions": [1000],
        "clicks": [100],
        "spend": [50.0],
        "roas": [2.5],
        "ctr": [10.0]
    }
    df = pd.DataFrame(data)
    with pytest.raises(SchemaValidationError):
        validate_schema(df)

def test_schema_validation_fail_invalid_type():
    data = {
        "date": [datetime.now()],
        "campaign_name": ["Test Campaign"],
        "adset_name": ["Test AdSet"],
        "impressions": ["invalid_int"], # Invalid type
        "clicks": [100],
        "spend": [50.0],
        "roas": [2.5],
        "ctr": [10.0]
    }
    df = pd.DataFrame(data)
    with pytest.raises(SchemaValidationError):
        validate_schema(df)

# --- Evaluator Tests ---

def test_evaluator_statistical_validation_pass():
    evaluator = EvaluatorAgent()
    valid_insights = json.dumps([
        {
            "hypothesis": "Test Hypothesis",
            "evidence": [{"metric": "ctr", "delta": "-10%"}],
            "impact": "High",
            "confidence": 0.8,
            "reasoning": "Test reasoning"
        }
    ])
    errors = evaluator.validate_statistical_rigor(valid_insights)
    assert len(errors) == 0

def test_evaluator_statistical_validation_fail_no_confidence():
    evaluator = EvaluatorAgent()
    invalid_insights = json.dumps([
        {
            "hypothesis": "Test Hypothesis",
            "evidence": [{"metric": "ctr", "delta": "-10%"}],
            "impact": "High",
            # Missing confidence
            "reasoning": "Test reasoning"
        }
    ])
    errors = evaluator.validate_statistical_rigor(invalid_insights)
    assert len(errors) > 0
    assert "Missing or invalid confidence score" in errors[0]

def test_evaluator_statistical_validation_fail_no_evidence():
    evaluator = EvaluatorAgent()
    invalid_insights = json.dumps([
        {
            "hypothesis": "Test Hypothesis",
            "evidence": [], # Empty evidence
            "impact": "High",
            "confidence": 0.8,
            "reasoning": "Test reasoning"
        }
    ])
    errors = evaluator.validate_statistical_rigor(invalid_insights)
    assert len(errors) > 0
    assert "No evidence provided" in errors[0]
