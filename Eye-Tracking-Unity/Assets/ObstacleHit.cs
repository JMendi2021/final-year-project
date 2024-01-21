using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ObstacleHit : MonoBehaviour
{
    [SerializeField] Material targetGreenMaterial;
    [SerializeField] Material targetRedMaterial;
    [SerializeField] GameObject center;
    private MeshRenderer childRenderer;


    private void Start()
    {
        childRenderer = center.GetComponent<MeshRenderer>();
    }

    private void Update() {
        ChangeMaterial(targetRedMaterial); // Should remain red when it is not observed
    }

    // When gaze hits the target, it should turn green.
    private void OnCollisionEnter(Collision other)
    {
        if (other.gameObject.CompareTag("Hit"))
        {
            ChangeMaterial(targetGreenMaterial);
        }
    }

    private void ChangeMaterial(Material newMaterial)
    {
        childRenderer.material = newMaterial;
    }
}
