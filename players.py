
player_colors = {
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
}

next_color = 0


class Player():
    def __init__(self, is_ai=False):
        global next_color
        self.is_ai = is_ai
        self.name = list(player_colors.keys())[next_color]
        self.color = player_colors[self.name]
        next_color += 1

        self.food = 0
        self.wood = 0


