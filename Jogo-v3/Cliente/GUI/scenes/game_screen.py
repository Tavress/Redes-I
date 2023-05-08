import threading
import pygame
from GUI.Text_Displayer import Text_Displayer
import GUI.scenes.game_screen
from GUI.Card import Card
from GUI.Window import Window
import message_handler as msgh
from main import get_matrix
lock = threading.RLock()


def get_GUI_inputs(is_my_turn: bool) -> tuple[int, int]:
    matrix = get_matrix()
    is_running = True
    selected = [0, 0]
    size = len(matrix)
    text_display = Text_Displayer(Window.current.screen, pygame.Vector2(
        Window.current.screen.get_width()//2, Window.current.screen.get_height()-80), (
        Window.current.screen.get_width()//2, 100), None, msgh.get_current_message(), (255, 255, 255))
    with lock:
        card_matrix = Card.get_card_matrix(size, matrix)
    if size < 1 or not is_my_turn:
        text_display.set_text_message(msgh.get_current_message())
        text_display.draw()
        pygame.display.update()
        return None
    while is_running:
        Window.current.clear()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.dict["key"] == pygame.K_KP_ENTER or event.dict["key"] == pygame.K_RETURN:
                    return ""
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


def draw_cards(card_matrix: list[list[Card]]):
    matrix = get_matrix()
    size = len(card_matrix)
    for i in range(size):
        for j in range(size):
            try:
                card_matrix[i][j].update(matrix[i][j])
                card_matrix[i][j].draw()
            except:
                pass


def show_inputs():
    matrix = get_matrix()
    is_running = True
    size = len(matrix)
    card_matrix = Card.get_card_matrix(size, matrix)
    text_display = Text_Displayer(Window.current.screen, pygame.Vector2(
        Window.current.screen.get_width()//2, Window.current.screen.get_height()-80), (
        Window.current.screen.get_width()//2, 100), None, msgh.get_current_message(), (255, 255, 255))
    if size < 1:
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
