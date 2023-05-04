
import services as svc

def get_message(disconnected,client,my_turn,matrix):
    while True:
        if len(disconnected) == 1:
            break
        msg = svc.receive(client)
        event = svc.check_event_message(msg,client,my_turn,disconnected,matrix)
        if msg and not event:
            print(f"{msg}", end='')

    print('\n\nDesconectado do servidor. Pressione <enter> para sair.\n')
    return 