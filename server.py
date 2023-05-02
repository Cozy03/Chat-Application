# File name: server.py
import socket
import threading

# Define the host and port for the server
HOST = 'localhost'
PORT = 8000

# Create a new server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server socket to the host and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

# Create a list to store the connected clients and their names
clients = []
names = []

# Define a function to handle client connections
def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    # Receive the client's name
    name = client_socket.recv(1024).decode()
    names.append(name)
    clients.append(client_socket)
    # Loop to receive messages from the client
    while True:
        try:
            # Receive the message from the client
            message = client_socket.recv(1024).decode()
            # Broadcast the message to all connected clients, with the sender's name included
            for client in clients:
                client.send(f"{name}: {message}".encode())
        except:
            # If there is an error receiving messages, remove the client from the list of connected clients
            index = clients.index(client_socket)
            clients.remove(client_socket)
            client_socket.close()
            name = names[index]
            names.remove(name)
            break

# Loop to accept new client connections
while True:
    # Wait for a new client connection
    client_socket, client_address = server_socket.accept()
    # Start a new thread to handle the client connection
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()