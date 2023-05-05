import pygame
from Card import *
from Input_Field import Input_Field
from Window import Window

def select_server(server : str, port : str):
    print("TODO")

# initialize Pygame
pygame.init()

# set the screen dimensions
screen_width = 640
screen_height = 480
input_window = Window(title="Jogo da Memória")
card_matrix = Card.get_card_matrix(n := 4)

# main game loop
is_running = True
is_my_turn = True

input_server = Input_Field(Window.current.screen,Vector2(200,20),Vector2(screen_width//2,screen_height//2),"Add Server", (0,0,0),"[0-9]|[.]")
input_port = Input_Field(Window.current.screen,Vector2(200,20),Vector2(screen_width//2,screen_height//2 + 80),"Add Port", (0,0,0),"[0-9]|[.]")
submit_button = Toggle(Window.current.screen,Vector2(screen_width//2,screen_height//2 + 160),Vector2(200,20), None,select_server,"Submit",(255,0,0))
inputs = [input_server,input_port]
while is_running:
    Window.current.clear()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for inp in inputs:
                if inp.check_mouse_hover(event):
                    inp.on_clicked()
                else:
                    inp.on_deselect()
        elif event.type == pygame.TEXTEDITING or event.type == pygame.TEXTINPUT:
            for inp in inputs:
                    inp.get_key_input(event)  
        elif event.type == pygame.KEYDOWN:
            if event.dict["key"] == pygame.K_BACKSPACE:
                for inp in inputs:
                    inp.remove_last_char()  
    
    for inp in inputs:
        inp.draw()
    submit_button.draw() 
    pygame.display.update()


while is_running:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # check if the button was clicked
            for i,j in range(n):
                if card_matrix[i][j].check_mouse_hover(event) and is_my_turn:
                    card_matrix[i][j].on_clicked()
                    print(i, j)

    for cards in card_matrix:
        for card in cards:
            card.draw()
    # update the screen
    pygame.display.update()

# quit Pygame
pygame.quit()
