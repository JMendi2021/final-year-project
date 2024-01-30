using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Segment : MonoBehaviour
{
    [Header("Spawn Settings")]
    [SerializeField] GameObject spawner;

    private SpawnObstacle _spawnObstacle;

    private void Start() {
        _spawnObstacle = spawner.GetComponent<SpawnObstacle>();
        if (_spawnObstacle == null) {
            Debug.LogError("SpawnObstacle Script is not attached to Spawn GameObject");
        }
    }
    public void ActivateSpawner(float speed) {
        _spawnObstacle.Spawn(speed);
    }
}
