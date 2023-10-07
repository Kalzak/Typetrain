from pynput import keyboard
import socket
import json
import time
import random
import os
import requests
from bs4 import BeautifulSoup

# Network data
HOST = '127.0.0.1'
PORT = 12345

# Networking stuff
client_socket = None

# Sentences for races
sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "A watched pot never boils.",
    "All that glitters is not gold.",
    "Actions speak louder than words.",
    "Where there's a will, there's a way.",
    "Every cloud has a silver lining.",
    "Don't count your chickens before they hatch.",
    "Birds of a feather flock together.",
    "A penny for your thoughts.",
    "You can't judge a book by its cover."
]

# Typing data
keystrokes = []
ctrl_pressed = False
typed_sentence = ""
target_sentence = ""
sentence_start_time = None

def on_key_press(key):
    global ctrl_pressed, typed_sentence, sentence_start_time

    if sentence_start_time is None:
        sentence_start_time = time.time() * 1000

    keypress_time = (time.time() * 1000) - sentence_start_time
    if keypress_time < 1:
        keypress_time = 0

    key_pressed = ""

    try:

        key_pressed = key.char

        if key_pressed == 'c' and ctrl_pressed == True:
            return False

        typed_sentence += key_pressed

    except AttributeError:

        key_pressed = str(key)

        if key == keyboard.Key.ctrl_l:
            ctrl_pressed = True

        if key == keyboard.Key.space:
            typed_sentence += " "

        if key == keyboard.Key.backspace:
            typed_sentence = typed_sentence[:-1]

    keystrokes.append({"key": key_pressed, "action": "down", "time": keypress_time})
    
    display_race(target_sentence, typed_sentence)


def on_key_release(key):
    global ctrl_pressed, keystrokes2

    key_pressed = ""

    if key == keyboard.Key.caps_lock:
        key = keyboard.Key.shift

    if key == keyboard.Key.ctrl_l:
        ctrl_pressed = False

    try:

        key_pressed = str(key.char)

    except AttributeError:

        key_pressed = str(key)

    try:
        keypress_time = (time.time() * 1000) - sentence_start_time
    except: 
        return True

    keystrokes.append({"key": key_pressed, "action": "up", "time": keypress_time})

    if typed_sentence == target_sentence:
        data = {
            "sentence": target_sentence,
            "keystrokes": keystrokes,
        }
        json_data = json.dumps(data)
        client_socket.send(json_data.encode('utf-8'))

        prep_new_race()
        display_race(target_sentence, typed_sentence)

def prep_new_race():
    global typed_sentence, keystrokes, sentence_start_time, target_sentence
    typed_sentence = ""
    keystrokes = []
    sentence_start_time = None

    # Uncomment for predetermined races
    target_sentence = random.choice(sentences)
    
    # Uncomment for typeracer races
    #target_sentence = get_new_text() 

def display_race(target_sentence, typed_sentence):
    green_text = "\033[32m"
    red_text = "\033[31m"
    reset_text = "\033[0m"

    correct_end_index = None
    wrong_end_index = None

    for i in range(0, len(typed_sentence)):
        if target_sentence[i] == typed_sentence[i] and wrong_end_index is None:
            correct_end_index = i + 1
        else:
            wrong_end_index = i + 1
    
    os.system("clear")
    if correct_end_index is not None:
        print(green_text + target_sentence[0:correct_end_index] + reset_text, end="")
    else:
        correct_end_index = 0

    if wrong_end_index is not None:
        print(red_text + target_sentence[correct_end_index:wrong_end_index] + reset_text, end="")
        print(target_sentence[wrong_end_index:])
    else:
        print(target_sentence[correct_end_index:])

def get_new_text():
    url = "https://typeracerdata.com/text?id=" + str(random.randint(1,750))
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        text_element = soup.find("p")
        return text_element.text[2:]

def main():
    global client_socket, target_sentence

    prep_new_race()
    display_race(target_sentence, typed_sentence)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    with keyboard.Listener(on_press = on_key_press, on_release = on_key_release, suppress=True) as listener:
        listener.join()

    client_socket.close()

if __name__ == "__main__":
    main()