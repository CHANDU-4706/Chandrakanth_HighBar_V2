from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime

class InputSchema(BaseModel):
    """
    Defines the expected schema for the input CSV data.
    """
    date: datetime
    campaign_name: str
    adset_name: str
    impressions: int = Field(ge=0)
    clicks: int = Field(ge=0)
    spend: float = Field(ge=0.0)
    roas: float = Field(ge=0.0)
    ctr: float = Field(ge=0.0, le=100.0) # Percentage or ratio? Assuming ratio 0-1 or % 0-100. Let's assume ratio for now, but usually CSVs have it.
                                         # Actually, let's be safe. If it's > 1 it might be %, if < 1 it might be ratio.
                                         # For now, just non-negative.
    
    class Config:
        extra = "ignore" # Allow extra columns but don't validate them

class Evidence(BaseModel):
    """
    Structured evidence supporting a hypothesis.
    """
    metric: str = Field(description="The metric that changed (e.g., 'ctr', 'cpm')")
    delta: str = Field(description="The change value (e.g., '-32%', '+15%')")
    segment: Optional[str] = Field(description="The segment where this was observed (e.g., 'Campaign A')")

class InsightOutput(BaseModel):
    """
    Structured output for an insight/hypothesis.
    """
    hypothesis: str = Field(description="The core hypothesis for the performance change")
    evidence: List[Evidence] = Field(description="List of data points supporting the hypothesis")
    impact: str = Field(description="Estimated impact (High, Medium, Low)")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0", ge=0.0, le=1.0)
    reasoning: str = Field(description="Explanation of how the evidence supports the hypothesis")

class CreativeRecommendation(BaseModel):
    """
    A single creative recommendation.
    """
    campaign_name: str
    current_performance_issue: str
    suggested_headline: str
    suggested_message: str
    reasoning: str = Field(description="How this creative addresses the specific insight")

class CreativeOutput(BaseModel):
    """
    Collection of creative recommendations.
    """
    recommendations: List[CreativeRecommendation]
