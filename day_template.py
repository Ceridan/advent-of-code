import os

from typing import List


def part1(data: List[str]) -> None:
    pass


def part2(data: List[str]) -> None:
    pass


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


file_path = os.path.join(os.path.dirname(__file__), 'data/dayXX.txt')
with open(file_path, 'r') as f:
    input_data = [line.strip() for line in f.readlines()]

    print('Day XX, part 1: %r' % (part1(input_data)))
    print('Day XX, part 2: %r' % (part2(input_data)))
