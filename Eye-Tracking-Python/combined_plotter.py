import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def calculate_angular_distance(x, y):
    # Calculate angular distance using arctangent
    return np.arctan2(y, x)

def calculate_velocity(angular_distance, timestamp):
    # Calculate velocity as the gradient of angular distance with respect to time
    time_diff = np.diff(timestamp)
    angular_distance_diff = np.diff(angular_distance)
    velocity = angular_distance_diff / time_diff
    return np.concatenate(([np.nan], velocity))  # Pad with NaN for the first data point

def plot_gaze_positions_combined(csv_file, annotations_file=None, plot_every=1, show_velocity=True, velocity_threshold=0.8):
    # Read CSV file with provided file name
    df = pd.read_csv(csv_file)

    df_subset = df.iloc[::plot_every, :]

    # Calculate angular distance per x and y
    df_subset['angular_distance'] = calculate_angular_distance(df_subset['norm_pos_x'], df_subset['norm_pos_y'])

    # Calculate velocity
    df_subset['velocity'] = calculate_velocity(df_subset['angular_distance'], df_subset['gaze_timestamp'])

    # Identify regions with large peaks in velocity (both high and low)
    saccade_regions_high = df_subset['velocity'] > velocity_threshold
    saccade_regions_low = df_subset['velocity'] < -velocity_threshold
    saccade_regions = saccade_regions_high | saccade_regions_low

    # Create a twin Axes sharing the x-axis
    fig, ax1 = plt.subplots(figsize=(15, 9))
    ax2 = ax1.twinx()

    # Plot gaze positions with adjusted timestamps on x-axis and raw velocity on y-axis
    if show_velocity:
        ax1.plot(df_subset['gaze_timestamp'], df_subset['velocity'], label='Gaze Velocity', linestyle='-', color='cornflowerblue', alpha=0.3)
    ax2.plot(df_subset['gaze_timestamp'], df_subset['angular_distance'], label='Angular Distance', linestyle='-', color='orange')  # Set alpha to control opacity

    # Highlight the line corresponding to saccades
    ax2.plot(df_subset['gaze_timestamp'], np.where(saccade_regions, df_subset['angular_distance'], np.nan), color='red', label='Saccade Line')

    ax1.set_xlim(df_subset['gaze_timestamp'].min(), df_subset['gaze_timestamp'].max())

    # Set labels and title
    ax1.set_xlabel('Timestamp')
    ax1.set_ylabel('Gaze Velocity', color='cornflowerblue')
    ax2.set_ylabel('Angular Distance', color='orange')
    ax1.grid(True)

    # Additional code for annotations
    if annotations_file:
        annotations_df = pd.read_csv(annotations_file)

        spawn_timestamps = annotations_df.loc[annotations_df['label'] == 'Object Spawned', 'timestamp'].values
        interception_timestamps = annotations_df.loc[annotations_df['label'] == 'Intercepted', 'timestamp'].values

        start_timestamp = annotations_df.loc[(annotations_df['label'] == 'Experiment Started'), 'timestamp'].values
        end_timestamp = annotations_df.loc[(annotations_df['label'] == 'Experiment Ended'), 'timestamp'].values

        # Draw vetical lines to indicate the start and end of an experiment
        plt.axvline(x=start_timestamp, color='black', linestyle='--')
        plt.text(start_timestamp, plt.ylim()[0] + (plt.ylim()[1] - plt.ylim()[0]) / 2, 
                 f'Experiment Started', rotation=90, verticalalignment='center', horizontalalignment='right', color='black')

        plt.axvline(x=end_timestamp, color='black', linestyle='--')
        plt.text(end_timestamp, plt.ylim()[0] + (plt.ylim()[1] - plt.ylim()[0]) / 2, 
                 f'Experiment Ended', rotation=90, verticalalignment='center', horizontalalignment='right', color='black')

        # Draw vertical lines for object spawning timestamps
        for timestamp in spawn_timestamps:
            plt.axvline(x=timestamp, color='red', linestyle='--', alpha=0.5)
            plt.text(timestamp, plt.ylim()[0] + (plt.ylim()[1] - plt.ylim()[0]) / 2, 
                     f'Object spawned on: {timestamp:.2f}', rotation=90, verticalalignment='center', horizontalalignment='right', color='red', alpha=0.5)
    
        # Draw vertical lines for object spawning timestamps
        for timestamp in interception_timestamps:
            plt.axvline(x=timestamp, color='green', linestyle='--', alpha=0.5)
            plt.text(timestamp, plt.ylim()[0] + (plt.ylim()[1] - plt.ylim()[0]) / 2, 
                     f'Interception made on: {timestamp:.2f}', rotation=90, verticalalignment='center', horizontalalignment='right', color='green', alpha=0.5)


    # Show the plot
    plt.legend()
    plt.show()

if __name__ == "__main__":
    gaze_csv_file = "gaze_positions.csv"
    annotations_csv_file = "annotations.csv"

    # Show both angular distance and velocity
    plot_gaze_positions_combined(gaze_csv_file, annotations_file=annotations_csv_file, plot_every=1)
