using UnityEngine;using System.Net;using System.Net.Sockets;using System.Text;using System.Threading;using System;
public class GestureUDPListener:MonoBehaviour{
 UdpClient client;Thread t;public int port=5005;
 volatile string cmd="";object lk=new object();
 void Start(){t=new Thread(Recv);t.IsBackground=true;t.Start();}
 void Recv(){
  client=new UdpClient(port);
  while(true){
   try{
    IPEndPoint ep=new IPEndPoint(IPAddress.Any,port);
    var d=client.Receive(ref ep);
    string s=Encoding.UTF8.GetString(d);
    string g=Parse(s);
    if(g!=""){lock(lk)cmd=g;}
   }catch(Exception){}
  }
 }
 string Parse(string j){
  int i=j.IndexOf(":"); if(i<0) return "";
  return j.Substring(i+1).Trim().Trim('"','{','}',' ');
 }
 public bool HasCommand(){return cmd!="" ;}
 public string GetCommand(){lock(lk)return cmd;}
 void OnApplicationQuit(){t.Abort();client.Close();}
}
