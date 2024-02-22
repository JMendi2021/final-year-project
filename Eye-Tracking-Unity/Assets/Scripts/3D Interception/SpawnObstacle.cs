using System.Collections;
using System.Collections.Generic;
using System.Numerics;
using UnityEngine;

public class SpawnObstacle : MonoBehaviour
{
    [SerializeField] GameObject[] obstacles;
    [SerializeField] float xRotation;


    public void Spawn(float speed, int id)
    {
        Debug.Log($"Spawning Obstacle {id} at speed {speed}");
        GameObject spawnedObject = Instantiate(obstacles[0], transform.position, UnityEngine.Quaternion.identity);
        Obstacle obstacle = spawnedObject.GetComponent<Obstacle>();
        obstacle.transform.parent = transform;
        obstacle.speed = speed;
        obstacle.id = id;
        
    }


}
