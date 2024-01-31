using System;
using System.Collections;
using System.Collections.Generic;
using PupilLabs;
using UnityEditor.Search;
using UnityEngine;
using UnityEngine.TestTools;

public class InterceptionController : MonoBehaviour
{
    // [Header("Experiment Settings")]
    // [SerializeField] String userName;
    // [SerializeField] int userID;

    // Allows the user to add or remove segments if needed.
    [Header("Segment Settings")]
    [SerializeField] Segment[] segments;
    [SerializeField] float obstacleSpeed;

    [Header("Spawn Settings")]
    [SerializeField] float spawnDelay;
    [SerializeField] int totalObstacles;

    [Header("Pupil Lab")]
    [SerializeField] bool enablePupilLab = true; // This is to test the application without the eye-trackers enabled.

    [SerializeField] GameObject gazeTracker;




    private bool _running = false;
    // private Boolean _calibrated = true;
    private int _spawnedObstacles = 0;
    private RecordingController pupilRecord;


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
                pupilRecord = gazeTracker.GetComponent<RecordingController>();
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
                Debug.Log("Beginning Experiment");
                if (pupilRecord != null)
                {
                    pupilRecord.StartRecording();
                }

                RunRandom();
            }
            else
            {
                Debug.Log("Please wait until the current experiment is over.");
            }
            // Call to get ready
        }
    }

    // This will cause the obstacles to spawn at a given rate up to a total number of times
    IEnumerator BeginExperiment()
    {
        while (_spawnedObstacles < totalObstacles)
        {
            ChooseRandomSegment().ActivateSpawner(obstacleSpeed);
            _spawnedObstacles++;
            yield return new WaitForSeconds(spawnDelay);
        }

        Debug.Log("Spawning Finished.");

        yield return new WaitForSeconds(10f);

        Debug.Log("Experiment has finished, resetting.");

        if (pupilRecord != null)
        {
            pupilRecord.StopRecording();
        }

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

}
