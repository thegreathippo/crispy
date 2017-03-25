from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.image import Image
from kivy.graphics.transformation import Matrix
import config


class ViewScreen(ScatterLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layers = []
        for i in range(-1, 2):
            layer = SpriteLayer(i)
            self.layers.append(layer)
            self.add_widget(layer)
        self.eids = dict()

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

    def move_camera(self, old_val, new_val):
        if old_val.x != new_val.x or old_val.y != new_val.y:
            vx, vy = new_val.x - old_val.x, new_val.y - old_val.y
            mat = Matrix().translate(vx, vy, 0)
            self.apply_transform(mat)
        if old_val.z != new_val.z:
            pass


class SpriteLayer(FloatLayout):

    def __init__(self, z, **kwargs):
        super().__init__(**kwargs)
        self.z = z
        self.y_sort = dict()
        self.eids = dict()

    def add_sprite(self, entity):
        sprite = Sprite(entity, self.z)
        if sprite.cell_x not in self.y_sort:
            self.y_sort[sprite.cell_x] = list()
        self.y_sort[sprite.cell_x].append(sprite)
        self.y_sort[sprite.cell_x].sort(key=lambda s: s.cell_y, reverse=True)
        self.reload()
        self.eids[entity.eid] = sprite

    def remove_sprite(self, eid):
        sprite = self.eids[eid]
        self.y_sort[sprite.cell_x].remove(sprite)
        if not self.y_sort[sprite.cell_x]:
            del self.y_sort[sprite.cell_x]
        del self.eids[eid]
        self.remove_widget(sprite)

    def move_sprite(self, eid, old_pos, new_pos):
        sprite = self.eids[eid]
        vx, vy = new_pos.x - old_pos.x, new_pos.y - old_pos.y
        sprite.move(vx, vy)
        self.y_sort[old_pos.x].remove(sprite)
        if not self.y_sort[old_pos.x]:
            del self.y_sort[old_pos.x]
        if sprite.cell_x not in self.y_sort:
            self.y_sort[sprite.cell_x] = list()
        self.y_sort[sprite.cell_x].append(sprite)
        self.y_sort[sprite.cell_x].sort(key=lambda s: s.cell_y, reverse=True)
        self.reload()

    def reload(self):
        self.clear_widgets()
        for x in self.y_sort:
            for s in self.y_sort[x]:
                self.add_widget(s)


class Sprite(Image):
    def __init__(self, entity, layer):
        super().__init__()
        data = entity.sprite
        sx, sy = config.transform_to_screen(data.x, data.y)
        self.cell_x = data.x
        self.cell_y = data.y
        self.cell_z = data.z
        self.allow_stretch = True
        self.size = config.SPRITE_SIZE
        self.size_hint = None, None
        self.x = sx
        self.y = sy + (layer * (int(config.TILE_SIZE // 2)))
        self.source = config.IMG_PATHS[entity.image][layer]

    def move(self, vx, vy):
        svx, svy = config.transform_to_screen(vx, vy)
        self.x += svx
        self.y += svy
        self.cell_x += vx
        self.cell_y += vy