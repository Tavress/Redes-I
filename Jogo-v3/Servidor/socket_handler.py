import socket
import services as svc


PORT = 65432
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)


def handle_client(conn, nJogadores, connections):
    if len(connections) < nJogadores:
        connections.append(conn)
        svc.send(conn, 'Você é o jogador número {}\n'.format(len(connections)))
        if len(connections) < nJogadores:
            svc.send(conn, '\nAguardando novos jogadores...\n')
        if len(connections) == nJogadores:
            svc.send_for_all(connections, 'O jogo irá começar!\n')
    else:
        svc.send(conn, 'Erro: o jogo já está lotado!')
        svc.send(conn, 'refused_connection')
        conn.close()


def start_server(nJogadores, connections):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}, port {PORT}")
    while True:
        conn, addr = server.accept()
        handle_client(conn, nJogadores, connections)
