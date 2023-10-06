import socket
import json

HOST = '127.0.0.1'
PORT = 12345

def process_data(data):
    sentence = data["sentence"]
    keystrokes = data["keystrokes"]
    total_time = data["total_time"]

    total_time = keystrokes[-1]["time"]

    actual_cpm = calculate_cpm(sentence, total_time)
    potential_cpm = calculate_potential_cpm(sentence, keystrokes)
    if potential_cpm == actual_cpm:
        potential_cpm = "N/A"
    print("Sentence: ", sentence)
    print("Actual CPM:    ", actual_cpm)
    print("Potential CPM: ", potential_cpm, "\n")

def calculate_cpm(sentence, total_time):
    num_chars = len(sentence)

    return (num_chars / total_time) * 60000

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

            if len(fail_indexes) == 0:
                fail_indexes.append(len(keystroke_times))
            else:
                if(fail_indexes[-1] > len(keystroke_times)-1):
                    fail_indexes[len(fail_indexes)-1] = len(keystroke_times)
                else:
                    fail_indexes.append(len(keystroke_times))

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

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((HOST, PORT))

    server_socket.listen(1)

    client_socket, client_address = server_socket.accept()

    while True:
        

        data = client_socket.recv(4096 * 32).decode('utf-8')
        #if not data:
        #    break

        #print(data)

        json_data = json.loads(data)
        process_data(json_data)

if __name__ == "__main__":
    main()