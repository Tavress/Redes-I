from pygame import Vector2
from GUI.Window import Window
import pygame


class Text_Displayer:
    def __init__(
        self,
        screen: pygame.Surface,
        position: Vector2,
        size: tuple[float, float],
        on_clicked,
        text="",
        text_color=(0.0, 0.0, 0.0),
    ):
        self.original_size = Vector2(size[0], size[1])

        if screen == None:
            self.screen = Window.current.screen
        else:
            self.screen = screen

        self.text_message = text
        self.text_color = text_color
        pivot_x = size[0] // 2
        pivot_y = size[1] // 2
        self.pivot = Vector2(pivot_x, pivot_y)
        self.position = Vector2(position.x - pivot_x, position.y - pivot_y)
        self.font = pygame.font.SysFont(None, 50)

        self.text = self.font.render(
            f"{self.text_message}", True, self.text_color)
        self.realign_position()

        self.is_enabled = True
        self.is_selected = True
        self.on_clicked_callback = on_clicked

    def realign_position(self):
        self.text = self.font.render(
            f"{self.text_message}", True, self.text_color)
        pivot_x = self.text.get_width() // 2
        pivot_y = self.text.get_height() // 2
        self.position = Vector2(
            self.position.x - pivot_x + self.pivot.x,
            self.position.y - pivot_y + self.pivot.y,
        )
        self.pivot = Vector2(pivot_x, pivot_y)

    def check_mouse_hover(self, event: pygame.event) -> bool:
        if (
            self.position.x < event.pos[0] < self.position.x +
                self.text.get_width()
            and self.position.y
            < event.pos[1]
            < self.position.y + self.text.get_height()
            and self.is_enabled
        ):
            return True
        return False

    def on_clicked(self):
        self.is_selected = not self.is_selected
        self.on_clicked_callback()

    def draw(self):
        self.realign_position()
        self.screen.blit(self.text, self.position)

    def set_enable(self, state: bool):
        self.is_enabled = state

    def set_text_message(self, message: str):
        self.text_message = message
