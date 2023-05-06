import pygame

from GUI.Card import Card


def get_GUI_inputs(size: int, is_my_turn: bool) -> tuple[int, int]:
    selected = [0, 0]
    card_matrix = Card.get_card_matrix(n := 4)
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, j in range(size):
                    if card_matrix[i][j].check_mouse_hover(event) and is_my_turn:
                        card_matrix[i][j].on_clicked()
                        print(i, j)
                        selected = [i, j]

        for cards in card_matrix:
            for card in cards:
                card.draw()
        pygame.display.update()
        return selected
