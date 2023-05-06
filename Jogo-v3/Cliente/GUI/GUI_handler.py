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
screen_width = 640
screen_height = 480
is_running = True

input_window = None


def start():
    global input_window
    pygame.init()
    input_window = Window(title="Preecha as informações de seu server.")


def quit():
    pygame.quit()


def get_ip_and_port() -> tuple[str, int]:
    server, port = GUI.scenes.input_screen.get_values(
        screen_width, screen_height)
    return (server, int(port))


def show_cards(matrix) -> str:
    result = GUI.scenes.game_screen.get_GUI_inputs(len(matrix), True)
    return f"{result[0]} {result[1]}"
