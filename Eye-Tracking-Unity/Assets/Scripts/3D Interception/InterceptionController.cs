
using System;
using System.Collections;
using System.Collections.Generic;
using System.Data.Common;
using PupilLabs;
using UnityEditor;
using UnityEditor.Search;
using UnityEngine;
using UnityEngine.TestTools;
using UnityEngine.TextCore;

public class InterceptionController : MonoBehaviour
{
    // [Header("Experiment Settings")]
    // [SerializeField] String userName;
    // [SerializeField] int userID;

    // Allows the user to add or remove segments if needed.
    [Header("Segment Settings")]
    [SerializeField] Segment[] segments;
    [SerializeField] GameObject segmentsObj;
    [SerializeField] float obstacleSpeed;

    [Header("Spawn Settings")]
    [SerializeField] float spawnDelay;
    [SerializeField] int totalObstacles;
    [SerializeField] bool randomSpeed;
    [SerializeField] float minSpeed;
    [SerializeField] float maxSpeed;


    [Header("Pupil Lab")]
    [SerializeField] bool enablePupilLab = true; // This is to test the application without the eye-trackers enabled.
    [SerializeField] GameObject gazeTracker;


    // public int _numOfInterception = 0;
    // public int _numbOfButtonPressed = 0;
    private bool _running = false;
    private int _spawnedObstacles = 0;

    // Pupil Lab Private Vars
    private RecordingController _pupilRecord;
    private AnnotationPublisher _pupilAnnotate;

    private bool showSegments = true;


    private void Start()
    {

        if (!enablePupilLab)
        {
            gazeTracker.SetActive(false);
            Debug.Log("Pupil Lab has been disabled.");
        }
        else
        {
            gazeTracker.SetActive(true);
            if (gazeTracker == null)
            {
                Debug.LogWarning("Gaze Tracker object not found, please attach gameObject to script");
            }
            else
            {
                _pupilRecord = gazeTracker.GetComponent<RecordingController>();
                _pupilAnnotate = gazeTracker.GetComponent<AnnotationPublisher>();
                Debug.Log("Pupil Lab has been enabled.");

            }
        }
    }


    // The experiment should begin once everything has been calibrated and the enter key has been pressed.
    private void Update()
    {
        // When M is pressed, this starts the experiment as long as the tracker is calibrated and it is not running an existing experiment
        if (Input.GetKeyDown(KeyCode.M))
        {
            if (!_running)
            {
                if (showSegments)
                {
                    Debug.Log("Beginning Experiment");
                    RunRandom();
                }
                else
                {
                    Debug.Log("Please ensure the environment is not hidden.");
                }
            }
            else
            {
                Debug.Log("Please wait until the current experiment is over.");
            }
        }
        else if (Input.GetKeyDown(KeyCode.H))
        {
            if (showSegments)
            {
                Debug.Log("Hiding Experiment");
                segmentsObj.SetActive(false);
                showSegments = false;

            }
            else
            {
                Debug.Log("Showing Experiment");
                segmentsObj.SetActive(true);
                showSegments = true;
            }
        }
    }

    // This will cause the obstacles to spawn at a given rate up to a total number of times
    IEnumerator BeginExperiment()
    {
        // if (_pupilRecord != null)
        // {
        //     annotationPublisher.SendAnnotation("Recording started");
        //     Debug.Log("Pupil Capture is now recording");
        //     _pupilRecord.StartRecording();
        // }

        if (enablePupilLab)
        {
            Debug.Log("Pupil Capture is now recording");
            _pupilRecord.StartRecording();
            yield return new WaitForSeconds(2f);
            _pupilAnnotate.SendAnnotation("Experiment Started");
        }

        while (_spawnedObstacles < totalObstacles)
        {
            float speed = obstacleSpeed;
            if (randomSpeed)
            {
                speed = (int)UnityEngine.Random.Range(minSpeed, maxSpeed);
            }
            _spawnedObstacles++;
            ChooseRandomSegment().ActivateSpawner(speed, _spawnedObstacles);

            if (enablePupilLab)
            {
                Dictionary<string, object> Spawn = new Dictionary<string, object>();
                Spawn["objectType"] = "Obstacle";
                Spawn["id"] = _spawnedObstacles;

                _pupilAnnotate.SendAnnotation("Spawning", customData: Spawn);
            }
            yield return new WaitForSeconds(spawnDelay);
        }

        Debug.Log("Spawning Finished.");

        yield return new WaitForSeconds(5f);

        if (enablePupilLab)
        {
            _pupilAnnotate.SendAnnotation("Experiment Ended");

            Debug.Log("Pupil Capture is no longer recording");
            yield return new WaitForSeconds(2);
            _pupilRecord.StopRecording();
        }

        Debug.Log("Experiment has finished, resetting.");

        // Resets the experiment data to allow new run through
        _spawnedObstacles = 0;
        _running = false;
    }

    // This runs the randomised test, segments are activated at random.
    private void RunRandom()
    {
        _running = true;
        StartCoroutine(BeginExperiment());
    }

    // This randomises the spawning of Obstacles using the different segments
    private Segment ChooseRandomSegment()
    {
        if (segments != null && segments.Length > 0)
        {
            int randomIndex = UnityEngine.Random.Range(0, segments.Length);
            return segments[randomIndex];
        }
        else
        {
            Debug.Log("Please ensure that the Segment List is populated.");
            return null;
        }
    }

    // Handles Pupil Core Recording
    private void RecordBeginEnd()
    {
        if (_pupilRecord != null)
        {
            if (!_pupilRecord.IsRecording)
            {

                Debug.Log("Pupil Capture is now recording");
                _pupilRecord.StartRecording();
                _pupilAnnotate.SendAnnotation("Recording started");
            }
            else
            {
                _pupilAnnotate.SendAnnotation("Recording Ended");
                Debug.Log("Pupil Capture is no longer recording");
                _pupilRecord.StopRecording();
            }
        }
    }

    // private void ReturnResults()
    // {
    //     float accuracy = _numOfInterception / _numbOfButtonPressed;
    //     Debug.Log($"The user has intercepted {_numOfInterception} out of {totalObstacles} \n with {accuracy.ToString("F2")}");
    // }

    public void Intercepted(int id, string obj)
    {
        Debug.Log("Obstacle intercepted");
        if (_pupilAnnotate != null)
        {
            Dictionary<string, object> Intercept = new Dictionary<string, object>();
            Intercept["objectType"] = obj;
            Intercept["id"] = id;

            _pupilAnnotate.SendAnnotation("Intercepted", customData: Intercept);
        }
    }

    // This function returns that the person is currently observing:
    // 1. Lane/Marker
    // 2. Target

    public void LookingAt(int id, string obj)
    {
        if (enablePupilLab)
        {
            Dictionary<string, object> LookingAt = new Dictionary<string, object>();
            LookingAt["objectType"] = obj;
            LookingAt["id"] = id;

            _pupilAnnotate.SendAnnotation("Looking At", customData: LookingAt);
        }
    }

    public void LookingAt(int id, string obj, int segm_id)
    {
        if (enablePupilLab)
        {
            Dictionary<string, object> LookingAt = new Dictionary<string, object>();
            LookingAt["objectType"] = obj;
            LookingAt["id"] = id;
            LookingAt["segmentLocation"] = segm_id;

            _pupilAnnotate.SendAnnotation("Looking At", customData: LookingAt);
        }
    }
}
