import pygame
from pygame import Vector2
from GUI.Button import Button
from GUI.Input_Field import Input_Field
from GUI.Text_Displayer import Text_Displayer

from GUI.Window import Window

is_running = True


def change_current_input(inputs: list[Input_Field]):
    if Input_Field.current_selected != None:
        current_index = inputs.index(Input_Field.current_selected)
        Input_Field.current_selected.on_deselect()
        inputs[(current_index + 1) % len(inputs)].on_clicked()


def do_on_click_events(inputs: list[Input_Field], buttons: list[Button], event):
    for inp in inputs:
        if inp.check_mouse_hover(event):
            inp.on_clicked()
        else:
            inp.on_deselect()
    for button in buttons:
        if button.check_mouse_hover(event):
            button.on_clicked()
        else:
            button.on_mouse_left()


def do_on_click_left_events(inputs, buttons, event):
    for button in buttons:
        if button.is_selected:
            button.on_mouse_left()


def submit():
    global is_running
    is_running = False


def get_values(screen_width, screen_height):
    global is_running
    game_title_text = Text_Displayer(
        Window.current.screen,
        Vector2(screen_width // 2, screen_height // 2 - 100),
        [100, 100],
        None,
        "Jogo da Memória",
        (255, 255, 255),
        50)
    input_server = Input_Field(
        Window.current.screen,
        Vector2(200, 20),
        Vector2(screen_width // 2, screen_height // 2),
        "Add Server",
        (0, 0, 0),
        "[0-9]|[.]",
    )
    input_port = Input_Field(
        Window.current.screen,
        Vector2(200, 20),
        Vector2(screen_width // 2, screen_height // 2 + 80),
        "Add Port",
        (0, 0, 0),
        "[0-9]|[.]",
    )
    submit_button = Button(
        Window.current.screen,
        Vector2(screen_width // 2, screen_height // 2 + 160),
        Vector2(200, 20),
        None,
        submit,
        "Submit",
        (255, 0, 0),
    )
    inputs = [input_server, input_port]
    buttons = [submit_button]
    while is_running:
        Window.current.clear()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                return "disconnected"
            elif event.type == pygame.MOUSEBUTTONUP:
                do_on_click_left_events(inputs, buttons, event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                do_on_click_events(inputs, buttons, event)
            elif event.type == pygame.TEXTEDITING or event.type == pygame.TEXTINPUT:
                for inp in inputs:
                    inp.get_key_input(event)
            elif event.type == pygame.KEYDOWN:
                if event.dict["key"] == pygame.K_BACKSPACE:
                    for inp in inputs:
                        inp.remove_last_char()
                if event.dict["key"] == pygame.K_TAB:
                    change_current_input(inputs)

        for inp in inputs:
            inp.draw()
        submit_button.draw()
        game_title_text.draw()
        pygame.display.update()
    return [input_server.inputed_text, input_port.inputed_text]
