import services as svc
from GUI.GUI_handler import start, quit


def play(client, my_turn, disconnected, matrix, input_cards, show_score, get_matrix):
    has_started = False
    play = ''

    while True:
        if len(matrix) < 1:
            continue
        if not has_started:
            start("Jogo da memória!!!")
            show_score()
            has_started = True
        if len(disconnected) == 1:
            break
        try:
            play = input_cards(len(my_turn) == 1, get_matrix)
            if play == "disconnected":
                disconnected.append(1)
                break
            if len(my_turn) == 1:
                svc.send(play, client)
        except:
            continue
    quit()
