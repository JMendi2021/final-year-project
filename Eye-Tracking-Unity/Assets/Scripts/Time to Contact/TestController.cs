using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class TestController : MonoBehaviour
{
    [SerializeField] SegmentController[] segments;
    [SerializeField] float fixedSpeed;
    [SerializeField] float spawnDelay;
    [SerializeField] int numberofObstacles;
    private bool started = false;


    // Start is called before the first frame update
    void Start()
    {
        Debug.Log("Press Space to start");
    }

    void Update()
    {
        if (Input.GetKey(KeyCode.Space) && started == false)
        {
            Debug.Log("Starting...");
            started = true;
            // AllTest();
            RandomTest();
        }
    }
    void ActivateSegment(SegmentController segment)
    {
        segment.objectSpeed = fixedSpeed;
        segment.Spawn();
    }

    void AllTest() // Spawns obstacles on all segments to check if it spawns
    {
        foreach (SegmentController segment in segments)
        {
            ActivateSegment(segment);
        }
    }

    void RandomTest()
    { // Spawns obstacles at random segments up to n times
        StartCoroutine(SpawnRandomObstacles());

    }

    IEnumerator SpawnRandomObstacles()
    {
        for (int i = 0; i < numberofObstacles; i++)
        {
            int index = UnityEngine.Random.Range(0, segments.Length);
            ActivateSegment(segments[index]);
            yield return new WaitForSeconds(spawnDelay);
        }
    }
}


