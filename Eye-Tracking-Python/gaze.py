# %% [markdown]
# # Gaze Interception
# This notebook takes in two files taken from the Pupil Recordings you have exported in Pupil Player. These are:
# - `gaze_positions.csv` (contains raw data in regards to the gaze made throughout the recording)
# - `info.player.json` (contains system and sync time used to format the recording timestamps)

# %%
# Imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
import json
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)
# File Paths
info_player_filePath = 'source/info.player.json'
gaze_csv_filePath = 'source/gaze_positions.csv'
annotations_filepath = 'source/annotations.csv'

# %%
# Helper Functions

# Calculate angular distance given Cartesian coordinates (x, y)
def calculate_angular_distance(x, y):
    return np.arctan2(y, x)

# Calculate velocity given angular distance and corresponding timestamps.
def calculate_velocity(angular_distance, timestamp):
    time_diff = np.diff(timestamp)
    angular_distance_diff = np.diff(angular_distance)
    velocity = angular_distance_diff / time_diff
    return np.concatenate(([np.nan], velocity))

# %% [markdown]
# Reading the `info.player` JSON to retrieve `start_time_synced_s` and `start_time_system_s`. This is used to format the timestamp correctly to indicate time throughout the experiment:

# %%
with open(info_player_filePath, 'r') as file:
    data = json.load(file)

start_time_synced_s = data.get('start_time_synced_s')
start_time_system_s = data.get('start_time_system_s')

offset = start_time_system_s - start_time_synced_s
print(f"Offset between system and synced start time: {offset}")

# %% [markdown]
# Reading the `gaze_position.csv`, reformatting the timestamps into seconds starting at 0:

# %%
gaze_df = pd.read_csv(gaze_csv_filePath)
print(f"There is a total of {len(gaze_df)} in the Gaze DataFrame")

# Converting timestamps into time (starting from 0)
def convert_timestamps_to_time(df, timestamp_column, offset):
    df.copy()
    df['time'] = df[timestamp_column] + offset
    df['time'] -= df['time'].min()
    return df

gaze_df = convert_timestamps_to_time(gaze_df, 'gaze_timestamp', offset)
print(gaze_df['time'])

# %% [markdown]
# Smoothing `norm_pos_x` and `norm_pos_y` and plotting on a Position x Time graph:

# %%
window_size = 10
gaze_df['smoothed_norm_pos_x'] = gaze_df['norm_pos_x'].rolling(window=window_size).median()
gaze_df['smoothed_norm_pos_y'] = gaze_df['norm_pos_y'].rolling(window=window_size).median()

fig, axs = plt.subplots(1, 2, figsize=(15, 6))

axs[0].plot(gaze_df['time'], gaze_df['norm_pos_x'], label='Original norm_pos_x')
axs[0].plot(gaze_df['time'], gaze_df['smoothed_norm_pos_x'], label=f'Smoothed norm_pos_x (window={window_size})', linestyle='--')
axs[0].set_title('Norm_pos_x')

axs[1].plot(gaze_df['time'], gaze_df['norm_pos_y'], label='Original norm_pos_y')
axs[1].plot(gaze_df['time'], gaze_df['smoothed_norm_pos_y'], label=f'Smoothed norm_pos_y (window={window_size})', linestyle='--')
axs[1].set_title('Norm_pos_y')

for ax in axs:
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Position')
    ax.legend()

# %% [markdown]
# # Plotting Angular Distance agaisnt Time

# %% [markdown]
# Calculating `angular_distance` of using normalised `x` and `y` (both smoothed and unsmoothed): 

# %%
gaze_df['angular_distance'] = calculate_angular_distance(gaze_df['norm_pos_x'], gaze_df['norm_pos_y'])
gaze_df['smoothed_angular_distance'] = calculate_angular_distance(gaze_df['smoothed_norm_pos_x'], gaze_df['smoothed_norm_pos_y'])

# Defining a graph to work with throughout the script:
figure, ax = plt.subplots(figsize=(16, 8))
smoothed_figure, ax2 = plt.subplots(figsize=(16, 8))

def plot_angular_graph(figure, ax, df, source='angular_distance', show_both=False):
    """
    Plot angular distance data from a DataFrame against time.

    Parameters:
        df: DataFrame containing angular distance data.
        source (str): Source of angular distance data ('angular_distance' or 'smoothed_angular_distance').
        show_both (bool): Whether to show both raw and smoothed angular distance on the same plot.
    """

    if show_both:
        ax.plot(df['time'], df['angular_distance'], label='Gaze Angular Distance',)
        ax.plot(df['time'], df['smoothed_angular_distance'], label=f'Smoothed Gaze Angular Distance', linestyle='--')
    
    else:
        if source == 'smoothed_angular_distance':
            ax.plot(df['time'], df['smoothed_angular_distance'], label=f'Smoothed Gaze Angular Distance', color='black')
        else:
            ax.plot(df['time'], df['angular_distance'], label='Gaze Angular Distance', color='black')

    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Angular Distance (rad)', color='black')

    ax.legend()
    fig.suptitle('Interception Experiment')

plot_angular_graph(figure, ax, gaze_df)
plot_angular_graph(smoothed_figure, ax2, gaze_df, source='smoothed_angular_distance')

combined_figure, ax3 = plt.subplots(figsize=(16, 8))
plot_angular_graph(combined_figure, ax3, gaze_df, show_both=True)


# %% [markdown]
# # Identifying Saccadic Movements
# Based on the research from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1190820/pdf/jphysiol00502-0164.pdf, Saccadic Movements have a stereotypical velocity graph where large peaks indicates a fast movement between two points (saccades). These are almost like straight lines between points.

# %% [markdown]
# Calculating the gradient (velocity) at each point of the graph:

# %% [markdown]
# We create a new column in the `gaze_df` dataframe where it calculates the angular velocity using the `time` and `angular_distance` between each point

# %%
gaze_df['angular_velocity'] = calculate_velocity(gaze_df['angular_distance'], gaze_df['time'])
gaze_df['smoothed_angular_velocity'] = calculate_velocity(gaze_df['smoothed_angular_distance'], gaze_df['time'])

def plot_velocity_graph(df, source='angular_velocity'):
    print(df[source])
    """
    Plot angular velocity data from a DataFrame against time.

    Parameters:
        df: DataFrame containing angular velocity data.
        source (str): Source of angular velocity data ('angular_velocity' by default).

    """

    plt.figure(figsize=(18, 6))
    plt.plot(df['time'], df[source], label=f'{source}',)

    plt.title('Angular Velocity x Time Graph')
    plt.xlabel('Time (s)')
    plt.ylabel('Angular Velocity (rad/s)')
    # plt.ylabel('Gaze Position')

    plt.legend()
    plt.tight_layout()

plot_velocity_graph(gaze_df, 'smoothed_angular_velocity')
plot_velocity_graph(gaze_df)

# %% [markdown]
# Identifying regions of high velocity (when a velocity at a point exceeds a threshold) and plot saccadic movements on the Angular Distance Time Graph:

# %% [markdown]
# `plot_saccade_graph` takes a column from the DataFrame (`angular_velocity` or `smoothed_angular_velocity`) and plots it agaisnt time.
# The parameter `show_velocity` allows to display the velocity graph (same as above) under the main graph

# %%
def plot_saccade_graph(fig, ax, df, source='angular_velocity', threshold_velocity=0.8, show_velocity=False):
    """
    Plot saccade-related data from a DataFrame agaisnt time. And optionally show the velocity graph under.

    Parameters:
        fig : The Figure object to plot on.
        ax : The primary Axes object to plot on.
        df : DataFrame containing saccade-related data.
        source (str): Source of data ('angular_velocity' or 'smoothed_angular_velocity' by default).
        threshold_velocity (float): Threshold for identifying saccades based on velocity.
        show_velocity (bool): Whether to show velocity data on the plot.
    """
    velocity_label = "Angular Velocity"
    source_angular = gaze_df['angular_distance']
    source_velocity = gaze_df['angular_velocity']

    saccade_regions_high = df[source] > threshold_velocity
    accade_regions_low = df[source] < -threshold_velocity
    saccade_regions = saccade_regions_high | accade_regions_low


    if (source == 'smoothed_angular_velocity'):
        source_angular = gaze_df['smoothed_angular_distance']
        source_velocity = gaze_df['smoothed_angular_velocity']
        velocity_label = "Smoothed Angular Velocity"
        angular_label = "Smoothed Angular Distance"
    else:
        source_angular = gaze_df['angular_distance']
        source_velocity = gaze_df['angular_velocity']

    
    # Plot for Unsmoothed Data
    ax.plot(gaze_df['time'], np.where(saccade_regions, source_angular, np.nan), color='red', label='Saccade Line')
    ax.legend(loc='upper left')

    if show_velocity:
        ax1_2 = ax.twinx()
        ax1_2.plot(gaze_df['time'], source_velocity, label=f'{velocity_label}', linestyle='-', color='cornflowerblue', alpha=0.2)
        ax1_2.set_ylabel('Velocity (rad/s)', color='cornflowerblue')
        ax1_2.legend(loc='upper right')

    # Set common title
    fig.suptitle('Interception Experiment')

vel_ang_fig, ax = plt.subplots(figsize=(16, 8))
plot_angular_graph(vel_ang_fig, ax, gaze_df)
plot_saccade_graph(vel_ang_fig, ax, gaze_df)

vel_ang_fig_smoothed, ax1_2 = plt.subplots(figsize=(16, 8))
plot_angular_graph(vel_ang_fig_smoothed, ax1_2, gaze_df, source='smoothed_angular_distance')
plot_saccade_graph(vel_ang_fig_smoothed, ax1_2, gaze_df, source='smoothed_angular_velocity', show_velocity=True)


# %% [markdown]
# # Identifying Smooth Pursuit
# Smooth pursuit occurs when the eyes tracks an moving object at a constant speed. There is roughly a constant velocity as the angular distance changes slowly, whereas Saccades are almost instant. We choose regions of the line where the change in velocity is under a threshold, and the change of angular distance is small enough to indicate the eyes moving between positions slowly.

# %% [markdown]
# `plot_smooth_pursuit_graph` takes a column from the DataFrame (`angular_velocity` or `smoothed_angular_velocity`) and plots it agaisnt time.
# The parameter `show_velocity` allows to display the velocity graph (same as above) under the main graph

# %%
def plot_smooth_pursuit_graph(fig, ax, df, source='angular_velocity', velocity_tolerance=0.5, angular_distance_threshold=0.001, show_velocity=False):
    """
    Plot smooth pursuit-related data from a DataFrame against time. And optionally show the velocity graph under.

    Parameters:
        fig : The Figure object to plot on.
        ax : The primary Axes object to plot on.
        df : DataFrame containing smooth pursuit-related data.
        source (str): Source of data ('smoothed_angular_velocity' or 'smoothed_angular_distance' by default).
        velocity_tolerance (float): Tolerance for velocity changes to identify smooth pursuit.
        angular_distance_threshold (float): Threshold for identifying angular distance changes in pursuit.
        show_velocity (bool): Whether to show velocity data on the plot.
    """
    velocity_label = "Angular Velocity"
    source_angular = gaze_df['angular_distance']
    source_velocity = gaze_df['smoothed_angular_velocity']

    if (source == 'smoothed_angular_velocity'):
        source_angular = gaze_df['smoothed_angular_distance']
        source_velocity = gaze_df['smoothed_angular_velocity']
        velocity_label = "Smoothed Angular Velocity"
    else:
        source_angular = gaze_df['angular_distance']
        source_velocity = gaze_df['angular_velocity']


    # Identify periods of smooth pursuit based on velocity and angular distance
    velocity_changes = np.abs(np.gradient(source_velocity))
    angular_distance_changes = np.abs(np.gradient(source_angular))

    pursuit_regions = (velocity_changes < velocity_tolerance) & (angular_distance_changes > angular_distance_threshold)

    # Plot for Smooth Pursuit Data
    ax.plot(df['time'], np.where(pursuit_regions, source_angular, np.nan), color='green', label='Smooth Pursuit Line')
    ax.legend(loc='upper left')

    if show_velocity:
        ax1_2 = ax.twinx()
        ax1_2.plot(df['time'], source_velocity, label=f'{velocity_label}', linestyle='-', color='cornflowerblue', alpha=0.5)
        ax1_2.set_ylabel('Velocity (rad/s)', color='cornflowerblue')
        ax1_2.legend(loc='upper right')

# Example usage for smooth pursuit
smooth_pursuit_fig, ax_smooth_pursuit = plt.subplots(figsize=(16, 8))
plot_angular_graph(smooth_pursuit_fig, ax_smooth_pursuit, gaze_df, source='smoothed_angular_distance')
plot_smooth_pursuit_graph(smooth_pursuit_fig, ax_smooth_pursuit, gaze_df, source='smoothed_angular_velocity', show_velocity=True)
plot_saccade_graph(smooth_pursuit_fig, ax_smooth_pursuit, gaze_df, source='smoothed_angular_velocity')


# %% [markdown]
# # Adding Annotations to the graph
# To identify when the experiment occurs within the recording, as well as when object spawned and intercepted, we use the `annotations.csv` file:

# %% [markdown]
# `add_annotations` looks at a gieven filepath to an `annotation_csv` file and uses `labels` and `timestamp` to determine where to plot events on a Angular Distance Time Graph

# %%
# Generate a random RGB color tuple.
def generate_random_color():
    return (random.random(), random.random(), random.random())

# Draw lines and labels representing spawned objects and interceptions on the given axis.
def draw_objects_and_interceptions(fig, ax, spawn_timestamps, interception_timestamps, annotations_df, obstacle_ids):
    object_colors = {}

    # Handle Spawning annotations
    for timestamp, obj_id, _ in zip(
        spawn_timestamps,
        annotations_df.loc[annotations_df['label'].str.startswith('Spawning'), 'id'],
        annotations_df.loc[annotations_df['label'].str.startswith('Spawning'), 'label']
    ):
        obj_type = annotations_df.loc[
            (annotations_df['label'].str.startswith('Spawning')) & (annotations_df['id'] == obj_id),
            'objectType'
        ].values[0] if 'objectType' in annotations_df.columns else None

        if obj_type == 'Obstacle' and obj_id in obstacle_ids:
            draw_object_line(ax, timestamp, obj_id, object_colors, is_interception=False)

    # Handle Interception annotations
    for timestamp, obj_id, _ in zip(
        interception_timestamps,
        annotations_df.loc[annotations_df['label'].str.startswith('Intercepted'), 'id'],
        annotations_df.loc[annotations_df['label'].str.startswith('Intercepted'), 'label']
    ):
        obj_type = annotations_df.loc[
            (annotations_df['label'].str.startswith('Intercepted')) & (annotations_df['id'] == obj_id),
            'objectType'
        ].values[0] if 'objectType' in annotations_df.columns else None

        if obj_type == 'Obstacle' and obj_id in obstacle_ids:
            draw_object_line(ax, timestamp, obj_id, object_colors, is_interception=True)

    return object_colors

# Draw vertical lines on the given axis to represent the start and end of an experiment and scale the x axis to those timestamps
def draw_experiment_lines(ax, start_timestamp, end_timestamp):
    ax.axvline(x=start_timestamp, color='black', linestyle='--')
    ax.axvline(x=end_timestamp, color='black', linestyle='--')
    ax.set_xlim(start_timestamp, end_timestamp)

# Draw a vertical line on the given axis to represent an object and add a text label.
def draw_object_line(ax, timestamp, obj_id, object_colors, is_interception):
    if obj_id not in object_colors:
        object_colors[obj_id] = generate_random_color()

    line_color = object_colors[obj_id]

    # Determine the vertical alignment based on interception or spawning
    vertical_alignment = 'top' if is_interception else 'bottom'  # Adjusted vertical alignment

    # Add a small offset for better visibility
    vertical_position = ax.get_ylim()[0] + 0.02 if vertical_alignment == 'bottom' else ax.get_ylim()[1] - 0.02

    ax.axvline(x=timestamp, color=line_color, linestyle='--', alpha=0.7)
    label_text = f'{"Intercepted" if is_interception else "Spawned"} {int(obj_id)} at {timestamp:.2f}'
    ax.text(
        timestamp, 
        vertical_position,  # Adjusted vertical position
        label_text, 
        rotation=90, 
        verticalalignment=vertical_alignment, 
        horizontalalignment='right', 
        color='black', 
        alpha=1
    )

# Plot regions on the given axis, using colors based on the object_colors dictionary for each object ID.
def plot_observations(ax, looking_at_timestamps, annotations_df, object_colors, fill_threshold=1.0):
    # Initialize variables for tracking close events
    current_obj_id = None
    start_time = None

    # new_legend_handles = {}

    for timestamp in looking_at_timestamps:
        obj_id = annotations_df.loc[annotations_df['time'] == timestamp, 'id'].values[0]

        if obj_id in object_colors:
            color = object_colors[obj_id]

            # Check if it's the same object and within the threshold
            if obj_id == current_obj_id and start_time is not None and timestamp - start_time <= fill_threshold:
                # Fill the region between the previous and current timestamp
                ax.axvspan(start_time, timestamp, color=color, alpha=1, facecolor=color)

            # Update tracking variables for the next iteration
            current_obj_id = obj_id
            start_time = timestamp


# Add annotations to a given plot.
def add_annotations(fig, ax, filepath='annotations.csv', show_observable=False):
    if filepath:
        annotations_df = pd.read_csv(filepath)
        annotations_df = convert_timestamps_to_time(annotations_df, 'timestamp', offset)

        # Filter annotations for 'Spawning' or 'Intercepted' labels and ObjectType 'Obstacle'
        filtered_annotations = annotations_df[
            (annotations_df['label'].isin(['Spawning', 'Intercepted'])) &
            (annotations_df['objectType'] == 'Obstacle')
        ]


        # Identifying different types of annotation to plot on the graph
        spawn_timestamps = filtered_annotations.loc[filtered_annotations['label'] == 'Spawning', 'time'].values
        interception_timestamps = filtered_annotations.loc[filtered_annotations['label'] == 'Intercepted', 'time'].values

        start_timestamp = annotations_df.loc[(annotations_df['label'] == 'Experiment Started'), 'time'].values
        end_timestamp = annotations_df.loc[(annotations_df['label'] == 'Experiment Ended'), 'time'].values

        draw_experiment_lines(ax, start_timestamp, end_timestamp)

        # Extract ObjectType 'Obstacle' and ID for plotting
        obstacle_ids = filtered_annotations.loc[:, 'id'].values

        object_colors = draw_objects_and_interceptions(fig, ax, spawn_timestamps, interception_timestamps, annotations_df, obstacle_ids)
        if show_observable:
            looking_at_timestamps = annotations_df.loc[annotations_df['label'] == 'Looking At', 'time'].values
            plot_observations(ax, looking_at_timestamps, annotations_df, object_colors)

ang_annotation_fig, ax = plt.subplots(figsize=(16, 8))
plot_angular_graph(ang_annotation_fig, ax, gaze_df)
add_annotations(ang_annotation_fig, ax, annotations_filepath, show_observable=False)

ang_annotation_fig_smoothed, ax1 = plt.subplots(figsize=(16, 8))
plot_angular_graph(ang_annotation_fig_smoothed, ax1, gaze_df, source='smoothed_angular_distance')
add_annotations(ang_annotation_fig_smoothed, ax1,annotations_filepath, show_observable=True)

# %% [markdown]
# `plot_experiment` is a uniform function that will use the default paramaters to plot angular distance with identified saccades and smooth pursuit, and annotations. We can choose between smoothed or unsmoothed data, as well as display velocity.

# %%
# Plot a combination of angular distance and saccade-related data for an experiment with corresponding annotations base on if they want to use the smoothed or raw data.
def plot_experiment(fig, ax, df, use_smooth=False, show_velocity=False, show_observable=False):
    if use_smooth:
        sourceDistance = 'smoothed_angular_distance'
        sourceVelocity = 'smoothed_angular_velocity'
    else:
        sourceDistance = 'angular_distance'
        sourceVelocity = 'angular_velocity'

    plot_angular_graph(fig, ax, df, sourceDistance)
    plot_smooth_pursuit_graph(fig, ax, df, sourceVelocity)
    plot_saccade_graph(fig, ax, df, sourceVelocity, show_velocity=show_velocity)
    add_annotations(fig, ax, annotations_filepath, show_observable=show_observable)

experiment, exp_ax = plt.subplots(figsize=(16, 8))
plot_experiment(experiment, exp_ax, gaze_df, use_smooth=True, show_velocity=False, show_observable=True)


