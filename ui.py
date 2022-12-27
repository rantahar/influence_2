import pygame
import pygame_gui


class ActionWindow():
    def __init__(self, manager):
        self.window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect((100, 100), (160, 240)),
            manager=manager,
        )
        self.hello_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), (100, 50)),
            text='Say Hello',
            container=self.window,
            manager=manager
        )

    def check_events(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.hello_button:
                print('Hello World!')
