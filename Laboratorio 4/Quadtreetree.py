import math

class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x  # Centro X
        self.y = y  # Centro Y
        self.w = w  # Semiancho
        self.h = h  # Semialto

    def contains(self, point):
        return (point[0] >= self.x - self.w and
                point[0] <= self.x + self.w and
                point[1] >= self.y - self.h and
                point[1] <= self.y + self.h)

    def intersects(self, range_box):
        return not (range_box.x - range_box.w > self.x + self.w or
                    range_box.x + range_box.w < self.x - self.w or
                    range_box.y - range_box.h > self.y + self.h or
                    range_box.y + range_box.h < self.y - self.h)

class Quadtree:
    def __init__(self, boundary, capacity=4):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False

    def subdivide(self):
        x, y = self.boundary.x, self.boundary.y
        w, h = self.boundary.w / 2, self.boundary.h / 2

        # Creamos los 4 cuadrantes
        nw = Rectangle(x - w, y + h, w, h)
        ne = Rectangle(x + w, y + h, w, h)
        sw = Rectangle(x - w, y - h, w, h)
        se = Rectangle(x + w, y - h, w, h)

        self.northwest = Quadtree(nw, self.capacity)
        self.northeast = Quadtree(ne, self.capacity)
        self.southwest = Quadtree(sw, self.capacity)
        self.southeast = Quadtree(se, self.capacity)
        self.divided = True

    def insert(self, point):
        if not self.boundary.contains(point):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True

        if not self.divided:
            self.subdivide()

        # Intentar insertar en los hijos
        return (self.northeast.insert(point) or
                self.northwest.insert(point) or
                self.southeast.insert(point) or
                self.southwest.insert(point))

    def query_range(self, range_box, found_points):
        if not self.boundary.intersects(range_box):
            return

        for p in self.points:
            if range_box.contains(p):
                found_points.append(p)

        if self.divided:
            self.northwest.query_range(range_box, found_points)
            self.northeast.query_range(range_box, found_points)
            self.southwest.query_range(range_box, found_points)
            self.southeast.query_range(range_box, found_points)

    def query_nearest(self, target, best=None):
        for p in self.points:
            dist = math.hypot(p[0] - target[0], p[1] - target[1])
            if best is None or dist < best[0]:
                best = (dist, p)

        if self.divided:
            for q in [self.northwest, self.northeast, self.southwest, self.southeast]:
                res = q.query_nearest(target, best)
                if res and (best is None or res[0] < best[0]):
                    best = res

        return best 