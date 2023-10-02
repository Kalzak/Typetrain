import json
import time
from pynput import keyboard
import os
import socket
import sys
import termios

HOST = '127.0.0.1'
PORT = 12345

key_timestamp = None
start_timestamp = None
keystrokes = []
current_key = None
sentence = "Hello there"
current_sentence = ""
ctrl_pressed = False
done = False

def on_key_press(key):
    global current_key, key_timestamp, current_sentence, ctrl_pressed, start_timestamp

    #os.system("clear")
    #print(sentence)

    current_time = time.time() * 1000
    timegap = 0
    if key_timestamp is not None:
        timegap = current_time - key_timestamp
    key_timestamp = current_time
    print("updated p: ", key_timestamp)

    if start_timestamp is None:
        start_timestamp = time.time() * 1000

    try:
        current_key = key.char
        current_sentence = current_sentence + current_key

        if ctrl_pressed == True and current_key == 'c':
            exit()
    except AttributeError:
        current_key = key
        if key == keyboard.Key.space:
            current_sentence = current_sentence + " "

        if key == keyboard.Key.backspace:
            current_sentence = current_sentence[:-1]

        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            ctrl_pressed = True
            

    print(current_sentence)

    keystrokes.append({"key": str(current_key), "action": "down", "time": timegap})

def on_key_release(key):
    global current_key, ctrl_pressed, key_timestamp

    current_time = time.time() * 1000
    timegap = current_time - key_timestamp
    key_timestamp = current_time
    print(key)
    
    

    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        ctrl_pressed = False

    keystrokes.append({"key": str(current_key), "action": "up", "time": timegap})
        
        

    if sentence == current_sentence:
        return False

def main():
    global current_sentence, keystrokes, start_timestamp, done

    
    while True:
    

        #os.system("clear")
        #print(sentence)
        print()

        with keyboard.Listener(on_press=on_key_press, on_release=on_key_release, suppress=True) as listener:
            listener.join()
        

        data = {
            "sentence": sentence,
            "keystrokes": keystrokes,
            "total_time": (time.time() * 1000) - start_timestamp
        }

        time.sleep(1)


        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))

        json_data = json.dumps(data)
        client_socket.send(json_data.encode('utf-8'))
        client_socket.close()


        keystrokes = []
        current_sentence = ""
        key_timestamp = None
        print("timestamp reset")
        start_timestamp = None





if __name__ == "__main__":
    main()