import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def calculate_angular_distance(x, y):
    # Calculate angular distance using arctangent
    return np.arctan2(y, x)

def plot_gaze_positions(csv_file, annotations_file=None, plot_every=100):
    # Read CSV file into a Pandas DataFrame
    df = pd.read_csv(csv_file)

    # Calculate angular distance
    df['angular_distance'] = calculate_angular_distance(df['norm_pos_x'], df['norm_pos_y'])

    # Subtract the minimum timestamp value to start from 0
    df['adjusted_timestamp'] = df['gaze_timestamp'] - df['gaze_timestamp'].min()

    df_subset = df.iloc[::plot_every, :]

    # Plot gaze positions with adjusted timestamps on x-axis and angular distance on y-axis
    plt.figure(figsize=(10, 6))
    plt.plot(df_subset['adjusted_timestamp'], df_subset['angular_distance'], label='Gaze Angular Distance', marker='o')

    # Plots x and y normalised gaze position and angular distance
    # plt.plot(df['adjusted_timestamp'], df['norm_pos_x'], label='X Position', marker='o', color='green')
    # plt.plot(df['adjusted_timestamp'], df['norm_pos_y'], label='Y Position', marker='o', color='red')

    # Load annotations file
    if annotations_file:
        annotations_df = pd.read_csv(annotations_file)
        key_timestamps = annotations_df['timestamp'].values

        # Draw vertical lines for key timestamps
        for timestamp in key_timestamps:
            plt.axvline(x=timestamp - df['gaze_timestamp'].min(), color='red', linestyle='--')

    # Customise the plot
    plt.title('Gaze Angular Distance Over Time with Annotations')
    plt.xlabel('Adjusted Timestamp')
    plt.ylabel('Angular Distance')
    # plt.ylabel('Gaze Position')
    plt.legend()
    plt.grid(True)

    # Show the plot
    plt.show()

if __name__ == "__main__":
    gaze_csv_file = "gaze_positions.csv"
    annotations_csv_file = "annotations.csv"
    plot_gaze_positions(gaze_csv_file, annotations_file=annotations_csv_file, plot_every=50)
