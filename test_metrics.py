#!/usr/bin/env python3
"""
Test script to debug the metrics function
"""

import sys
import os
sys.path.append('.')

try:
    from validator.spam_detector import get_model_metrics
    import json
    
    print("Testing get_model_metrics function...")
    result = get_model_metrics()
    
    if isinstance(result, dict):
        if "error" in result:
            print("Error:", result["error"])
        else:
            print("Success! Metrics:")
            print(json.dumps(result, indent=2))
    else:
        print("Unexpected result type:", type(result))
        print("Result:", result)
        
except Exception as e:
    print("Exception occurred:", str(e))
    import traceback
    traceback.print_exc()
