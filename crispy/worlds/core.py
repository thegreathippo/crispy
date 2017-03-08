from .grids import Grid2, Graph


def _empty(arg):
    pass


class World(Grid2):
    cell_defaults = {"solid": True,
                     "image": "void",
                     "wall": False,
                     "denizen": None,
                     "gui_callback": _empty
                     }

    @staticmethod
    def carve(cells, denizen=None):
        for cell in cells:
            convert_to_space(cell, denizen)
            for adj in cell.adjacents:
                if is_solid(adj):
                    convert_to_wall(adj)

    @staticmethod
    def fill(cells):
        for cell in cells:
            if any(not is_solid(n) for n in cell.adjacents):
                convert_to_wall(cell)
            else:
                convert_to_fill(cell)
            for node in cell.adjacents:
                if all(is_solid(n) for n in node.adjacents):
                    convert_to_fill(node)


def is_solid(cell):
    return cell.solid


def is_wall(cell):
    return cell.wall


def convert_to_space(cell, denizen):
    cell.image = "floor"
    cell.denizen = denizen
    cell.solid = False
    cell.wall = False
    cell.gui_callback(cell)


def convert_to_wall(cell):
    cell.image = "wall"
    cell.solid = True
    cell.wall = True
    cell.gui_callback(cell)


def convert_to_fill(cell):
    cell.image = "void"
    cell.solid = True
    cell.wall = False
    cell.gui_callback(cell)