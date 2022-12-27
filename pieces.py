import itertools
from players import Player


class GamePiece():
    def __init__(self, tile):
        self.tile = tile

    def get_owner(self):
        return self.tile.owner

    def get_tile(self):
        return self.tile

    def get_type(self):
        return "unknown"

    def update(self):
        pass


class City(GamePiece):
    id_iterator = itertools.count()
    all = []

    def __init__(self, name, tile, level=1):
        super().__init__(tile)
        self.name = name
        self.level = level
        self.owner = tile.owner
        self.id = next(City.id_iterator)
        City.all.append(self)

    def get_owner(self):
        return self.owner

    def change_owner(self):
        self.owner = self.tile.owner

    def get_type(self):
        return "city"+str(self.level)

    def collect_resources(self):
        if self.owner:
            for nb_tile in self.tile.neighbors:
                self.owner.food += nb_tile.food_production()
                self.owner.wood += nb_tile.wood_production()

    def distance_to_tile(self, tile):
        return self.tile.distance_to(tile)

    def set_influences(self, board):
        for tile in board.all_tiles:
            n = self.level - self.tile.distance_to(tile) + 1
            if n > 0:
                tile.influences[self.id] = n
            else:
                tile.influences[self.id] = 0

            new_owner = tile.owner
            max_influence = 0
            for player in Player.all:
                influence = 0
                for city in City.all:
                    if city.owner is player:
                        influence += tile.influences[city.id]
                if influence > max_influence:
                    new_owner = player
                if influence == max_influence:
                    # tie
                    new_owner = tile.owner
            tile.owner = new_owner

    def update(self, board):
        self.set_influences(board)






