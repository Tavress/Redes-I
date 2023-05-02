import os

HEADER = 64
FORMAT = 'utf-8'

def limpaTela():
    
    os.system('cls' if os.name == 'nt' else 'clear')

def send(msg,client):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def receive(client):
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)

    return msg


def check_event_message(msg,client,my_turn,disconnected):
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
