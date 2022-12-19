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

    print(rows, columns)

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


map_tiles = load_tileset('assets/elite_command_art_terrain/tileset.png')[0]


class Hexagon:
    def __init__(self, center_x, center_y, size):
        self.center_x = center_x
        self.center_y = center_y
        self.size = size
        self.width = math.sqrt(3) * size
        self.height = 2 * size
        print(self.width, self.height)

        # Calculate the vertices of the hexagon
        self.vertices = []
        for i in range(6):
            angle = math.pi * (1/3 * i + 1/6)
            x = center_x + size * math.cos(angle)
            y = center_y + size * math.sin(angle)
            self.vertices.append((x, y))

    def draw(self, screen, debug=False):
        # Draw the hexagon sprite on the screen
        tile = map_tiles[0]
        # Scale and draw the tile image. Adjust the size a bit to remove
        # floating point caps
        tile = pygame.transform.scale(tile, (self.width+2, self.height+2))
        screen.blit(tile, (self.center_x - self.width//2-1, self.center_y - self.height//2-1))

        # Draw the outline of the hexagon
        pygame.draw.polygon(screen, (0, 0, 0), self.vertices, 1)


pygame.init()
screen = pygame.display.set_mode((640, 480))
screen.fill((255, 255, 255))


# Set the dimensions of the hexagons
hex_size = 50
hex_width = math.sqrt(3) * hex_size
hex_height = 2 * hex_size

# Set the starting position for the grid
start_x = 50
start_y = 50

# Set the number of rows and columns in the grid
rows = 10
columns = 10


# Create a 2D list to store the hexagon objects
hex_grid = []
for i in range(rows):
    hex_grid.append([])
    for j in range(columns):
        # Calculate the center position of the hexagon
        center_x = start_x + j * hex_width
        center_y = start_y + i * (hex_height + hex_size)//2
        if i % 2 == 1:
            center_x += hex_width//2
        # Create a hexagon object and add it to the grid
        hexagon = Hexagon(center_x, center_y, hex_size)
        hex_grid[i].append(hexagon)


# Draw the hexagonal grid
for i in range(rows):
    for j in range(columns):
        hexagon = hex_grid[i][j]
        hexagon.draw(screen, i==0 and j==0)


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

