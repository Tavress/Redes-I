import pygame
import GUI.GUI_handler as gui
from GUI.Window import Window
from GUI.Card import Card
import socket_handler as sck
import threading
import message_handler as msgh
import play_handler as plh

disconnected = []
my_turn = []
matrix = []

gui.start()
# Início da execução do programa cliente
# print('Informe o IP do servidor: ')
# SERVER = str(input())
# print('Informe a porta: ')
# PORT = int(input())
gui.quit()
ADDR = ("192.168.0.6", 65432)  # (SERVER, PORT)

# Cria a conexão TCP com o servidor
client = sck.start_client(ADDR)


def get_GUI_inputs(is_my_turn: bool) -> tuple[int, int]:
    global matrix
    is_running = True
    selected = [0, 0]
    size = len(matrix)
    card_matrix = Card.get_card_matrix(size, matrix)
    if size < 1 or not is_my_turn:
        draw_cards(card_matrix)
        pygame.display.update()
        return None
    while is_running:
        Window.current.clear()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(size):
                    for j in range(size):
                        if card_matrix[i][j].check_mouse_hover(event) and is_my_turn:
                            card_matrix[i][j].on_clicked()
                            card_matrix[i][j].update(matrix[i][j])
                            is_running = False
                            selected = [i, j]
        draw_cards(card_matrix)
        pygame.display.update()
    return f"{selected[0]} {selected[1]}"
    # return selected


def draw_cards(card_matrix):
    size = len(card_matrix)
    for i in range(size):
        for j in range(size):
            card_matrix[i][j].update(matrix[i][j])
            card_matrix[i][j].draw()


def show_inputs():
    global matrix
    is_running = True
    size = len(matrix)
    card_matrix = Card.get_card_matrix(size, matrix)
    if size < 1:
        draw_cards(card_matrix)
        pygame.display.update()
        return None
    Window.current.clear()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
    draw_cards(card_matrix)
    pygame.display.update()


msg_thread = threading.Thread(target=msgh.get_message, args=(
    disconnected, client, my_turn, matrix))
play_thread = threading.Thread(target=plh.play, args=(
    client, my_turn, disconnected, matrix, get_GUI_inputs, show_inputs))

msg_thread.daemon = True

msg_thread.start()
play_thread.start()
