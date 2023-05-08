import tkinter as tk
import pygame
from pygame._sdl2 import messagebox
import GUI.GUI_handler as gui
from GUI.Text_Displayer import Text_Displayer
from GUI.Toggle import Toggle
from GUI.Window import Window
from GUI.Card import Card
import services as svc
import socket_handler as sck
import threading
import message_handler as msgh
import play_handler as plh

disconnected = []
my_turn = []
matrix = []
text_message = ""
lock = threading.RLock()

gui.start("Preecha as informaçãoes do server!")
# Início da execução do programa cliente
# print('Informe o IP do servidor: ')
# SERVER = str(input())
# print('Informe a porta: ')
# PORT = int(input())
ADDR = ("172.24.64.1", 65432)  # gui.get_ip_and_port()  #   # (SERVER, PORT)
gui.quit()

# Cria a conexão TCP com o servidor
client = sck.start_client(ADDR)


def get_GUI_inputs(is_my_turn: bool) -> tuple[int, int]:
    global matrix, text_message
    is_running = True
    selected = [0, 0]
    size = len(matrix)
    text_display = Text_Displayer(Window.current.screen, pygame.Vector2(
        Window.current.screen.get_width()//2, Window.current.screen.get_height()-100), (
        Window.current.screen.get_width()//2, 100), None, text_message, (255, 255, 255))
    with lock:
        card_matrix = Card.get_card_matrix(size, matrix)
    if size < 1 or not is_my_turn:
        draw_cards(card_matrix)
        text_display.set_text_message(msgh.get_current_message())
        text_display.draw()
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
        text_display.set_text_message(msgh.get_current_message())
        text_display.draw()
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
    global matrix, text_message
    is_running = True
    size = len(matrix)
    with lock:
        card_matrix = Card.get_card_matrix(size, matrix)
    text_display = Text_Displayer(Window.current.screen, pygame.Vector2(
        Window.current.screen.get_width()//2, Window.current.screen.get_height()-100), (
        Window.current.screen.get_width()//2, 100), None, text_message, (255, 255, 255))
    card_matrix = Card.get_card_matrix(size, matrix)
    if size < 1:
        draw_cards(card_matrix)
        text_display.set_text_message(msgh.get_current_message())
        text_display.draw()
        pygame.display.update()
        return None
    Window.current.clear()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
    text_display.set_text_message(msgh.get_current_message())
    text_display.draw()
    draw_cards(card_matrix)
    pygame.display.update()


def show_score(disconnected):
    window = tk.Tk()
    window.title("Placar")

    label = tk.Label(window, text="Placar dos jogares\n\n")
    label.pack()
    old_player_list = ''
    while True:
        if len(disconnected) == 1:
            break
        player_list = svc.get_score_list()
        if old_player_list != player_list:
            label.destroy()
            label = tk.Label(window, text="Placar dos jogares\n\n")
            label.pack()
            for jog in player_list.split('\n'):
                label.config(text=label.cget('text') + f"{jog}\n")
            old_player_list = player_list
        window.update()


msg_thread = threading.Thread(target=msgh.get_message, args=(
    disconnected, client, my_turn, matrix))
score_thread = threading.Thread(
    target=show_score, args=(disconnected,))
play_thread = threading.Thread(target=plh.play, args=(
    client, my_turn, disconnected, matrix, get_GUI_inputs, show_inputs, score_thread.start))

msg_thread.daemon = True
msg_thread.start()
play_thread.start()
