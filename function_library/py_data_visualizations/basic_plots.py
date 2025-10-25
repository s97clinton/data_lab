import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_histogram(df: pd.DataFrame, column: str, column_name: str, bins: int = 50, output_path: str = None, show: bool = True) -> None:
    """
    Function:
    - Visualizes the distribution of a numerical column using a histogram with zero, mean, and median lines.

    Parameters:
    <df> (pd.DataFrame): DataFrame containing the numerical column data.
    <column> (str): The column name of the numerical column to visualize.
    <column_name> (str): The display name of the numerical column for plot titles and labels.
    <bins> (int): Number of bins for the histogram (default: 50).
    <output_path> (str, optional): File path to save the plot. If None, plot is not saved.
    <show> (bool): Whether to display the plot (default: True).

    Returns:
    - None
    """
    if df.empty:
        print("No data available.")
        return
    fig, ax = plt.subplots(figsize=(8, 6))
    try:
        column_data = df[column].dropna().sample(min(10000, len(df)))
        ax.hist(column_data, bins=bins, color=plt.cm.Set3(0), edgecolor='black', alpha=0.7)
        ax.set_xlabel(column)
        ax.set_ylabel('Frequency')
        ax.set_title(f'{column_name} Distribution', fontweight='bold')
        ax.axvline(0, color='blue', linestyle='--', label='Zero Line')
        ax.axvline(column_data.mean(), color='red', linestyle='--', label=f'Mean: {column_data.mean():.2f}')
        ax.axvline(column_data.median(), color='green', linestyle='--', label=f'Median: {column_data.median():.2f}')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
        if output_path:
            fig.savefig(output_path, dpi=150, bbox_inches='tight')
        if show:
            plt.show()
    except Exception as e:
        ax.text(0.5, 0.5, f'Error: {str(e)[:30]}', ha='center', va='center')
        if show:
            plt.show()
    finally:
        plt.close()

def plot_bar_plot_with_optional_breakdown(df: pd.DataFrame, column_one: str, column_one_name: str, column_two: str = None, column_two_name: str = None, x_label_rotation: int = 0, output_path: str = None, show: bool = True, agg_func: callable = None) -> None:
    """
    Function:
    - Visualizes the values in <column_one>, optionally broken up by <column_two>, using a bar plot.
    - If <column_two> is None, visualizes the value counts of <column_one>.
    - Supports custom aggregation functions for grouped data.

    Parameters:
    <df> (pd.DataFrame): DataFrame containing the specified columns.
    <column_one> (str): The first column to visualize.
    <column_one_name> (str): Descriptive name for the first column.
    <column_two> (str, optional): The second column to group by.
    <column_two_name> (str, optional): Descriptive name for the second column.
    <x_label_rotation> (int): Rotation angle for x-axis labels in degrees (default: 0).
    <output_path> (str, optional): File path to save the plot. If None, plot is not saved.
    <show> (bool): Whether to display the plot (default: True).
    <agg_func> (callable, optional): Custom aggregation function for grouped data (default: None, uses value_counts).

    Returns:
    - None
    """
    if df.empty:
        print("No data available.")
        return

    fig, ax = plt.subplots(figsize=(8, 6))
    try:
        if column_one in df.columns and column_two in df.columns and column_two is not None:
            if agg_func is None:
                grouped_data = df.groupby(column_two)[column_one].apply(
                    lambda x: (x == 'C').mean() * 100 if len(x) > 0 else 0
                )
            else:
                grouped_data = df.groupby(column_two)[column_one].apply(agg_func)
            ax.bar(grouped_data.index, grouped_data.values, color='#9b59b6')
            ax.set_xlabel(column_two_name)
            ax.set_ylabel(column_one_name)
            ax.set_title(f'{column_one_name} by {column_two_name}', fontweight='bold')
        elif column_one in df.columns and column_two is None:
            counts = df[column_one].value_counts().sort_index()
            ax.bar(counts.index, counts.values, color='#f39c12')
            ax.set_xlabel(column_one_name)
            ax.set_ylabel('Number of Records')
            ax.set_title(f'Records by {column_one_name}', fontweight='bold')
        else:
            ax.text(0.5, 0.5, f'No {column_one}/{column_two} data', ha='center', va='center')
            if show:
                plt.show()
            return

        ax.tick_params(axis='x', rotation=x_label_rotation)

        if output_path:
            fig.savefig(output_path, dpi=150, bbox_inches='tight')
        if show:
            plt.show()

    except Exception as e:
        print(f"Error: {e}")
        ax.text(0.5, 0.5, 'No data', ha='center', va='center')
        if show:
            plt.show()
    finally:
        plt.close()

def plot_numeric_col_avg_std_by_cat_column(data: pd.DataFrame, numeric_col: str, numeric_col_name: str, cat_column: str, cat_col_name: str, x_label: str = None, output_path: str = None, show: bool = True) -> None:
    """
    Function:
    - Visualizes the mean value for a numeric_col, broken up by a second cat_column, with error bars for standard deviation using a horizontal bar plot for a specified
    numeric_col.

    Parameters:
    <data> (pd.DataFrame): DataFrame containing 'player_role' and the specified numeric_col columns.
    <numeric_col> (str): The movement numeric_col to visualize.
    <numeric_col_name> (str): The name of the movement numeric_col for labeling.
    <output_path> (str, optional): File path to save the plot. If None, plot is not saved.
    <show> (bool): Whether to display the plot (default: True).

    Returns:
    - None
    """
    if data.empty:
        print("No data available.")
        return
    fig, ax = plt.subplots(figsize=(8, 6))
    try:
        cat_column_numeric_cols = data.groupby(cat_column)[numeric_col].agg(['mean', 'std']).sort_values('mean')
        ax.barh(range(len(cat_column_numeric_cols)), cat_column_numeric_cols['mean'], xerr=cat_column_numeric_cols['std'], color='#3498db')
        ax.set_yticks(range(len(cat_column_numeric_cols)))
        ax.set_yticklabels(cat_column_numeric_cols.index, fontsize=8)
        ax.set_xlabel(x_label)
        ax.set_title(f'{numeric_col_name} by {cat_col_name}', fontweight='bold')
        ax.grid(True, alpha=0.3)
        if output_path:
            fig.savefig(output_path, dpi=150, bbox_inches='tight')
        if show:
            plt.show()
    except Exception:
        ax.text(0.5, 0.5, 'No data', ha='center', va='center')
        if show:
            plt.show()
    finally:
        plt.close()

def plot_scatter_plot(data: pd.DataFrame, column_one: str, column_two: str, output_path: str = None, show: bool = True) -> None:
    """
    Function:
    - Visualizes the relationship between two numerical features using a scatter plot.

    Parameters:
    <data> (pd.DataFrame): DataFrame containing the numerical feature data.
    <column_one> (str): The column name of the first feature (x-axis).
    <column_two> (str): The column name of the second feature (y-axis).
    <output_path> (str, optional): File path to save the plot. If None, plot is not saved.
    <show> (bool): Whether to display the plot (default: True).

    Returns:
    - None
    """
    if data.empty:
        print("No data available.")
        return
    fig, ax = plt.subplots(figsize=(8, 6))
    try:
        sample = data[[column_one, column_two]].dropna().sample(min(5000, len(data)))
        ax.scatter(sample[column_one], sample[column_two], alpha=0.3, s=1)
        ax.set_xlabel(column_one)
        ax.set_ylabel(column_two)
        ax.set_title(f'{column_one} vs {column_two}', fontweight='bold')
        ax.grid(True, alpha=0.3)
        if output_path:
            fig.savefig(output_path, dpi=150, bbox_inches='tight')
        if show:
            plt.show()
    except Exception:
        ax.text(0.5, 0.5, 'No data', ha='center', va='center')
        if show:
            plt.show()
    finally:
        plt.close()

def plot_compare_density_plots_by_cat_column(df: pd.DataFrame, numeric_col: str, numeric_col_name: str, cat_column: str, cat_col_name: str, cat_col_sel_one: str, cat_col_sel_two: str, x_label: str = None, output_path: str = None, show: bool = True) -> None:
    """
    Function:
    - Visualizes the distribution comparison for two categories within a categorical column using overlapping histograms; 
    the two values within the categorical column are denoted by <cat_col_sel_one> and <cat_col_sel_two>.

    Parameters:
    <df> (pd.DataFrame): DataFrame containing the categorical and numerical columns.
    <cat_col_name> (str): The name of the categorical column for labeling.
    <cat_column> (str): The categorical column to group by.
    <numeric_col> (str): The numerical column to visualize.
    <numeric_col_name> (str): The name of the numerical column for labeling.
    <output_path> (str, optional): File path to save the plot. If None, plot is not saved.
    <show> (bool): Whether to display the plot (default: True).

    Returns:
    - None
    """
    if df.empty:
        print("No data available.")
        return
    fig, ax = plt.subplots(figsize=(8, 6))
    try:
        for selection in [cat_col_sel_one, cat_col_sel_two]:
            cat_metrics = df[df[cat_column] == selection][numeric_col].dropna()
            ax.hist(cat_metrics, bins=30, alpha=0.5, label=selection, density=True)
        ax.set_xlabel(x_label)
        ax.set_ylabel('Density')
        ax.set_title(f'{numeric_col_name}: {cat_col_sel_one} vs {cat_col_sel_two}', fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        if output_path:
            fig.savefig(output_path, dpi=150, bbox_inches='tight')
        if show:
            plt.show()
    except Exception:
        ax.text(0.5, 0.5, 'No data', ha='center', va='center')
        if show:
            plt.show()
    finally:
        plt.close()

def plot_box_whisker_num_col_by_cat_col(df: pd.DataFrame, num_col: str, num_col_name: str, cat_col: str, cat_col_name: str, top_n: int = 5, output_path: str = None, show: bool = True) -> None:
    """
    Function:
    - Visualizes a numerical column distribution across top_n values in cat_col using a box plot.

    Parameters:
    <df> (pd.DataFrame): DataFrame containing the specified num_col and cat_col.
    <num_col> (str): The numerical column to visualize.
    <cat_col> (str): The categorical column to break up the data by.
    <top_n> (int): Number of top positions to include (default: 5).
    <output_path> (str, optional): File path to save the plot. If None, plot is not saved.
    <show> (bool): Whether to display the plot (default: True).

    Returns:
    - None
    """
    if df.empty:
        print("No data available.")
        return
    fig, ax = plt.subplots(figsize=(8, 6))
    try:
        top_pos = df[cat_col].value_counts().head(top_n).index
        box_data = [df[df[cat_col] == pos][num_col].dropna() for pos in top_pos]
        bp = ax.boxplot(box_data, labels=top_pos, patch_artist=True)
        for patch, color in zip(bp['boxes'], plt.cm.Set2(range(len(top_pos)))):
            patch.set_facecolor(color)
        ax.set_ylabel(num_col_name)
        ax.set_title(f'{num_col_name} by {cat_col_name} for Top {top_n} Qualifiers', fontweight='bold')
        ax.grid(True, alpha=0.3)
        if output_path:
            fig.savefig(output_path, dpi=150, bbox_inches='tight')
        if show:
            plt.show()
    except Exception:
        ax.text(0.5, 0.5, 'No data', ha='center', va='center')
        if show:
            plt.show()
    finally:
        plt.close()

def plot_pie_chart_distribution(df: pd.DataFrame, column: str, column_name: str, output_path: str = None, show: bool = True) -> None:
    """
    Function:
    - Visualizes the distribution of column data using a pie chart.

    Parameters:
    <data> (pd.DataFrame): DataFrame containing the specified column.
    <column> (str): Column name to visualize.
    <column_name> (str): Descriptive name for the column to use in the plot title.
    <output_path> (str, optional): File path to save the plot. If None, plot is not saved.
    <show> (bool): Whether to display the plot (default: True).

    Returns:
    - None
    """
    if df.empty:
        print("No data available.")
        return
    fig, ax = plt.subplots(figsize=(8, 6))
    try:
        if column in df.columns:
            col_counts = df[column].value_counts()
            ax.pie(col_counts.values, labels=col_counts.index, autopct='%1.1f%%', startangle=45)
            ax.set_title(f'{column_name} Distribution', fontweight='bold')
            if output_path:
                fig.savefig(output_path, dpi=150, bbox_inches='tight')
            if show:
                plt.show()
        else:
            ax.text(0.5, 0.5, f'No {column} data', ha='center', va='center')
            if show:
                plt.show()
    except Exception:
        ax.text(0.5, 0.5, 'No data', ha='center', va='center')
        if show:
            plt.show()
    finally:
        plt.close()

def plot_polar_histogram(df: pd.DataFrame, column: str, column_name: str, output_path: str = None, show: bool = True) -> None:
    """
    Function:
    - Visualizes the distribution of specified column data in a polar histogram.

    Parameters:
    <df> (pd.DataFrame): DataFrame containing column data in degrees.
    <column> (str): Column name to visualize.
    <column_name> (str): Descriptive name for the column to use in the plot title.
    <output_path> (str, optional): File path to save the plot. If None, plot is not saved.
    <show> (bool): Whether to display the plot (default: True).

    Returns:
    - None
    """
    if df.empty:
        print("No data available.")
        return
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='polar')
    try:
        column_sample = df[column].dropna().sample(min(5000, len(df)))
        column_hist, column_bins = np.histogram(column_sample, bins=36, range=(0, 360))
        theta = np.linspace(0, 2*np.pi, 36, endpoint=False)
        ax.bar(theta, column_hist, width=2*np.pi/36, bottom=0)
        ax.set_title(f'{column_name} Distribution (Polar)', fontweight='bold', pad=20)
        if output_path:
            fig.savefig(output_path, dpi=150, bbox_inches='tight')
        if show:
            plt.show()
    except Exception:
        ax.text(0, 0, 'No data', ha='center', va='center')
        if show:
            plt.show()
    finally:
        plt.close()