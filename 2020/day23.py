import os

from typing import List


class Cup:
    def __init__(self, val: int, next_: 'Cup' = None):
        self.val = val
        self.next = next_

    def __repr__(self):
        return str(self.val)


def part1(cups_list: str, turns: int) -> str:
    current = _parse_cups_list(cups_list)

    for turn in range(1, turns + 1):
        removed = current.next
        removed_set = {removed.val, removed.next.val, removed.next.next.val}

        v = current.val - 1 if current.val > 1 else 9
        while v in removed_set:
            v = v - 1 if v > 1 else 9

        current.next = removed.next.next.next
        destination = current.next

        while destination.val != v:
            destination = destination.next

        removed.next.next.next = destination.next
        destination.next = removed

        current = current.next

    while current.val != 1:
        current = current.next

    current = current.next
    result = ''
    while current.val != 1:
        result += str(current.val)
        current = current.next

    return result


def part2(cups_list: str, turns: int, cups_amount: int) -> int:
    current, one, destinations = _parse_million_cups_list(cups_list, cups_amount)

    for turn in range(1, turns + 1):
        removed = current.next
        removed_set = {removed.val, removed.next.val, removed.next.next.val}

        destination = None
        for cup in destinations[current.val]:
            if cup.val not in removed_set:
                destination = cup
                break

        current.next = removed.next.next.next

        removed.next.next.next = destination.next
        destination.next = removed

        current = current.next

    return one.next.val * one.next.next.val


def _parse_cups_list(cups_list: str):
    first = None
    prev = None
    current = None

    for ch in cups_list.strip():
        if not first:
            first = Cup(int(ch))
            prev = first
        else:
            current = Cup(int(ch))
            prev.next = current
            prev = current

    current.next = first
    return first


def _parse_million_cups_list(cups_list: str, amount: int):
    cups = {i: Cup(i) for i in range(1, amount + 1)}

    destinations = {
        **{
            1: [cups[amount], cups[amount - 1], cups[amount - 2], cups[amount - 3]],
            2: [cups[1], cups[amount], cups[amount - 1], cups[amount - 2]],
            3: [cups[2], cups[1], cups[amount], cups[amount - 1]],
            4: [cups[3], cups[2], cups[1], cups[amount]],
        },
        **{i: [cups[i - 1], cups[i - 2], cups[i - 3], cups[i - 4]] for i in range(5, amount + 1)}
    }

    first = None
    prev = None
    current = None

    for ch in cups_list.strip():
        if not first:
            first = cups[int(ch)]
            prev = first
        else:
            current = cups[int(ch)]
            prev.next = current
            prev = current

    for i in range(10, amount + 1):
        current = cups[i]
        prev.next = current
        prev = current

    current.next = first

    return first, cups[1], destinations


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test('92658374', part1('389125467', turns=10))
test('67384529', part1('389125467', turns=100))
test(149245887792, part2('389125467', turns=10000000, cups_amount=1000000))


file_path = os.path.join(os.path.dirname(__file__), 'data/day23.txt')
with open(file_path, 'r') as f:
    input_data = f.read()

    print('Day 23, part 1: %r' % (part1(input_data, turns=100)))
    print('Day 23, part 2: %r' % (part2(input_data, turns=10000000, cups_amount=1000000)))
