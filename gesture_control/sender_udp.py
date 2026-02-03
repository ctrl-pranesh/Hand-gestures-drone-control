import socket,json
IP="127.0.0.1";PORT=5005
sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
def send_udp(g):
    sock.sendto(json.dumps({"gesture":g}).encode(),(IP,PORT))
