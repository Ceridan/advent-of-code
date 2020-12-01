import os


# Solution
def part1(input_data) -> None:
    pass


def part2(input_data) -> None:
    pass


# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)


# Solve real puzzle
dir_path = os.path.dirname(__file__)
file_path = os.path.join(dir_path, 'data/day{{XX}}.txt')
with open(file_path, 'r') as f:
    input_data = [int(line) for line in f.readlines()]

    print('Day 01, part 1: %r' % (part1(input_data)))
    print('Day 01, part 2: %r' % (part2(input_data)))
