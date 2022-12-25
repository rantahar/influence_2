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


piece_sprites = load_tileset("assets/Toens_Medieval_Strategy_Sprite_Pack/tileset.png", 16, 16)
land_sprites = load_tileset('assets/elite_command_art_terrain/tileset.png', 34, 32)[0]

map_sprites = {
    'forest': land_sprites[3],
    'meadow': land_sprites[0]
}

piece_sprites = {
    'unknown': piece_sprites[5][6],
    "city1": piece_sprites[1][0],
}


