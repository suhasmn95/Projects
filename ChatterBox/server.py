import socket
import threading
import tkinter as tk
from tkinter import messagebox

# List to store client sockets and their addresses
clients = []

# Global server socket variable
server_socket = None

# Function to handle communication with each client
def handle_client(client_socket, client_address):
    clients.append((client_socket, client_address))
    update_client_list()

    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                # Broadcast message to other clients
                broadcast_message(message, client_socket)
            else:
                break
    except:
        pass
    finally:
        # Remove client from list and close socket
        clients.remove((client_socket, client_address))
        update_client_list()
        client_socket.close()

# Function to send message to all clients
def broadcast_message(message, client_socket):
    for client in clients:
        if client[0] != client_socket:
            try:
                client[0].send(message.encode('utf-8'))
            except:
                pass

# Function to update the listbox with connected clients
def update_client_list():
    client_listbox.delete(0, tk.END)  # Clear the listbox
    for client in clients:
        client_listbox.insert(tk.END, f"{client[1]}")  # Add client address to the listbox

# Function to disconnect the selected client
def disconnect_client():
    try:
        selected_client = client_listbox.curselection()
        if selected_client:
            selected_client = selected_client[0]
            client_socket, client_address = clients[selected_client]

            # Send disconnect message and close connection
            client_socket.send("You are disconnected from the server.".encode('utf-8'))
            client_socket.close()

            # Remove client from the list and update the GUI
            clients.pop(selected_client)
            update_client_list()
            messagebox.showinfo("Client Disconnected", f"Client {client_address} has been disconnected.")
        else:
            messagebox.showwarning("No Client Selected", "Please select a client to disconnect.")
    except Exception as e:
        messagebox.showerror("Error", f"Error disconnecting client: {e}")

# Function to start the server and accept incoming connections
def start_server():
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)

    print("Server is running... Waiting for connections.")
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

# Function to close the server and clean up
def close_server():
    global server_socket
    # Close the server socket and all client connections
    if server_socket:
        for client in clients:
            client[0].close()
        server_socket.close()
    root.quit()

# GUI setup
root = tk.Tk()
root.title("Server - Client Management")
root.geometry("400x400")

# Listbox to show connected clients
client_listbox = tk.Listbox(root, width=50, height=10)
client_listbox.pack(pady=10)

# Button to disconnect selected client
disconnect_button = tk.Button(root, text="Disconnect Client", width=20, command=disconnect_client)
disconnect_button.pack(pady=10)

# Add a "Quit" button to close the server and GUI
quit_button = tk.Button(root, text="Quit Server", width=20, command=close_server)
quit_button.pack(pady=10)

# Start the server in a separate thread so it does not block the GUI
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

# Set the window close event to stop the server
root.protocol("WM_DELETE_WINDOW", close_server)

# Run the GUI event loop
root.mainloop()
