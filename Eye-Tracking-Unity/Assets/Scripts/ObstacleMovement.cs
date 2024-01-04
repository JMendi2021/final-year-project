using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ObstacleMovement : MonoBehaviour
{
    // Start is called before the first frame update
    [SerializeField] public float speed;
    private const float UnityUnitsPerMeter = 1f;

    void Update()
    {
        Move();

        // Destroys the object once it passes the playzone lower bounds
        if (gameObject.transform.position.x > 40)
        {
            Destroy(gameObject);
        }
    }

    void Move()
    {
        // Convert speed from meters per second to Unity units per second
        float speedInUnityUnitsPerSecond = speed / UnityUnitsPerMeter;
        // Move the object down the lane
        transform.Translate(Vector3.forward * speedInUnityUnitsPerSecond * Time.deltaTime);
    }
}
