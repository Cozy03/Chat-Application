# File name: client.py
import socket
import threading
import tkinter as tk

# Define the host for the server
HOST = 'localhost'

# Define the port number for this client
PORT = 8000

# Create a new client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((HOST, PORT))

# Prompt the user for a name
name = input("Enter your name: ")

# Send the name to the server
client_socket.send(name.encode())

# Define a function to handle sending messages to the server
def send_message(event=None):
    message = input_box.get()
    if message:
        # Send the message to the server with the client's name
        client_socket.send(f"{name}: {message}".encode())

# Create a new Tkinter window
window = tk.Tk()
window.title("Chat Application")

# Add a message display area
message_frame = tk.Frame(window)
scrollbar = tk.Scrollbar(message_frame)
message_list = tk.Listbox(message_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
message_list.pack(side=tk.LEFT, fill=tk.BOTH)
message_frame.pack()

# Add an input box and a send button
input_box = tk.Entry(window, width=50)
input_box.bind("<Return>", send_message)
input_box.pack()
send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack()

# Define a function to receive messages from the server and display them
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            message_list.insert(tk.END, message)
        except:
            # If there is an error receiving messages, exit the loop and close the socket
            client_socket.close()
            break

# Start a new thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Start the Tkinter main loop
window.mainloop()
