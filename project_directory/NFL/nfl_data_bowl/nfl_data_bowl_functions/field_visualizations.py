import matplotlib.pyplot as plt
import pandas as pd

def safe_hist2d(ax, x_col, y_col, data, title, cmap='YlOrRd'):
    """
    Function:
    - Helper function for safe plotting (kept as-is); 
    creates a 2D histogram on the provided axis with error handling for missing or invalid data.

    Parameters:
    <ax> (matplotlib.axes.Axes): The axis to plot the histogram on.
    <x_col> (str): Name of the column for x-axis data.
    <y_col> (str): Name of the column for y-axis data.
    <data> (pd.DataFrame): DataFrame containing the data to plot.
    <title> (str): Title of the plot.
    <cmap> (str): Colormap for the histogram (default: 'YlOrRd').

    Returns:
    - bool: True if the plot was successful, False otherwise.
    """
    try:
        if x_col in data.columns and y_col in data.columns:
            valid_data = data[[x_col, y_col]].dropna()
            if len(valid_data) > 0:
                h = ax.hist2d(valid_data[x_col], valid_data[y_col], 
                              bins=[40, 20], cmap=cmap, cmin=1)
                ax.set_title(title, fontsize=10, fontweight='bold')
                ax.set_xlabel('X (yards)', fontsize=8)
                ax.set_ylabel('Y (yards)', fontsize=8)
                plt.colorbar(h[3], ax=ax, fraction=0.046, pad=0.04)
                return True
    except Exception as e:
        ax.text(0.5, 0.5, f'Error: {str(e)[:30]}', ha='center', va='center')
    return False

def visualize_overall_density(data: pd.DataFrame, output_path: str = None, show: bool = True) -> None:
    """
    Function:
    - Visualizes the overall player density on the field using a 2D histogram.

    Parameters:
    <data> (pd.DataFrame): DataFrame containing player position data with 'x' and 'y' columns.
    <output_path> (str, optional): File path to save the plot. If None, plot is not saved.
    <show> (bool): Whether to display the plot (default: True).

    Returns:
    - None
    """
    if data.empty:
        print("No data available.")
        return
    viz_sample = data.sample(min(100000, len(data)))
    fig, ax = plt.subplots(figsize=(8, 6))
    if safe_hist2d(ax, 'x', 'y', viz_sample, 'Overall Player Density'):
        if output_path:
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
        if show:
            plt.show()
    else:
        plt.close()

def visualize_speed_zone(data: pd.DataFrame, quantile: float, output_path: str = None, show: bool = True) -> None:
    """
    Function:
    - Visualizes player positions for a given speed quantile using a 2D histogram.

    Parameters:
    <data> (pd.DataFrame): DataFrame containing player position and speed data with 'x', 'y', and 's' columns.
    <quantile> (float): Quantile threshold for speed (e.g., 0.5 for 50th percentile).
    <output_path> (str, optional): File path to save the plot. If None, plot is not saved.
    <show> (bool): Whether to display the plot (default: True).

    Returns:
    - None
    """
    if data.empty:
        print("No data available.")
        return
    viz_sample = data.sample(min(100000, len(data)))
    fig, ax = plt.subplots(figsize=(8, 6))
    try:
        speed_threshold = viz_sample['s'].quantile(quantile)
        high_speed = viz_sample[viz_sample['s'] > speed_threshold]
        if safe_hist2d(ax, 'x', 'y', high_speed, f'Speed > {quantile*100:.0f}th %ile', 'Reds'):
            if output_path:
                plt.savefig(output_path, dpi=150, bbox_inches='tight')
            if show:
                plt.show()
        else:
            plt.close()
    except Exception:
        ax.text(0.5, 0.5, 'No data', ha='center', va='center')
        if show:
            plt.show()
        else:
            plt.close()

def visualize_acceleration_zone(data: pd.DataFrame, quantile: float, output_path: str = None, show: bool = True) -> None:
    """
    Function:
    - Visualizes player positions for a given acceleration quantile using a 2D histogram.

    Parameters:
    <data> (pd.DataFrame): DataFrame containing player position and acceleration data with 'x', 'y', and 'a' columns.
    <quantile> (float): Quantile threshold for acceleration (e.g., 0.5 for 50th percentile).
    <output_path> (str, optional): File path to save the plot. If None, plot is not saved.
    <show> (bool): Whether to display the plot (default: True).

    Returns:
    - None
    """
    if data.empty:
        print("No data available.")
        return
    viz_sample = data.sample(min(100000, len(data)))
    fig, ax = plt.subplots(figsize=(8, 6))
    try:
        acc_threshold = viz_sample['a'].quantile(quantile)
        high_acc = viz_sample[viz_sample['a'] > acc_threshold]
        if safe_hist2d(ax, 'x', 'y', high_acc, f'Accel > {quantile*100:.0f}th %ile', 'Blues'):
            if output_path:
                plt.savefig(output_path, dpi=150, bbox_inches='tight')
            if show:
                plt.show()
        else:
            plt.close()
    except Exception:
        ax.text(0.5, 0.5, 'No data', ha='center', va='center')
        if show:
            plt.show()
        else:
            plt.close()

def visualize_player_role(data: pd.DataFrame, role: str, output_path: str = None, show: bool = True) -> None:
    """
    Function:
    - Visualizes player positions for a specific role using a 2D histogram; possible roles include 'Targeted Receiver',
    'Other Route Runner', 'Passer', 'Defensive Coverage'.

    Parameters:
    <data> (pd.DataFrame): DataFrame containing player position and role data with 'x', 'y', and 'player_role' columns.
    <role> (str): The player role to visualize (e.g., 'Targeted Receiver', ).
    <output_path> (str, optional): File path to save the plot. If None, plot is not saved.
    <show> (bool): Whether to display the plot (default: True).

    Returns:
    - None
    """
    if data.empty:
        print("No data available.")
        return
    viz_sample = data.sample(min(100000, len(data)))
    fig, ax = plt.subplots(figsize=(8, 6))
    try:
        role_data = viz_sample[viz_sample['player_role'] == role]
        if safe_hist2d(ax, 'x', 'y', role_data, f'{role} Positions', 'Greens'):
            if output_path:
                plt.savefig(output_path, dpi=150, bbox_inches='tight')
            if show:
                plt.show()
        else:
            plt.close()
    except Exception:
        ax.text(0.5, 0.5, 'No data', ha='center', va='center')
        if show:
            plt.show()
        else:
            plt.close()

def visualize_position_heatmap(data: pd.DataFrame, position: str, output_path: str = None, show: bool = True) -> None:
    """
    Function:
    - Visualizes player positions for a specific position using a 2D histogram; possible <position> values include ['QB',
    'RB', 'FB', 'WR', 'TE', 'NT', 'DT', 'DE', 'OLB', 'ILB', 'MLB', 'SS', 'FS', 'S', 'CB'].

    Parameters:
    <data> (pd.DataFrame): DataFrame containing player position data with 'x', 'y', and 'player_position' columns.
    <position> (str): The player position to visualize (e.g., 'QB').
    <output_path> (str, optional): File path to save the plot. If None, plot is not saved.
    <show> (bool): Whether to display the plot (default: True).

    Returns:
    - None
    """
    if data.empty:
        print("No data available.")
        return
    viz_sample = data.sample(min(100000, len(data)))
    fig, ax = plt.subplots(figsize=(8, 6))
    try:
        pos_data = viz_sample[viz_sample['player_position'] == position]
        if safe_hist2d(ax, 'x', 'y', pos_data, f'{position} Heat Map', 'viridis'):
            if output_path:
                plt.savefig(output_path, dpi=150, bbox_inches='tight')
            if show:
                plt.show()
        else:
            plt.close()
    except Exception:
        ax.text(0.5, 0.5, 'No data', ha='center', va='center')
        if show:
            plt.show()
        else:
            plt.close()

def visualize_ball_landing_zones(data: pd.DataFrame, output_path: str = None, show: bool = True) -> None:
    """
    Function:
    - Visualizes ball landing zones using a 2D histogram.

    Parameters:
    <data> (pd.DataFrame): DataFrame containing ball landing position data with 'ball_land_x' and 'ball_land_y' columns.
    <output_path> (str, optional): File path to save the plot. If None, plot is not saved.
    <show> (bool): Whether to display the plot (default: True).

    Returns:
    - None
    """
    if data.empty:
        print("No data available.")
        return
    viz_sample = data.sample(min(100000, len(data)))
    fig, ax = plt.subplots(figsize=(8, 6))
    if safe_hist2d(ax, 'ball_land_x', 'ball_land_y', viz_sample, 'Ball Landing Zones', 'Oranges'):
        if output_path:
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
        if show:
            plt.show()
    else:
        plt.close()

def visualize_direction_movement(data: pd.DataFrame, dir_min: float, dir_max: float, output_path: str = None, show: bool = True) -> None:
    """
    Function:
    - Visualizes player positions for a specific direction range using a 2D histogram.

    Parameters:
    <data> (pd.DataFrame): DataFrame containing player position and direction data with 'x', 'y', and 'dir' columns.
    <dir_min> (float): Minimum direction angle in degrees.
    <dir_max> (float): Maximum direction angle in degrees.
    <output_path> (str, optional): File path to save the plot. If None, plot is not saved.
    <show> (bool): Whether to display the plot (default: True).

    Returns:
    - None
    """
    if data.empty:
        print("No data available.")
        return
    viz_sample = data.sample(min(100000, len(data)))
    fig, ax = plt.subplots(figsize=(8, 6))
    try:
        dir_data = viz_sample[(viz_sample['dir'] >= dir_min) & (viz_sample['dir'] < dir_max)]
        if safe_hist2d(ax, 'x', 'y', dir_data, f'Direction {dir_min}°-{dir_max}°', 'plasma'):
            if output_path:
                plt.savefig(output_path, dpi=150, bbox_inches='tight')
            if show:
                plt.show()
        else:
            plt.close()
    except Exception:
        ax.text(0.5, 0.5, 'No data', ha='center', va='center')
        if show:
            plt.show()
        else:
            plt.close()

def visualize_player_side(data: pd.DataFrame, side: str, output_path: str = None, show: bool = True) -> None:
    """
    Function:
    - Visualizes player positions for a specific team side (Offense/Defense) using a 2D histogram.

    Parameters:
    <data> (pd.DataFrame): DataFrame containing player position and side data with 'x', 'y', and 'player_side' columns.
    <side> (str): The team side to visualize ('Offense' or 'Defense').
    <output_path> (str, optional): File path to save the plot. If None, plot is not saved.
    <show> (bool): Whether to display the plot (default: True).

    Returns:
    - None
    """
    if data.empty:
        print("No data available.")
        return
    viz_sample = data.sample(min(100000, len(data)))
    fig, ax = plt.subplots(figsize=(8, 6))
    try:
        side_data = viz_sample[viz_sample['player_side'] == side]
        if safe_hist2d(ax, 'x', 'y', side_data, f'{side} Positions', 'coolwarm'):
            if output_path:
                plt.savefig(output_path, dpi=150, bbox_inches='tight')
            if show:
                plt.show()
        else:
            plt.close()
    except Exception:
        ax.text(0.5, 0.5, 'No data', ha='center', va='center')
        if show:
            plt.show()
        else:
            plt.close()

def visualize_early_frames(data: pd.DataFrame, output_path: str = None, show: bool = True) -> None:
    """
    Function:
    - Visualizes player positions for early frames (1-5) using a 2D histogram.

    Parameters:
    <data> (pd.DataFrame): DataFrame containing player position and frame data with 'x', 'y', and 'frame_id' columns.
    <output_path> (str, optional): File path to save the plot. If None, plot is not saved.
    <show> (bool): Whether to display the plot (default: True).

    Returns:
    - None
    """
    if data.empty:
        print("No data available.")
        return
    viz_sample = data.sample(min(100000, len(data)))
    fig, ax = plt.subplots(figsize=(8, 6))
    try:
        early_frames = viz_sample[viz_sample['frame_id'] <= 5]
        if safe_hist2d(ax, 'x', 'y', early_frames, 'Early Frames (1-5)', 'spring'):
            if output_path:
                plt.savefig(output_path, dpi=150, bbox_inches='tight')
            if show:
                plt.show()
        else:
            plt.close()
    except Exception:
        ax.text(0.5, 0.5, 'No data', ha='center', va='center')
        if show:
            plt.show()
        else:
            plt.close()