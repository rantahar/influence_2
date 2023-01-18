import pygame
import pygame_gui
import pieces

apple = pygame.image.load('assets/apple_paint.png')
apple = pygame.transform.scale(apple, (32, 32))
apple.set_colorkey((0, 0, 0))
labor = pygame.image.load('assets/labor_paint.png')
labor = pygame.transform.scale(labor, (32, 32))
labor.set_colorkey((0, 0, 0))


class TileWindow():
    def __init__(self, manager, tile, player):
        self.tile = tile
        self.buttons = {}
        self.upgrade_buttons = {}
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
                price = cls.price()
                panel = pygame_gui.elements.UIPanel(
                    pygame.Rect((10, 80*i + 10), (210, 70)),
                    manager=manager,
                    container=self.window
                )
                pygame_gui.elements.UILabel(
                    relative_rect=pygame.Rect((0, 0), (140, 40)),
                    text=cls.title,
                    manager=manager,
                    container=panel
                )
                if "labor" in price.keys():
                    pygame_gui.elements.UIImage(
                        relative_rect=pygame.Rect((0, 40), (32, 32)),
                        image_surface=labor,
                        manager=manager,
                        container=panel
                    )
                    pygame_gui.elements.UILabel(
                        relative_rect=pygame.Rect((20, 40), (40,32)),
                        text=f":{price['labor']}",
                        manager=manager,
                        container=panel
                    )
                if "food" in price.keys():
                    pygame_gui.elements.UIImage(
                        relative_rect=pygame.Rect((60, 40), (32, 32)),
                        image_surface=apple,
                        manager=manager,
                        container=panel
                    )
                    pygame_gui.elements.UILabel(
                        relative_rect=pygame.Rect((80, 40), (40,32)),
                        text=f":{price['food']}",
                        manager=manager,
                        container=panel
                    )
                self.buttons[key] = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((150, 10), (50, 50)),
                    text="Buy",
                    container=panel,
                    manager=manager
                )
                i += 1

    def init_game_piece_window(self, manager, tile, player):
        position = tile.get_absolute_position()
        self.window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect(position, (260, 320)),
            manager=manager,
        )
        self.piece = [p for p in tile.pieces if p.show_game_piece_window][0]
        if self.piece.get_owner() is player:
            upgrades = self.piece.get_upgrades()
            i = 0
            for key in upgrades.keys():
                price = upgrades[key]["price"]
                if player.can_afford(price) and self.piece.can_upgrade(key):
                    panel = pygame_gui.elements.UIPanel(
                        pygame.Rect((10, 80*i + 10), (210, 70)),
                        manager=manager,
                        container=self.window
                    )
                    pygame_gui.elements.UILabel(
                        relative_rect=pygame.Rect((0, 0), (140, 40)),
                        text=key,
                        manager=manager,
                        container=panel
                    )
                    if "labor" in price.keys():
                        pygame_gui.elements.UIImage(
                            relative_rect=pygame.Rect((0, 40), (32, 32)),
                            image_surface=labor,
                            manager=manager,
                            container=panel
                        )
                        pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect((20, 40), (40,32)),
                            text=f":{price['labor']}",
                            manager=manager,
                            container=panel
                        )
                    if "food" in price.keys():
                        pygame_gui.elements.UIImage(
                            relative_rect=pygame.Rect((60, 40), (32, 32)),
                            image_surface=apple,
                            manager=manager,
                            container=panel
                        )
                        pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect((80, 40), (40,32)),
                            text=f":{price['food']}",
                            manager=manager,
                            container=panel
                        )
                    self.upgrade_buttons[key] = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((150, 10), (50, 50)),
                        text="Buy",
                        container=panel,
                        manager=manager
                    )
                    i += 1

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
            for key in self.upgrade_buttons:
                if event.ui_element == self.upgrade_buttons[key]:
                    player.upgrade(self.piece, key)
                    self.window.kill()
