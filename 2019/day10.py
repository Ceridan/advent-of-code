import math
import os


# Solution
def part1(data, print_coords=False):
    grid = create_grid(data)
    result_sum = 0
    for xc in range(len(grid)):
        for yc in range(len(grid[xc])):
            if grid[xc][yc] == 0:
                continue
            sight = dict()
            for xt in range(len(grid)):
                for yt in range(len(grid[xt])):
                    if grid[xt][yt] == 0 or (xc, yc) == (xt, yt):
                        continue
                    dx = 1 if xc > xt else 0
                    dy = 1 if yc > yt else 0
                    k, b = get_equation_params((xc, yc), (xt, yt))
                    if (k, b, dx, dy) in sight:
                        sight[(k, b, dx, dy)].append((xt, yt))
                    else:
                        sight[(k, b, dx, dy)] = [(xt, yt)]
            current_sum = len(sight.keys())
            if current_sum > result_sum:
                result_sum = current_sum
                inverted_result_pos = (yc, xc)
    if print_coords:
        print('Asteroid coordinates: ', inverted_result_pos)
    return result_sum


def part2(data, laser_coords, asteroid_index):
    yc, xc = laser_coords
    grid = create_grid(data)
    sights = [dict(), dict(), dict(), dict()]
    for xt in range(len(grid)):
        for yt in range(len(grid[xt])):
            if grid[xt][yt] == 0 or (xc, yc) == (xt, yt):
                continue
            dist = get_distance((xc, yc), (xt, yt))
            sin, cos = get_sin_cos((xc, yc), (xt, yt), dist)
            quadrant = get_quadrant(sin, cos)
            if (sin, cos) in sights[quadrant]:
                sights[quadrant][(sin, cos)].append((xt, yt, dist))
            else:
                sights[quadrant][(sin, cos)] = [(xt, yt, dist)]

    result = []
    k = 0
    while len(result) < asteroid_index:
        if sights[k]:
            coords = sorted(sights[k].keys(), key=lambda elem: elem[0] if k in (0, 3) else -elem[0])
            for coord in coords:
                vals = sorted(sights[k][coord], key=lambda elem: elem[2])
                val = (vals[0][0], vals[0][1])
                result.append(val)
                if len(vals) > 1:
                    sights[k][coord] = vals[1:]
                else:
                    del sights[k][coord]
        k = (k + 1) % 4
    return result[asteroid_index - 1][1] * 100 + result[asteroid_index - 1][0]


def get_quadrant(sin, cos):
    if sin >= 0 and cos < 0:
        return 0
    elif sin >= 0 and cos >= 0:
        return 1
    elif sin < 0 and cos > 0:
        return 2
    return 3


def create_grid(data):
    lines = [l for l in data.split('\n') if l]
    grid = []
    for line in lines:
        row = [1 if v == '#' else 0 for v in line]
        grid.append(row)
    return grid


def get_equation_params(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    if x1 == x2:
        return (x1, None)
    k = round((y2 - y1) / (x2 - x1), 10)
    b = y1 - k * x1
    return (k, b)


def get_sin_cos(point1, point2, distance):
    x1, y1 = point1
    x2, y2 = point2
    nx2 = x2 - x1
    ny2 = y2 - y1
    return (round(ny2 / distance, 10), round(nx2 / distance, 10))


def get_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2) 


# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)


test(8, part1("""
.#..#
.....
#####
....#
...##
"""))

test(33, part1("""
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
"""))

test(35, part1("""
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
"""))

test(41, part1("""
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
"""))

test(210, part1("""
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""))


test(1403, part2("""
.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....#...###..
..#.#.....#....##
""", laser_coords=(8, 3), asteroid_index=36))

test(802, part2("""
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
""", laser_coords=(11, 13), asteroid_index=200))


# Solve real puzzle
dir_path = os.path.dirname(__file__)
file_path = os.path.join(dir_path, 'data/day10.txt')
with open(file_path, 'r') as file:
    input_data = file.read()

print('Day 10, part 1: %r' % (part1(input_data, print_coords=True)))
print('Day 10, part 2: %r' % (part2(input_data, laser_coords=(11, 19), asteroid_index=200)))
