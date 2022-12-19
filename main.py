import pygame
import math


def load_tileset(filename):
    # Load the map tiles
    tileset = pygame.image.load(filename)
    tileset_width, tileset_height = tileset.get_size()
    tile_height = 34
    tile_width = 32

    rows = tileset_height // tile_height
    columns = tileset_width // tile_width

    # Create a 2D list to store the tiles
    tiles = []
    for i in range(rows):
        tiles.append([])
        for j in range(columns):
            x = j * tile_width
            y = i * tile_height
            # Create a surface for the tile
            tile_surface = pygame.Surface((tile_width, tile_height))
            # Copy the tile image from the tileset image to the tile surface
            tile_surface.blit(tileset, (0, 0), (x, y, tile_width, tile_height))
            # Set the colorkey for the tile surface
            tile_surface.set_colorkey((0, 0, 0))
            # Add the tile surface to the list of tiles
            tiles[i].append(tile_surface)

    return tiles


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

    def draw(self, screen, map_tiles, debug=False):
        # Draw the hexagon sprite on the screen
        tile = map_tiles[0]
        # Scale and draw the tile image. Adjust the size a bit to remove
        # floating point caps
        tile = pygame.transform.scale(tile, (self.width+2, self.height+2))
        screen.blit(tile, (self.center_x - self.width//2-1, self.center_y - self.height//2-1))

        # Draw the outline of the hexagon
        pygame.draw.polygon(screen, (0, 0, 0), self.vertices, 1)


class HexMap():
    def __init__(self, rows = 10, cols = 10):
        self.rows = rows
        self.cols = cols

        # Set the dimensions of the hexagons
        self.hex_size = 50
        self.hex_width = math.sqrt(3) * self.hex_size
        self.hex_height = 2 * self.hex_size

        # Set the starting position for the grid
        self.start_x = self.hex_size
        self.start_y = self.hex_size

        # Initialize screen and fill with white
        self.screen = pygame.display.set_mode((640, 480))
        self.screen.fill((255, 255, 255))

        self.map_tiles = load_tileset('assets/elite_command_art_terrain/tileset.png')[0]

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

    def draw_tile(self, tile):
        # Draw a tile
        hexagon = self.hex_grid[tile.x][tile.y]
        hexagon.draw(self.screen, self.map_tiles)


class Tile:
    def __init__(self, x, y, hexMap):
        self.x = x
        self.y = y
        self.qup = None
        self.rup = None
        self.sup = None
        self.qdn = None
        self.rdn = None
        self.sdn = None
        self.neighbors = None


class Board:
    def __init__(self, rows=10, cols=10):
        # Maps and draws hexagons on a lattice
        self.hexMap = HexMap(rows, cols)

        self.rows = rows
        self.cols = cols

        self.tiles = [[Tile(x, y, self.hexMap) for y in range(cols)] for x in range(cols)]

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
                self.hexMap.draw_tile(tile)


pygame.init()

board = Board(10, 10)
board.draw()

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Update game state here
    # Render game screen here
    pygame.display.update()
    clock.tick(60)


pygame.quit()

