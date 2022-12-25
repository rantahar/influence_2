import pygame
import math
import random
import pieces
from sprites import map_sprites, piece_sprites


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
        self.start_x = self.hex_size + 320
        self.start_y = self.hex_size + 240

        # Initialize screen and fill with white
        self.surface = pygame.Surface((self.board_width + 1280, self.board_height + 480))
        self.surface.fill((255, 255, 255))
        self.viewport = pygame.Rect((320, 240), (640, 480))

        # Create a 2D list to store the hexagon objects
        self.hex_grid = []
        for i in range(self.rows):
            self.hex_grid.append([])
            for j in range(self.cols):
                # Calculate the center position of the hexagon
                center_x = self.start_x + j * self.hex_width
                center_y = self.start_y + i * (self.hex_height + self.hex_size)//2
                if i % 2 == 1:
                    center_x += self.hex_width//2
                # Create a hexagon object and add it to the grid
                hexagon = Hexagon(center_x, center_y, self.hex_size)
                self.hex_grid[i].append(hexagon)

    def scroll_right(self, step):
        self.viewport.x -= step

    def scroll_up(self, step):
        self.viewport.y -= step

    def draw_tile(self, tile):
        # Draw a tile
        hexagon = self.hex_grid[tile.x][tile.y]
        sprite = map_sprites[tile.land_type]
        hexagon.draw(self.surface, sprite)

        for piece in tile.pieces:
            hexagon.draw_piece(self.surface, piece)


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
        self.owner = "white"

        self.pieces = []

    def place(self, piece):
        self.pieces.append(piece)


class Board:
    def __init__(self, rows=10, cols=10):
        # Maps and draws hexagons on a lattice
        self.tileMap = TileMap(rows, cols)

        self.rows = rows
        self.cols = cols

        self.tiles = [[Tile(x, y, self.tileMap) for y in range(cols)] for x in range(cols)]

        for x in range(self.cols):
            for y in range(self.rows):
                tile = self.tiles[x][y]
                if x % 2 == 1:
                    tile.qup = self.tiles[(x+1)%cols][y]
                    tile.sup = self.tiles[x][(y+1)%rows]
                    tile.rup = self.tiles[(x+cols-1)%cols][(y+rows-1)%rows]
                    tile.qdn = self.tiles[(x+cols-1)%cols][y]
                    tile.sdn = self.tiles[x][(y+rows-1)%rows]
                    tile.rdn = self.tiles[(x+1)%cols][(y+1)%rows]
                else:
                    tile.qup = self.tiles[(x+1)%cols][y]
                    tile.sup = self.tiles[(x+cols-1)%cols][(y+1)%rows]
                    tile.rup = self.tiles[x][(y+rows-1)%rows]
                    tile.qdn = self.tiles[(x+cols-1)%rows][y]
                    tile.sdn = self.tiles[(x+1)%rows][(y+rows-1)%rows]
                    tile.rdn = self.tiles[x][(y+1)%rows]

                tile.neighbors = [tile.qup, tile.sup, tile.rup, tile.qdn, tile.sdn, tile.rdn]

    def draw(self):
        for x in range(self.cols):
            for y in range(self.rows):
                tile = self.tiles[x][y]
                self.tileMap.draw_tile(tile)

    def new_city(self, x, y):
        self.tiles[x][y].new_city()


pygame.init()
screen = pygame.display.set_mode((640, 480))


board = Board(10, 10)
board.tiles[2][2].place(pieces.City("name", board.tiles[2][2]))
board.draw()

tileMap = board.tileMap
screen.blit(tileMap.surface, (0, 0), tileMap.viewport)


panel_surface = pygame.Surface((200, 480))
panel_rect = panel_surface.get_rect()
panel_rect.topleft = (0, 0)

# Set the background color for the panel
panel_surface.fill((200, 200, 200))

# Draw some options on the panel surface
font = pygame.font.Font(None, 36)
text_surface = font.render("Option 1", True, (0, 0, 0))
text_rect = text_surface.get_rect()
text_rect.topleft = (10, 10)
panel_surface.blit(text_surface, text_rect)

text_surface = font.render("Option 2", True, (0, 0, 0))
text_rect = text_surface.get_rect()
text_rect.topleft = (10, 50)
panel_surface.blit(text_surface, text_rect)


clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # scrolling:
    scroll_right = 0
    scroll_up = 0
    if keys[pygame.K_LEFT]:
        scroll_right += 5
    if keys[pygame.K_RIGHT]:
        scroll_right -= 5
    if keys[pygame.K_UP]:
        scroll_up += 5
    if keys[pygame.K_DOWN]:
        scroll_up -= 5
    # Update game state here
    tileMap.scroll_right(scroll_right)
    tileMap.scroll_up(scroll_up)
    # Render game screen here
    screen.blit(tileMap.surface, (0, 0), tileMap.viewport)
    screen.blit(panel_surface, panel_rect)
    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)


pygame.quit()

