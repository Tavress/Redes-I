from __future__ import annotations
import pygame


class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def to_turple(self) -> tuple[float, float]:
        return (self.x, self.y)


class Card:
    original_image = pygame.image.load("cliente\\GUI\\src\\button.png")
    screen: pygame.Surface

    @staticmethod
    def set_screen(new_screen: pygame.surface):
        Card.screen = new_screen

    @staticmethod
    def get_card_matrix(size: int) -> list[list[Card]]:
        Card.original_image = pygame.transform.scale_by(Card.original_image, 1 / size)
        cards = []
        for i in range(size):
            cards.append([])
            for j in range(size):
                x = (
                    i * Card.screen.get_width() / (size)
                    + 2 * Card.original_image.get_width()
                )
                y = (
                    j * Card.screen.get_height() / (size)
                    + Card.original_image.get_height()
                )
                cards[i].append(
                    Card(
                        0,
                        Card.screen,
                        Vector(x, y),
                    )
                )
        return cards

    def __init__(
        self,
        number: int,
        screen: pygame.Surface,
        position: Vector,
        text_color=(0.0, 0.0, 0.0),
        scale_factor=1,
    ):
        self.value = number
        self.image = self.original_image.copy()
        self.screen = screen

        self.button = pygame.Surface(self.image.get_size())
        pivot_x = self.button.get_width() // 2
        pivot_y = self.button.get_height() // 2
        self.pivot = Vector(pivot_x, pivot_y)
        self.button_pos = Vector(position.x - pivot_x, position.y - pivot_y)
        self.change_color((255, 255, 255))

        font = pygame.font.SysFont(None, 50)

        self.text_color = text_color
        self.text = font.render(f"{self.value}", True, (0, 0, 0))
        text_x = (
            self.button.get_width() // 2
            + self.button_pos.x
            - self.text.get_width() // 2
        )
        text_y = (
            self.button.get_height() // 2
            + self.button_pos.y
            - self.text.get_height() // 2
        )

        self.text_pos = (text_x, text_y)

        self.is_selected = False

    def check_mouse_hover(self, event: pygame.event) -> bool:
        if (
            self.button_pos.x
            < event.pos[0]
            < self.button_pos.x + self.button.get_width()
            and self.button_pos.y
            < event.pos[1]
            < self.button_pos.y + self.button.get_height()
        ):
            return True
        return False

    def on_clicked(self):
        if self.is_selected:
            self.change_color((255, 255, 255))
        else:
            self.change_color((105, 105, 105))
        self.is_selected = not self.is_selected

    def draw(self):
        self.screen.blit(self.button, self.button_pos.to_turple())
        self.screen.blit(self.text, self.text_pos)

    def change_color(self, color: pygame.color):
        self.button = pygame.Surface(self.image.get_size())
        self.button.fill(color)
        self.button.blit(self.image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.image = self.original_image.copy()
