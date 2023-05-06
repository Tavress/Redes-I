from GUI.Toggle import Toggle


import pygame
from pygame import Surface, Vector2


class Button(Toggle):
    def __init__(
        self,
        screen: Surface,
        position: Vector2,
        size: tuple[float, float],
        image: pygame.image,
        on_clicked,
        text="",
        text_color=(0, 0, 0),
        scale_factor=1,
    ):
        super().__init__(
            screen, position, size, image, on_clicked, text, text_color, scale_factor
        )
        self.is_selected

    def on_clicked(self):
        self.is_selected = True
        self.set_color()
        self.on_clicked_callback()

    def on_mouse_left(self):
        self.is_selected = False
        self.set_color()

    def check_mouse_hover(self, event: pygame.event) -> bool:
        if (
            self.position.x < event.pos[0] < self.position.x + self.button.get_width()
            and self.position.y
            < event.pos[1]
            < self.position.y + self.button.get_height()
            and self.is_enabled
        ):
            return True
        return False
