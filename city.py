from other_pieces import GamePiece, Road
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
