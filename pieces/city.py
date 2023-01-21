from .other_pieces import GamePiece, Road
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
                # Tie. Even if the old owner has less, they keep it.
                new_owner = tile.owner
        tile.owner = new_owner


class City(GamePiece):
    all = []
    title = "City"
    buildings = {
        "Ditch": {
            "requires": {"city_level": 2},
            "price": {"labor": 5},
            "grants": {"defence": 1},
        }
    }

    def __init__(self, tile, player, level=1):
        super().__init__(tile, player)
        self.name = "name"
        self.level = level
        self.owner = player
        self._queue = {}
        self.built = []
        if Road not in [type(p) for p in tile.pieces]:
            Road(tile, player)
        self.show_game_piece_window = True
        City.all.append(self)
        self.tile.place(self)

    @classmethod
    def can_build_at(cls, player, tile):
        if tile.land_type != "meadow":
            return False
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
    def ai_can_build_with_road(cls, player, tile):
        if tile.land_type != "meadow":
            return False
        for piece in tile.pieces:
            if type(piece) is not Road:
                return False
        if not Road.can_build_at(player, tile):
            return False
        if tile.owner is None or tile.owner is player:
            for city in City.all:
                if city.distance_to_tile(tile) < 3:
                    return False
            return True
        return False

    def get_upgrades(self):
        upgrade = {
            "requires": {},
            "description": "Increase city population.",
            "price": {
                "labor": 10*self.level,
                "food": self.level
            },
            "grants": {"level": 1}
        }
        buildings = City.buildings.copy()
        buildings["upgrade"] = upgrade
        return buildings

    def can_upgrade(self, name):
        if name in self._queue.keys():
            return False
        if name in self.built:
            return False
        upgrades = self.get_upgrades()
        if name not in upgrades.keys():
            return False
        for r in upgrades[name]["requires"].keys():
            require = upgrades[name]["requires"][r]
            if r == "city_level":
                if require > self.level:
                    return False
            elif require not in self.built:
                return False
        return True

    def queue(self, building):
        upgrades = self.get_upgrades()
        if building in upgrades.keys() and building not in self._queue and building not in self.built:
            upgrade = upgrades[building]
            price = upgrade["price"]
            self._queue[building] = [price["labor"], building]

    def check_queue(self, labor):
        for p in list(self._queue.keys()):
            project = self._queue[p]
            cost = project[0]
            if cost > labor:
                project[0] -= labor
                labor = 0
            else:
                labor -= cost
                self.build_upgrade(project[1])
                del self._queue[p]
        return labor

    def build_upgrade(self, name):
        upgrades = self.get_upgrades()
        if name in upgrades:
            upgrade = upgrades[name]
            if "multiple" in upgrade.keys():
                if not upgrade["multiple"]:
                    self.built.append(name)
            grants = upgrade["grants"]
            if "level" in grants.keys():
                self.level += grants["level"]
        find_tile_owners(self.tile.board)

    def get_owner(self):
        return self.owner

    def change_owner(self):
        self.owner = self.tile.owner

    def get_sprite_id(self):
        if self.level > 4:
            return "city5"
        return "city"+str(self.level)

    def production(self):
        upgrade_queued = "upgrade" in self._queue.keys()
        population = self.level + upgrade_queued
        food_consumption = population*(population-1)//2
        return {
            "labor": self.level,
            "food": -food_consumption
        }

    def distance_to_tile(self, tile):
        return self.tile.distance_to(tile)

    def add_influences(self, board):
        for tile in board.all_tiles:
            n = self.level//5 - self.tile.distance_to(tile) + 2
            if n > 0:
                tile.influences[self.owner] += n

    def end_turn(self, player):
        if (player is self.owner) and (self.owner is not self.tile.owner):
            self.owner = self.tile.owner
