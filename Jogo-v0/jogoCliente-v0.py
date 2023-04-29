import socket
import threading

HEADER = 64
PORT = 65432
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

my_turn = []

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(ADDR)

def send(msg):
    client.send(msg.encode(FORMAT))


def play():
    print('entrei no play')
    play = ''
    while True:
        if len(my_turn) > 0:
            print('entrei no condicional my_turn')
            play = input()
            send(play)

        if play == DISCONNECT_MESSAGE:
            client.close()
            break

def get_message():
    while True:
        msg = client.recv(1024).decode(FORMAT)
        if msg:
            print(f"{msg}")
        if msg.startswith("your"):
            my_turn.append(1)
            print(my_turn)
        if msg == 'end_of_your_turn':
            my_turn.remove(1)


msg_thread = threading.Thread(target=get_message)
play_thread = threading.Thread(target=play)

msg_thread.start()
play_thread.start()

