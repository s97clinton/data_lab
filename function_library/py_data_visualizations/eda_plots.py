import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def correlation_heatmap(df: pd.DataFrame, numerical_features: list, output_path: str = None, show: bool = True) -> None:
    """
    Function:
    - Visualizes the correlation matrix of numerical features using a heatmap.

    Parameters:
    <df> (pd.DataFrame): DataFrame containing numerical features.
    <numerical_features> (list): List of numerical feature column names to use for PCA.
    <output_path> (str, optional): File path to save the plot. If None, plot is not saved.
    <show> (bool): Whether to display the plot (default: True).

    Returns:
    - None
    """
    if df.empty or not all(col in df.columns for col in numerical_features):
        print("No data available or missing required columns.")
        return
    fig, ax = plt.subplots(figsize=(8, 6))
    try:
        cluster_sample = df[numerical_features].dropna().sample(min(5000, len(df)))
        corr_matrix = cluster_sample.corr()
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', ax=ax)
        ax.set_title('Feature Correlation Matrix', fontweight='bold')
        if output_path:
            fig.savefig(output_path, dpi=150, bbox_inches='tight')
        if show:
            plt.show()
    except Exception:
        ax.text(0.5, 0.5, 'Correlation failed', ha='center', va='center')
        if show:
            plt.show()
    finally:
        plt.close()
