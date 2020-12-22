import heapq
import os
from collections import deque

from typing import List, Tuple


def part1(deck: List[str]) -> int:
    player1, player2 = _parse_deck(deck)

    while player1 and player2:
        _, num1 = heapq.heappop(player1)
        _, num2 = heapq.heappop(player2)

        winner = player1 if num1 > num2 else player2
        w = heapq.nlargest(1, winner)[0][0] if winner else 0
        heapq.heappush(winner, (w + 1, max(num1, num2)))
        heapq.heappush(winner, (w + 2, min(num1, num2)))

    return _calculate_score(player1, player2)


def part2(deck: List[str]) -> int:
    player1, player2 = _parse_deck(deck)
    _, p1, p2 = _recursive_combat(player1, player2)
    return _calculate_score(player1, player2)


def _recursive_combat(player1: List[Tuple[int, int]], player2: List[Tuple[int, int]]) -> Tuple[bool, List[Tuple[int, int]], List[Tuple[int, int]]]:
    states = set()

    while player1 and player2:
        current_state = f'{str([num for _, num in heapq.nsmallest(len(player1), player1)])}{str([num for _, num in heapq.nsmallest(len(player2), player2)])}'
        if current_state in states:
            return True, [], []

        states.add(current_state)

        _, num1 = heapq.heappop(player1)
        _, num2 = heapq.heappop(player2)

        if num1 <= len(player1) and num2 <= len(player2):
            new_player1 = [pair for pair in heapq.nsmallest(num1, player1)]
            heapq.heapify(player1)
            new_player2 = [pair for pair in heapq.nsmallest(num2, player2)]
            heapq.heapify(player2)
            is_p1, _, _ = _recursive_combat(new_player1, new_player2)
            winner = player1 if is_p1 else player2
            w = heapq.nlargest(1, winner)[0][0] if winner else 0
            heapq.heappush(winner, (w + 1, num1 if is_p1 else num2))
            heapq.heappush(winner, (w + 2, num2 if is_p1 else num1))
            continue

        winner = player1 if num1 > num2 else player2
        w = heapq.nlargest(1, winner)[0][0] if winner else 0
        heapq.heappush(winner, (w + 1, max(num1, num2)))
        heapq.heappush(winner, (w + 2, min(num1, num2)))

    return len(player1) > 0, player1, player2


def _calculate_score(player1: List[Tuple[int, int]], player2: List[Tuple[int, int]]) -> int:
    winner = player1 if player1 else player2
    score = 0
    n = len(winner)
    i = 0

    while winner:
        _, num = heapq.heappop(winner)
        score += num * (n - i)
        i += 1

    return score


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

test(105, part2([
    'Player 1:',
    '43',
    '19',
    '',
    'Player 2:',
    '2',
    '29',
    '14',
]))

test(291, part2([
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
