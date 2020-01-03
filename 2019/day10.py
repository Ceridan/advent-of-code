import os


# Solution
def part1(data):
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
    return result_sum


def part2(data):
    return 0


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
    k = (y2 - y1) / (x2 - x1)
    b = y1 - k * x1
    return (k, b)


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


# Solve real puzzle
dir_path = os.path.dirname(__file__)
file_path = os.path.join(dir_path, 'data/day10.txt')
with open(file_path, 'r') as file:
    input_data = file.read()

print('Day 10, part 1: %r' % (part1(input_data)))
print('Day 10, part 2: %r' % (part2(input_data)))
