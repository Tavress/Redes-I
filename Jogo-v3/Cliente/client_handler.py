import GUI.GUI_handler as gui
import services as svc
import main

message = ""
disconnected = []
my_turn = []
matrix = []


def get_current_message():
    global message
    return message


def handle():
    global message, disconnected, matrix, my_turn, client
    has_started = False
    play = ''
    while True:
        if len(disconnected) == 1:
            break
        msg = svc.receive(client)
        event = svc.check_event_message(
            msg, client, my_turn, disconnected, matrix)
        if msg and not event:
            message = msg
            print(f"{msg}", end='')
        if len(matrix) == 0:
            continue
        if not has_started:
            gui.start("Jogo da memória!!!")
            main.show_score()
            has_started = True
        if len(my_turn) == 1:
            # gui.show_cards(matrix)
            play = main.get_GUI_inputs(len(my_turn) == 1)
            svc.send(play, client)
        else:
            main.show_inputs()
    return
