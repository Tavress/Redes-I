import services as svc
import GUI.GUI_handler as gui


def play(client, my_turn, disconnected, matrix, input_cards, show_cards, show_score):
    has_started = False
    play = ''

    while True:
        if len(matrix) < 1:
            continue
        if not has_started:
            gui.start("Jogo da memória!!!")
            show_score()
            has_started = True
        if len(disconnected) == 1:
            break
        try:
            if len(my_turn) == 1:
                play = input_cards(len(my_turn) == 1)
                if len(my_turn) == 1:
                    svc.send(play, client)
            else:
                show_cards()
        except:
            continue
    gui.quit()
