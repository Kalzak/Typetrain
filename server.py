import socket
import json

HOST = '127.0.0.1'
PORT = 12345

def process_data(data):
    sentence = data["sentence"]
    keystrokes = data["keystrokes"]
    total_time = data["total_time"]
    
    total_time_calculated = get_total_time(keystrokes)
    
    print(sentence)
    print(total_time)
    print(total_time_calculated)

def get_total_time(keystrokes):
    total = 0

    for item in keystrokes:

        print(item)

        total += item["time"]

    return total

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((HOST, PORT))

    server_socket.listen(1)

    while True:
        client_socket, client_address = server_socket.accept()

        data = client_socket.recv(4096 * 32).decode('utf-8')
        if not data:
            break

        print(data)

        json_data = json.loads(data)
        process_data(json_data)

        print("connected")

if __name__ == "__main__":
    main()