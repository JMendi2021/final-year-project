using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class VRV_PlayerMovement : MonoBehaviour
{
    [SerializeField] float xUpperBound = 35.0f, xLowerBound = 40.0f;
    void Update()
    {
        // This ensures that the player remains within the upper and lower bounds of the playspace
        if (transform.position.x < xUpperBound)
        {
            transform.position = new Vector3(xUpperBound, transform.position.y, transform.position.z);
        }
        else if (transform.position.x > xLowerBound)
        {
            transform.position = new Vector3(xLowerBound, transform.position.y, transform.position.z);
        }
    }
}
