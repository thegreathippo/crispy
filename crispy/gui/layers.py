import kvy
import utils
import constants

Z_TOP = 10
Z_BOTTOM = -10


class View(kvy.ScatterLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layers = dict()
        for z in range(Z_BOTTOM, Z_TOP + 1):
            layer = SpriteLayer(z)
            self.layers[z] = layer
        self.screen_camera = utils.Point3(0, 0, 0)
        self.eid_to_layer = dict()
        self.eid_to_sprite = dict()
        self.add_widget(self.layers[-1])
        self.add_widget(self.layers[0])
        self.add_widget(self.layers[1])

    def load_sprite(self, entity, sprite_data):
        eid = entity.eid
        layer = self.layers[sprite_data.z]
        sprite = layer.add_sprite(sprite_data)
        self.eid_to_layer[eid] = layer
        self.eid_to_sprite[eid] = sprite

    def unload_sprite(self, entity):
        eid = entity.eid
        layer = self.eid_to_layer[eid]
        sprite = self.eid_to_sprite[eid]
        layer.remove_sprite(sprite)
        del self.eid_to_layer[eid]
        del self.eid_to_sprite[eid]

    def change_sprite(self, entity, old_data, new_data):
        eid = entity.eid
        if old_data.z != new_data.z:
            self.remove_sprite(entity)
            self.load_sprite(entity, new_data)
        else:
            layer = self.eid_to_layer[eid]
            sprite = self.eid_to_sprite[eid]
            vx, vy = new_data.x - old_data.x, new_data.y - old_data.y
            layer.move_sprite(sprite, vx, vy)


class SpriteLayer(kvy.FloatLayout):

    def __init__(self, z, **kwargs):
        super().__init__(**kwargs)
        self.z = z
        self.depth = dict()

    def add_widget(self, widget, depth=0):
        self.depth[widget] = depth
        if len(self.children) == 0:
            return super().add_widget(widget)
        else:
            for i, element in enumerate(list(self.children)):
                if self.depth[element] > depth:
                    return super().add_widget(widget, i)
        super().add_widget(widget, len(self.children))

    def remove_widget(self, widget):
        del self.depth[widget]
        super().remove_widget(widget)

    def clear_widgets(self, children=None):
        if children:
            for child in children:
                del self.depth[child]
        else:
            self.depth.clear()
        super().clear_widgets(children)

    def add_sprite(self, sprite_data):
        sprite = Sprite(sprite_data)
        self.add_widget(sprite, sprite.cell_y)
        return sprite

    def remove_sprite(self, sprite):
        self.remove_widget(sprite)

    def move_sprite(self, sprite, vx, vy):
        sprite.move(vx, vy)
        if vy:
            self.remove_widget(sprite)
            self.add_widget(sprite, sprite.cell_y)


class Sprite(kvy.Image):
    def __init__(self, sprite_data):
        super().__init__()
        cx, cy, cz, img = sprite_data
        self.cell_x, self.cell_y, self.cell_z = cx, cy, cz
        sx, sy = kvy.transform_grid_to_touch(cx, cy)
        self.x = sx
        self.y = sy + (cz * (int(constants.TILE_SIZE // 2)))
        self.source = constants.IMG_PATHS[img][cz]

    def move(self, vx, vy):
        svx, svy = kvy.transform_grid_to_touch(vx, vy)
        self.x += svx
        self.y += svy
        self.cell_x += vx
        self.cell_y += vy
