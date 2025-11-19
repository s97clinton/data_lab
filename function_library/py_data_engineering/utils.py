import json
import pandas as pd

def categorize_dataframe_columns(df: pd.DataFrame) -> dict:
    """
    Function:
    -Categorizes DataFrame columns by data type into separate lists.

    Parameters:
    <df> Pandas DataFrame: DataFrame to sort.
    
    Returns:
    <dict>: Dictionary with keys 'string', 'float', 'integer', 'bool', 'other'
            and values as lists of column names
    """
    string_cols = []
    float_cols = []
    integer_cols = []
    bool_cols = []
    other_cols = []
    
    for col in df.columns:
        dtype = df[col].dtype
        if dtype == 'string' or pd.api.types.is_string_dtype(dtype):
            string_cols.append(col)
        elif dtype == 'float64' or dtype == 'float32' or pd.api.types.is_float_dtype(dtype):
            float_cols.append(col)
        elif pd.api.types.is_integer_dtype(dtype) or pd.api.types.is_signed_integer_dtype(dtype) or pd.api.types.is_unsigned_integer_dtype(dtype):
            integer_cols.append(col)
        elif pd.api.types.is_bool_dtype(dtype):
            bool_cols.append(col)
        else:
            other_cols.append(col)
    return {'string': string_cols, 'float': float_cols, 'integer': integer_cols, 'bool': bool_cols, 'other': other_cols}
        

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
    
def convert_string_to_boolean(value: any) -> any:
    """
    Function: 
    -Converts mixed type of None when updating a True/False
    string to Boolean type.

    Parameters:
    <value> (any): Value to check

    Returns:
    <value> (any): Updated Value
    """
    if value == 'True':
        return True
    elif value == 'False':
        return False
    elif value == 'None' or pd.isna(value):
        return None
    return value