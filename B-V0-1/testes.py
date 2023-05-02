"""
msg = "Ola Mundo Lindo"
msg = f"{len(msg):<{64}}" + msg
print(msg)
msg = bytes(msg, 'utf-8')
print(f"Em bystes: {msg}")
print(f"Em int: {int(msg[:64])}")
msg_length = int(msg[:64])
print(msg_length)
msg = msg.decode('utf-8')
full_mensagem = msg[64:]
print(full_mensagem)
"""
HEADER = 64
FORMAT = 'utf-8'
msg = "Ola Mundo lindo do meu coração.\n"
print(f"MENSAGEM: {msg}")
message = msg.encode(FORMAT)
print(f"MENSAGEM CODIFICADA: {message}")
msg_length = len(message)
print(f"TAMANHO DA MENSAGEM CODIFICADA: {msg_length}")
send_length = str(msg_length).encode(FORMAT)
print(f"TAMANHO CODIFICADO EM STR E FORMAT: {send_length}")
send_length += b' ' * (HEADER - len(send_length))
print(f"CABEÇALHO DA MENSAGEM + CALCULO: {send_length}\n")

msg_lengthh = send_length.decode(FORMAT)
print(f"CABEÇALHO DECODIFICADO: {msg_lengthh}\n")
if msg_lengthh:
    msg_lengthh = int(msg_lengthh)
    print(f"CABEÇALHO DECODIFICADO EM INT: {msg_lengthh}")
    print(f"Mensagem Decodificada: {message.decode(FORMAT)}\n")


