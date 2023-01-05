import pygame
import pygame_gui
import pieces


class TileWindow():
    def __init__(self, manager, tile, player):
        self.tile = tile
        self.buttons = {}
        self.upgrade_button = None
        self.piece = None

        game_piece_window = any([p.show_game_piece_window for p in tile.pieces])
        if game_piece_window:
            self.init_game_piece_window(manager, tile, player)
        else:
            self.init_empty_tile_window(manager, tile, player)

    def init_empty_tile_window(self, manager, tile, player):
        position = tile.get_absolute_position()
        self.window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect(position, (260, 320)),
            manager=manager,
        )
        i = 0
        for key in pieces.piece_classes:
            cls = pieces.piece_classes[key]
            if cls.can_build_at(player, tile):
                self.buttons[key] = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((10, 60*i + 10), (210, 50)),
                    text=cls.title,
                    container=self.window,
                    manager=manager
                )
                i += 1

    def init_game_piece_window(self, manager, tile, player):
        position = tile.get_absolute_position()
        self.window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect(position, (160, 240)),
            manager=manager,
        )
        self.piece = [p for p in tile.pieces if p.show_game_piece_window][0]
        if self.piece.can_upgrade(player):
            self.upgrade_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((10, 10), (100, 50)),
                text='Upgrade',
                container=self.window,
                manager=manager
            )

    def if_clicked_inside(self, event):
        return self.window.check_clicked_inside_or_blocking(event)

    def kill(self):
        self.window.kill()

    def check_events(self, event, player):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            for key in self.buttons:
                if event.ui_element == self.buttons[key]:
                    player.build_at(pieces.piece_classes[key], self.tile)
                    self.window.kill()
            if event.ui_element == self.upgrade_button:
                player.upgrade(self.piece)
                self.window.kill()
