TILE_SIZE = 32
SPRITE_SIZE = TILE_SIZE, TILE_SIZE + (TILE_SIZE // 2)

DEFAULT_SAVE_PATH = "game.pkl"

ERASE_MODE = "erase mode"
DRAW_FLOOR_MODE = "draw floor mode"
DRAW_WALL_MODE = "draw wall mode"
DRAW_PLAYER_MODE = "draw player mode"
DRAW_MONSTER_MODE = "draw monster mode"
DRAW_ROOF_MODE = "draw roof mode"


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


def transform_to_grid(x, y):
    ret_x = int(x // TILE_SIZE)
    ret_y = int(y // TILE_SIZE)
    return ret_x, ret_y


def transform_to_screen(x, y):
    ret_x = x * TILE_SIZE
    ret_y = y * TILE_SIZE
    return ret_x, ret_y


class _Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0


CAMERA = _Camera()
