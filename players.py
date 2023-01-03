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

        self.resources = {}

    def can_afford(self, price):
        for key in price.keys():
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
        if self.can_afford(price) and piece_class.can_build_at(self, tile):
            tile.place(piece_class(tile))
            self.pay_resources(price)

    def upgrade(self, piece):
        if piece.get_owner() is not self:
            return False
        price = piece.upgrade_price()
        if self.can_afford(price):
            piece.upgrade()
            self.pay_resources(price)
            return True
        return False


