using UnityEngine;using UnityEngine.UI;
public class WebcamBackground:MonoBehaviour{
 public RawImage rawImage;WebCamTexture tex;
 void Start(){
  if(WebCamTexture.devices.Length==0)return;
  tex=new WebCamTexture();tex.Play();
  if(rawImage!=null){rawImage.texture=tex;rawImage.material.mainTexture=tex;}
 }
 void OnDisable(){if(tex!=null)tex.Stop();}
}
