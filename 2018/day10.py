import re

# Solution
def part1(data, modifier):
    return process_board(data, modifier)[0]

def part2(data, modifier):
    return process_board(data, modifier)[1]

def process_board(data, modifier):
    board = SkyBoard(data, modifier)
    current_size = board.board_size()
    new_size = current_size
    seconds = modifier
    while current_size >= new_size:
        board.step()
        current_size = new_size
        new_size = board.board_size()
        seconds += 1
    board.step(-1)
    seconds -= 1
    return (str(board), seconds)

class SkyBoard:
    def __init__(self, data, modifier):
        self._points = []
        for line in data:
            pattern = r'[0-9-]+'
            pos_x, pos_y, vel_x, vel_y = re.findall(pattern, line)
            p = Point(int(pos_x) + int(vel_x) * modifier, int(pos_y) + int(vel_y) * modifier, int(vel_x), int(vel_y))
            self._points.append(p)

    def __str__(self):
        mn, mx = self._min_max()
        s = '\n'
        for y in range(mn.y, mx.y + 1):
            for x in range(mn.x, mx.x + 1):
                s += '#' if Point(x, y) in self._points else '.'
            s += '\n'
        return s

    def board_size(self):
        mn, mx = self._min_max()
        return mx.x - mn.x + mx.y - mn.y

    def step(self, modifier = 1):
        for p in self._points:
            p.x += p.vx * modifier
            p.y += p.vy * modifier
    
    def _min_max(self):
        min_y = min(p.y for p in self._points)
        min_x = min(p.x for p in self._points)
        max_y = max(p.y for p in self._points)
        max_x = max(p.x for p in self._points)
        return (Point(min_x, min_y), Point(max_x, max_y))

class Point:
    def __init__(self, x, y, vx = 0, vy = 0):
        self.x = x
        self.y = y        
        self.vx = vx
        self.vy = vy
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

# Tests
def test(expected, actual):
    assert expected == actual, print('Expected:', expected, '\nActual:', actual)

test('''
#...#..###
#...#...#.
#...#...#.
#####...#.
#...#...#.
#...#...#.
#...#...#.
#...#..###
''', part1([
    'position=< 9,  1> velocity=< 0,  2>',
    'position=< 7,  0> velocity=<-1,  0>',
    'position=< 3, -2> velocity=<-1,  1>',
    'position=< 6, 10> velocity=<-2, -1>',
    'position=< 2, -4> velocity=< 2,  2>',
    'position=<-6, 10> velocity=< 2, -2>',
    'position=< 1,  8> velocity=< 1, -1>',
    'position=< 1,  7> velocity=< 1,  0>',
    'position=<-3, 11> velocity=< 1, -2>',
    'position=< 7,  6> velocity=<-1, -1>',
    'position=<-2,  3> velocity=< 1,  0>',
    'position=<-4,  3> velocity=< 2,  0>',
    'position=<10, -3> velocity=<-1,  1>',
    'position=< 5, 11> velocity=< 1, -2>',
    'position=< 4,  7> velocity=< 0, -1>',
    'position=< 8, -2> velocity=< 0,  1>',
    'position=<15,  0> velocity=<-2,  0>',
    'position=< 1,  6> velocity=< 1,  0>',
    'position=< 8,  9> velocity=< 0, -1>',
    'position=< 3,  3> velocity=<-1,  1>',
    'position=< 0,  5> velocity=< 0, -1>',
    'position=<-2,  2> velocity=< 2,  0>',
    'position=< 5, -2> velocity=< 1,  2>',
    'position=< 1,  4> velocity=< 2,  1>',
    'position=<-2,  7> velocity=< 2, -2>',
    'position=< 3,  6> velocity=<-1, -1>',
    'position=< 5,  0> velocity=< 1,  0>',
    'position=<-6,  0> velocity=< 2,  0>',
    'position=< 5,  9> velocity=< 1, -2>',
    'position=<14,  7> velocity=<-2,  0>',
    'position=<-3,  6> velocity=< 2, -1>',
], 1))

test(3, part2([
    'position=< 9,  1> velocity=< 0,  2>',
    'position=< 7,  0> velocity=<-1,  0>',
    'position=< 3, -2> velocity=<-1,  1>',
    'position=< 6, 10> velocity=<-2, -1>',
    'position=< 2, -4> velocity=< 2,  2>',
    'position=<-6, 10> velocity=< 2, -2>',
    'position=< 1,  8> velocity=< 1, -1>',
    'position=< 1,  7> velocity=< 1,  0>',
    'position=<-3, 11> velocity=< 1, -2>',
    'position=< 7,  6> velocity=<-1, -1>',
    'position=<-2,  3> velocity=< 1,  0>',
    'position=<-4,  3> velocity=< 2,  0>',
    'position=<10, -3> velocity=<-1,  1>',
    'position=< 5, 11> velocity=< 1, -2>',
    'position=< 4,  7> velocity=< 0, -1>',
    'position=< 8, -2> velocity=< 0,  1>',
    'position=<15,  0> velocity=<-2,  0>',
    'position=< 1,  6> velocity=< 1,  0>',
    'position=< 8,  9> velocity=< 0, -1>',
    'position=< 3,  3> velocity=<-1,  1>',
    'position=< 0,  5> velocity=< 0, -1>',
    'position=<-2,  2> velocity=< 2,  0>',
    'position=< 5, -2> velocity=< 1,  2>',
    'position=< 1,  4> velocity=< 2,  1>',
    'position=<-2,  7> velocity=< 2, -2>',
    'position=< 3,  6> velocity=<-1, -1>',
    'position=< 5,  0> velocity=< 1,  0>',
    'position=<-6,  0> velocity=< 2,  0>',
    'position=< 5,  9> velocity=< 1, -2>',
    'position=<14,  7> velocity=<-2,  0>',
    'position=<-3,  6> velocity=< 2, -1>',
], 1))

# Solve real puzzle 
filename = 'data/day10.txt'
data = [line.rstrip('\n') for line in open(filename, 'r')]

print('Day 10, part 1:\n', part1(data, 10000))
print('Day 10, part 2: %r' % (part2(data, 10000)))

