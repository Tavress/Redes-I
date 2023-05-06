import socket_handler as sck
import threading
import message_handler as msgh
import play_handler as plh

disconnected = []
my_turn = []
matrix = []

# Início da execução do programa cliente
print('Informe o IP do servidor: ')
SERVER = str(input())
print('Informe a porta: ')
PORT = int(input())
ADDR = (SERVER, PORT)

# Cria a conexão TCP com o servidor
client = sck.start_client(ADDR)


msg_thread = threading.Thread(target=msgh.get_message, args=(
    disconnected, client, my_turn, matrix))
play_thread = threading.Thread(target=plh.play, args=(
    client, my_turn, disconnected, matrix))

msg_thread.daemon = True

msg_thread.start()
play_thread.start()
