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

        self.food = 0
        self.tools = 0

    def build_road_at(self, tile):
        price = pieces.Road.price()
        print(price)
        if price["food"] <= self.food:
            tile.place(pieces.Road(tile))
            self.food -= pieces.Road.price()["food"]

    def build_city_at(self, tile):
        price = pieces.City.price()
        print(price)
        if price["food"] <= self.food and price["tools"] <= self.tools:
            tile.place(pieces.Road(tile))
            tile.place(pieces.City("name", tile))
            self.food -= pieces.City.price()["food"]
            self.tools -= pieces.City.price()["tools"]

    def upgrade(self, city):
        price = 10*city.level
        if self.food >= price:
            self.food -= price
            city.upgrade()


