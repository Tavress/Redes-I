import socket
import threading

HEADER = 64
PORT = 65432
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

my_turn = False

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(ADDR)

def send(msg):
    client.send(msg.encode(FORMAT))


def play():
    play = ''
    while True:
        if my_turn:
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
        if msg == 'your_turn':
            my_turn = True
        if msg == 'end_of_your_turn':
            my_turn = False
msg_thread = threading.Thread(target=get_message)
play_thread = threading.Thread(target=play)

msg_thread.start()
play_thread.start()

