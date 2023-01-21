
def load_map(filename):
    players = []
    land_types = []
    with open(filename) as f:
        for y, line in enumerate(f.readlines()):
            line = line.strip()
            land_types_row = []
            for x, type in enumerate(line.split(" ")):
                try:
                    number = int(type)
                    players.append({"x": x, "y": y, "number": number})
                    land_types_row.append("meadow")
                    continue
                except:
                    pass

                if type == "f":
                    land_types_row.append("forest")
                elif type == "w":
                    land_types_row.append("water")
                elif type == "m":
                    land_types_row.append("meadow")
                elif type == "M":
                    land_types_row.append("mountain")
            land_types.append(land_types_row)

    return land_types, players


            
