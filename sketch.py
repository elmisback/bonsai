
import Tkinter
import random
import math


class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent

    def __sub__(self, node):
        return Node(self.x - node.x, self.y - node.y)

    def __add__(self, node):
        return Node(self.x + node.x, self.y + node.y)

    def __iter__(self):
        return iter([self.x, self.y])

    def __repr__(self):
        return "Node(x={x}, y={y}, parent={parent})".format(**self.__dict__)

    def __cmp__(self, node):
        return cmp((self.x, self.y), (node.x, node.y))

def intersect(((x00, y00), (x01, y01)), ((x10, y10), (x11, y11))):
    """Determines whether the lines intersect.

    See http://stackoverflow.com/questions/563198/
         how-do-you-detect-where-two-line-segments-intersect
    """
    p = (float(x00), float(y00))
    r = (float(x01 - x00), float(y01 - y00))
    q = (float(x10), float(y10))
    s = (float(x11 - x10), float(y11 - y10))

    cross = lambda (a, b), (c, d): a * d - b * c
    dot = lambda (a, b), (c,d): (a * c) + (b * d)
    sub = lambda (a, b), (c,d): (a - c, b - d)
    # q + u s gives the point of possible intersection.
    if cross(r, s) == 0:
        if cross(sub(q, p), r) == 0:
            # Colinear
            t0 = dot(sub(q, p), r) / dot(r, r)
            t1 = t0 + dot(s, r) / dot(r, r)
            if dot(s, r) < 0:
                tmp = t0
                t0 = t1
                t1 = tmp
            if t0 > 1 or t1 < 0:
                return False
            return True  # (overlapping)
        else:
            # Parallel
            return False
    else:
        u = cross(sub(q, p), r) / cross(r, s)
        t = cross(sub(q, p), s) / cross(r, s)
        if 0 <= u <= 1 and 0 <= t <= 1:
            # The segments meet at
            #  q + u s = p + t r
            return True
        return False  # No intersection.

def valid_line((x0, y0), (x1, y1)):
    maxwidth = 1000
    maxheight = 1000
    if x1 < 0 or y1 < 0 or x1 >= maxwidth or y1 >= maxwidth:
        return False
    for line in lines:
        if Node(x0, y0) in line:
            continue
        if intersect(((x0, y0), (x1, y1)), line):
            return False
    return True

def grow_from(p, dist):
    """Creates a new segment starting at x0, y0."""
    (x0, y0) = p
    x1, y1 = -1, -1
    dot = lambda (a, b), (c,d): (a * c) + (b * d)
    mag = lambda (a, b): (a**2 + b**2)**.5
    if p.parent:
        v = (x0 - p.parent.x, y0 - p.parent.y)
        w = (1, 0)
        old_theta = math.acos(dot(v, w) / (mag(v) * mag(w)))
    else:
        old_theta = math.pi/2
    tries = 5
    while not valid_line((x0, y0), (x1, y1)):
        if tries == 0:
            return False
        # f(.5) = old_theta
        # f(1) = old_theta + math.pi
        # f(0) = old_theta - math.pi
        # f(x) = old_theta - math.pi + 2x * math.pi
        #
        #theta = old_theta - math.pi + 2 * random.triangular() * math.pi
        theta = random.gauss(old_theta, 1.3 - tries * .1)# - math.pi + 2 * random.triangular() * math.pi
        if not p.parent: theta = math.pi/2
        #theta = random.random() * 2 * math.pi
        x1, y1 = (x0 + dist * math.cos(theta),
                  y0 - dist * math.sin(theta))
        tries -= 1
    return Node(x1, y1, p)

def grow_trunk(start, dist, width):
    for i in xrange(5):
        end = grow_from(start, dist * (.7 ** i))
        if not end:
            break
        line = (start, end)
        lines.append(line)
        w.create_line(map(tuple, line), width=width * (.8 ** i))
        start = end

root = Tkinter.Tk()
w = Tkinter.Canvas(root, width=1000, height=1000)
w.pack()

lines = []
start = Node(350, 700)
grow_trunk(start, 120, 20.0)

n = len(lines)
for _, p1 in list(lines):
    grow_trunk(p1, 60, 10.0)
to_grow = lines[n:]
n = len(lines)
for _, p1 in to_grow:
    grow_trunk(p1, 30, 5.0)
to_grow = lines[n:]
n = len(lines)
for _, p1 in to_grow:
    grow_trunk(p1, 15, 2.0)

print "Entering mainloop."
Tkinter.mainloop()
