import socket
import threading

HEADER = 64
PORT = 65432
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(ADDR)

connections = []

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connections.append((addr))
    print(f'[ACTIVE CONNECTIONS] {connections}')

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                conn.send("[DISCONNECTED] disconnected from the server".encode(FORMAT))
                conn.close()
                connections.remove(addr)
                print(f"[{addr}] DISCONNECTED")
                print(f'[ACTIVE CONNECTIONS] {connections}')
                break

            print(f"[{addr}] {msg}")
            conn.send(f"[NOTIFICATION] message {msg} received".encode(FORMAT))


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args = (conn, addr))
        thread.start()

print("[STARTING] server is starting...")
start()