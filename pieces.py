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

    def __init__(self, tile, player):
        self.tile = tile
        self.id = next(GamePiece.id_iterator)
        self.rotations = None
        self.show_game_piece_window = False
        GamePiece.all.append(self)

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
        super().__init__(tile, player)
        Project.all.append(self)
        self.piece_class = piece_class
        self.work_left = work_left
        self.owner = player
        self.tile.place(self)

    def get_owner(self):
        return self.owner

    def progress(self, labor):
        if not self.piece_class.can_finish_project(self.owner, self.tile):
            self.cancel()
            return labor
        if labor <= 0:
            return 0
        if labor >= self.work_left:
            self.tile.place(self.piece_class(self.tile, self.owner))
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

    def __init__(self, tile, player, level=1):
        super().__init__(tile, player)
        self.name = "name"
        self.level = level
        self.owner = player
        self.queue = {}
        if Road not in [type(p) for p in tile.pieces]:
            Road(tile, player)
        self.show_game_piece_window = True
        City.all.append(self)
        self.tile.place(self)

    @classmethod
    def can_build_at(cls, player, tile):
        on_road = False
        for piece in tile.pieces:
            if type(piece) is not Road:
                return False
            if type(piece) is Road and piece.owner is player:
                on_road = True
        if on_road or tile.owner == player:
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
        if "upgrade" in self.queue.keys():
            return False
        if self.get_owner() is not player:
            return False
        if player.can_afford(self.upgrade_price()):
            return True
        return False

    def queue_upgrade(self):
        self.queue_building(
            "upgrade",
            self.upgrade_price()["labor"],
            self.upgrade
        )

    def queue_building(self, name, labor, finish_function):
        self.queue[name] = [labor, finish_function]

    def check_queue(self, labor):
        for project in list(self.queue.keys()):
            cost = self.queue[project][0]
            if cost > labor:
                self.queue[project][0] -= labor
                labor = 0
            else:
                labor -= cost
                self.queue[project][1]()
                del self.queue[project]
        return labor

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
        upgrade_queued = "upgrade" in self.queue.keys()
        food_level = self.level + upgrade_queued
        food_consumption = food_level*(food_level-1)//2
        return {
            "labor": self.level,
            "food": -food_consumption
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

    def __init__(self, tile, player):
        super().__init__(tile, player)
        self.owner = player
        self.rotations = []
        self.tile.place(self)

    @classmethod
    def can_build_at(cls, player, tile):
        if Road in [type(p) for p in tile.pieces]:
            return False

        for nb in tile.neighbors:
            for piece in nb.pieces:
                if type(piece) is Road:
                    if nb.owner is player or piece.get_owner() is player:
                        return True
        return False

    @classmethod
    def price(cls):
        return {"labor": 1}

    def get_sprite_id(self):
        return "road"

    def get_owner(self):
        return self.owner

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

    def __init__(self, tile, player):
        super().__init__(tile, player)
        self.tile.place(self)

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

    def __init__(self, tile, player):
        super().__init__(tile, player)
        self.tile.place(self)

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




