from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.image import Image
from kivy.graphics.transformation import Matrix
import utils
import config
import constants


class ViewScreen(ScatterLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layers = []
        for i in range(-1, 2):
            layer = SpriteLayer(i)
            self.layers.append(layer)
            self.add_widget(layer)
        self.eids = dict()
        self.camera = utils.Point3(0, 0, 0)

    def load_sprite(self, entity):
        layer = self.layers[entity.sprite.z]
        layer.add_sprite(entity)
        self.eids[entity.eid] = layer

    def remove_sprite(self, eid):
        layer = self.eids[eid]
        layer.remove_sprite(eid)
        del self.eids[eid]

    def move_sprite(self, eid, old_pos, new_pos):
        layer = self.eids[eid]
        layer.move_sprite(eid, old_pos, new_pos)

    def follow_camera(self, camera):
        x, y = utils.get_centered_camera(camera.x, camera.y)
        sx, sy = utils.transform_to_screen(x, y)
        z, sz = camera.z, camera.z
        if (sx, sy, sz) != self.camera:
            dx = self.camera.x - sx
            dy = self.camera.y - sy
            dz = self.camera.z - sz
            self.adjust_camera(dx, dy, dz)
            self.camera = utils.Point3(sx, sy, sz)

    def adjust_camera(self, dx, dy, dz):
        mat = Matrix().translate(dx, dy, 0)
        self.apply_transform(mat)
        if dz:
            pass


class LayerManager:

    def __init__(self, widget):
        self.add_widget = widget.add_widget
        self.remove_widget = widget.remove_widget
        self.children = widget.children
        self.layers = dict()

    def add(self, widget, layer):
        self.layers[widget] = layer
        if len(self.children) == 0:
            self.add_widget(widget)
            return
        else:
            for i, element in enumerate(list(self.children)):
                if self.layers[element] > layer:
                    self.add_widget(widget, i)
                    return
        self.add_widget(widget, len(self.children))

    def move(self, widget, layer):
        self.remove_widget(widget)
        self.add(widget, layer)

    def remove(self, widget):
        self.remove_widget(widget)
        del self.layers[widget]


class SpriteLayer(FloatLayout):

    def __init__(self, z, **kwargs):
        super().__init__(**kwargs)
        self.z = z
        self.eids = dict()
        self.layers = LayerManager(self)

    def add_sprite(self, entity):
        sprite = Sprite(entity, self.z)
        self.layers.add(sprite, entity.y)
        self.eids[entity.eid] = sprite

    def remove_sprite(self, eid):
        sprite = self.eids[eid]
        self.layers.remove(sprite)

    def move_sprite(self, eid, old_pos, new_pos):
        sprite = self.eids[eid]
        vx, vy = new_pos.x - old_pos.x, new_pos.y - old_pos.y
        sprite.move(vx, vy)
        self.layers.move(sprite, new_pos.y)


class Sprite(Image):
    def __init__(self, entity, layer):
        super().__init__()
        data = entity.sprite
        sx, sy = utils.transform_to_screen(data.x, data.y)
        self.cell_x = data.x
        self.cell_y = data.y
        self.cell_z = data.z
        self.allow_stretch = True
        self.size = config.SPRITE_SIZE
        self.size_hint = None, None
        self.x = sx
        self.y = sy + (layer * (int(config.TILE_SIZE // 2)))
        self.source = constants.IMG_PATHS[entity.sprite.image][layer]

    def move(self, vx, vy):
        svx, svy = utils.transform_to_screen(vx, vy)
        self.x += svx
        self.y += svy
        self.cell_x += vx
        self.cell_y += vy