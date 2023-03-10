import pygame
import math
import random
from sprites import map_sprites, piece_sprites
import pieces
import maps
from players import Player, AIPlayer


class Hexagon:
    def __init__(self, center_x, center_y, size):
        self.center_x = center_x
        self.center_y = center_y
        self.size = size
        self.width = math.sqrt(3) * size
        self.height = 2 * size

        self.rect = None

        # Calculate the vertices of the hexagon
        self.vertices = []
        for i in range(6):
            angle = math.pi * (1/3 * i + 1/6)
            x = center_x + size * math.cos(angle)
            y = center_y + size * math.sin(angle)
            self.vertices.append((x, y))

    def draw(self, screen, sprite, debug=False):
        # Draw the hexagon sprite on the screen

        # Scale and draw the tile image. Adjust the size a bit to remove
        # floating point caps
        sprite = pygame.transform.scale(sprite, (self.width+2, self.height+2))
        self.rect = screen.blit(sprite, (self.center_x - self.width//2-1, self.center_y - self.height//2-1))

        # Draw the outline of the hexagon
        pygame.draw.polygon(screen, (0, 0, 0), self.vertices, 1)

    def draw_piece(self, screen, piece):
        sprite = piece_sprites[piece.get_sprite_id()]
        if piece.rotations is None:
            size = self.width
            sprite = pygame.transform.scale(sprite, (size, size))
            screen.blit(sprite, (self.center_x-size//2, self.center_y-size//2))
        else:
            # These are roads. TODO: Should set the size in the sprite sheet to be
            # consistent and general
            sprite = pygame.transform.scale(sprite, (self.width, self.height))
            for rot in piece.rotations:
                rotated = pygame.transform.rotate(sprite, rot)
                width, height = rotated.get_size()
                screen.blit(rotated, (self.center_x-width//2, self.center_y-height//2))

    def draw_line(self, screen, dir, color):
        if dir == "rdn":
            x1, y1 = self.vertices[0]
            x2, y2 = self.vertices[1]
            x1, y1, x2, y2 = x1-4, y1-4, x2, y2-4
        elif dir == "sup":
            x1, y1 = self.vertices[1]
            x2, y2 = self.vertices[2]
            x1, y1, x2, y2 = x1, y1-4, x2+4, y2-4
        elif dir == "qdn":
            x1, y1 = self.vertices[2]
            x2, y2 = self.vertices[3]
            x1, y1, x2, y2 = x1+4, y1, x2+4, y2-4
        elif dir == "rup":
            x1, y1 = self.vertices[3]
            x2, y2 = self.vertices[4]
            x1, y1, x2, y2 = x1+4, y1-4, x2+4, y2+4
        elif dir == "sdn":
            x1, y1 = self.vertices[4]
            x2, y2 = self.vertices[5]
            x1, y1, x2, y2 = x1, y1+4, x2-4, y2+4
        elif dir == "qup":
            x1, y1 = self.vertices[5]
            x2, y2 = self.vertices[0]
            x1, y1, x2, y2 = x1-4, y1+4, x2-4, y2-4
        pygame.draw.line(screen, color, (x1, y1), (x2, y2), 8)


class TileMap():
    def __init__(self, rows=10, cols=10, window_width = 800, window_height = 600):
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
        self.overlay_surface = pygame.Surface((self.board_width + window_width, self.board_height + window_height))
        self.overlay_surface.set_colorkey((0,0,0))
        self.overlay_surface.fill((0,0,0))
        self.overlay_surface.set_alpha(100)

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
                hexagon.draw_line(self.overlay_surface, "qup", tile.owner.color)
            if tile.rup.owner is None or tile.owner != tile.rup.owner:
                hexagon.draw_line(self.overlay_surface, "rup", tile.owner.color)
            if tile.sup.owner is None or tile.owner != tile.sup.owner:
                hexagon.draw_line(self.overlay_surface, "sup", tile.owner.color)
            if tile.qdn.owner is None or tile.owner != tile.qdn.owner:
                hexagon.draw_line(self.overlay_surface, "qdn", tile.owner.color)
            if tile.sdn.owner is None or tile.owner != tile.sdn.owner:
                hexagon.draw_line(self.overlay_surface, "sdn", tile.owner.color)
            if tile.rdn.owner is None or tile.owner != tile.rdn.owner:
                hexagon.draw_line(self.overlay_surface, "rdn", tile.owner.color)

    def draw(self, screen):
        screen.blit(self.surface, (0, 0), self.viewport)
        screen.blit(self.overlay_surface, (0, 0), self.viewport)

    def clear(self):
        self.overlay_surface.fill((0, 0, 0))


class Tile:
    def __init__(self, x, y, board, land_type):
        self.x = x
        self.y = y
        self.qup = None
        self.rup = None
        self.sup = None
        self.qdn = None
        self.rdn = None
        self.sdn = None
        self.neighbors = None
        self.board = board
        self.land_type = land_type

        self.hexagon = self.board.tileMap.hex_grid[x][y]

        if y % 2 == 1:
            self.doubled_x = 2*x+1
        else:
            self.doubled_x = 2*x


        self.owner = None
        self.influences = {}

        self.pieces = []

    def distance_to(self, tile):
        dx = abs(self.doubled_x - tile.doubled_x)
        dy = abs(self.y - tile.y)
        return dy + max(0, (dx-dy))/2

    def distance_to_point(self, point):
        return math.sqrt(
            (point[0] - self.hexagon.center_x)**2 +
            (point[1] - self.hexagon.center_y)**2
        )

    def get_absolute_position(self):
        return (self.hexagon.center_x - self.board.viewport.x,
                self.hexagon.center_y - self.board.viewport.y)

    def get_neighbour_closest_to_point(self, point):
        dist = self.distance_to_point(point)
        for nb in self.neighbors:
            d2 = nb.distance_to_point(point)
            if d2 < dist:
                return nb
        return self

    def place(self, piece):
        self.pieces.append(piece)
        piece.update()
        for tile in self.neighbors:
            for piece in tile.pieces:
                piece.update()
        pieces.find_tile_owners(self.board)

    def __str__(self):
        return f'({self.x}, {self.y})'


class Board:
    def __init__(self, window_width = 800, window_height = 600, map = "default"):
        # Maps and draws hexagons on a lattice
        land_types, players = maps.load_map(f"assets/maps/{map}.txt")
        self.rows = len(land_types)
        self.cols = len(land_types[0])

        self.tileMap = TileMap(self.rows, self.cols)
        self.viewport = self.tileMap.viewport

        self.tiles = [
            [Tile(x, y, self, land_types[y][x]) for y in range(self.rows)]
            for x in range(self.cols)
        ]

        self.all_tiles = [tile for row in self.tiles for tile in row]

        for x in range(self.cols):
            for y in range(self.rows):
                tile = self.tiles[x][y]
                if y % 2 == 1:
                    tile.qup = self.tiles[(x+1)%self.cols][y]
                    tile.sup = self.tiles[x][(y+1)%self.rows]
                    tile.rup = self.tiles[x][(y+self.rows-1)%self.rows]
                    tile.qdn = self.tiles[(x+self.cols-1)%self.cols][y]
                    tile.sdn = self.tiles[(x+1)%self.cols][(y+self.rows-1)%self.rows]
                    tile.rdn = self.tiles[(x+1)%self.cols][(y+1)%self.rows]
                else:
                    tile.qup = self.tiles[(x+1)%self.cols][y]
                    tile.sup = self.tiles[(x+self.cols-1)%self.cols][(y+1)%self.rows]
                    tile.rup = self.tiles[(x+self.cols-1)%self.cols][(y+self.rows-1)%self.rows]
                    tile.qdn = self.tiles[(x+self.cols-1)%self.cols][y]
                    tile.sdn = self.tiles[x][(y+self.rows-1)%self.rows]
                    tile.rdn = self.tiles[x][(y+1)%self.rows]

                tile.neighbors = [tile.qup, tile.sup, tile.rup, tile.qdn, tile.sdn, tile.rdn]

        for player in players:
            tile = self.tiles[player["x"]][player["y"]]
            if player["number"] == 1:
                player = Player()
            else:
                player = AIPlayer()
            tile.owner = player
            pieces.City(tile, player)

    def scroll_right(self, step):
        self.viewport.x -= step

    def scroll_up(self, step):
        self.viewport.y -= step

    def check_tile_clicked(self, mouse_position):
        shifted_position = (
            mouse_position[0] + self.viewport.x,
            mouse_position[1] + self.viewport.y,
        )
        for tile in self.all_tiles:
            if tile.hexagon.rect.collidepoint(shifted_position):
                return tile.get_neighbour_closest_to_point(shifted_position)
        return None

    def draw(self, screen):
        self.tileMap.clear()
        for x in range(self.cols):
            for y in range(self.rows):
                tile = self.tiles[x][y]
                self.tileMap.draw_tile(tile)

        self.tileMap.draw(screen)
