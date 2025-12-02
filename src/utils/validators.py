import pandas as pd
from typing import List, Dict, Any
from src.utils.logger import logger
from src.utils.error_handler import SchemaValidationError
from src.schema import InputSchema
from pydantic import ValidationError

def validate_schema(df: pd.DataFrame) -> bool:
    """
    Validates that the DataFrame contains the required columns and types using Pydantic.
    """
    logger.info("Starting strict schema validation...")
    
    # Check for required columns first (fast fail)
    required_fields = InputSchema.__fields__.keys()
    missing_columns = [field for field in required_fields if field not in df.columns]
    
    if missing_columns:
        error_msg = f"Schema Validation Failed: Missing columns: {missing_columns}"
        logger.error(error_msg)
        raise SchemaValidationError(error_msg)
    
    # Validate each row
    errors = []
    for index, row in df.iterrows():
        try:
            InputSchema(**row.to_dict())
        except ValidationError as e:
            errors.append(f"Row {index}: {e}")
            if len(errors) >= 5: # Limit error reporting
                break
    
    if errors:
        error_msg = f"Schema Validation Failed with {len(errors)} errors. First few:\n" + "\n".join(errors)
        logger.error(error_msg)
        raise SchemaValidationError(error_msg)
    
    logger.info("✅ Data schema validation passed.")
    return True
