import pandas as pd

def basic_dataframe_description(df: pd.DataFrame, descriptive_name: str, transpose_description: bool = False) -> pd.DataFrame:
    """
    Function:
    - Prints a basic overview of a Pandas Dataframe, including the shape, columns, memory usage,
    missing values, number of columns with missing values, and the different data types in the
    Pandas DataFrame.

    Parameters:
    <df> (Pandas DataFrame): The DataFrame to be described.
    <descriptive_name> (str): A descriptive name for the DataFrame to be used in print statements.
    <transpose_description> (bool): Whether to transpose the output of df.describe(). Default is False.

    Returns:
    <df.describe()> (Pandas DataFrame): The output of the DataFrame's describe() method.
    """
    if df.empty:
        print(f"The DataFrame '{descriptive_name}' is empty.")
        return
    print(f"\n{descriptive_name} Overview:")
    print(f" Shape: {df.shape}")
    print(f" Columns: {df.shape[1]}")
    print(f" Memory: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    missing = df.isnull().sum()
    if missing.sum() > 0:
        print(f" Missing values: {missing.sum()} total")
        print(f" Columns with missing values: {(missing > 0).sum()}")
        missing_columns = missing[missing > 0].index.tolist()
        print(f" Columns with missing values: {missing_columns}")
        print("  Missing values per column:")
        for col in missing_columns:
            print(f"    {col}: {missing[col]}")
    else:
        print(" Missing values: None")

    dtypes = df.dtypes.value_counts()
    print(f" Data types: {dict(dtypes)}")
    if transpose_description:
        return df.describe().T
    else:
        return df.describe()
    