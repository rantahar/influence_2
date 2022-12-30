import pygame
import pygame_gui

import pieces


class TileWindow():
    def __init__(self, manager, tile):
        self.tile = tile
        position = tile.get_absolute_position()
        #position = (position[0] - 30, position[1] - 30)
        self.window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect(position, (160, 240)),
            manager=manager,
        )
        self.road_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), (100, 50)),
            text='Path',
            container=self.window,
            manager=manager
        )
        self.city_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 80), (100, 50)),
            text='City',
            container=self.window,
            manager=manager
        )

    def if_clicked_inside(self, event):
        return self.window.check_clicked_inside_or_blocking(event)

    def kill(self):
        self.window.kill()

    def check_events(self, event, player):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.road_button:
                self.tile.place(pieces.Road(self.tile))
                player.food -= pieces.Road.price()["food"]
            if event.ui_element == self.city_button:
                self.tile.place(pieces.Road(self.tile))
                self.tile.place(pieces.City("name", self.tile))
                price = pieces.City.price()
                for key in price:
                    player.__setattr__(key,
                        player.__getattribute__(key) - pieces.City.price()["food"]
                    )
