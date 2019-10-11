using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using UnityEngine.Events;

public class KinectDirectionalizer : MonoBehaviour
{
    [Serializable]
    public class HitEvent : UnityEvent<Vector3>{}
  private Vector3 prevDir = Vector3.zero;
  private Vector3 hit = Vector3.zero;
  public bool applyTransform = true;
  public bool invTransform = false;
  public HitEvent onLocalized;

  // Start is called before the first frame update
  void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        Debug.DrawRay(transform.position, prevDir);
    Debug.DrawLine(transform.position, hit);
  }

    public void VecIn(SpacebrewClient.SpacebrewMessage message){
        Debug.Log("got message");
        Debug.Log(message.valueNode);
    SimpleJSON.JSONArray arr = message.valueNode.AsArray;
    //switching from Z up to Unity's Y up
    prevDir.x = arr[0].AsFloat;
    prevDir.z = arr[1].AsFloat;
    prevDir.y = arr[2].AsFloat;
    if (applyTransform)
    {
      if (!invTransform)
      {
        prevDir = transform.rotation * prevDir;
      } else
      {
        prevDir = Quaternion.Inverse(transform.rotation) * prevDir;
      }
    }
    //lets assume sounds happen 1m above the ground
    Plane plane = new Plane(Vector3.up, Vector3.up);
    Ray ray = new Ray(transform.position, prevDir);
    float hitAt = 0;
    if (plane.Raycast(ray, out hitAt)){
      hit = ray.origin + ray.direction * hitAt;
      onLocalized.Invoke(hit);
    }
  }
}
