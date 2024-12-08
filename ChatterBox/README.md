### **Simple Chat Application (Real-Time Communication)**
This project implements a real-time chat application using Python. It includes a client-server architecture with the server handling communication between multiple clients. The application uses sockets for real-time message transmission and **Tkinter** for a simple graphical user interface (GUI). 

The server can be used for managing client connections. The server allows multiple clients to connect and chat in real-time. The server's GUI displays all active clients and provides functionality to terminate individual client connections.

## Features:
- Real-time communication between multiple clients.
- GUI-based chat interface using Tkinter.
- Simple client-server model with socket implementation.
- Broadcast messages to all connected clients (except the sender).
## Requirements:
- Python 3.x
- Tkinter (usually included with Python by default)
- No additional libraries are required, but you can install **tkinter** using the following command if necessary:
```bash
pip install tk
```
## File Structure:
```bash
/chat_app
  ├── client.py        # Client-side GUI and communication logic
  ├── server.py        # Server-side communication logic
  ├── README.md        # Project documentation

```
# How to Run:
1. **Start the Server**:
Run the server.py file first. The server will listen for incoming client connections.

```bash
python server.py
```
2. **Start the Client(s)**:
Run the client.py file in a new terminal for each client you want to run. Multiple clients can be run on the same machine or different machines (ensure they connect to the correct IP address and port).

```bash
python client.py
```
3. **Chat**:
- Once connected, you can type your message in the input field and click the "Send" button to send messages.
- Messages from other clients will appear in the chat box in real-time.
4. **Close the Application**:
Simply close the client or server window to stop the application. The server will disconnect all clients when it shuts down.

## Code Explanation:
## **Server** ('server.py'):
- The server listens for incoming connections on 'localhost' (127.0.0.1) at port '12345'.
- For each connected client, a new thread is spawned to handle communication independently.
- Messages received from a client are broadcast to all other connected clients.
- **Server-side GUI**: Displays a list of connected clients and allows the server admin to terminate selected clients.
## **Client** ('client.py'):
- The client connects to the server at localhost:12345.
- The GUI is created using Tkinter, where users can type and send messages.
- Incoming messages from other clients are displayed in the GUI in real-time.
## Main Functions:
- send_message(): Sends messages from the client to the server.
- receive_messages(): Listens for incoming messages from the server and displays them in the chat box.
- broadcast_message(): Sends a message to all connected clients, except the sender.
## How It Works:
1. **Server Side**:

- The server continuously listens for incoming client connections.
- When a client connects, it is added to a list of clients, and a new thread is spawned to handle communication with that client.
- When the server receives a message from any client, it is forwarded to all other connected clients.
2. **Client Side**:

- The client connects to the server and displays the chat interface using Tkinter.
- It allows users to type messages and send them to the server.
- Messages from other clients are received and displayed in the chat window.
## Future Enhancements:
- Add user authentication and unique usernames.
- Support for private messaging between users.
- Implement message persistence using a database (e.g., SQLite).
- Implement emojis, file sharing, or multimedia support.
- Add notifications or sound alerts for new messages.
## License:
This project is open-source and available for modification and use. There is no specific license associated with this project. Feel free to use, modify, and distribute it as per your requirements.
