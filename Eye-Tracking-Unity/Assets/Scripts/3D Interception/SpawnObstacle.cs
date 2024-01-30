using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SpawnObstacle : MonoBehaviour
{
    [SerializeField] GameObject[] obstacles;

    public void Spawn(float speed)
    {
        Debug.Log($"Spawning Obstacle at speed {speed}");
        GameObject spawnedObject = Instantiate(obstacles[0], transform.position, Quaternion.identity);
        Obstacle obstacle = spawnedObject.GetComponent<Obstacle>();
        obstacle.transform.parent = transform;
        obstacle.speed = speed;
    }


}
