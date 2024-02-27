using System.Collections;
using System.Collections.Generic;
using System.Drawing.Design;
using System.Security.Cryptography.X509Certificates;
using PupilLabs;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.Controls;
using UnityEngine.XR.Interaction.Toolkit;

public class Obstacle : MonoBehaviour
{

    [SerializeField] public float speed;
    [SerializeField] InputActionReference triggerL;
    [SerializeField] InputActionReference triggerR;
    [SerializeField] Material interceptedMaterial;
    [SerializeField] Renderer targetRenderer;

    public int id;

    [Header("Interception Zone")]
    // [SerializeField] InterceptionController ic;

    [SerializeField] float maxSegmentDistance = -2.0f;
    [SerializeField] float minMarkerDistance = 2.5f;
    [SerializeField] float maxMarkerDistance = 1.0f;

    private bool _canMove = true;
    private InterceptionController ic;
    private string _objectType = "Obstacle";


    void Start()
    {
        ic = FindObjectOfType<InterceptionController>();
    }

    // Update is called once per frame
    void Update()
    {
        if (_canMove)
        {
            transform.Translate(-1 * Vector3.forward * speed * Time.deltaTime); // The obstacle should move towards the player
            OnMarker();
            PassBoundry();
        }
    }

    // This performs the logic if an object is within the Interception Zone and the Space or Left Controller Trigger is pressed.
    private void OnMarker()
    {
        if (Input.GetKeyDown(KeyCode.Space) || triggerL.action.triggered || triggerR.action.triggered)
        {
            Intercepted();
        }
    }

    // Checks if the object exceeds pass the segment boundry
    private void PassBoundry()
    {
        if (transform.position.z < maxSegmentDistance)
        {
            Destroy(gameObject);
        }
    }

    private void Intercepted()
    {
        Debug.Log("Intercept Button Pressed!");
        if (transform.position.z > maxMarkerDistance && transform.position.z < minMarkerDistance)
        {
            targetRenderer.material = interceptedMaterial;
            _canMove = false;
            ic.Intercepted(id, _objectType);
            StartCoroutine(DelayDestroy());
        }
    }

    IEnumerator DelayDestroy()
    {
        yield return new WaitForSeconds(1.0f);
        Destroy(gameObject);
    }

    private void OnObserved()
    {
        Debug.Log($"{_objectType} {id} is observed");
        ic.LookingAt(id, _objectType);
    }

    // private void OnCollisionEnter(Collision other)
    // {
    //     Debug.Log($"{_objectType} {id} is observed");
    //     ic.LookingAt(id, _objectType);
    // }
}

