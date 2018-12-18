import re
from collections import deque

# Solution
def part1(data):
    result = calculate_spring_water(data, '|~')
    return result

def part2(data):
    result = calculate_spring_water(data, '~')
    return result

def calculate_spring_water(data, water_tiles):
    points, mn, mx = read_data(data)
    board = init_board(points, mn, mx)
    source_x = 500 - mn[0] + 1
    board[0][source_x] = '+'
    fall_down((source_x, 1), board)
    result = sum([sum([1 for x in range(0, len(board[y])) if board[y][x] in water_tiles]) for y in range(mn[1], len(board))])
    return result

def fall_down(start_point, board):
    points = deque([(start_point)])
    filled = []
    while len(points) > 0:
        x, y = points.popleft()
        while y < len(board):
            if board[y][x] == '.':
                board[y][x] = '|'
            elif board[y][x] in '~#':
                if (x, y - 1) not in filled:
                    filled.append((x, y - 1))
                    fill_result = fill_line((x, y - 1), board)
                    for p in fill_result:
                        points.append(p)
                break
            y += 1

def fill_line(point, board):
    x, y = point
    if y == 0 or y == len(board) - 1:
        return []
    lborder = rborder = False
    for lx in range(x - 1, -1, -1):
        if board[y][lx] == '#':
            lborder = True
            break
        board[y][lx] = '|'
        if board[y + 1][lx] not in '~#':
            break
    for rx in range(x + 1, len(board[0])):
        if board[y][rx] == '#':
            rborder = True
            break
        board[y][rx] = '|'
        if board[y + 1][rx] not in '~#':
            break
    if lborder and rborder:
        for ix in range(lx + 1, rx):
            board[y][ix] = '~'
        if y - 1 > 0:
            return [(x, y - 1)]
    fall_down_points = []
    if not lborder:
        fall_down_points.append((lx, y))
    if not rborder:
        fall_down_points.append((rx, y))
    return fall_down_points

def init_board(points, mn, mx):
    board = [[points[(x, y)] if (x, y) in points else '.' for x in range(mn[0] - 1, mx[0] + 2)] for y in range(0, mx[1] + 1)]
    return board

def read_data(data):
    pattern = r'(x|y)=([0-9]+), (x|y)=([0-9]+)\.\.([0-9]+)'
    clay_points = {}
    for line in data:
        c1, v1, _, v21, v22 = re.findall(pattern, line)[0]
        v1, v21, v22 = int(v1), int(v21), int(v22)
        if c1 == 'x':
            for y in range(v21, v22 + 1):
                clay_points[(v1, y)] = '#'
        else:
            for x in range(v21, v22 + 1):
                clay_points[(x, v1)] = '#'
    x_min = min(x[0] for x in clay_points.keys())
    x_max = max(x[0] for x in clay_points.keys())
    y_min = min(y[1] for y in clay_points.keys())
    y_max = max(y[1] for y in clay_points.keys())
    return (clay_points, (x_min, y_min), (x_max, y_max))

def print_board(board):
    # filename = 'data/day17_output.txt'
    # f = open(filename, 'w')
    for y in range(len(board)):
        print(''.join(board[y]))
    #     f.write(''.join(board[y]) + '\n')
    # f.close()

# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)

test(57, part1([
    'x=495, y=2..7',
    'y=7, x=495..501',
    'x=501, y=3..7',
    'x=498, y=2..4',
    'x=506, y=1..2',
    'x=498, y=10..13',
    'x=504, y=10..13',
    'y=13, x=498..504',
]))

test(29, part2([
    'x=495, y=2..7',
    'y=7, x=495..501',
    'x=501, y=3..7',
    'x=498, y=2..4',
    'x=506, y=1..2',
    'x=498, y=10..13',
    'x=504, y=10..13',
    'y=13, x=498..504',
]))

# Solve real puzzle 
filename = 'data/day17.txt'
data = [line.rstrip('\n') for line in open(filename, 'r')]

print('Day 17, part 1: %r' % (part1(data)))
print('Day 17, part 2: %r' % (part2(data)))
