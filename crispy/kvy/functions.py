from kivy.clock import Clock
from kivy.core.window import Window
import constants


__all__ = ["schedule_interval", "transform_touch_to_grid", "transform_grid_to_touch", "get_grid_size",
           "get_touched_cell", "get_centered_camera"]


def schedule_interval(func):
    Clock.schedule_interval(func, 0)


def transform_touch_to_grid(x, y=None):
    if y is None:
        x, y = x
    ret_x = int(x // constants.TILE_SIZE)
    ret_y = int(y // constants.TILE_SIZE)
    return ret_x, ret_y


def transform_grid_to_touch(x, y=None):
    if y is None:
        x, y = x
    ret_x = x * constants.TILE_SIZE
    ret_y = y * constants.TILE_SIZE
    return ret_x, ret_y


def get_grid_size():
    sx, sy = Window.system_size
    width = int(sx // constants.TILE_SIZE)
    height = int(sy // constants.TILE_SIZE)
    return width, height


def get_touched_cell(pos, camera):
    t_x, t_y = pos
    c_u, c_v = camera.x, camera.y
    t_u, t_v = transform_touch_to_grid(t_x, t_y)
    size = get_grid_size()
    w, h = int(size[0] // 2), int(size[1] // 2)
    d_x, d_y = c_u - w, c_v - h
    return t_u + d_x, t_v + d_y


def get_centered_camera(x, y):
    sx, sy = Window.system_size
    d_x = int((sx // constants.TILE_SIZE) // 2)
    d_y = int((sy // constants.TILE_SIZE) // 2)
    center_x = x - d_x
    center_y = y - d_y
    return center_x, center_y
