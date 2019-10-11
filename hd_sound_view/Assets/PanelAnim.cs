using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using DG.Tweening;

public class PanelAnim : MonoBehaviour
{
  public float minTime = .1f;
  public float maxTime = 5;
  public float maxDistance = 10;
  public float minDistance = 1;
  public Material[] materials;
  private int index = 0;
  // Start is called before the first frame update
  void Start()
  {

  }

  // Update is called once per frame
  void Update()
  {

  }

  public void Trigger(Vector3 source)
  {
    if (materials == null || materials.Length == 0){
      //nothing to do here;
      Debug.LogWarning("[PanelAnim.Trigger] no materials configured, aborting.");
      return;
    }
    if (index >= materials.Length){
      //wrap around
      index = 0;
    }
    Material m = materials[index];
    m.SetVector("_Position", source);
    m.SetFloat("_Distance", minDistance);
    m.DOFloat(maxDistance, "_Distance", Random.Range(minTime, maxTime)).SetEase(Ease.Linear);
    index++;
  }
}
