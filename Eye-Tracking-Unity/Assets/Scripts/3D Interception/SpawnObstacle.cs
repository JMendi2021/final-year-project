using System.Collections;
using System.Collections.Generic;
using System.Numerics;
using UnityEngine;

public class SpawnObstacle : MonoBehaviour
{
    [SerializeField] GameObject[] obstacles;
    [SerializeField] float xRotation;


    public void Spawn(float speed, int id, int segm_id)
    {
        Debug.Log($"Spawning Obstacle {id} at speed {speed} on segment {segm_id}");
        GameObject spawnedObject = Instantiate(obstacles[0], transform.position, UnityEngine.Quaternion.identity);
        Obstacle obstacle = spawnedObject.GetComponent<Obstacle>();
        obstacle.transform.parent = transform;
        obstacle.speed = speed;
        obstacle.id = id;
        obstacle.segm_id = segm_id;
    }


}
