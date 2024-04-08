# Final Year Project

- **Name**: Jhundon De Leon Mendi
- **Student ID**: 2272652
- **Course**: BSc Computer Science
- **Module Credits**: 40
- **Supervisor**: Sang-Hoon Yeo (s.yeo@bham.ac.uk - Sports, Exercise and Rehabilitation)

---

Due to the GitLab push limit of 400mb, a [GitHub repository](https://github.com/JMendi2021/final-year-project) has been made to record history and code access.

There are a total of **four executable files** in this project, each linking to their corresponding section to how to run them, these are:

1. [Unity Experiment - 3D/2D Object Interception with Eye Tracking](#3d2d-object-interception-with-eye-tracking)
2. [Gaze Analyser](#using-gaze-analyser) (Jupyter Notebook)
3. [Gaze Visualiser](#using-gaze-visualiser) (Jupyter Notebook)
4. [Pupillometry](#using-pupillometry) (Jupyter Notebook)

Before using the Jupyter Notebooks, you will need to [process the recording](#using-pupil-player) and the following libraries installed using the commands
- `pip install pandas`
- `pip install matplotlib`
- `pip install numpy`

## 3D/2D Object Interception with Eye Tracking
To run this experiment, with Pupil Core, you will require the following:
1. HTC Vive 2016 Headset 
2. Pupil Lab's HTC Vive Binocular Addon (SteamVR required) 
3. Unity 2022.3.13f1 (`hmd-eyes` should already be downloaded within)

Once you have the HTC Vive headset setup, SteamVR running correctly with OpenXR set to default, as well as Pupil Capture running:
1. Open the `Eye-Tracking-Unity` file within the Unity Editor and this should open the scene.
2. Under the Project, you can find the scenes within the `Assets/Scenes` directory and press either the 2D or 3D scene depending on the requirement.
3. The Controller can interact with the `Interception Controller` Game Object within the `INTERCEPTION TEST` section in the Hierarchy view to view and modify the following under the Spawn Settings:
    - `Spawn Delay` - The rate object spawns between each other
    - `Total Obstacles` - Total number of objects in the experiment
    - Enable `Random Speed` - Set a range from `Min Speed` and `Max Speed`
    - `Enable Pupil Lab` - If using another eye-tracking system or need to run the scene without the eye-tracking enabled.
4. To start the scene, press the `Play` option at the top of the editor and check if the project is running through the headset.

When either 2D/3D experiment scene is running, you may need to calibrate the headset through the Pupil Capture before running the Unity Experiment:
1. In both camera view of the eyes, ask the participant to rotate their eyes in a full circle until a blue circle forms confidently around the eyes
2. View one of the camera feeds and do the following:
    1. Go into the settings (Gear Icon) to switch the view into `ROI` and adjust the blue square around the eyes
    2. Go back into setting and switch to `Algorithm View` and go into `Pye3D Detector` (under the gear icon).
    3. Adjust the Pupil Intensity Range so that the yellow area focuses mainly on the 
    4. Adjust the `Pupil Min` and `Pupil Max` so that the moving circle that appears remains between the two red circles.
    5. Repeat for the other eye
3. Once defining the parameters in Pupil Capture, you will now need to calibrate the headset in the Unity Scene.
    1. Hide the experiment by pressing `H`
    2. Display the Calibration Markers by pressing `P` and notify the user that these will appear in the order starting from the center, right, top right, top left, left, bottom left, and finally bottom right. Each side will have 3 markers which mean there will be 21 markers in total.
    3. Press `P` again to hide the markers and, once ready, press `C` to begin calibration.
    4. Once calibration is finish, display the markers with `P` and ask the participant to view the markers indicated by the controller.
    5. Observe the tracking through the Pupil Capture to check if gaze is fixed around those points, and repeat the calibration again if necessary.

Once the calibration is all set, press `H` to show the experiment, and the experiment is run as followed:
1. Press `M` to begin the experiment.
2. The objects will begin to appear a few second when `M` is pressed and the Pupil Capture should start recording.
3. The participant will need to press the `Space` to use the `Front Trigger` on either controller when the object appears over the interception area.
    - Remember to ask to keep their head as still as possible.
4. Once the experiment is finished, no more object should appear and indicated in the console.
    - The recording should end and found in the parent directory of `Asset` as the current date.
        - You will find the files appear in the order of when they are recorded (acending order) within.

You can repeat the experiment without re-running the scene by pressing `M` again. Otherwise, you can now move onto processing the raw data.

## Using Pupil Player

To begin analysing the data collected from the Unity Project which has been recorded by Pupil Core, you will need to make sure to have Pupil Player installed for this:
1. Open Pupil Player and drag the recorded file (usually found within the Unity Project directory and within the day it has been recorded and formatted similarily to '000', '001', etc.) into the window. It will take a moment to process the recording.
2. Once it has processed, a new window which will open a viewable recording of the experiment. Feel free to watch and make reference throughout.
3. Near the top right, select `Plugin Manager` and make sure the following plugins are enabled: `Annotation Player`, `Fixation Detector`, `Raw Data Exporter`. These will be used for analysis and you can modify the parameters as needed using the options below the Plugin Mananger
    - For `Raw Data Exporter`,  I would recommend turning off `Include Low Confidence Data` as it removes points that exceeds as a normal outliers. These are usually when the trackers has failed to track correctly.
    - For `Fixation`, you can determine how long a fixation will last. I have it as `200` and `300` for minimum and maximum.
4. Now, on the left side, there is an option to export the recording. This will generate a number of `.csv` files that you will use which are all found under `[Recording Folder] > exports` which, similarily, should be using the similar format as the recording names (000, 001, etc.). The greatest value is the latest export/recording.
5. Once you are inside the export file, copy and paste the following files: `annotations.csv`, `gaze_position.csv`, `fixations.csv`, and `pupil_position.csv` into the `experiment_source` folder of the project file.
    - `pupil_position.csv` isn't required but it can be used with the pupillometry notebook.
    - Make sure that any past data inside the source has been removed or stored somewhere else
4. Within the previous directory of export, there is a file called `info.player.json`. Copy that file into `experiment_source` as well.

That is all the files that you will need to run the `Gaze Analyser` notebook.

## Using Gaze Analyser
Once you have these files within the source file (you can find examples in `2D` or `3D` directory), you can run the notebook entirely.
- In most cases, this is where you will need to modify the values within the function calls to fit the participant and classify the movements as best as possible.


This notebook will take in `gaze_positions`, `fixations`, `annotations`,  and `info.player` and create several csv files and JSON that will contain the necessary data that can be accessed to see what kind of data has been processed from the raw data in the `analysed_output` directory. This will also produce the graph at the same time.
- It will contain records are a specific eye movements (fixations, smooth pursuits, and saccades) base on thresholds provided to each function.
    - These functions can be given adjusted parameters different to the default
- It will also output the Time-To-Contact estimation as a CSV file and display a graph that can be enabled/disabled within the notebook by adding/removing the function call at the bottom
- Note that it will overwrite whatever already exists in the directory.

It will also calculate related fields such as `angular distance`, and `angular velocity` which are used to identify movement types.

## Using Gaze Visualiser
Similar to the analyser, this notebook looks to create an interactive graph using the exported CSV and JSON files. This should be able to provide researchers where specific movements, or events, has occured throughout the experiment. This allows to use past data exported by the analyser if need to be.

You can use `plot_data` to display the group and specify which movements you would want to see. Followed by that function, you can use `add_annotations` with the filepath and offset to identify the following:
1. Colour Coded Objects - Each object are given a specific colour to identify events related to them
2. Regions of Observation - A region using specific colours to signify what the user is looking at.
3. Spawning and Intercept Lines - These lines signifies when an object has spawned, and has been intercepted. These are also coloured by their corresponding object colours.

To run this, you will simply copy and paste all of the exported data from the analyser and into the `visualiser_source` directory and run the entire script. This should produce the same graph as within the Gaze Analyser notebook.
- You can enable or disable the annotations at the end of the notebook by removing/adding the function call.

## Using Pupillometry
Similarily to the Gaze Analyser, this notebook uses `pupil_positions`, `annotations`, and `info.player` to plot a graph that represents the eye diameter of each eye. You should have these files already within `experiment_source` directory, and you can simply run the notebook as a whole.
- This should display the graph.
- You can enable or disable the annotations at the end of the notebook by removing/adding the function call
- TTC graph can be enabled/disabled within the notebook by adding/removing the function call at the bottom of the notebook
