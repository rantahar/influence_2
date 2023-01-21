from .city import City, find_tile_owners
from .other_pieces import *

piece_classes = {
    "city": City,
    "road": Road,
    "farm": Farm,
    "woodlodge": WoodLodge,
    "hunterscamp": HuntersCamp,
    "finshingcamp": FishingCamp,
    "mine": Mine,
}
