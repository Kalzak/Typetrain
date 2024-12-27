import socket
import json

# Define host and port for the server
HOST = '127.0.0.1'
PORT = 12345

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections (max 1)
server_socket.listen(1)
print(f"Server listening on {HOST}:{PORT}")

# Accept a connection from a client
client_socket, client_address = server_socket.accept()
print(f"Connected to {client_address}")

# Receive and print JSON data from the client
while True:
    data = client_socket.recv(4096).decode('utf-8')
    if not data:
        break
    json_data = json.loads(data)
    print("Received JSON data from client:")
    print(json.dumps(json_data, indent=4))

# Close the sockets
client_socket.close()
server_socket.close()
