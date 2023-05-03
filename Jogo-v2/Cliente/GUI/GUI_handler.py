import pygame
from card import *



# initialize Pygame
pygame.init()

# set the screen dimensions
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jogo da Memória")

Card.set_screen(screen)
cards = Card.get_card_matrix(n:=4)

# main game loop
running = True
while running:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # check if the button was clicked
            for i in range(n):
                for j in range(n):
                    if cards[i][j].check_mouse_hover(event):
                        cards[i][j].on_clicked()
                        print(i,j)

    for i in range(n):
        for card in cards[i]:
            card.draw()
    # update the screen
    pygame.display.update()

# quit Pygame
pygame.quit()