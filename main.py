import pygame
import pygame_gui
import math
import random
import pieces
from players import Player
from board import Board

window_width = 800
window_height = 600


def end_turn(board):
    print("Turn ended!")


pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
ui_manager = pygame_gui.UIManager((window_width, window_height))
board = Board(10, 10, window_width, window_height)

tile = board.tiles[2][2]
player = Player()
tile.owner = player
city = pieces.City("name", tile)
city.level = 2
tile.place(city)
tile = board.tiles[2][5]
player = Player()
tile.owner = player
city = pieces.City("name", tile)
tile.place(city)

print(tile.rup.influences)

end_turn_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((window_width - 110, window_height-60), (100, 50)),
    text='End turn',
    manager=ui_manager
)


clock = pygame.time.Clock()
running = True
while running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == end_turn_button:
                end_turn(board)

        #window.check_events(event)
        ui_manager.process_events(event)

    keys = pygame.key.get_pressed()

    # scrolling:
    scroll_right = 0
    scroll_up = 0
    if keys[pygame.K_LEFT]:
        scroll_right += window_width//100
    if keys[pygame.K_RIGHT]:
        scroll_right -= window_width//100
    if keys[pygame.K_UP]:
        scroll_up += window_height//100
    if keys[pygame.K_DOWN]:
        scroll_up -= window_height//100


    # Update game state here
    board.scroll_right(scroll_right)
    board.scroll_up(scroll_up)

    ui_manager.update(time_delta)

    # Render game screen here
    board.draw(screen)
    ui_manager.draw_ui(screen)

    pygame.display.update()
    clock.tick(60)


pygame.quit()

