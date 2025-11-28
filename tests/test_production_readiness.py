import unittest
import pandas as pd
import os
import time
from src.utils.validators import validate_schema
from src.utils.error_handler import safe_execute, AgentError
from src.utils.logger import setup_logger

class TestProductionReadiness(unittest.TestCase):

    def test_schema_validation(self):
        # Valid DataFrame
        valid_data = {
            "date": [pd.Timestamp("2023-01-01")],
            "campaign_name": ["Test"],
            "ad_set_name": ["Test"],
            "ad_name": ["Test"],
            "impressions": [100],
            "clicks": [10],
            "spend": [100.0],
            "roas": [2.0],
            "cpm": [10.0],
            "ctr": [0.1],
            "cpc": [10.0]
        }
        df = pd.DataFrame(valid_data)
        self.assertTrue(validate_schema(df))

        # Invalid DataFrame
        invalid_data = {"date": [pd.Timestamp("2023-01-01")]}
        df_invalid = pd.DataFrame(invalid_data)
        with self.assertRaises(ValueError):
            validate_schema(df_invalid)

    def test_retry_logic(self):
        self.counter = 0
        
        @safe_execute(retries=2, backoff_factor=0.1, raise_on_error=True)
        def failing_function():
            self.counter += 1
            if self.counter < 3:
                raise Exception("Fail")
            return "Success"

        # Should succeed on 3rd attempt (initial + 2 retries)
        result = failing_function()
        self.assertEqual(result, "Success")
        self.assertEqual(self.counter, 3)

    def test_retry_failure(self):
        self.counter = 0
        
        @safe_execute(retries=1, backoff_factor=0.1, raise_on_error=True)
        def always_failing():
            self.counter += 1
            raise Exception("Fail")

        with self.assertRaises(AgentError):
            always_failing()
        
        # Should have tried 2 times (initial + 1 retry)
        self.assertEqual(self.counter, 2)

if __name__ == '__main__':
    unittest.main()
