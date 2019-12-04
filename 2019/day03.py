import os


# Solution
def part1(data):
    grid = dict()
    parse_line(data[0], grid, 1)
    parse_line(data[1], grid, 2)
    result = min(abs(x[0]) + abs(x[1]) for x in grid.keys() if grid[x][0] == 3 and x != (0, 0))
    return result


def part2(data):
    grid = dict()
    parse_line(data[0], grid, 1)
    parse_line(data[1], grid, 2)
    result = min(grid[x][1] for x in grid.keys() if grid[x][0] == 3 and x != (0, 0))
    return result


def parse_line(line, grid, value):
    steps = 0
    current = (0, 0)
    next_current = (0, 0)
    for path in line.split(','):
        x, y = current
        direction = path[0]
        if direction == 'U':
            next_current = (x, y + int(path[1:]))
        elif direction == 'R':
            next_current = (x + int(path[1:]), y)
        elif direction == 'D':
            next_current = (x, y - int(path[1:]))
        elif direction == 'L':
            next_current = (x - int(path[1:]), y)
        steps = fill_grid(grid, current, next_current, value, steps)
        current = next_current


def fill_grid(grid, start, end, value, steps):
    for (x, y) in generate_steps(start, end):
        steps += 1
        if (x, y) not in grid:
            grid[(x, y)] = [value, steps]
        elif (grid[(x, y)][0] & value) == 0:
            grid[(x, y)][0] |= value
            grid[(x, y)][1] += steps
    return steps


def generate_steps(start, end):
    if start[0] == end[0]:
        step = 1 if end[1] - start[1] > 0 else -1
        y = start[1]
        while y != end[1]:
            y += step
            yield (start[0], y)
    elif start[1] == end[1]:
        step = 1 if end[0] - start[0] > 0 else -1
        x = start[0]
        while x != end[0]:
            x += step
            yield (x, start[1])


# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)


test(6, part1(['R8,U5,L5,D3', 'U7,R6,D4,L4']))
test(159, part1(['R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83']))
test(135, part1(['R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7']))
test(30, part2(['R8,U5,L5,D3', 'U7,R6,D4,L4']))
test(610, part2(['R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83']))
test(410, part2(['R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7']))

# Solve real puzzle
file_path = os.path.abspath('data/day03.txt')
input_data = [line.rstrip('\n') for line in open(file_path, 'r')]

print('Day 03, part 1: %r' % (part1(input_data)))
print('Day 03, part 2: %r' % (part2(input_data)))
