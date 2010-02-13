
import random
import copy
import Image
import aggdraw

MAXPOLYGONS = 40
MAXPOINTS = 15

class DNA:
    def __init__(self, string=[], environ = {}):
        self._string = string
        self._environ = environ
        self._mutations = 0
        self._image = None

        if len(self._string) < MAXPOLYGONS:
            self.polygon_fill()

    def print_info(self):
        print '\tmutations:',
        print self._mutations

        print '\tpolygons:',
        print len(self._string)

        pls = []
        for p in self._string:
            pls.append(len(p[0]))
        total = sum(pls)
        print '\tavg points:',
        print float(total)/len(self._string)

    def get_image(self):
        if not self._image:
            width = self._environ['width']
            height = self._environ['height']
            self._image = Image.new('RGB', (width, height))
            self.draw_polygons()
        
        return self._image

    def draw_polygons(self):
        d = aggdraw.Draw(self._image)
        for poly in self._string:
            self.draw_polygon(poly, d)
        d.flush()

    def draw_polygon(self, poly, d):
        points = reduce(lambda x, y: x + y, poly[0], [])
        r, g, b, a = poly[1]

        b = aggdraw.Brush((r, g, b), a)
        d.polygon(points, None, b)

    def polygon_fill(self):
        for i in range(MAXPOLYGONS):
            self.add_black_polygon()

    def _random_point(self):
        max_x = self._environ.get('width', 0)
        max_y = self._environ.get('height', 0)

        return [
                random.randint(0, max_x),
                random.randint(0, max_y),
                ]

    def _move_point(self, point):
        x = point[0]
        y = point[1]

        x += random.randint(-40, 40)
        x = min(x, self._environ.get('height', 0))
        x = max(x, 0)

        y += random.randint(-40, 40)
        y = min(y, self._environ.get('width', 0))
        y = max(y, 0)

        point[0] = x
        point[1] = y

    def _change_color(self, color):
        color += random.randint(-80, 80)
        color = min(color, 255)
        color = max(color, 0)
        return color

    def add_black_polygon(self):
        if len(self._string) >= MAXPOLYGONS:
            return

        points = []
        for i in range(3):
            points.append(self._random_point())

        colors = [0, 0, 0, 0]

        self._string.append([
            points,
            colors,
            ])

    def add_polygon(self):
        if len(self._string) >= MAXPOLYGONS:
            return

        #if len(self._string) == 0:
        if True:
            points = []
            for i in range(3):
                points.append(self._random_point())

            colors = []
            for i in range(3):
                colors.append(
                        random.randint(0, 255))

            min_a = self._environ.get('min-alpha', 60)
            max_a = self._environ.get('max-alpha', 180)

            colors.append(random.randint(min_a, max_a))

            self._string.append([
                points,
                colors,
                ])

        else:
            newpoly = copy.deepcopy(self._string[-1])
            self._string.append(newpoly)
            self.mutate_polygon(len(self._string)-1)

    def add_point(self, p):
        points = self._string[p][0]

        k = random.randint(1, len(points)-1)

        p1 = points[k-1]
        p2 = points[k]

        max_x = max(p1[0], p2[0])
        min_x = min(p1[0], p2[0])
        max_y = max(p1[1], p2[1])
        min_y = min(p1[1], p2[1])

        x = random.randint(min_x, max_x)
        y = random.randint(min_y, max_y)

        np = [x, y]

        points.insert(k, np)

    def mutate_polygon(self, p):
        poly = self._string[p]

        # these need to be weighted somehow.
        # don't want add-point to be called as often as the
        # other two.
        ops = ['move-point', 'change-color']
        if len(poly[0]) < MAXPOINTS:
            ops.append('add-point')

        op = random.choice(ops)

        #print op # debug
        if op == 'add-point':
            points = poly[0]
            #points.append(self._random_point())
            self.add_point(p)
        elif op == 'move-point':
            points = poly[0]
            point = random.choice(points)
            self._move_point(point)
        elif op == 'change-color':
            colors = poly[1]
            c = random.randint(0, 2)
            colors[c] = self._change_color(colors[c])

            a = colors[3] + random.randint(-20, 20)
            min_a = self._environ.get('min-alpha', 60)
            max_a = self._environ.get('max-alpha', 180)

            a = min(a, max_a)
            a = max(a, min_a)

            colors[3] = a

    def mutate(self):
        # if there are no polygons, create one
        if len(self._string) == 0:
            self.add_polygon()

        else:
            p = random.randint(0, len(self._string)-1)
            self.mutate_polygon(p)

        # invalidate image so it gets recreated
        self._image = None
        self._mutations += 1

    def copy(self):
        newstring = copy.deepcopy(self._string)
        newenv = self._environ.copy()
        new = DNA(newstring, newenv)
        new._mutations = self._mutations
        if self._image:
            new._image = self._image
        return new

if __name__ == '__main__':
    d = DNA(environ={'height': 200, 'width': 300})
    print d._string
    c = d.copy()
    for i in range(10):
        c.mutate()
        print c._string
    

