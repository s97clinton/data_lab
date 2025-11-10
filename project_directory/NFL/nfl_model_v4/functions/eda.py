import pandas as pd

def nfl_spread_total_pivot_table(df: pd.DataFrame, index: str, columns: str, spread_or_total: str) -> pd.DataFrame:
    """
    Function:
    -Creates Pivot Tables for various spread/total win/loss/push breakdowns, adding either
    'win_perc' or 'over_perc' based on <spread_or_total> parameter, which MUST have a value of
    either 'spread' or 'total'.

    Parameters:
    <df> (Pandas Dataframe): Original DataFrame containing data to create pivot table.
    <index> (str): Column to be passed to df.pivot_table() as index.
    <columns> (str): Column to be passed to df.pivot_table() as column.
    <spread_or_total> (str): Determines whether function will add 'win_perc' or 'over_perc'.

    Returns:
    <pivot_df> (Pandas DataFrame): Enhanced Pivot Table.
    """
    if spread_or_total not in ['spread', 'total']:
        raise ValueError
    else:
        pivot_df = df.pivot_table(
            index=index,
            columns=columns,
            values='game_id',
            aggfunc='count',
            fill_value=0,
            margins=True
        )
        if spread_or_total == 'spread':
            pivot_df['win_perc'] = round((pivot_df['win'] / (pivot_df['win'] + pivot_df['loss']))*100, 2)
        else:
            pivot_df['over_perc'] = round((pivot_df['over'] / (pivot_df['over'] + pivot_df['under']))*100, 2)       
        pivot_df['push_perc'] = round((pivot_df['push'] / pivot_df['All'])*100, 2)
        pivot_df.to_csv(f"csv_output/schedule_eda/spreads_totals/{index}_{columns}_pivot_table.csv")
        return pivot_df