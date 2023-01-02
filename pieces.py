import itertools
from players import Player


piece_prices = {
    "city": {
        "labor": 10,
    },
    "path": {
        "labor": 1,
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
    all = []
    id_iterator = itertools.count()

    def __init__(self, tile):
        self.tile = tile
        self.id = next(GamePiece.id_iterator)
        GamePiece.all.append(self)
        self.rotations = None
        self.show_game_piece_window = False

    @classmethod
    def can_build_at(cls, player, tile):
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
        return {}

    def add_influences(self):
        pass

    def update(self):
        pass

    def end_turn(self):
        pass

    def can_upgrade(self, player):
        return False


class City(GamePiece):
    all = []

    def __init__(self, name, tile, level=1):
        super().__init__(tile)
        self.name = name
        self.level = level
        self.owner = tile.owner
        self.show_game_piece_window = True
        City.all.append(self)

    @classmethod
    def can_build_at(cls, player, tile):
        if tile.owner == player:
            #has_road = Road in [type(p) for p in tile.pieces]
            #if has_road:
            #    for city in City.all:
            #        if city.distance_to_tile(tile) < 3:
            #            return False
            #return has_road
            for city in City.all:
                if city.distance_to_tile(tile) < 3:
                    return False
            return True
        return False

    @classmethod
    def price(cls):
        return piece_prices["city"]

    def upgrade_price(self):
        return {
            "labor": 10*self.level,
            "food": self.level,
        }

    def upgrade(self):
        self.level += 1
        find_tile_owners(self.tile.board)

    def get_owner(self):
        return self.owner

    def change_owner(self):
        self.owner = self.tile.owner

    def get_sprite_id(self):
        return "city"+str(self.level)

    def production(self):
        return {
            "labor": 1
        }

    def distance_to_tile(self, tile):
        return self.tile.distance_to(tile)

    def add_influences(self, board):
        for tile in board.all_tiles:
            n = self.level - self.tile.distance_to(tile) + 1
            if n > 0:
                tile.influences[self.owner] += n

    def end_turn(self, player):
        if (player is self.owner) and (self.owner is not self.tile.owner):
            self.owner = self.tile.owner


class Road(GamePiece):
    def __init__(self, tile):
        super().__init__(tile)
        self.rotations = []

    @classmethod
    def can_build_at(cls, player, tile):
        if Road in [type(p) for p in tile.pieces]:
            return False

        for nb in tile.neighbors:
            if nb.owner is player:
                if Road in [type(p) for p in nb.pieces]:
                    return True
        return False

    @classmethod
    def price(cls):
        return piece_prices["path"]

    def add_influences(self, board):
        for nb in self.tile.neighbors:
            if nb.owner is not None:
                if Road in [type(p) for p in nb.pieces]:
                    self.tile.influences[nb.owner] += 1

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


