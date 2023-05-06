import services as svc
import GUI.GUI_handler as gui


def play(client, my_turn, disconnected, matrix, input_cards, show_cards):
    gui.start()
    play = ''
    while True:
        if len(matrix) == 0:
            continue
        if len(disconnected) == 1:
            break
        if len(my_turn) == 1:
            play = input_cards(len(my_turn) == 1)  # gui.show_cards(matrix)
            svc.send(play, client)
        else:
            show_cards()
            print('Aguarde a sua vez!')
    return
