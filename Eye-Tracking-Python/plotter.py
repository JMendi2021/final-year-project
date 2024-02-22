import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def calculate_angular_distance(x, y):
    # Calculate angular distance using arctangent
    return np.arctan2(y, x)

def plot_gaze_positions(csv_file, annotations_file=None, plot_every=1):
    # Read CSV file with provided file name
    df = pd.read_csv(csv_file)

    # Calculate angular distance per x and y
    df['angular_distance'] = calculate_angular_distance(df['norm_pos_x'], df['norm_pos_y'])
    df_subset = df.iloc[::plot_every, :]

    # Plot gaze positions with adjusted timestamps on x-axis and angular distance on y-axis
    plt.figure(figsize=(10, 6))

    plt.plot(df_subset['gaze_timestamp'], df_subset['angular_distance'], label='Gaze Angular Distance', linestyle='-', color='cornflowerblue')

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

    plt.xlim(df_subset['gaze_timestamp'].min(), end_timestamp) # Adjust the scale of the horizontal axis
    
    plt.title('Gaze Angular Distance Over Timestamp')
    plt.xlabel('Timestamp')
    plt.ylabel('Gaze Angular Distance')
    # plt.ylabel('Gaze Position')
    plt.legend()
    plt.grid(True)

    # Show the plot
    plt.show()

if __name__ == "__main__":
    gaze_csv_file = "gaze_positions.csv"
    annotations_csv_file = "annotations.csv"
    plot_gaze_positions(gaze_csv_file, annotations_csv_file, plot_every=1)

