from pynput import keyboard
import socket
import json
import time
import random
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import openai

# Network data
HOST = '127.0.0.1'
PORT = 12346

# Networking stuff
client_socket = None

# Api
openai_api_key = None

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

# Settings
training = False
training_type = None
text_type = None
focus = False

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

    keystrokes.append({"key": key_pressed, "action": "down", "time": round(keypress_time, 2)})
    
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

    keystrokes.append({"key": key_pressed, "action": "up", "time": round(keypress_time, 2)})

    if typed_sentence == target_sentence:
        data = {
            "sentence": target_sentence,
            "keystrokes": keystrokes,
        }

        if training == True:
            data["training"] = True;
    
        json_data = json.dumps(data)
        #client_socket.send(json_data.encode('utf-8'))

        send_data(json_data)

        prep_new_race()
        display_race(target_sentence, typed_sentence)

def send_data(json_data):
    serialized_data = json.dumps(json_data).encode('utf-8')
    length = len(serialized_data)
    client_socket.sendall(f"{length:<10}".encode('utf-8'))
    client_socket.sendall(serialized_data)

def prep_new_race():
    global typed_sentence, keystrokes, sentence_start_time, target_sentence
    typed_sentence = ""
    keystrokes = []
    sentence_start_time = None

    if training == True:
        if training_type != "error":
            if focus == True:
                target_sentence = generate_focus_text(get_slow_words())
            else:
                target_sentence = get_training_text(get_slow_words())
        else:
            if focus == True:
                target_sentence = generate_focus_text(get_error_words())
            else:
                target_sentence = get_training_text(get_error_words())
    else:
        if text_type == "simple":
            target_sentence = random.choice(sentences)
        else:
            target_sentence = get_new_text()

def generate_focus_text(wordlist):
    paragraph = []
    while len(paragraph) < 30:
        random_string = random.choice(wordlist)
        paragraph.append(random_string)
    return ' '.join(paragraph)

def display_race(target_sentence, typed_sentence):
    green_text = "\033[32m"
    red_text = "\033[31m"
    reset_text = "\033[0m"

    correct_end_index = None
    wrong_end_index = None

    for i in range(0, len(typed_sentence)):
        if i < len(target_sentence) and (target_sentence[i] == typed_sentence[i] and wrong_end_index) is None:
            correct_end_index = i + 1
        else:
            wrong_end_index = i + 1
    
    os.system("clear")
    if correct_end_index is not None:
        correct_text = target_sentence[0:correct_end_index]
        print(green_text + correct_text + reset_text, end="")
    else:
        correct_end_index = 0

    if wrong_end_index is not None:
        if wrong_end_index <= len(target_sentence):
            error_text = target_sentence[correct_end_index:wrong_end_index].replace(" ", "_")
        else:
            error_text = (target_sentence[correct_end_index:] + typed_sentence[len(target_sentence):]).replace(" ", "_")
        print(red_text + error_text + reset_text, end="")
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

def get_slow_words():
    # 1. Read the JSON data from a file
    data = None
    try:
        with open('userdata.json', 'r') as f:
            data = json.load(f)
    except:
        time.sleep(0.1)
        with open('userdata.json', 'r') as f:
            data = json.load(f)
    
    # 2. Extract and organize the data needed to compute average CPM for each word
    words = []
    avg_cpms = []
    for word, attempts in data['success_words'].items():
        cpms = [attempt['cpm'] for attempt in attempts[-100:]]  # Take the last 100 attempts, or less if not available
        avg_cpm = sum(cpms) / len(cpms) if cpms else 0  # Calculate average CPM
        words.append(word)
        avg_cpms.append(avg_cpm)

    # Sorting data by average CPM
    sorted_indices = sorted(range(len(avg_cpms)), key=lambda k: avg_cpms[k])
    words = [words[i] for i in sorted_indices]
    avg_cpms = [avg_cpms[i] for i in sorted_indices]

    words = words[0:50] + words[-50:]

    return random.sample(words, 15)

def get_training_text(words):
    filtered_array = [s for s in words if '\"' not in s]
    words_string = "\n - ".join(filtered_array)
    request_string = "Can you create a paragraph that uses some of the following words that I can use for typing practice? You don't have to use all of them. Oh yeah and I'm using you as an API so can you only just reply the paragrahp and that's it? 130 words max please. Here are the words: \n - " + words_string

    completion = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = [
            {'role': 'user', 'content': request_string}
        ],
        temperature = 1
    )

    return completion['choices'][0]['message']['content']


def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def calculate_error_rate(data):
    error_rate = {}
    for word, entries in data["fail_words"].items():
        success_count = len(data["success_words"].get(word, []))
        error_rate[word] = len(entries) / (len(entries) + success_count)
    return error_rate

def get_error_words():
    user_data = load_json("userdata.json")
    user_error_rate = calculate_error_rate(user_data)
    
    # Filter out words with more than 2 errors
    user_error_rate = {k: v for k, v in user_error_rate.items() if len(user_data["fail_words"][k]) > 2}
    
    # Sort by error rate and get the top 50 words
    sorted_words = sorted(user_error_rate, key=user_error_rate.get, reverse=True)[:50]

    return random.sample(sorted_words, 15)

def main():
    global client_socket, target_sentence, training, openai_api_key, training_type, text_type, focus

    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    wants_to_train = input("Type \"yes\" for training, otherwise press enter: ")
    if wants_to_train == "yes":
        training = True
        training_type = input("\"cpm\" or \"error\" training: ")
        wants_focus_training = input("\"focus\" for focused training: ")
        if wants_focus_training == "focus":
            focus = True;
    else:
        text_type = input("\"simple\" or \"typeracer\" texts: ")

        

    prep_new_race()
    display_race(target_sentence, typed_sentence)



    with keyboard.Listener(on_press = on_key_press, on_release = on_key_release, suppress=True) as listener:
        listener.join()

    input("Press enter to exit")

    client_socket.close()

if __name__ == "__main__":
    main()