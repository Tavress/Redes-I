import os
import tkinter as tk
from pygame._sdl2 import messagebox
import pyautogui
import pygame

from GUI.Window import Window

HEADER = 64
FORMAT = 'utf-8'


score_list = ''


def limpaTela():

    os.system('cls' if os.name == 'nt' else 'clear')


def send(msg, client):
    if msg == None:
        return
    try:
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)
    except:
        return


def receive(client):
    try:
        msg_length = client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = client.recv(msg_length).decode(FORMAT)

        return msg
    except:
        return None


def check_event_message(msg, client, my_turn, disconnected, matrix):
    global score_list
    if msg == 'your_turn':
        if len(my_turn) == 0:
            my_turn.append(1)
            messagebox(
                "Sua vez!",
                "Sua vez de jogar =)",
                info=True,
                buttons=("OK",),
            )
            # pygame.display.set_caption("Sua vez de jogar.")
            # Window.current.change_title("Sua vez de jogar.")
        return True
    elif msg == 'end_of_your_turn':
        if len(my_turn) == 1:
            my_turn.remove(1)
            messagebox(
                "Acabou sua vez",
                "Vez do adversário jogar >=)",
                info=True,
                buttons=("OK",),
            )
            # pygame.display.set_caption("Espere seu turno.")
        return True
    elif msg == 'limpa_tela':
        limpaTela()
        matrix.clear()
        return True
    elif msg == 'game_over':
        client.close()
        disconnected.append(1)
        return True
    elif msg == 'refused_connection':
        disconnected.append(1)
        return True
    elif msg == 'matrix':
        receive_matrix(matrix, client)
        return True
    elif msg.startswith("P="):
        jog = msg.split("P=")[1]
        score_list = jog
        return True
    return False


def get_score_list():
    global score_list
    return score_list


def receive_matrix(matrix, client):
    dim = int(receive(client))
    for i in range(0, dim):
        line = []
        line_as_string = receive(client)
        line = line_as_string.split(',')
        line.pop(0)
        if len(line) > 0:
            matrix.append(line)
