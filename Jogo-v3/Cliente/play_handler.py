import services as svc

def play(client,my_turn,disconnected):
    play = ''
    while True:
        play = input()
        if len(disconnected) == 1:
            break
        if len(my_turn) == 1:
            svc.send(play,client)
        else:
            print('Aguarde a sua vez!')
    return