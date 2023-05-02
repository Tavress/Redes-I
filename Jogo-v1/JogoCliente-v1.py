import socket
import threading
import os

HEADER = 64
#PORT = 65432
FORMAT = 'utf-8'
#SERVER = socket.gethostbyname(socket.gethostname())

def limpaTela():
    
    os.system('cls' if os.name == 'nt' else 'clear')

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def receive():
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)

    return msg


def check_event_message(msg):
    if msg == 'your_turn':
        if len(my_turn) == 0:
            my_turn.append(1)
        return True
    elif msg == 'end_of_your_turn':
        if len(my_turn) == 1:
            my_turn.remove(1)
        return True
    elif msg == 'limpa_tela':
        limpaTela()
        return True
    elif msg == 'game_over':
        client.close()
        disconnected.append(1)
        return True
    elif msg == 'refused_connection':
        disconnected.append(1)
        return True

    return False

def play():
    play = ''
    while True:
        play = input()
        if len(disconnected) == 1:
            break
        if len(my_turn) == 1:
            send(play)
        else:
            print('Aguarde a sua vez!')
    return

def get_message():
    while True:
        if len(disconnected) == 1:
            break
        msg = receive()
        event = check_event_message(msg)
        if msg and not event:
            print(f"{msg}", end='')

    print('\n\nDesconectado do servidor. Pressione <enter> para sair.\n')
    return 
       

my_turn = []
disconnected = []

print('Informe o IP do servidor: ')
SERVER = str(input())
print('Informe a porta: ')
PORT = int(input())

ADDR = (SERVER,PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(ADDR)
msg = receive()
print(msg)

msg_thread = threading.Thread(target=get_message)
play_thread = threading.Thread(target=play)

msg_thread.daemon = True

msg_thread.start()
play_thread.start()
