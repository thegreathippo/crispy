ENTITY_PLAYER = 0

MODE_ERASE = "erase mode"
MODE_DRAW_FLOOR = "draw floor mode"
MODE_DRAW_WALL = "draw wall mode"
MODE_DRAW_PLAYER = "draw player mode"
MODE_DRAW_MONSTER = "draw monster mode"
MODE_DRAW_ROOF = "draw roof mode"


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