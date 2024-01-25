using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
public class ObstacleHit : MonoBehaviour
{
    [SerializeField] Material targetGreenMaterial;
    [SerializeField] Material targetRedMaterial;
    [SerializeField] GameObject center;
    private Renderer childRenderer;


    private void Start()
    {
        childRenderer = center.GetComponent<Renderer>();
    }

    private void Update()
    {
        ChangeMaterial(targetRedMaterial); // Should remain red when it is not observed
        // Physics.Raycast(rayOrigin.gameObject.transform.position, )
    }

    // When gaze hits the target, it should turn green.
    private void OnSphereCastHit()
    {
        Debug.Log("Sphere hit, changing colour.");
        ChangeMaterial(targetGreenMaterial);
    }

    private void ChangeMaterial(Material newMaterial)
    {
        childRenderer.material = newMaterial;
    }
}
