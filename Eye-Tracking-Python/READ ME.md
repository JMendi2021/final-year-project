# Using the Gaze Analyser and Pupillometry Scripts
To begin analysing the data collected from the Unity Project which has been recorded by Pupil Core, you will need to make sure to have Pupil Player installed for this:
1. Open Pupil Player and drag the recorded file (usually found within the Unity Project directory and within the day it has been recorded and formatted similarily to '000', '001', etc.) into the window. It will take a moment to process the recording.
2. Once it has processed, a new window which will open a viewable recording of the experiment. Feel free to watch and make reference throughout.
3. Near the top right, select `Plugin Manager` and make sure the following plugins are enabled: `Annotation Player`, `Fixation Detector`, `Raw Data Exporter`. These will be used for analysis and you can modify the parameters as needed using the options below the Plugin Mananger
    - For `Raw Data Exporter`,  I would recommend turning off `Include Low Confidence Data` as it removes points that exceeds as a normal outliers. These are usually when the trackers has failed to track correctly.
    - For `Fixation`, you can determine how long a fixation will last. I have it as `200` and `300` for minimum and maximum.
4. Now, on the left side, there is an option to export the recording. This will generate a number of `.csv` files that you will use which are all found under `[Recording Folder] > exports` which, similarily, should be using the similar format as the recording names (000, 001, etc.). The greatest value is the latest export/recording.
5. Once you are inside the export file, copy and paste the following files: `annotations.csv`, `gaze_position.csv`, `fixations.csv`, and `pupil_position.csv` into the `source` folder of the project file.
    - `pupil_position.csv` isn't required but it can be used with the pupillometry notebook.
    - Make sure that any past data inside the source has been removed or stored somewhere else
4. Within the previous directory of export, there is a file called `info.player.json`. Copy that file into `source` as well.

That is all the files that you will need to run the notebooks.

## Using Gaze Analyser
This notebook will take in `gaze_positions`, `fixations`, and `info.player` and create several csv files and JSON that will contain the necessary data that can be accessed to see what kind of data has been processed from the raw data. This will also produce the graph at the same time.
- It will contain records are a specific eye movements (fixations, smooth pursuits, and saccades) base on thresholds provided to each function.
    - These functions can be given adjusted parameters different to the default

It will also calculate related fields such as `angular distance`, and `angular velocity` which are used to identify movement types.

## Using Gaze Visualiser
Similar to the analyser, this notebook looks to create an interactive graph using the exported csv and json files. This should be able to provide researchers where specific movements, or events, has occured throughout the experiment. This allows to use past data exported by the analyser if need to be.

You can use `plot_data` to display the group and specify which movements you would want to see. Followed by that function, you can use `add_annotations` with the filepath and offset to identify the following:
1. Colour Coded Objects - Each object are given a specific colour to identify events related to them
2. Regions of Observation - A region using specific colours to signify what the user is looking at.
3. Spawning and Intercept Lines - These lines signifies when an object has spawned, and has been intercepted. These are also coloured by their corresponding object colours.