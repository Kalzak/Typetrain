import socket
import json
import os
import matplotlib.pyplot as plt
import time
from flask import Flask, request, jsonify
from flask_cors import CORS

HOST = '127.0.0.1'
PORT = 12345

plt.ion()

app = Flask(__name__)
CORS(app)

def process_data(data):
    sentence = data["sentence"]
    keystrokes = data["keystrokes"]
    training = False
    if "training" in data:
        training = True

    total_time = keystrokes[-1]["time"]
    optimal_time = calculate_optimal_time(sentence, keystrokes)
    actual_cpm = calculate_cpm(sentence, total_time)
    potential_cpm = calculate_potential_cpm(sentence, keystrokes)
    actual_wpm = calculate_wpm(sentence, total_time)
    potential_wpm = calculate_potential_wpm(sentence, keystrokes)
    fail_words = find_fail_words(sentence, keystrokes)
    success_words = find_success_words(sentence, keystrokes)

    print("Sentence:      ", sentence)
    print("Actual time:   ", total_time)
    print("Potential time:", optimal_time)
    print("Actual CPM:    ", actual_cpm)
    print("Potential CPM: ", potential_cpm)
    print("Actual WPM:    ", actual_wpm)
    print("Potential WPM: ", potential_wpm)
    print("Fail words:    ", fail_words)
    print("Success words: ", success_words, "\n")

    if training == False:
        write_data("userdata.json", sentence, total_time, optimal_time, actual_cpm, potential_cpm, actual_wpm, potential_wpm, fail_words, success_words)
    else:
        write_data("userdata.training.json", sentence, total_time, optimal_time, actual_cpm, potential_cpm, actual_wpm, potential_wpm, fail_words, success_words)

def write_data(file_path, sentence, a_time, p_time, a_cpm, p_cpm, a_wpm, p_wpm, f_words, s_words):

    data = None

    if not os.path.exists(file_path):
        data = {
            "sentence_history": [],
            "success_words": {},
            "fail_words": {},
        }
    else:
        with open(file_path, "r") as file:
            data = json.load(file)
    
    sentence_number = 0
    if len(data["sentence_history"]) != 0:
        sentence_number = data["sentence_history"][0]["number"] + 1

    # Insert new sentence into sentence history
    sentence_history_data = {
        "sentence": sentence,
        "a_time": a_time,
        "p_time": p_time,
        "a_cpm": a_cpm,
        "p_cpm": p_cpm,
        "a_wpm": a_wpm,
        "p_wpm": p_wpm,
        "number": sentence_number
    }
    data["sentence_history"].insert(0, sentence_history_data)

    # Insert success word data
    for s_word in s_words:
        s_word_data = {
            "word": s_word[0],
            "time": s_word[1],
            "cpm": s_word[2],
            "number": sentence_number,
        }
        if s_word_data["word"] in data["success_words"]:
            data["success_words"][s_word_data["word"]].insert(0, s_word_data)
        else:
            data["success_words"][s_word_data["word"]] = [s_word_data]

    # Insert fail word data
    for f_word in f_words:
        f_word_data = {
            "word": f_word[0],
            "index": f_word[1],
            "letter": f_word[2],
            "number": sentence_number,
        }
        if f_word_data["word"] in data["fail_words"]:
            data["fail_words"][f_word_data["word"]].insert(0, f_word_data)
        else:
            data["fail_words"][f_word_data["word"]] = [f_word_data]

    # Write to file
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

def calculate_wpm(sentence, total_time):
    return (len(sentence.split(" ")) / total_time) * 60000

def calculate_potential_wpm(sentence, keystrokes):
    optimal_time = calculate_optimal_time(sentence, keystrokes)
    return calculate_wpm(sentence, optimal_time)

def calculate_cpm(sentence, total_time):
    return (len(sentence) / total_time) * 60000

def calculate_optimal_time(sentence, keystrokes):
    keystroke_times = []
    fail_indexes = []
    typed_sentence = []

    for keystroke in keystrokes:
        if keystroke["action"] == "up":
            continue
        if len(keystroke["key"]) == 1: 
            keystroke_times.append(keystroke["time"])
            typed_sentence.append(keystroke["key"])
        elif keystroke["key"] == "Key.space":
            keystroke_times.append(keystroke["time"])
            typed_sentence.append(" ")
        elif keystroke["key"] == "Key.backspace":
            keystroke_times = keystroke_times[:-1]
            typed_sentence = typed_sentence[:-1]

            new_fail_index = len(typed_sentence)

            while len(fail_indexes) != 0 and fail_indexes[-1] >= new_fail_index:
                fail_indexes.pop()
            fail_indexes.append(new_fail_index)


    if len(fail_indexes) == 0:
        return keystrokes[-1]["time"]

    all_timediffs = []

    base_range = 0
    for fail_index in fail_indexes:
        subarray = keystroke_times[base_range:fail_index]
        base_range = fail_index

        timediffs = []
        for i in range(1,len(subarray)):
            timediffs.append(subarray[i] - subarray[i-1])

        all_timediffs.extend(timediffs)

    subarray = keystroke_times[base_range:len(keystroke_times)]
    timediffs = []
    for i in range(1,len(subarray)):
        timediffs.append(subarray[i] - subarray[i-1])

    all_timediffs.extend(timediffs)

    average_time_per_good_character = sum(all_timediffs) / len(all_timediffs)

    optimal_time = len(sentence) * average_time_per_good_character

    return optimal_time

def calculate_potential_cpm(sentence, keystrokes):
    optimal_time = calculate_optimal_time(sentence, keystrokes)
    return calculate_cpm(sentence, optimal_time)

def find_fail_words(sentence, keystrokes):
    fail_words = []
    fail_indexes = []
    fail_letters = ["" for _ in range(len(sentence))]
    typed_sentence = ""
    already_error = False

    for keystroke in keystrokes:

        key = keystroke["key"]

        if keystroke["action"] == "up":
            continue

        if len(key) == 1:
            typed_sentence += key
        if key == "Key.space":
            typed_sentence += " "
        if key == "Key.backspace":
            typed_sentence = typed_sentence[:-1]

        if typed_sentence != sentence[:len(typed_sentence)]:
            if already_error == False:
                fail_indexes.append(len(typed_sentence) - 1)
                fail_letters[len(typed_sentence)-1] = key
                already_error = True
        else:
            already_error = False

    word = ""
    error_in_word = False
    error_in_word_letter = ""
    error_in_word_index = 0
    word_start_index = 0
    for i in range(0, len(sentence)):

        if sentence[i] == " " or i == len(sentence)-1:
            if error_in_word:
                index_in_word_fail = error_in_word_index - word_start_index
                # Ignore typos that aren't alphanumeric ( commas, question marks, symbols etc)
                #if word.lower()[index_in_word_fail].isalpha(): # was orginally isalnum but annoying to deal with quotes etc
                #    fail_words.append([word.lower(), index_in_word_fail, error_in_word_letter.lower()])


                original_word = word
                trimmed_word = trim_non_alnum(original_word)

                # Calculate how many characters were removed from the start
                num_chars_removed = original_word.index(trimmed_word)

                # Adjust the error index
                adjusted_index = index_in_word_fail - num_chars_removed

                # Only append if the adjusted_index is valid and the error_in_word_letter is alphabetic
                if 0 <= adjusted_index < len(trimmed_word) and trimmed_word[adjusted_index].isalpha():
                    fail_words.append([trimmed_word.lower(), adjusted_index, error_in_word_letter.lower()])

            word = ""
            error_in_word = False
            word_start_index = i + 1
        else:
            word += sentence[i]
            if i in fail_indexes:
                if error_in_word == False:
                    error_in_word = True
                    error_in_word_index = i
                    error_in_word_letter = fail_letters[i]

    return fail_words

def trim_non_alnum(word):
    while word and not word[0].isalnum():
        word = word[1:]
    while word and not word[-1].isalnum():
        word = word[:-1]
    return word

def find_success_words(sentence, keystrokes):
    success_words = []
    typed_word = ""
    word_number = 0
    had_error = False
    split_sentence = sentence.split()
    first_letter_time = None
    
    for keystroke in keystrokes:

        key = keystroke["key"]

        if first_letter_time is None:
            first_letter_time = keystroke["time"]

        if keystroke["action"] == "up":
            continue

        if len(key) == 1:
            typed_word += key
        if key == "Key.space":
            if len(typed_word) != 0:
                typed_word += " "
        if key == "Key.backspace":
            typed_word = typed_word[:-1]
            had_error = True

        if typed_word == split_sentence[word_number]:
            if had_error == False:
                time_to_type = keystroke["time"] - first_letter_time
                clean_word = clean_success_word(typed_word)
                word_cpm = calculate_cpm(clean_word, time_to_type)
                success_words.append([clean_word, time_to_type, word_cpm])
            
            had_error = False
            typed_word = ""
            word_number += 1
            first_letter_time = None
    
    return success_words

def clean_success_word(word):
    if word[-1] == "." or word[-1] == "," or word[-1] == "?":
        word = word[:-1]
    return word.lower()

def plot_data(data):
    # Calculate average CPM for each word
    avg_cpm = {}
    for word, entries in data.items():
        if len(word) < 3:
            continue
        if len(entries) < 5:
            continue
        total_cpm = sum(entry['cpm'] for entry in entries)
        avg_cpm[word] = total_cpm / len(entries)
    
    # Sort words by average CPM
    sorted_words = sorted(avg_cpm, key=avg_cpm.get)
    sorted_avg_cpm = [avg_cpm[word] for word in sorted_words]
    
    plt.xticks(rotation=90)
    plt.plot(sorted_words, sorted_avg_cpm)
    plt.draw()
    plt.pause(3)
    plt.clf()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket, client_address = server_socket.accept()


    if os.path.exists("userdata.json"):
        with open("userdata.json", 'r') as file:
            try:
                stats = json.load(file)
                #plot_data(stats)
            except:
                print("The bug happened let's see if it happens again")
                try:
                    stats = json.load(file)
                    #plot_data(stats)
                except:
                    print("yeah failed twice")
            

    while True:

        
        data = None

        #data = receive_data(client_socket)
        data = receive_data(app)

        if not data:
            break

        with open('output.txt', 'w') as file:
            file.write(data)

        print(data)

        json_data = json.loads(data)
        process_data(json_data)

        with open("userdata.json", 'r') as file:
            stats = json.load(file)
            #plot_data(stats)

def receive_data(sock):
    length = int(sock.recv(10).decode('utf-8').strip())
    print(length)
    chunks = []
    bytes_received = 0
    while bytes_received < length:
        chunk = sock.recv(min(length - bytes_received, 4096))
        if not chunk:
            raise RuntimeError("Socket connection broken")
        chunks.append(chunk)
        bytes_received += len(chunk)
    
    serialized_data = b"".join(chunks)
    return json.loads(serialized_data.decode('utf-8'))

@app.route('/', methods=['POST'])
def receive_data_html():
    json_data = request.get_json()
    print("Received data:", json_data)
    
    # Process the data here

    process_data(json_data)
    return jsonify({"status": "success", "message": "Data received"}), 200


if __name__ == "__main__":
    app.run(port=8000)
    main()
