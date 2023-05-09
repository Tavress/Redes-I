import sys
import threading
import pygame
from GUI.scenes import input_screen, game_screen
from GUI.Window import Window

screen_width = 600
screen_height = 600
is_running = True
lock = threading.RLock()
game_window = None


def start(title):
    global game_window
    if game_window is not None:
        return
    pygame.init()
    game_window = Window((screen_width, screen_height), title)


def quit():
    global game_window
    game_window = None
    pygame.quit()


def get_ip_and_port() -> tuple[str, int]:
    try:
        server, port = input_screen.get_values(
            screen_width, screen_height)
        return (server, int(port))
    except:
        sys.exit()


def get_GUI_inputs(is_my_turn: bool, get_matrix) -> tuple[int, int]:
    return game_screen.get_GUI_inputs(is_my_turn, get_matrix)
