from collections import deque
import re

# Solution
def part1(data):
    pattern = r'([0-9]+), ([0-9]+)'
    border = Point(0, 0)
    points = deque()
    ids = {}
    for i in range(len(data)):
        (x, y) = re.findall(pattern, data[i])[0]
        (id, x, y) = (i, int(x), int(y))
        if border.x < x: border.x = x
        if border.y < y: border.y = y
        ids[id] = 0
        points.append(NamedPoint(id, x, y, 0))
    border.x += 1
    border.y += 1
    matrix = [[None for ix in range(border.x + 1)] for iy in range(border.y + 1)]
    while len(points) > 0:
        current_point = points.popleft()
        top = NamedPoint(current_point.id, current_point.x, current_point.y - 1, current_point.dist + 1)
        right = NamedPoint(current_point.id, current_point.x + 1, current_point.y, current_point.dist + 1)
        bottom = NamedPoint(current_point.id, current_point.x, current_point.y + 1, current_point.dist + 1)
        left = NamedPoint(current_point.id, current_point.x - 1, current_point.y, current_point.dist + 1)
        point_step(top, points, matrix, ids, border)
        point_step(right, points, matrix, ids, border)
        point_step(bottom, points, matrix, ids, border)
        point_step(left, points, matrix, ids, border)
    (_, val) = max(ids.items(), key=lambda x: x[1])
    return val

def part2(data, limit):
    pattern = r'([0-9]+), ([0-9]+)'
    border = Point(0, 0)
    points = []
    region = 0
    for i in range(len(data)):
        (x, y) = re.findall(pattern, data[i])[0]
        (x, y) = (int(x), int(y))
        points.append(Point(x, y))
        if border.x < x: border.x = x
        if border.y < y: border.y = y
    border.x += 1
    border.y += 1
    for y in range(border.y + 1):
        for x in range(border.x + 1):
            if check_distance(points, Point(x, y), limit):
                region += 1
    return region

def point_step(next_point, points, matrix, ids, border):
    if check_out_of_border(next_point, border):
        ids[next_point.id] = -1
        return
    if matrix[next_point.y][next_point.x] is None:
        matrix[next_point.y][next_point.x] = (next_point.id, next_point.dist)
        if ids[next_point.id] > -1: ids[next_point.id] += 1
        points.append(next_point)
        return
    (m_id, m_dist) = matrix[next_point.y][next_point.x]
    if next_point.dist < m_dist:
        if m_id is not None and ids[m_id] > -1: ids[m_id] -= 1
        matrix[next_point.y][next_point.x] = (next_point.id, next_point.dist)
        if ids[next_point.id] > -1: ids[next_point.id] += 1
        points.append(next_point)
    elif next_point.dist == m_dist and next_point.id != m_id:
        if m_id is not None and ids[m_id] > -1: ids[m_id] -= 1
        matrix[next_point.y][next_point.x] = (None, m_dist)

def check_out_of_border(point, border):
    return point.x < 0 or point.y < 0 or point.x > border.x or point.y > border.y

def check_distance(points, current_point, limit):
    sum = 0
    for p in points:
        sum += abs(p.x - current_point.x) + abs(p.y - current_point.y)
        if sum >= limit:
            return False
    return True

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class NamedPoint(Point):
    def __init__(self, id, x, y, dist):
        self.id = id
        self.dist = dist
        super(NamedPoint, self).__init__(x, y)

# Test
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)

test(17, part1(['1, 1', '1, 6', '8, 3', '3, 4', '5, 5', '8, 9']))
test(16, part2(['1, 1', '1, 6', '8, 3', '3, 4', '5, 5', '8, 9'], 32))

# Solve real puzzle 
filename = 'data/day06.txt'
data = [line.rstrip('\n') for line in open(filename, 'r')]

print('Day 06, part 1: %r' % (part1(data)))
print('Day 06, part 2: %r' % (part2(data, 10000)))