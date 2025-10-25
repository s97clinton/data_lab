import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean

def calculate_receiver_separation_at_catch_point(input_df: pd.DataFrame, output_df: pd.DataFrame) -> pd.DataFrame:
    """
    Function:
    - Calculate the straight-line distance between the "targeted" receiver
    and (1) the nearest defender and (2) the average distance to all defenders
    at the moment of catch (final frame of the play for the receiver).
    - This is accomplished by (1) using the <input_df> to identify the targeted receiver
    for each play, (2) locating that receiver in the <output_df> to find their final position,
    and (3) calculating distances to all defenders at that frame.

    Parameters:
    <input_df> (pd.DataFrame): Input data from NFL data bowl.
    <output_df> (pd.DataFrame): Output data from NFL data bowl.

    Returns:
    pd.DataFrame: DataFrame with receiver separation metrics.
    """
    results = []
    
    # Get unique plays
    plays = input_df[['game_id', 'play_id']].drop_duplicates()
    
    for _, play in plays.iterrows():
        # Get play data
        play_input = input_df[(input_df['game_id'] == play['game_id']) & 
                              (input_df['play_id'] == play['play_id'])]
        play_output = output_df[(output_df['game_id'] == play['game_id']) & 
                               (output_df['play_id'] == play['play_id'])]
        
        # Get targeted receiver
        receiver_input = play_input[play_input['player_role'] == 'Targeted Receiver']
        
        if len(receiver_input) > 0:
            receiver_id = receiver_input['nfl_id'].iloc[0]
            
            # Get receiver trajectory in output
            receiver_output = play_output[play_output['nfl_id'] == receiver_id]
            
            if len(receiver_output) > 0:
                # Get final frame position
                final_frame = receiver_output['frame_id'].max()
                final_pos = receiver_output[receiver_output['frame_id'] == final_frame]
                
                if len(final_pos) > 0:
                    rec_x = final_pos['x'].iloc[0]
                    rec_y = final_pos['y'].iloc[0]
                    
                    # Calculate distance to all defenders at final frame
                    defenders_final = play_output[(play_output['frame_id'] == final_frame) & 
                                                  (play_output['nfl_id'] != receiver_id)]
                    
                    if len(defenders_final) > 0:
                        distances = []
                        for _, defender in defenders_final.iterrows():
                            dist = np.sqrt((rec_x - defender['x'])**2 + 
                                         (rec_y - defender['y'])**2)
                            distances.append(dist)
                        
                        min_def_distance_catch_point = min(distances) if distances else 0
                        avg_def_distance_catch_point = np.mean(distances) if distances else 0
                        
                        results.append({
                            'game_id': play['game_id'],
                            'play_id': play['play_id'],
                            'nearest_def_distance_catch_point': round(min_def_distance_catch_point, 3),
                            'avg_def_distance_catch_point': round(avg_def_distance_catch_point, 3)
                        })
    
    return pd.DataFrame(results)



def calculate_defender_accelerometer_metric(input_df: pd.DataFrame, output_df: pd.DataFrame) -> pd.DataFrame:
    """
    Function:
    - This function (1) uses the <input_df> to identify defensive players on a given play,
    (2) tracks their movement in the <output_df> over the first three frames after the ball is thrown,
    and (3) computes a metric reflecting the average absolute change in speed (as a proxy for acceleration magnitude)
    based on Euclidean distances traveled between these frames.
    - This calculation is rife with inherent problems; not all defenders should be reacting to all passes,
    and there are all sorts of differences between a defender playing in man vs zone, breaking from depth, etc.
    - However, this metric provides an example of how to work with changing velocities in the output_df,
    and the approach could be useful in a more refined context.

    Parameters:
    <input_df> (pd.DataFrame): Input data from NFL data bowl.
    <output_df> (pd.DataFrame): Output data from NFL data bowl.

    Returns:
    pd.DataFrame: DataFrame with defender accelerometer metrics.
    """
    results = []
    
    plays = input_df[['game_id', 'play_id']].drop_duplicates()
    
    for _, play in plays.iterrows():
        play_input = input_df[(input_df['game_id'] == play['game_id']) & 
                              (input_df['play_id'] == play['play_id'])]
        play_output = output_df[(output_df['game_id'] == play['game_id']) & 
                               (output_df['play_id'] == play['play_id'])]
        
        # Get defensive players
        defenders_input = play_input[play_input['player_side'] == 'Defense']
        
        for defender_id in defenders_input['nfl_id'].unique():
            defender_output = play_output[play_output['nfl_id'] == defender_id]
            
            if len(defender_output) >= 3:
                # Calculate acceleration change in first 3 frames
                early_frames = defender_output[defender_output['frame_id'] <= 3]
                if len(early_frames) >= 3:
                    # Calculate velocity change
                    dx = early_frames['x'].diff()
                    dy = early_frames['y'].diff()
                    velocities = np.sqrt(dx**2 + dy**2)
                    
                    # Response metric
                    defender_accelerometer_metric = velocities.diff().abs().mean()
                    
                    results.append({
                        'game_id': play['game_id'],
                        'play_id': play['play_id'],
                        'defender_id': defender_id,
                        'defender_accelerometer_metric': defender_accelerometer_metric
                    })
    
    return pd.DataFrame(results)



def calculate_receiver_ball_in_air_straightline_euclidean_efficiency(input_df: pd.DataFrame, output_df: pd.DataFrame) -> pd.DataFrame:
    """
    Function:
    - Calculate how "efficiently" (according to euclidean straight-line comparison) move to the ball "catch point" by
    taking (1) the receiver's coordinates in the first "frame" of the <output_df> for that play, (2) the ball's landing coordinates,
    (3) the euclidean distances traveled by the receiver in each distinct "frame" of the play, which aggregates to a "total distance traveled",
    and (4) calculating the (direct distance to ball) / (total distance traveled) to get an efficiency metric.
    - Efficiency is defined as the ratio of direct distance to total distance traveled where a value of 1 represents a perfectly efficient path, values less than 1
    are less efficient paths, and values greater than 1 indicate the receiver did not travel the required distance to reach the ball's landing point.
    1 .
    - In reality, this metric is flawed as receivers may need to adjust a path, avoid defenders, but it is a useful starting point
    to determine the path the receiver took to the anticipated catch point.
    
    Parameters:
    <input_df> (pd.DataFrame): Input data from NFL data bowl.
    <output_df> (pd.DataFrame): Output data from NFL data bowl.
    
    Returns:
    pd.DataFrame: DataFrame with receiver euclidean straightline efficiency metrics.
    """
    results = []
    
    plays = input_df[['game_id', 'play_id']].drop_duplicates()
    
    for _, play in plays.iterrows():
        play_input = input_df[(input_df['game_id'] == play['game_id']) & 
                              (input_df['play_id'] == play['play_id'])]
        play_output = output_df[(output_df['game_id'] == play['game_id']) & 
                               (output_df['play_id'] == play['play_id'])]
        
        # Get targeted receiver
        receiver_input = play_input[play_input['player_role'] == 'Targeted Receiver']
        
        if len(receiver_input) > 0:
            receiver_id = receiver_input['nfl_id'].iloc[0]
            ball_x = receiver_input['ball_land_x'].iloc[0]
            ball_y = receiver_input['ball_land_y'].iloc[0]
            
            receiver_output = play_output[play_output['nfl_id'] == receiver_id]
            
            if len(receiver_output) > 1:
                # Calculate total distance traveled
                total_distance = 0
                positions = receiver_output[['x', 'y']].values
                for i in range(1, len(positions)):
                    total_distance += euclidean(positions[i-1], positions[i])
                
                # Calculate direct distance to ball
                start_pos = receiver_output.iloc[0]
                direct_distance = euclidean([start_pos['x'], start_pos['y']], [ball_x, ball_y])
                
                # Efficiency = direct / total (higher is more efficient)
                efficiency = direct_distance / (total_distance) if total_distance > 0 else 0
                
                results.append({
                    'game_id': play['game_id'],
                    'play_id': play['play_id'],
                    'route_efficiency': efficiency,
                    'total_distance': total_distance,
                    'direct_distance': direct_distance
                })
    
    return pd.DataFrame(results)