import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random

def calculate_angular_distance(x, y):
    return np.arctan2(y, x)

def calculate_velocity(angular_distance, timestamp):
    time_diff = np.diff(timestamp)
    angular_distance_diff = np.diff(angular_distance)
    velocity = angular_distance_diff / time_diff
    return np.concatenate(([np.nan], velocity))

def generate_random_color():
    return (random.random(), random.random(), random.random())

def draw_experiment_lines(start_timestamp, end_timestamp):
    plt.axvline(x=start_timestamp, color='black', linestyle='--')
    plt.text(start_timestamp, plt.ylim()[0] + (plt.ylim()[1] - plt.ylim()[0]) / 2, 
             f'Experiment Started', rotation=90, verticalalignment='center', horizontalalignment='right', color='black')

    plt.axvline(x=end_timestamp, color='black', linestyle='--')
    plt.text(end_timestamp, plt.ylim()[0] + (plt.ylim()[1] - plt.ylim()[0]) / 2, 
             f'Experiment Ended', rotation=90, verticalalignment='center', horizontalalignment='right', color='black')

def draw_object_line(timestamp, label, object_colors):
    object_number = label.split(' ')[-1]

    if object_number not in object_colors:
        object_colors[object_number] = generate_random_color()

    plt.axvline(x=timestamp, color=object_colors[object_number], linestyle='--', alpha=0.7)
    plt.text(timestamp, plt.ylim()[0] + (plt.ylim()[1] - plt.ylim()[0]) / 2, 
            f'{label} {object_number} at: {timestamp:.2f}', rotation=90, verticalalignment='center', horizontalalignment='right', color=object_colors[object_number], alpha=0.7)

def draw_objects_and_interceptions(spawn_timestamps, interception_timestamps, object_colors, annotations_df):
    for timestamp, label in zip(spawn_timestamps, annotations_df.loc[annotations_df['label'].str.startswith('Spawned'), 'label']):
        draw_object_line(timestamp, label, object_colors)

        object_number = label.split(' ')[-1]
        corresponding_interception = annotations_df.loc[(annotations_df['label'].str.startswith('Intercepted')) & (annotations_df['label'].str.endswith(object_number)), 'timestamp'].values
        if len(corresponding_interception) > 0:
            plt.axvline(x=corresponding_interception[0], color=object_colors[object_number], linestyle='--', alpha=0.7)

    for timestamp, label in zip(interception_timestamps, annotations_df.loc[annotations_df['label'].str.startswith('Intercepted'), 'label']):
        draw_object_line(timestamp, label, object_colors)

def adjust_timestamps_to_zero(df, timestamp_column):
    min_timestamp = df[timestamp_column].min()
    df[timestamp_column] -= min_timestamp
    return df

def draw_experiment_lines(start_timestamp, end_timestamp, max_timestamp):
    plt.axvline(x=start_timestamp, color='black', linestyle='--')
    plt.text(start_timestamp, plt.ylim()[0] + (plt.ylim()[1] - plt.ylim()[0]) / 2, 
             f'Experiment Started', rotation=90, verticalalignment='center', horizontalalignment='right', color='black')

    plt.axvline(x=end_timestamp, color='black', linestyle='--')
    plt.text(end_timestamp, plt.ylim()[0] + (plt.ylim()[1] - plt.ylim()[0]) / 2, 
             f'Experiment Ended', rotation=90, verticalalignment='center', horizontalalignment='right', color='black')

    plt.xlim(0, max_timestamp)

def plot_gaze_positions_combined(csv_file, annotations_file=None, plot_every=1, show_velocity=True, velocity_threshold=0.8, show_saccades_line=False):
    # Read CSV file with provided file name
    df = pd.read_csv(csv_file)

    df_subset = df.iloc[::plot_every, :]

    # Adjust timestamps to start from 0
    df_subset = adjust_timestamps_to_zero(df_subset, 'gaze_timestamp')

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
    ax1.plot(df_subset['gaze_timestamp'], df_subset['angular_distance'], label='Angular Distance', linestyle='-', color='orange', alpha=0.5)

    if show_velocity:
        ax2.plot(df_subset['gaze_timestamp'], df_subset['velocity'], label='Gaze Velocity', linestyle='-', color='cornflowerblue', alpha=0.2)  # Set alpha to control opacity

    # Highlight the line corresponding to saccades
    if show_saccades_line:
        ax1.plot(df_subset['gaze_timestamp'], np.where(saccade_regions, df_subset['angular_distance'], np.nan), color='red', label='Saccade Line', alpha=0.5)

    max_timestamp = df_subset['gaze_timestamp'].max()

    # Additional code for annotations
    if annotations_file:
        annotations_df = pd.read_csv(annotations_file)

        # List of timestamp columns to adjust for annotations
        timestamp_columns_to_adjust_annotations = ['timestamp']

        # Adjust annotation timestamps to start from 0
        annotations_df = adjust_timestamps_to_zero(annotations_df, timestamp_columns_to_adjust_annotations)

        spawn_timestamps = annotations_df.loc[annotations_df['label'].str.startswith('Spawned'), 'timestamp'].values
        interception_timestamps = annotations_df.loc[annotations_df['label'].str.startswith('Intercepted'), 'timestamp'].values

        start_timestamp = annotations_df.loc[(annotations_df['label'] == 'Experiment Started'), 'timestamp'].values
        end_timestamp = annotations_df.loc[(annotations_df['label'] == 'Experiment Ended'), 'timestamp'].values

        draw_experiment_lines(start_timestamp, end_timestamp, max_timestamp)

        # Create a dictionary to store colors for each object number
        object_colors = {}

        draw_objects_and_interceptions(spawn_timestamps, interception_timestamps, object_colors, annotations_df)

    # Set labels and title
    ax1.set_xlabel('Timestamp')
    ax1.set_ylabel('Angular Distance', color='orange')
    ax2.set_ylabel('Gaze Velocity', color='cornflowerblue')
    ax1.grid(True)

    # Display legends
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # Show the plot
    plt.legend()
    plt.show()


if __name__ == "__main__":
    gaze_csv_file = "gaze_positions.csv"
    annotations_csv_file = "annotations.csv"
    plot_gaze_positions_combined(gaze_csv_file, annotations_file=annotations_csv_file, velocity_threshold=0.5, show_velocity=False, show_saccades_line=True)
