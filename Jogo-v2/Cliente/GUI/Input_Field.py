from __future__ import annotations
import re
import pygame
from pygame import Vector2
from GUI.Toggle import Toggle


class Input_Field(Toggle):
    current_selected = None

    def __init__(
        self,
        screen: pygame.surface,
        size: Vector2,
        position: Vector2,
        default_text="",
        text_color=(0.0, 0.0, 0.0),
        regular_expression="",
        scale_factor=1,
        padding=(0, 0),
    ):
        super().__init__(
            screen=screen,
            position=position,
            size=size,
            on_clicked=self.do,
            text=default_text,
            text_color=text_color,
            scale_factor=scale_factor,
            image=None,
        )
        self.default_text = default_text
        self.inputed_text = ""
        self.regular_expression = regular_expression
        self.is_selected = False
        self.padding = padding
        self.place_text()

    def on_clicked(self):
        super().on_clicked()
        if self.is_selected:
            pygame.key.start_text_input()
            Input_Field.current_selected = self
        else:
            self.on_deselect()
        pygame.key.set_text_input_rect(self.button.get_rect())

    def on_deselect(self):
        if self.is_selected:
            self.is_selected = False
            pygame.key.stop_text_input()
            Input_Field.current_selected = None
            self.change_color((255, 255, 255))

    def get_key_input(self, event: pygame.event.Event):
        if self.is_selected:
            txt = event.dict["text"]
            if self.regular_expression != "":
                mtch = re.match(self.regular_expression, txt)
                if mtch != None:
                    self.inputed_text += mtch.string
            else:
                self.inputed_text += txt
            print(self.inputed_text)
            self.place_text()

    # pygame.key.stop_text_input()

    def remove_last_char(self):
        if self.is_selected:
            self.inputed_text = self.inputed_text[:-1]
            self.place_text()

    def place_text(self):
        if len(self.inputed_text) > 0:
            self.text_messsage = self.inputed_text
        else:
            self.text_messsage = self.default_text
        self.update_text()
        self.fit_text()
        # self.button = pygame.transform.scale(self.button,size=self.text.get_size())

    def do(self):
        pass
