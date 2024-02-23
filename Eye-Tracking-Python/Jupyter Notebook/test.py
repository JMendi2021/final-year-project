# %% [markdown]
# # Interception Gaze Visualiser
# This notebook takes in three csv files taken from the Pupil Recordings you have exported in Pupil Capture. These are:
# - `annotations.csv` (contains annotations that indicates important events during the recording)
# - `gaze_positions.csv` (contains raw data in regards to the gaze made throughout the recording)

# %%
# Imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
import json
import datetime

# %%
# Helper Functions
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

    plt.axvline(x=end_timestamp, color='black', linestyle='--')


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

    plt.axvline(x=end_timestamp, color='black', linestyle='--')

    plt.xlim(start_timestamp, end_timestamp)

# %% [markdown]
# Reading the `info.player` JSON to retrieve `start_time_synced_s` and `start_time_system_s`. This is used to format the timestamp correctly to indicate time throughout the experiment:

# %%
info_player_filePath = "info.player.json"
with open(info_player_filePath, 'r') as file:
    data = json.load(file)

start_time_synced_s = data.get('start_time_synced_s')
start_time_system_s = data.get('start_time_system_s')

offset = start_time_system_s - start_time_synced_s
print(f"Offset between system and synced start time: {offset}")

# %% [markdown]
# Reading the `gaze_position.csv`, adjusting the timestamps into seconds starting at 0:

# %%
gaze_csv_filePath = "gaze_positions.csv"
gaze_df = pd.read_csv(gaze_csv_filePath)
print(f"There is a total of {len(gaze_df)} in the Gaze DataFrame")

# Converting timestamps into seconds (starting from 0)
def convert_timestamps_to_seconds(df, timestamp_column, offset):
    df['seconds'] = df[timestamp_column] + offset
    df['seconds'] -= df['seconds'].min()
    return df

gaze_df = convert_timestamps_to_seconds(gaze_df, 'gaze_timestamp', offset)
print(gaze_df['seconds'])

# %% [markdown]
# Smoothing `norm_pos_x` and `norm_pos_y` and plotting on a Position x Time graph:

# %%
window_size = 10
gaze_df['smoothed_norm_pos_x'] = gaze_df['norm_pos_x'].rolling(window=window_size).mean()
gaze_df['smoothed_norm_pos_y'] = gaze_df['norm_pos_y'].rolling(window=window_size).mean()

fig, axs = plt.subplots(1, 2, figsize=(15, 6))

axs[0].plot(gaze_df['seconds'], gaze_df['norm_pos_x'], label='Original norm_pos_x')
axs[0].plot(gaze_df['seconds'], gaze_df['smoothed_norm_pos_x'], label=f'Smoothed norm_pos_x (window={window_size})', linestyle='--')
axs[0].set_title('Norm_pos_x')

axs[1].plot(gaze_df['seconds'], gaze_df['norm_pos_y'], label='Original norm_pos_y')
axs[1].plot(gaze_df['seconds'], gaze_df['smoothed_norm_pos_y'], label=f'Smoothed norm_pos_y (window={window_size})', linestyle='--')
axs[1].set_title('Norm_pos_y')

for ax in axs:
    ax.set_xlabel('Time')
    ax.set_ylabel('Position')
    ax.legend()

plt.tight_layout()
plt.show()

# %% [markdown]
# Calculating `angular_distance` of using normalised `x` and `y` (both smoothed and unsmoothed): 

# %%
gaze_df['angular_distance'] = calculate_angular_distance(gaze_df['norm_pos_x'], gaze_df['norm_pos_y'])
gaze_df['smoothed_angular_distance'] = calculate_angular_distance(gaze_df['smoothed_norm_pos_x'], gaze_df['smoothed_norm_pos_y'])

plt.figure(figsize=(10, 6))

plt.plot(gaze_df['seconds'], gaze_df['angular_distance'], label='Gaze Angular Distance',)
plt.plot(gaze_df['seconds'], gaze_df['smoothed_angular_distance'], label=f'Smoothed Gaze Angular Distance', linestyle='--')

plt.title('Angular Distance')
plt.xlabel('Time')
plt.ylabel('Angular Distance')
# plt.ylabel('Gaze Position')

plt.legend()
plt.grid(True)
plt.tight_layout()


# %% [markdown]
# Reeding the `annotations.csv` and then plotting the annotations shows when the experiment has started, ended, and when objects has spawned or has been intercepted. This occurs only if the annotation filepath has been indicated

# %%
annotations_filePath = "annotations.csv"

max_timestamp = gaze_df['seconds'].max()

if annotations_filePath:
    annotations_df = pd.read_csv(annotations_filePath)

    # Convert timestamps to seconds and start from 0
    annotations_df = convert_timestamps_to_seconds(annotations_df, 'timestamp', offset)

    spawn_timestamps = annotations_df.loc[annotations_df['label'].str.startswith('Spawned'), 'seconds'].values
    interception_timestamps = annotations_df.loc[annotations_df['label'].str.startswith('Intercepted'), 'seconds'].values

    start_timestamp = annotations_df.loc[(annotations_df['label'] == 'Experiment Started'), 'seconds'].values
    end_timestamp = annotations_df.loc[(annotations_df['label'] == 'Experiment Ended'), 'seconds'].values

    draw_experiment_lines(start_timestamp, end_timestamp, max_timestamp)

    # Create a dictionary to store colors for each object number
    object_colors = {}

    draw_objects_and_interceptions(spawn_timestamps, interception_timestamps, object_colors, annotations_df)



