using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Segment : MonoBehaviour
{
    [Header("Spawn Settings")]
    [SerializeField] GameObject spawner;
    [SerializeField] int segmentID;

    private InterceptionController ic;
    // private string _objectType = "Segment";

    private SpawnObstacle _spawnObstacle;

    private void Start()
    {
        _spawnObstacle = spawner.GetComponent<SpawnObstacle>();
        // ic = FindObjectOfType<InterceptionController>();
        if (_spawnObstacle == null)
        {
            Debug.LogError("SpawnObstacle Script is not attached to Spawn GameObject");
        }
    }
    public void ActivateSpawner(float speed, int id)
    {
        _spawnObstacle.Spawn(speed, id, segmentID);
    }

//     private void OnObserved()
//     {
//         Debug.Log($"{_objectType} {segmentID} is observed");
//         ic.LookingAt(segmentID, _objectType);
//     }
}
