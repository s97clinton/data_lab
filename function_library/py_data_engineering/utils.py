import json
import pandas as pd

def is_empty(value: any) -> bool:
    """
    Function:
    -Checks if a value is considered 'empty'.
    
    Parameters:
    <value> (any): Value to check
    
    Returns 
    -True for None, NaN, empty string, or other placeholders you define.
    """
    return value is None or pd.isna(value) or str(value).strip() == ''

def is_json_serializable(value: any) -> bool:
    """
    Function: 
    -Checks if a value is "json-serializable" for use in pipelines and other applications.

    Parameters:
    <value> (any): Value to check

    Returns:
    -True for value that work inside json.dumps()
    """
    try:
        json.dumps(value)
        return True
    except (TypeError, OverflowError):
        return False