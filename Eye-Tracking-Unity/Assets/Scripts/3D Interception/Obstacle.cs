using System.Collections;
using System.Collections.Generic;
using PupilLabs;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.Controls;
using UnityEngine.XR.Interaction.Toolkit;

public class Obstacle : MonoBehaviour
{

    [SerializeField] public float speed;
    [SerializeField] InputActionReference trigger;
    private float _maxSegmentDistance = -2.0f;
    private float _minMarkerDistance = 2.1f;
    private float _maxMarkerDistance = 1.0f;


    // Update is called once per frame
    void Update()
    {
        transform.Translate(-1 * Vector3.forward * speed * Time.deltaTime); // The obstacle should move towards the player
        OnMarker();
        PassBoundry();
    }

    // This performs the logic if an object is within the Interception Zone and the Space or Left Controller Trigger is pressed.
    private void OnMarker()
    {
        if (Input.GetKeyDown(KeyCode.Space) || trigger.action.triggered)
        {
            Debug.Log("Intercept Button Pressed!");
            if (transform.position.z > _maxMarkerDistance && transform.position.z < _minMarkerDistance)
            {
                Debug.Log("Object intercepted!");
                Destroy(gameObject);
            }
        }


    }

    // Checks if the object exceeds pass the segment boundry
    private void PassBoundry()
    {
        if (transform.position.z < _maxSegmentDistance)
        {
            Destroy(gameObject);
        }
    }


}
