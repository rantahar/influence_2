import pygame
import pygame_gui
import math
import random
import pieces
from players import Player, player_colors
from sprites import map_sprites, piece_sprites

window_width = 800
window_height = 600


class Hexagon:
    def __init__(self, center_x, center_y, size):
        self.center_x = center_x
        self.center_y = center_y
        self.size = size
        self.width = math.sqrt(3) * size
        self.height = 2 * size

        # Calculate the vertices of the hexagon
        self.vertices = []
        for i in range(6):
            angle = math.pi * (1/3 * i + 1/6)
            x = center_x + size * math.cos(angle)
            y = center_y + size * math.sin(angle)
            self.vertices.append((x, y))

    def draw(self, screen, tile, debug=False):
        # Draw the hexagon sprite on the screen

        # Scale and draw the tile image. Adjust the size a bit to remove
        # floating point caps
        tile = pygame.transform.scale(tile, (self.width+2, self.height+2))
        screen.blit(tile, (self.center_x - self.width//2-1, self.center_y - self.height//2-1))

        # Draw the outline of the hexagon
        pygame.draw.polygon(screen, (0, 0, 0), self.vertices, 1)

    def draw_piece(self, screen, piece):
        sprite = piece_sprites[piece.get_type()]
        size = self.width*3//5
        sprite = pygame.transform.scale(sprite, (size, size))
        screen.blit(sprite, (self.center_x-size//2, self.center_y-size//2))

    def draw_line(self, screen, dir, color):
        if dir == "rdn":
            x1, y1 = self.vertices[0]
            x2, y2 = self.vertices[1]
            x1, y1, x2, y2 = x1-4, y1-4, x2, y2-4
        elif dir == "sup":
            x1, y1 = self.vertices[1]
            x2, y2 = self.vertices[2]
            x1, y1, x2, y2 = x1-4, y1-4, x2, y2-4
        elif dir == "qdn":
            x1, y1 = self.vertices[2]
            x2, y2 = self.vertices[3]
        elif dir == "rup":
            x1, y1 = self.vertices[3]
            x2, y2 = self.vertices[4]
        elif dir == "sdn":
            x1, y1 = self.vertices[4]
            x2, y2 = self.vertices[5]
        elif dir == "qup":
            x1, y1 = self.vertices[5]
            x2, y2 = self.vertices[0]
        pygame.draw.line(screen, color, (x1, y1), (x2, y2), 8)


class TileMap():
    def __init__(self, rows = 10, cols = 10):
        self.rows = rows
        self.cols = cols

        # Set the dimensions of the hexagons
        self.hex_size = 50
        self.hex_width = math.sqrt(3) * self.hex_size
        self.hex_height = 2 * self.hex_size
        self.board_width = self.hex_width*cols + self.hex_size
        self.board_height = self.hex_height*rows

        # Set the starting position for the grid
        self.start_x = self.hex_size + window_width//2
        self.start_y = self.hex_size + window_height//2

        # Initialize screen and fill with white
        self.surface = pygame.Surface((self.board_width + window_width, self.board_height + window_height))
        self.surface.fill((255, 255, 255))
        self.viewport = pygame.Rect(
            (window_width//2, window_height//2),
            (window_width, window_height)
        )

        # Create a 2D list to store the hexagon objects
        self.hex_grid = []
        for j in range(self.cols):
            self.hex_grid.append([])
            for i in range(self.rows):
                # Calculate the center position of the hexagon
                center_x = self.start_x + j * self.hex_width
                center_y = self.start_y + i * (self.hex_height + self.hex_size)//2
                if i % 2 == 1:
                    center_x += self.hex_width//2
                # Create a hexagon object and add it to the grid
                hexagon = Hexagon(center_x, center_y, self.hex_size)
                self.hex_grid[j].append(hexagon)

    def draw_tile(self, tile):
        # Draw a tile
        hexagon = self.hex_grid[tile.x][tile.y]
        sprite = map_sprites[tile.land_type]
        hexagon.draw(self.surface, sprite)

        for piece in tile.pieces:
            hexagon.draw_piece(self.surface, piece)

        if tile.owner:
            if tile.qup.owner is None or tile.owner != tile.qup.owner:
                hexagon.draw_line(self.surface, "qup", tile.owner.color)
            if tile.rup.owner is None or tile.owner != tile.rup.owner:
                hexagon.draw_line(self.surface, "rup", tile.owner.color)
            if tile.sup.owner is None or tile.owner != tile.sup.owner:
                hexagon.draw_line(self.surface, "sup", tile.owner.color)
            if tile.qdn.owner is None or tile.owner != tile.qdn.owner:
                hexagon.draw_line(self.surface, "qdn", tile.owner.color)
            if tile.sdn.owner is None or tile.owner != tile.sdn.owner:
                hexagon.draw_line(self.surface, "sdn", tile.owner.color)
            if tile.rdn.owner is None or tile.owner != tile.rdn.owner:
                hexagon.draw_line(self.surface, "rdn", tile.owner.color)


class Tile:
    def __init__(self, x, y, tileMap):
        self.x = x
        self.y = y
        self.qup = None
        self.rup = None
        self.sup = None
        self.qdn = None
        self.rdn = None
        self.sdn = None
        self.neighbors = None

        self.land_type = random.choice(['forest', 'meadow'])
        self.owner = None

        self.pieces = []

    def place(self, piece):
        self.pieces.append(piece)

    def __str__(self):
        return f'({self.x}, {self.y})'


class Board:
    def __init__(self, rows=10, cols=10):
        # Maps and draws hexagons on a lattice
        self.tileMap = TileMap(rows, cols)
        self.surface = self.tileMap.surface
        self.viewport = self.tileMap.viewport

        self.rows = rows
        self.cols = cols

        self.tiles = [
            [Tile(x, y, self.tileMap) for y in range(cols)]
            for x in range(cols)
        ]

        for x in range(self.cols):
            for y in range(self.rows):
                tile = self.tiles[x][y]
                if y % 2 == 1:
                    tile.qup = self.tiles[(x+1)%cols][y]
                    tile.sup = self.tiles[x][(y+1)%rows]
                    tile.rup = self.tiles[x][(y+rows-1)%rows]
                    tile.qdn = self.tiles[(x+cols-1)%cols][y]
                    tile.sdn = self.tiles[(x+1)%cols][(y+rows-1)%rows]
                    tile.rdn = self.tiles[(x+1)%cols][(y+1)%rows]
                else:
                    tile.qup = self.tiles[(x+1)%cols][y]
                    tile.sup = self.tiles[(x+cols-1)%cols][(y+1)%rows]
                    tile.rup = self.tiles[(x+cols-1)%cols][(y+rows-1)%rows]
                    tile.qdn = self.tiles[(x+cols-1)%rows][y]
                    tile.sdn = self.tiles[x][(y+rows-1)%rows]
                    tile.rdn = self.tiles[x][(y+1)%rows]

                tile.neighbors = [tile.qup, tile.sup, tile.rup, tile.qdn, tile.sdn, tile.rdn]

    def scroll_right(self, step):
        self.viewport.x -= step

    def scroll_up(self, step):
        self.viewport.y -= step

    def draw(self, screen):
        for x in range(self.cols):
            for y in range(self.rows):
                tile = self.tiles[x][y]
                self.tileMap.draw_tile(tile)
        screen.blit(board.surface, (0, 0), board.viewport)


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


pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
ui_manager = pygame_gui.UIManager((window_width, window_height))

board = Board(10, 10)
tile = board.tiles[2][2]
player = Player()
tile.owner = player
tile.rup.owner = player
tile.rdn.owner = player
city = pieces.City("name", tile)
tile.place(pieces.City("name", tile))
tile.rup.place(pieces.City("name", tile))
tile.rup.rup.place(pieces.City("name", tile))
tile.rdn.place(pieces.City("name", tile))
tile.rdn.rdn.place(pieces.City("name", tile))

window = ActionWindow(ui_manager)


clock = pygame.time.Clock()
running = True
while running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        window.check_events(event)
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

