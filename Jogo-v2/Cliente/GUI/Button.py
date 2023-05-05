from pygame import Vector2
from Window import Window
import pygame


class Toggle:
    def __init__(
        self,
        screen: pygame.Surface,
        position: Vector2,
        size: tuple[float, float],
        image: pygame.image,
        on_clicked,
        text="",
        text_color=(0.0, 0.0, 0.0),
        scale_factor=1,
    ):
        if image != None:
            self.image = image
        else:
            self.image = pygame.Surface(size)
            self.image.fill((255, 255, 255))
        self.original_image = self.image.copy()
        self.original_size = Vector2(size[0],size[1])

        if screen == None:
            self.screen = Window.current.screen
        else:
            self.screen = screen
        self.button = pygame.Surface(self.image.get_size())
        pivot_x = self.button.get_width() // 2
        pivot_y = self.button.get_height() // 2
        self.pivot = Vector2(pivot_x, pivot_y)
        self.position = Vector2(position.x - pivot_x, position.y - pivot_y)
        self.change_color((255, 255, 255))

        self.text_messsage = text
        self.text_color = text_color
        self.update_text()
        self.fit_text()
        
        self.is_enabled = True
        self.on_clicked_callback = on_clicked

    def realign_position(self):
        pivot_x = self.button.get_width() // 2
        pivot_y = self.button.get_height() // 2
        self.position = Vector2(self.position.x - pivot_x + self.pivot.x, self.position.y - pivot_y+ self.pivot.y)
        self.pivot = Vector2(pivot_x, pivot_y)

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

    def update_text(self):
        font = pygame.font.SysFont(None, 50)
        
        self.text = font.render(f"{self.text_messsage}", True, self.text_color)
        text_x = (
            self.button.get_width() // 2 + self.position.x - self.text.get_width() // 2
        )
        text_y = (
            self.button.get_height() // 2
            + self.position.y
            - self.text.get_height() // 2
        )

        self.text_pos = (text_x, text_y)

    def on_clicked(self):
        self.is_selected = not self.is_selected
        self.set_color()
        self.on_clicked_callback()

    def draw(self):
        self.screen.blit(self.button, self.position)
        self.update_text()
        self.screen.blit(self.text, self.text_pos)

    def change_color(self, color: pygame.color):
        self.button.fill(color)
        self.button.blit(self.image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.image = self.original_image.copy()
    
    def set_color(self):
        if self.is_selected:
            self.change_color((105, 105, 105))  
        else:
            self.change_color((255, 255, 255))

    def set_enable(self, state: bool):
        self.is_enabled = state

    def fit_text(self):
        if self.text.get_width() > self.original_size.x:
            self.button = pygame.transform.scale(self.button,size=(self.text.get_width(),self.button.get_height()))
        if self.text.get_height() > self.original_size.y:
            self.button = pygame.transform.scale(self.button,size=(self.button.get_width(),self.text.get_height()))
        self.realign_position()


#class Button(Toggle):