from __future__ import annotations
import pygame
from pygame import Vector2
from GUI.Toggle import Toggle
from GUI.Window import Window


class Card(Toggle):
    original_image = pygame.image.load("GUI\\src\\button.png")
    corrected_image = original_image
    screen: pygame.surface

    @staticmethod
    def get_card_matrix(size: int, matrix) -> list[list[Card]]:
        Card.screen = Window.current.screen
        factor = (1 / size) if size > 0 else 1
        real_height = Card.screen.get_height() - 100  # OFFset
        Card.corrected_image = pygame.transform.scale_by(
            Card.original_image, factor)
        cards = []
        for i in range(size):
            cards.append([])
            for j in range(size):
                x = (
                    (i+1) * Card.screen.get_width() / (size) -
                    Card.screen.get_width() / (2 * size)
                )
                y = (
                    (j+1) * real_height / (size) -
                    real_height / (2 * size)
                )
                try:
                    cards[i].append(
                        Card(
                            matrix[i][j],
                            pygame.Vector2(x, y),
                            scale_factor=factor)
                    )
                except:
                    cards[i].append(
                        Card(
                            -1,
                            pygame.Vector2(x, y),
                            scale_factor=factor)
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
            size=Card.corrected_image.get_size(),
            on_clicked=self.reveal,
            text=number,
            text_color=text_color,
            scale_factor=scale_factor,
            image=Card.corrected_image.copy(),
        )

        self.value = number
        self.image = self.original_image.copy()

        self.is_selected = False

    def update(self, value):
        self.value = value
        self.text_messsage = self.value
        self.update_text()

    def reveal(self):
        if self.value == -1:
            raise ValueError("Card hasnt been received.")
