using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TestController : MonoBehaviour
{
    [SerializeField] SegmentController[] segments;
    [SerializeField] float speed; 
    [SerializeField] bool isRandom;


    // Start is called before the first frame update
    void Start()
    {
        segments[0].Spawn();
        segments[1].Spawn();
    }


}
