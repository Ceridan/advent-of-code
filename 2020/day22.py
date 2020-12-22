import heapq
import os

from typing import List, Tuple


def part1(deck: List[str]) -> int:
    player1, player2 = _parse_deck(deck)

    while player1 and player2:
        _, num1 = heapq.heappop(player1)
        _, num2 = heapq.heappop(player2)

        if num1 > num2:
            w = heapq.nlargest(1, player1)[0][0] if player1 else 0
            heapq.heappush(player1, (w + 1, num1))
            heapq.heappush(player1, (w + 2, num2))
        else:
            w = heapq.nlargest(1, player2)[0][0] if player2 else 0
            heapq.heappush(player2, (w + 1, num2))
            heapq.heappush(player2, (w + 2, num1))

    winner = player1 if player1 else player2
    score = 0
    n = len(winner)
    i = 0

    while winner:
        _, num = heapq.heappop(winner)
        score += num * (n - i)
        i += 1

    return score


def part2(deck: List[str]) -> None:
    pass


def _parse_deck(deck: List[str]) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    player1 = []
    player2 = []

    player = 1

    for line in deck:
        if not line:
            continue

        if line == 'Player 1:':
            continue
        elif line == 'Player 2:':
            player = 2
            continue

        if player == 1:
            player1.append(int(line))
        else:
            player2.append(int(line))

    heap1 = [(w, num) for w, num in enumerate(player1)]
    heapq.heapify(heap1)

    heap2 = [(w, num) for w, num in enumerate(player2)]
    heapq.heapify(heap2)

    return heap1, heap2


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test(306, part1([
    'Player 1:',
    '9',
    '2',
    '6',
    '3',
    '1',
    '',
    'Player 2:',
    '5',
    '8',
    '4',
    '7',
    '10',
]))


file_path = os.path.join(os.path.dirname(__file__), 'data/day22.txt')
with open(file_path, 'r') as f:
    input_data = [line.strip() for line in f.readlines()]

    print('Day 22, part 1: %r' % (part1(input_data)))
    print('Day 22, part 2: %r' % (part2(input_data)))
