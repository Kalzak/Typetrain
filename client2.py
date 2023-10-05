from pynput import keyboard
import socket
import json
import time

HOST = '127.0.0.1'
PORT = 12346

# Networking stuff
client_socket = None

# Typing stuff
keystrokes = []
ctrl_pressed = False
typed_sentence = ""
target_sentence = "Hello there"
sentence_start_time = None

def on_key_press(key):
    global ctrl_pressed, typed_sentence, sentence_start_time

    if sentence_start_time is None:
        sentence_start_time = time.time() * 1000

    key_pressed_string = ""

    try:

        key_pressed_string = key.char

        if key.char == 'c' and ctrl_pressed == True:
            return False

        typed_sentence = typed_sentence + key_pressed_string

    except AttributeError:

        key_pressed_string = str(key)

        if key == keyboard.Key.ctrl_l:
            ctrl_pressed = True

        if key == keyboard.Key.space:
            typed_sentence = typed_sentence + " "

        if key == keyboard.Key.backspace:
            typed_sentence = typed_sentence[:-1]

    keypress_time = (time.time() * 1000) - sentence_start_time

    if keypress_time < 1:
        keypress_time = 0

    keystrokes.append({"key": key_pressed_string, "action": "down", "time": keypress_time})
    #print(key_pressed_string)
    print(typed_sentence)


def on_key_release(key):


    global ctrl_pressed, keystrokes, typed_sentence, sentence_start_time

    key_pressed_string = ""

    if key == keyboard.Key.caps_lock:
        key = keyboard.Key.shift

    if key == keyboard.Key.ctrl_l:
        ctrl_pressed = False

    try:

        key_pressed_string = str(key.char)

    except AttributeError:

        key_pressed_string = str(key)

    try:
        keypress_time = (time.time() * 1000) - sentence_start_time
    except: 
        keypress_time = 0

    keystrokes.append({"key": key_pressed_string, "action": "up", "time": keypress_time})
    #print(key_pressed_string)

    if typed_sentence == target_sentence:
        data = {
            "sentence": target_sentence,
            "keystrokes": keystrokes,
            "total_time": (time.time() * 1000) - sentence_start_time
        }
        json_data = json.dumps(data)
        client_socket.send(json_data.encode('utf-8'))

        typed_sentence = ""
        keystrokes = []
        sentence_start_time = None


def main():
    global client_socket

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    with keyboard.Listener(on_press = on_key_press, on_release = on_key_release, suppress=True) as listener:
        listener.join()

    client_socket.close()

    print(keystrokes)



if __name__ == "__main__":
    main()