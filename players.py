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

    def build_road_at(self, tile):
        price = pieces.Road.price()
        if self.can_afford(price):
            tile.place(pieces.Road(tile))
            self.pay_resources(price)

    def build_woodlodge_at(self, tile):
        price = pieces.WoodLodge.price()
        if self.can_afford(price):
            tile.place(pieces.WoodLodge(tile))
            self.pay_resources(price)

    def build_farm_at(self, tile):
        price = pieces.Farm.price()
        print(self.resources)
        print(price)
        if self.can_afford(price):
            tile.place(pieces.Farm(tile))
            self.pay_resources(price)

    def build_city_at(self, tile):
        price = pieces.City.price()
        if self.can_afford(price):
            tile.place(pieces.Road(tile))
            tile.place(pieces.City("name", tile))
            self.pay_resources(price)

    def upgrade(self, city):
        price = city.upgrade_price()
        if self.can_afford(price):
            city.upgrade()
            self.pay_resources(price)


