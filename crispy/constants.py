TILE_SIZE = 16
SPRITE_SIZE = TILE_SIZE, TILE_SIZE + (TILE_SIZE // 2)

DEFAULT_SAVE_PATH = "game.pkl"


EID_NULL = 0
EID_PLAYER = 1
EID_CAMERA = 2

EID_TRANSLATION = {
    0: EID_NULL,
    1: EID_PLAYER,
    2: EID_CAMERA
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