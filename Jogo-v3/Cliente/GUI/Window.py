from __future__ import annotations
import pygame


class Window:
    current: Window

    def __init__(self, size=(640, 480), title="Tela"):
        self.size = pygame.Vector2(size[0], size[1])
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption(title)
        Window.current = self

    def clear(self):
        self.screen.fill((0, 0, 0))
