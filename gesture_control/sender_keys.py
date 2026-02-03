from pynput.keyboard import Controller,Key
import time
keyboard=Controller()
MAP={'FORWARD':'w','BACK':'s','LEFT':'a','RIGHT':'d','UP':Key.space,'DOWN':Key.ctrl}
last=None;lt=0;DB=150
def send_key(g):
    global last,lt
    now=time.time()*1000
    if g==last and now-lt<DB: return
    last=g;lt=now
    if g in MAP:
        k=MAP[g]
        keyboard.press(k);keyboard.release(k)
