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
choices_dict = {}


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connections.append(conn)
    print(f'[ACTIVE CONNECTIONS] {connections}')
    if len(connections) == 2:
        for con in connections:
            con.send("[NOTIFICAÇÃO] Escolha sua opção (pedra, papel ou tesoura): ".encode(FORMAT))

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                conn.send("[DISCONNECTED] disconnected from the server".encode(FORMAT))
                conn.close()
                connections.remove(conn)
                print(f"[{addr}] DISCONNECTED")
                print(f'[ACTIVE CONNECTIONS] {connections}')
                break

            print(f"[{addr}] {msg}")
            choices_dict[conn] = msg
            conn.send(f"[NOTIFICAÇÃO] Sua jogada: {msg}".encode(FORMAT))


def start_server():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args = (conn, addr))
        thread.start()

    
def game():
    while True:
        if len(choices_dict) == 2:
            if(choices_dict[connections[0]] == choices_dict[connections[1]]):
                for con in connections:
                    con.send("[NOTIFICAÇÃO] Empate!".encode(FORMAT))
            elif(choices_dict[connections[0]] == 'pedra' and choices_dict[connections[1]] == 'tesoura') or \
                (choices_dict[connections[0]] == 'papel' and choices_dict[connections[1]] == 'pedra') or \
                (choices_dict[connections[0]] == 'tesoura' and choices_dict[connections[1]] == 'papel'):

                connections[0].send('[NOTIFICAÇÃO] Você venceu!'.encode(FORMAT))
                connections[1].send('[NOTIFICAÇÃO] Você perdeu!'.encode(FORMAT))
            else:
                connections[1].send('[NOTIFICAÇÃO] Você venceu!'.encode(FORMAT))
                connections[0].send('[NOTIFICAÇÃO] Você perdeu!'.encode(FORMAT))

            connections[0].close()
            connections[1].close()
            break


game_thread = threading.Thread(target=game)
game_thread.start()
start_server()
