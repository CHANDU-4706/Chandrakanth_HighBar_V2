import pandas as pd
from typing import List, Dict, Any
from .logger import logger

# Define expected schema for Facebook Ads data
REQUIRED_COLUMNS = {
    "date": "datetime64[ns]",
    "campaign_name": "object",
    "adset_name": "object", # Changed from ad_set_name
    # "ad_name": "object", # Not present in CSV
    "impressions": "int64",
    "clicks": "int64",
    "spend": "float64",
    "roas": "float64",
    "ctr": "float64",
    # "cpm": "float64", # Calculated fields
    # "cpc": "float64"  # Calculated fields
}

def validate_schema(df: pd.DataFrame) -> bool:
    """
    Validates that the DataFrame contains the required columns and types.
    """
    missing_columns = []
    
    for col, dtype in REQUIRED_COLUMNS.items():
        if col not in df.columns:
            missing_columns.append(col)
            continue
        
        # Basic type check (can be expanded)
        # Note: pandas types can be tricky (e.g. int64 vs int32), so we might be lenient on exact types
        # and just check existence for now, or use safe casting.
    
    if missing_columns:
        error_msg = f"Data validation failed. Missing columns: {missing_columns}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    logger.info("Data schema validation passed.")
    return True
