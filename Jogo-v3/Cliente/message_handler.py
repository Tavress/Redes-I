import services as svc

message = ""


def get_message(disconnected, client, my_turn, matrix):
    global message
    while True:
        if len(disconnected) == 1:
            break
        msg = svc.receive(client)
        event = svc.check_event_message(
            msg, client, my_turn, disconnected, matrix)
        if msg and not event:
            message = msg
            print(f"{msg}\n")
    print('\n\nDesconectado do servidor. Feche a página para sair.\n')
    return


def get_current_message():
    global message
    return message
