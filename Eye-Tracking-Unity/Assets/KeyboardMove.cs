using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class KeyboardMove : MonoBehaviour
{
    // This script is to allow movement using keyboard
    [SerializeField] float speed = 5.0f;

    // Update is called once per frame
    void Update()
    {
        float horizontalInput = Input.GetAxis("Horizontal");
        float verticalInput = Input.GetAxis("Vertical");

        Vector3 movement = new Vector3(horizontalInput, 0f, verticalInput) * speed * Time.deltaTime;
        transform.Translate(movement);
    }
}
