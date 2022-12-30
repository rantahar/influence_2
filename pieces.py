import itertools
from players import Player


piece_prices = {
    "city": {
        "food": 10,
    },
    "path": {
        "food": 1
    }
}


def find_influences(board):
    for tile in board.all_tiles:
        tile.influences = {}
        for player in Player.all:
            tile.influences[player] = 0

    for tile in board.all_tiles:
        for piece in tile.pieces:
            piece.add_influences(board)


def find_tile_owners(board):
    find_influences(board)

    for tile in board.all_tiles:
        new_owner = tile.owner
        max_influence = 0
        for player in Player.all:
            influence = tile.influences[player]
            if influence > max_influence:
                new_owner = player
                max_influence = influence
            elif influence == max_influence:
                # tie
                new_owner = tile.owner
        tile.owner = new_owner


class GamePiece():
    id_iterator = itertools.count()

    def __init__(self, tile):
        self.tile = tile
        self.id = next(GamePiece.id_iterator)
        self.rotations = None

    @classmethod
    def can_build_at(cls, tile):
        return False

    @classmethod
    def price(cls):
        return {}

    def get_owner(self):
        return self.tile.owner

    def get_tile(self):
        return self.tile

    def get_sprite_id(self):
        return "unknown"

    def production(self):
        return {
            "food": 0,
            "wood": 0
        }

    def add_influences(self):
        pass

    def update(self):
        pass


class City(GamePiece):
    all = []

    def __init__(self, name, tile, level=1):
        super().__init__(tile)
        self.name = name
        self.level = level
        self.owner = tile.owner
        City.all.append(self)

    @classmethod
    def can_build_at(cls, tile):
        for nb in tile.neighbors:
            if Road in [type(p) for p in nb.pieces]:
                return True
        return False

    @classmethod
    def price(cls):
        return piece_prices["city"]

    def get_owner(self):
        return self.owner

    def change_owner(self):
        self.owner = self.tile.owner

    def get_sprite_id(self):
        return "city"+str(self.level)

    def collect_resources(self):
        if self.owner:
            for nb_tile in self.tile.neighbors:
                if nb_tile.land_type == "meadow":
                    self.owner.food += 1
                elif nb_tile.land_type == "forest":
                    self.owner.wood += 1

                for piece in nb_tile.pieces:
                    self.owner.food += piece.production()["food"]
                    self.owner.wood += piece.production()["wood"]

    def distance_to_tile(self, tile):
        return self.tile.distance_to(tile)

    def add_influences(self, board):
        for tile in board.all_tiles:
            n = self.level - self.tile.distance_to(tile) + 1
            if n > 0:
                tile.influences[self.owner] += n


class Road(GamePiece):
    def __init__(self, tile):
        super().__init__(tile)
        self.rotations = []

    @classmethod
    def can_build_at(cls, tile):
        for nb in tile.neighbors:
            if Road in [type(p) for p in nb.pieces]:
                return True
        return False

    @classmethod
    def price(cls):
        return piece_prices["path"]

    def add_influences(self, board):
        self.tile.influences[self.tile.owner] += 1
        for tile in self.tile.neighbors:
            tile.influences[self.tile.owner] += 1

    def get_sprite_id(self):
        return "road"

    def update(self):
        self.rotations = []
        if Road in [type(p) for p in self.tile.qup.pieces]:
            self.rotations.append(0)
        if Road in [type(p) for p in self.tile.qdn.pieces]:
            self.rotations.append(180)
        if Road in [type(p) for p in self.tile.rup.pieces]:
            self.rotations.append(120)
        if Road in [type(p) for p in self.tile.rdn.pieces]:
            self.rotations.append(300)
        if Road in [type(p) for p in self.tile.sup.pieces]:
            self.rotations.append(240)
        if Road in [type(p) for p in self.tile.sdn.pieces]:
            self.rotations.append(60)


