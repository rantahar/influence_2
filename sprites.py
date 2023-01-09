import pygame


def load_tileset(filename, tile_height, tile_width):
    # Load the map tiles
    tileset = pygame.image.load(filename)
    tileset_width, tileset_height = tileset.get_size()

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


road_sprite = load_tileset('assets/roads.png', 34, 32)[0][0]

city_1 = load_tileset('assets/building_2.png', 256, 256)[0][0]
city_2 = load_tileset('assets/town_1_3.png', 256, 256)[0][0]
city_3 = load_tileset('assets/town_2_3.png', 256, 256)[0][0]
farm = load_tileset('assets/farm_1.png', 256, 256)[0][0]
woodlodge = load_tileset('assets/woodlodge_1.png', 256, 256)[0][0]
flag = load_tileset('assets/project_1.png', 256, 256)[0][0]

grass_sprite = load_tileset('assets/grass_2.png', 340, 320)[0][0]
forest_sprite = load_tileset('assets/forest_2.png', 340, 320)[0][0]
mountain_sprite = load_tileset('assets/mountain_1.png', 340, 320)[0][0]

map_sprites = {
    'forest': forest_sprite,
    'meadow': grass_sprite,
    'mountain': mountain_sprite,
}

piece_sprites = {
    'unknown': flag,
    'project': flag,
    "city1": city_1,
    "city2": city_2,
    "city3": city_3,
    "city4": city_3,
    "city5": city_3,
    "road": road_sprite,
    "woodlodge": woodlodge,
    "farm": farm,
}


