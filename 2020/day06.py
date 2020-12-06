import os


from collections import defaultdict
from typing import List


# Solution
def part1(form_data: str) -> int:
    groups = _parse_form_data(form_data)
    answer_count = 0

    for group in groups:
        answers = {}
        for answer in ''.join(group):
            answers[answer] = 1
        answer_count += sum(answers.values())

    return answer_count


def part2(form_data: str) -> int:
    groups = _parse_form_data(form_data)
    answer_count = 0

    for group in groups:
        answers = defaultdict(int)
        for answer in ''.join(group):
            answers[answer] += 1
        answer_count += sum([1 for v in answers.values() if v == len(group)])

    return answer_count


def _parse_form_data(form_data: str) -> List[List[str]]:
    forms = form_data.split('\n\n')
    groups = []

    for group_data in forms:
        group = group_data.strip().split('\n')
        groups.append(group)

    return groups

# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)


test(11, part1("""
abc

a
b
c

ab
ac

a
a
a
a

b
"""))

test(6, part2("""
abc

a
b
c

ab
ac

a
a
a
a

b
"""))


# Solve real puzzle
dir_path = os.path.dirname(__file__)
file_path = os.path.join(dir_path, 'data/day06.txt')
with open(file_path, 'r') as f:
    input_data = f.read()

    print('Day 06, part 1: %r' % (part1(input_data)))
    print('Day 06, part 2: %r' % (part2(input_data)))
