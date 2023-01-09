import pygame
import pygame_gui
import pieces
from players import Player, AIPlayer
from board import Board
from itertools import cycle
from ui import TileWindow


window_width = 800
window_height = 600


pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
ui_manager = pygame_gui.UIManager((window_width, window_height))
board = Board(10, 10, window_width, window_height)

textbox = pygame_gui.elements.UITextBox(
    html_text="Hello",
    relative_rect=(-2, -2, window_width+4, 50),
)


tile = board.tiles[2][2]
player = Player()
tile.owner = player
tile.land_type = "meadow"
city = pieces.City(tile, player)

tile = board.tiles[2][5]
player = AIPlayer()
tile.owner = player
tile.land_type = "meadow"
city = pieces.City(tile, player)

player_turns = cycle(Player.all)
active_player = None


def start_turn():
    global active_player

    for city in pieces.City.all:
        if city.owner is active_player:
            city.change_owner()
    pieces.find_tile_owners(board)

    # next player
    active_player = next(player_turns)

    # count resources:
    active_player.resources["labor"] = 0
    active_player.resources["food"] = 0
    for piece in pieces.GamePiece.all:
        if piece.tile.owner is active_player:
            production = piece.production()
            for key in production.keys():
                if key not in player.resources:
                    active_player.resources[key] = production[key]
                else:
                    active_player.resources[key] += production[key]

    # Progress any ongoing projects
    labor = active_player.resources["labor"]
    for project in pieces.Project.all[:]:
        if project.get_owner() is active_player:
            labor = project.progress(labor)
    for city in pieces.City.all:
        labor = city.check_queue(labor)
    active_player.resources["labor"] = labor

    textbox.set_text(f"player: {active_player.name}, labor: {active_player.resources['labor']}, food: {active_player.resources['food']}")


start_turn()


end_turn_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((window_width - 110, window_height-60), (100, 50)),
    text='End turn',
    manager=ui_manager
)


windows = []
clock = pygame.time.Clock()
running = True
while running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        consumed = ui_manager.process_events(event)

        if consumed:
            break

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == end_turn_button:
                start_turn()

        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()

            clicked_tile = board.check_tile_clicked(event.pos)
            if clicked_tile:
                for window in windows:
                    if type(window) == TileWindow:
                        window.kill()
                window = TileWindow(ui_manager, clicked_tile, active_player)
                windows.append(window)

        for window in windows:
            window.check_events(event, active_player)
        ui_manager.process_events(event)


    textbox.set_text(f"player: {active_player.name}, labor: {active_player.resources['labor']}, food: {active_player.resources['food']}")

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

    # AI actions
    if active_player.is_ai:
        active_player.take_turn(board)
        start_turn()

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

