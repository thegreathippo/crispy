from .customdicts import *
from .bases import *
import collections
import config
import kivy
from kivy.config import Config
from kivy.clock import Clock
from kivy.core.window import Window

kivy.require("1.9.0")
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


Point3 = collections.namedtuple("Point3", ["x", "y", "z"])


def schedule_interval(func, time=0):
    def schedule_once(*args):
        Clock.schedule_once(func, -1)
    Clock.schedule_interval(schedule_once, 0)



def transform_to_grid(x, y):
    ret_x = int(x // config.TILE_SIZE)
    ret_y = int(y // config.TILE_SIZE)
    return ret_x, ret_y


def transform_to_screen(x, y):
    ret_x = x * config.TILE_SIZE
    ret_y = y * config.TILE_SIZE
    return ret_x, ret_y


def get_size_in_cells():
    sx, sy = Window.system_size
    width = int(sx // config.TILE_SIZE)
    height = int(sy // config.TILE_SIZE)
    return width, height


def get_touched_cell(pos, camera):
    t_x, t_y = pos
    c_u, c_v = camera.x, camera.y
    t_u, t_v = transform_to_grid(t_x, t_y)
    size = get_size_in_cells()
    w, h = int(size[0] // 2), int(size[1] // 2)
    d_x, d_y = c_u - w, c_v - h
    return t_u + d_x, t_v + d_y


def get_centered_camera(x, y):
    sx, sy = Window.system_size
    d_x = int((sx // config.TILE_SIZE) // 2)
    d_y = int((sy // config.TILE_SIZE) // 2)
    center_x = x - d_x
    center_y = y - d_y
    return center_x, center_y
