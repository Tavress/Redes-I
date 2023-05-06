import socket
import services as svc

def start_client(ADDR):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect(ADDR)
    msg = svc.receive(client)
    print(msg)

    return client