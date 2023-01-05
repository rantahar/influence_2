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

    def __init__(self, is_ai=False):
        global next_color
        self.is_ai = is_ai
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
                tile.place(piece_class(tile))
                self.pay_resources(price)
            else:
                labor_cost = price["labor"] - self.resources["labor"]
                price["labor"] = self.resources["labor"]
                self.pay_resources(price)
                tile.place(pieces.Project(tile, piece_class, labor_cost, self))

    def upgrade(self, piece):
        if not piece.can_upgrade(self):
            return False
        price = piece.upgrade_price()
        if self.can_afford(price):
            labor = self.resources["labor"]
            piece.queue_upgrade()
            self.resources["labor"] = piece.check_queue(labor)
            price["labor"] = 0
            self.pay_resources(price)
            return True
        return False


