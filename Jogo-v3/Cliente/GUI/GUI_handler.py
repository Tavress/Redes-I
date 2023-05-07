import pygame
import GUI.scenes.input_screen
import GUI.scenes.game_screen
from GUI.Button import Button
from GUI.Toggle import *
from GUI.Card import Card
from GUI.Input_Field import Input_Field
from GUI.Window import Window

# initialize Pygame

# set the screen dimensions
screen_width = 1280
screen_height = 960
is_running = True

input_window = None


def start(title):
    global input_window
    pygame.init()
    input_window = Window((screen_width, screen_height), title)


def quit():
    pygame.quit()


def get_ip_and_port() -> tuple[str, int]:
    server, port = GUI.scenes.input_screen.get_values(
        screen_width, screen_height)
    return (server, int(port))


def show_cards(matrix) -> str:
    global input_window
    result = GUI.scenes.game_screen.get_GUI_inputs(matrix, True)
    if result is None:
        return ""
    return f"{result[0]} {result[1]}"
