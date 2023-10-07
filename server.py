import socket
import json

HOST = '127.0.0.1'
PORT = 12345

def process_data(data):
    sentence = data["sentence"]
    keystrokes = data["keystrokes"]

    total_time = keystrokes[-1]["time"]
    actual_cpm = calculate_cpm(sentence, total_time)
    potential_cpm = calculate_potential_cpm(sentence, keystrokes)
    fail_words = find_fail_words(sentence, keystrokes)
    
    if potential_cpm == actual_cpm:
        potential_cpm = "N/A"

    print("Sentence: ", sentence)
    print("Actual CPM:    ", actual_cpm)
    print("Potential CPM: ", potential_cpm)
    print("Fail words:", fail_words, "\n")

def calculate_cpm(sentence, total_time):
    return (len(sentence) / total_time) * 60000

def calculate_potential_cpm(sentence, keystrokes):
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
        return calculate_cpm(sentence, keystrokes[-1]["time"])

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

    potential_cpm = calculate_cpm(sentence, optimal_time)

    return potential_cpm

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
                fail_words.append([word, error_in_word_index - word_start_index, error_in_word_letter])
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

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    client_socket, client_address = server_socket.accept()

    while True:

        data = client_socket.recv(4096 * 32).decode('utf-8')

        if not data:
            break

        json_data = json.loads(data)
        process_data(json_data)

if __name__ == "__main__":
    main()