using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ObstacleMovement : MonoBehaviour
{
    // Start is called before the first frame update
    [SerializeField] public float speed = 10f;
    [SerializeField] float UnityUnitsPerMeter = 1f;
    [SerializeField] float activationXPosition = 25f;
    private CapsuleCollider _capsuleCollider;

    void Start()
    {
        _capsuleCollider = gameObject.GetComponent<CapsuleCollider>();
        _capsuleCollider.enabled = false;
    }
    void Update()
    {
        Move();
        if (transform.position.x > activationXPosition)
        {
            _capsuleCollider.enabled = true;
            Debug.Log("Collider Enabled at x-position: " + transform.position.x);
        }
    }

    // void Update() {
    //     Move();
    // }

    void Move()
    {
        // Convert speed from meters per second to Unity units per second
        float speedInUnityUnitsPerSecond = speed / UnityUnitsPerMeter;
        // Move the object down the lane
        transform.Translate(Vector3.right * speedInUnityUnitsPerSecond * Time.deltaTime);
    }
}
