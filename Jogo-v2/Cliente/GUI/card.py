from __future__ import annotations
import pygame
from pygame import Vector2
from Button import Toggle
from Window import Window


class Card(Toggle):
    original_image = pygame.image.load("GUI\\src\\button.png")
    screen : pygame.surface

    @staticmethod
    def get_card_matrix(size: int) -> list[list[Card]]:
        Card.screen = Window.current.screen
        Card.original_image = pygame.transform.scale_by(Card.original_image, 1 / size)
        cards = []
        for i in range(size):
            cards.append([])
            for j in range(size):
                x = (
                    i * Card.screen.get_width() / size
                    + 2 * Card.original_image.get_width()
                )

                y = (
                    j * Card.screen.get_height() / size
                    + Card.original_image.get_height()
                )
                cards[i].append(
                    Card(
                        0,
                        pygame.Vector2(x, y),
                    )
                )
        return cards

    def __init__(
        self,
        number: int,
        position: pygame.Vector2,
        text_color=(0.0, 0.0, 0.0),
        scale_factor=1,
    ):
        super().__init__(
            screen=Card.screen,
            position=position,
            size=Card.original_image.get_size(),
            on_clicked = self.reveal,
            text=number,
            text_color=text_color,
            scale_factor=scale_factor,
            image=Card.original_image.copy(),
        )

        self.value = number
        self.image = self.original_image.copy()

        self.is_selected = False

    def reveal(self):
        pass
