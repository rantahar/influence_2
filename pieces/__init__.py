from .city import City, find_tile_owners
from .other_pieces import GamePiece, Road, Farm, WoodLodge, Project


piece_classes = {
    "city": City,
    "road": Road,
    "farm": Farm,
    "woodlodge": WoodLodge,
}
