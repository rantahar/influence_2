from sprites import piece_sprites as sprites


class GamePiece():
    def __init__(self, tile):
        self.tile = tile

    def get_owner(self):
        return self.tile.owner

    def get_tile(self):
        return self.tile

    def get_sprite(self):
        return sprites[5][6]


class City(GamePiece):
    def __init__(self, name, tile, level=1):
        super().__init__(tile)
        self.name = name
        self.level = level
        self.owner = tile.owner

    def get_owner(self):
        return self.owner

    def change_owner(self):
        self.owner = self.tile.owner

    def get_sprite(self):
        return sprites[1][0]

    def food_production(self):
        food = 0
        for nb_tile in self.tile.neighbors:
            food += nb_tile.food_production()
        return food

    def wood_production(self):
        food = 0
        for nb_tile in self.tile.neighbors:
            food += nb_tile.wood_production()
        return food




