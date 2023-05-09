from GUI.GUI_handler import start, quit, get_ip_and_port, get_GUI_inputs
import socket_handler as sck
import threading
import message_handler as msgh
import play_handler as plh
import score_handler as score

disconnected = []
my_turn = []
matrix = []


def get_matrix():
    global matrix
    return matrix


start("Preecha as informaçãoes do server!")
ADDR = get_ip_and_port()
quit()

# Cria a conexão TCP com o servidor
client = sck.start_client(ADDR)

msg_thread = threading.Thread(target=msgh.get_message, args=(
    disconnected, client, my_turn, matrix))
score_thread = threading.Thread(
    target=score.show_score, args=(disconnected,))
play_thread = threading.Thread(target=plh.play, args=(
    client, my_turn, disconnected, matrix, get_GUI_inputs, score_thread.start, get_matrix))

msg_thread.daemon = True
msg_thread.start()
play_thread.start()
