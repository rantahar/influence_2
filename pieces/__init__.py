from .city import City, find_tile_owners
from .other_pieces import GamePiece, Project, Road, Farm, WoodLodge, HuntersCamp, Mine


piece_classes = {
    "city": City,
    "road": Road,
    "farm": Farm,
    "woodlodge": WoodLodge,
    "hunterscamp": HuntersCamp,
    "mine": Mine,
}
