TILE_SIZE = 16
SPRITE_SIZE = TILE_SIZE, TILE_SIZE + (TILE_SIZE // 2)

INPUT_NORTH = object()
INPUT_SOUTH = object()
INPUT_EAST = object()
INPUT_WEST = object()
INPUT_NORTH_EAST = object()
INPUT_NORTH_WEST = object()
INPUT_SOUTH_EAST = object()
INPUT_SOUTH_WEST = object()
INPUT_NONE = object()

DIRECTIONS = {
    INPUT_NORTH: (0, 1, 0),
    INPUT_SOUTH: (0, -1, 0),
    INPUT_EAST: (1, 0, 0),
    INPUT_WEST: (-1, 0, 0),
    INPUT_NORTH_EAST: (1, 1, 0),
    INPUT_NORTH_WEST: (-1, 1, 0),
    INPUT_SOUTH_EAST: (1, -1, 0),
    INPUT_SOUTH_WEST: (-1, -1, 0),
    INPUT_NONE: (0, 0, 0)
}

EDIT_MODE_ERASE = "edit erase mode"
EDIT_MODE_FLOOR = "edit floor mode"
EDIT_MODE_WALL = "edit wall mode"
EDIT_MODE_PLAYER = "edit player mode"
EDIT_MODE_MONSTER = "edit monster mode"
EDIT_MODE_SELECT = "select focus mode"

EDIT_DRAW_MODES = [EDIT_MODE_FLOOR, EDIT_MODE_WALL, EDIT_MODE_MONSTER]

IMG_GRANITE = "img_granite"
IMG_PLAYER = "img_player"
IMG_MONSTER = "img_monster"

IMG_PATHS = {
    IMG_GRANITE: {
        -1: "gui/blocks/granite_floor.png",
        0: "gui/blocks/granite_wall.png",
        1: "gui/blocks/granite_wall.png"
    },
    IMG_PLAYER: {
        -1: "gui/creatures/player.png",
        0: "gui/creatures/player.png",
        1: "gui/creatures/player.png"
    },
    IMG_MONSTER: {
        -1: "gui/creatures/monster.png",
        0: "gui/creatures/monster.png",
        1: "gui/creatures/monster.png"
    }
}