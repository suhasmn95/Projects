import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Function to send messages to the server
def send_message():
    message = entry.get()
    try:
        if message:
            client_socket.send(message.encode('utf-8'))
            entry.delete(0, tk.END)
    except:
        messagebox.showerror("error", "connection lost")

# Function to receive messages from the server
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                chat_box.insert(tk.END, message + '\n')
                chat_box.yview(tk.END)
        except:
            break

# Set up the GUI window
root = tk.Tk()
root.title("Chat Application")
root.geometry("400x400")

# Create the chat box (ScrolledText widget for scrollable text area)
chat_box = scrolledtext.ScrolledText(root, width=50, height=15, wrap=tk.WORD)
chat_box.pack(pady=10)

# Create an entry widget for typing messages
entry = tk.Entry(root, width=40)
entry.pack(pady=5)

# Create a button to send messages
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=5)

# Set up the client socket to connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

# Start a thread to listen for incoming messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

# Run the Tkinter event loop
root.mainloop()
