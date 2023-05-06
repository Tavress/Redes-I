HEADER = 64
FORMAT = 'utf-8'


def receive(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)

    return msg

def send(conn,msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)

def send_for_all(connections,msg):
    for con in connections:
        send(con,msg)

def send_matrix(con,dim,tabuleiro):
    send(con,"matrix")
    send(con,str(dim))
    for i in range(0,dim):
        line = str(i)
        for j in range(0,dim):
            if tabuleiro[i][j] == '-':
                line += ',-'
            elif tabuleiro[i][j] >= 0:
                line += "," + str(tabuleiro[i][j])
            else:
                line += ",?"
        send(con,line)
