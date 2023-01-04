import itertools
from players import Player


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
        if tile.owner is not player:
            return False
        for piece_class in [type(p) for p in tile.pieces]:
            if piece_class is not Road:
                return False
        return True

    @classmethod
    def can_finish_project(cls, player, tile):
        if tile.owner is not player:
            return False
        for piece_class in [type(p) for p in tile.pieces]:
            if piece_class is not Road and piece_class is not Project:
                return False
        return True

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

    def add_influences(self, board):
        pass

    def update(self):
        pass

    def end_turn(self):
        pass

    def can_upgrade(self, player):
        return False


class Project(GamePiece):
    title = "Building Project"
    all = []

    def __init__(self, tile, piece_class, work_left, player):
        super().__init__(tile)
        Project.all.append(self)
        self.piece_class = piece_class
        self.work_left = work_left
        self.owner = player

    def get_owner(self):
        return self.owner

    def progress(self, labor):
        if not self.piece_class.can_finish_project(self.owner, self.tile):
            self.cancel()
            return labor
        if labor <= 0:
            return 0
        if labor >= self.work_left:
            self.tile.place(self.piece_class(self.tile))
            labor_left = labor - self.work_left
            self.cancel()
            return labor_left
        else:
            self.work_left -= labor
            return 0

    def cancel(self):
        Project.all.remove(self)
        self.tile.pieces.remove(self)
        del self

    def get_sprite_id(self):
        return "project"


class City(GamePiece):
    all = []
    title = "City"

    def __init__(self, tile, level=1):
        super().__init__(tile)
        self.name = "name"
        self.level = level
        self.owner = tile.owner
        self.show_game_piece_window = True
        City.all.append(self)

    @classmethod
    def can_build_at(cls, player, tile):
        if not super().can_build_at(player, tile):
            return False
        if tile.owner == player:
            for city in City.all:
                if city.distance_to_tile(tile) < 3:
                    return False
            return True
        return False

    @classmethod
    def price(cls):
        return {"labor": 10}

    def upgrade_price(self):
        return {
            "labor": 10*self.level,
            "food": self.level,
        }

    def can_upgrade(self, player):
        if self.get_owner() is not player:
            return False
        if player.can_afford(self.upgrade_price()):
            return True
        return False

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
            "labor": self.level,
            "food": 1-self.level
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
    title = "Road"

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
        return {"labor": 1}

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


class Farm(GamePiece):
    title = "Farm"

    def __init__(self, tile):
        super().__init__(tile)

    @classmethod
    def can_build_at(cls, player, tile):
        if not super().can_build_at(player, tile):
            return False
        if tile.owner is player and tile.land_type == "meadow":
            return True
        return False

    @classmethod
    def price(cls):
        return {"labor": 1}

    def get_sprite_id(self):
        return "farm"

    def production(self):
        return {"food": 1}


class WoodLodge(GamePiece):
    title = "Wood Gatherer's Lodge"

    def __init__(self, tile):
        super().__init__(tile)

    @classmethod
    def can_build_at(cls, player, tile):
        if not super().can_build_at(player, tile):
            return False
        if tile.land_type == "forest":
            return True
        return False

    @classmethod
    def price(cls):
        return {"labor": 1}

    def get_sprite_id(self):
        return "woodlodge"

    def production(self):
        return {"labor": 1}




piece_classes = {
    "city": City,
    "road": Road,
    "farm": Farm,
    "woodlodge": WoodLodge,
}




