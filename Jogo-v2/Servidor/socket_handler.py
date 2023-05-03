import socket
import threading
import services as svc


PORT = 65432
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

def handle_client(conn,nJogadores,connections):
    if len(connections) < nJogadores:
        connections.append(conn)
        svc.send(conn,'Você é o jogador número {}\nAguardando novos jogadores...\n'.format(len(connections)))
    else:
        svc.send(conn,'Erro: o jogo já está lotado!')
        svc.send(conn,'refused_connection')
        conn.close()
    

def start_server(nJogadores,connections):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}, port {PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args = (conn,nJogadores,connections))
        thread.start()
