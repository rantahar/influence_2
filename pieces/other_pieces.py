import itertools



prices = {
    "Building Project": {},
    "Road": {"labor": 1},
    "City": {"labor": 10},
    "Farm": {"labor": 5},
    "Wood Gatherer's Hut": {"labor": 1},
    "Hunter's Camp": {"labor": 2},
    "Fishing Camp": {"labor": 1},
    "Mine": {"labor": 5},
}

production = {
    "Building Project": {},
    "Road": {},
    "Farm": {"food": 2},
    "Wood Gatherer's Hut": {"labor": 1},
    "Hunter's Camp": {"food": 1},
    "Fishing Camp": {"food": 2},
    "Mine": {"labor": 3},
}

# City production determined by the city class in city.py


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
        return dict(prices[cls.title])

    def get_owner(self):
        return self.tile.owner

    def get_tile(self):
        return self.tile

    def get_sprite_id(self):
        return "unknown"

    def production(self):
        return production[self.title]

    def add_influences(self, board):
        pass

    def update(self):
        pass

    def end_turn(self):
        pass

    def can_upgrade(self, name):
        return False

    def get_upgrades(self):
        return {}

    def check_queue(self, labor):
        return labor


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

    def get_sprite_id(self):
        return "farm"


class WoodLodge(GamePiece):
    title = "Wood Gatherer's Hut"

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

    def get_sprite_id(self):
        return "woodlodge"


class HuntersCamp(GamePiece):
    title = "Hunter's Camp"

    def __init__(self, tile, player):
        super().__init__(tile, player)
        self.tile.place(self)

    @classmethod
    def can_build_at(cls, player, tile):
        if not super().can_build_at(player, tile):
            return False
        if tile.land_type in ["forest", "meadow"]:
            return True
        return False
    
    def get_sprite_id(self):
        return "woodlodge"
    

class FishingCamp(GamePiece):
    title = "Fishing Camp"

    def __init__(self, tile, player):
        super().__init__(tile, player)
        self.tile.place(self)

    @classmethod
    def can_build_at(cls, player, tile):
        if not super().can_build_at(player, tile):
            return False
        if tile.land_type == "water":
            return True
        return False
    
    def get_sprite_id(self):
        return "woodlodge"


class Mine(GamePiece):
    title = "Mine"

    def __init__(self, tile, player):
        super().__init__(tile, player)
        self.tile.place(self)

    @classmethod
    def can_build_at(cls, player, tile):
        if not super().can_build_at(player, tile):
            return False
        if tile.land_type == "mountain":
            return True
        return False
    
    def get_sprite_id(self):
        return "woodlodge"
