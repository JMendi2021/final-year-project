using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SegmentController : MonoBehaviour
{
    [SerializeField] public float objectSpeed;
    [SerializeField] GameObject[] modelPrefabs;
    [SerializeField] GameObject marker;
    [SerializeField] GameObject player;
    [SerializeField] public bool isRandomSpeed = false;
    [SerializeField] public float minSpeed;
    [SerializeField] public float maxSpeed;

    private GameObject spawnedObject;

    void Update()
    {

    }


    // This is responsible for when the user gazes at either Marker or Obstacle in a specific order
    void DetectGaze()
    {

    }

    // Depending on the Time-To-Contact Controller, this spawns the approaching obstacle with a random mesh
    public void Spawn()
    {
        if (spawnedObject == null)
        {
            int index = Random.Range(0, modelPrefabs.Length);
            spawnedObject = Instantiate(modelPrefabs[index], transform.position, Quaternion.identity);
            // spawnedObject.transform.Rotate(Vector3.up, 90.0f);
            ObstacleMovement obstacle = spawnedObject.GetComponent<ObstacleMovement>();
            obstacle.speed = objectSpeed;
        }

    }
}
