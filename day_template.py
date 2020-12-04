import os


# Solution
from typing import List


def part1(data: List[str]) -> None:
    pass


def part2(data: List[str]) -> None:
    pass


# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)


# Solve real puzzle
dir_path = os.path.dirname(__file__)
file_path = os.path.join(dir_path, 'data/dayXX.txt')
with open(file_path, 'r') as f:
    input_data = [line.strip() for line in f.readlines()]

    print('Day XX, part 1: %r' % (part1(input_data)))
    print('Day XX, part 2: %r' % (part2(input_data)))
