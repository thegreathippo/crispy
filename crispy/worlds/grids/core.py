import collections
import math
from .graphs import Graph


CARDINALS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
]

ORDINALS = [
    (1, 1),
    (-1, 1),
    (-1, -1),
    (1, -1)
]

Cell = collections.namedtuple("Cell", ["x", "y"])
Edge = collections.namedtuple("Edge", ["uv"])
Arc = collections.namedtuple("Arc", ["u", "v"])


class Grid2:
    cell_defaults = {}
    edge_defaults = {}
    arc_defaults = {}
    cell_cls = Cell
    edge_cls = Edge
    arc_cls = Arc
    graph_cls = Graph

    def __init__(self, **kwargs):
        self._cells = dict()
        self._edges = dict()
        self._arcs = dict()
        if kwargs:
            self.cell_defaults = kwargs

        class Cell(self.cell_cls):
            @property
            def edge(self):
                return _get_edge_dict(self)

            @property
            def arc(self):
                return _get_arc_dict(self)

            @property
            def edges(self):
                return self._get_edges(self)

            @property
            def arcs(self):
                return self._get_arcs(self)

            @property
            def cardinal_edges(self):
                return self._get_cardinal_edges(self)

            @property
            def cardinal_arcs(self):
                return self._get_cardinal_arcs(self)

            @property
            def adjacents(self):
                return self._get_adjacencies(self)

            @property
            def cardinals(self):
                return self._get_cardinals(self)

            @property
            def ordinals(self):
                return self._get_ordinals(self)

            _get_edges = self._get_edges
            _get_arcs = self._get_arcs
            _get_cardinal_edges = self._get_cardinal_edges
            _get_cardinal_arcs = self._get_cardinal_arcs
            _get_adjacencies = self._get_adjacencies
            _get_cardinals = self._get_cardinals
            _get_ordinals = self._get_ordinals

        class Edge(self.edge_cls):
            pass

        class Arc(self.arc_cls):
            pass

        self._Cell = Cell
        self._Edge = Edge
        self._Arc = Arc

    def __call__(self, x, y):
        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError("{0}, {1} are not valid x-y coords".format(x, y))
        if (x, y) not in self._cells:
            cell = self._Cell(x, y)
            for attr in self.cell_defaults:
                setattr(cell, attr, self.cell_defaults[attr])
            self._cells[cell] = cell
        return self._cells[(x, y)]

    def edge(self, u, v):
        try:
            u, v = self(*u), self(*v)
        except (TypeError, ValueError):
            raise ValueError("{0}, {1} are not valid cells".format(u, v))
        if v not in u.adjacents or u not in v.adjacents:
            raise ValueError("{0}, {1} do not share an edge".format(u, v))
        uv = frozenset([u, v])
        if uv not in self._edges:
            edge = self._Edge(uv)
            for attr in self.edge_defaults:
                setattr(edge, attr, self.edge_defaults[attr])
            self._edges[uv] = edge
        return self._edges[uv]

    def arc(self, u, v):
        try:
            u, v = self(*u), self(*v)
        except (TypeError, ValueError):
            raise ValueError("{0}, {1} are not valid cells".format(u, v))
        if v not in u.adjacents or u not in v.adjacents:
            raise ValueError("{0}, {1} do not share an arc".format(u, v))
        if (u, v) not in self._arcs:
            arc = self._Arc(u, v)
            for attr in self.arc_defaults:
                setattr(arc, attr, self.arc_defaults[attr])
            self._arcs[(u, v)] = arc
        return self._arcs[(u, v)]

    def get_block(self, x, y, w, h):
        cells = set()
        w_i, h_i = 1, 1
        if w < 0:
            w_i = -1
        if h < 0:
            h_i = -1
        for cy in range(y, h + y, h_i):
            for cx in range(x, w + x, w_i):
                cells.add(self(cx, cy))
        return self.graph_cls(cells)

    def get_circle(self, x, y, radius):
        cells = set()
        for _x in range(-radius, radius):
            for _y in range(-radius, radius):
                if math.hypot(_x, _y) < radius:
                    cells.add(self(x + _x, y + _y))
        return self.graph_cls(cells)

    def _get_edges(self, cell):
        edges = set()
        for adjacent in cell.adjacents:
            edges.add(self.edge(cell, adjacent))
        return edges

    def _get_arcs(self, cell):
        arcs = set()
        for adjacent in cell.adjacents:
            arcs.add(self.arc(cell, adjacent))
        return arcs

    def _get_cardinal_edges(self, cell):
        edges = set()
        for cardinal in cell.cardinals:
            edges.add(self.edge(cell, cardinal))
        return edges

    def _get_cardinal_arcs(self, cell):
        arcs = set()
        for cardinal in cell.cardinals:
            arcs.add(self.arc(cell, cardinal))
        return arcs

    def _get_adjacencies(self, cell):
        x, y = cell
        adjacents = set()
        for xy in CARDINALS + ORDINALS:
            vx, vy = x + xy[0], y + xy[1]
            adjacents.add(self(vx, vy))
        return adjacents

    def _get_cardinals(self, cell):
        x, y = cell
        cardinals = set()
        for xy in CARDINALS:
            vx, vy = x + xy[0], y + xy[1]
            cardinals.add(self(vx, vy))
        return cardinals

    def _get_ordinals(self, cell):
        x, y = cell
        ordinals = set()
        for xy in ORDINALS:
            vx, vy = x + xy[0], y + xy[1]
            ordinals.add(self(vx, vy))
        return ordinals

    def __iter__(self):
        return iter(list(self._cells.keys()))


def _get_edge_dict(cell):
    edge_dict = dict()
    for edge in cell.edges:
        for c in edge.uv:
            if c == cell:
                continue
            edge_dict[c] = edge
    return edge_dict


def _get_arc_dict(cell):
    arc_dict = dict()
    for arc in cell.arcs:
        arc_dict[arc.v] = arc
    return arc_dict

