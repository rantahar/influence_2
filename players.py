import pieces

player_colors = {
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
}

next_color = 0


class Player():
    all = []

    def __init__(self):
        global next_color
        self.is_ai = False
        self.name = list(player_colors.keys())[next_color]
        self.color = player_colors[self.name]
        next_color += 1
        Player.all.append(self)

        self.resources = {"labor": 0, "food": 0}

    def can_afford(self, price):
        for key in price.keys():
            if key != "labor":
                if key not in self.resources:
                    return False
                if price[key] > self.resources[key]:
                    return False
        return True

    def pay_resources(self, price):
        for key in price.keys():
            self.resources[key] -= price[key]

    def build_at(self, piece_class, tile):
        price = piece_class.price()
        if piece_class.can_build_at(self, tile) and self.can_afford(price):
            if price["labor"] <= self.resources["labor"]:
                piece_class(tile, self)
                self.pay_resources(price)
            else:
                labor_cost = price["labor"] - self.resources["labor"]
                price["labor"] = self.resources["labor"]
                self.pay_resources(price)
                pieces.Project(tile, piece_class, labor_cost, self)

    def upgrade(self, piece, name):
        if not piece.can_upgrade(name):
            return False
        upgrades = piece.get_upgrades()
        if name in upgrades.keys():
            upgrade = upgrades[name]
            price = upgrade["price"]
            if self.can_afford(price):
                piece.queue(name)
                labor = self.resources["labor"]
                self.resources["labor"] = piece.check_queue(labor)
                price["labor"] = 0
                self.pay_resources(price)
                return True
        return False


class AIPlayer(Player):

    def __init__(self):
        super().__init__()
        self.is_ai = True
        self.next_city_location = None
        self.previous_road = None

    def take_turn(self, board):
        for tile in board.all_tiles:
            if tile.owner is self:
                if tile.land_type == "forest":
                    self.build_at(pieces.WoodLodge, tile)
                elif tile.land_type == "meadow":
                    self.build_at(pieces.Farm, tile)

        if self.resources["food"] > 0:
            for city in pieces.City.all:
                if city.owner is self:
                    self.upgrade(city, "upgrade")

        while self.resources["labor"] > 0:
            next_city = self.find_next_city_location(board)
            if next_city is None:
                break
            if self.previous_road is next_city:
                self.build_at(pieces.City, next_city)
                self.next_city_location = None
                continue
            for tile in board.all_tiles:
                if pieces.Road.can_build_at(self, tile):
                    if self.previous_road is None or tile.distance_to(next_city) < self.previous_road.distance_to(next_city):
                        self.build_at(pieces.Road, tile)
                        self.previous_road = tile
                        continue

    def find_next_city_location(self, board):
        if self.next_city_location is not None:
            return self.next_city_location

        best_goodness = 0
        best_tile = None
        for tile in board.all_tiles:
            if not pieces.City.ai_can_build_with_road(self, tile):
                continue
            goodness = 0
            for city in pieces.City.all:
                dist = city.distance_to_tile(tile)
                if dist < 3:
                    goodness -= 100000000
                if dist >= 3:
                    goodness += 10 - dist
            for nb in tile.neighbors:
                if nb.land_type == "meadow":
                    goodness += 2
            if goodness > best_goodness:
                best_goodness = goodness
                best_tile = tile
        return best_tile





