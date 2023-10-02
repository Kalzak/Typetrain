import socket
import json

# Define host and port for the server
HOST = '127.0.0.1'
PORT = 12345

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((HOST, PORT))
print(f"Connected to {HOST}:{PORT}")

# Create a sample JSON data to send to the server
data_to_send = {
    "name": "John Doe",
    "age": 30,
    "city": "New York"
}

# Send JSON data to the server
json_data = json.dumps(data_to_send)
client_socket.send(json_data.encode('utf-8'))

# Close the socket
client_socket.close()
