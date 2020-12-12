import os
from collections import namedtuple

from typing import List


Action = namedtuple('Action', "action value")

COMPASS_TO_INT = {'E': 0, 'N': 1, 'W': 2, 'S': 3}
INT_TO_COMPASS = {0: 'E', 1: 'N', 2: 'W', 3: 'S'}


class Ship:
    def __init__(self, actions: List[str], direction: str):
        self._actions = actions
        self._direction = direction
        self._compass = {'E': 0, 'N': 0, 'W': 0, 'S': 0}

    def move(self) -> int:
        for act in self._actions:
            action = Action(act[0], int(act[1:]))
            self._process_single_action(action)

        distance = abs(self._compass['E'] - self._compass['W']) + abs(self._compass['N'] - self._compass['S'])
        return distance

    def _process_single_action(self, action: Action) -> None:
        if action.action == 'F':
            self._compass[self._direction] += action.value
        elif action.action in ['L', 'R']:
            pivot = (action.value // 90) % 4
            pivot = pivot if action.action == 'L' else (4 - pivot) % 4
            pivot = (COMPASS_TO_INT[self._direction] + pivot) % 4
            self._direction = INT_TO_COMPASS[pivot]
        else:
            self._compass[action.action] += action.value


class Waypoint:
    def __init__(self, ew: Action, ns: Action):
        self.EW = ew
        self.NS = ns

    def move(self, action: Action):
        act, val = action

        if act in ['L', 'R']:
            pivot = (val // 90) % 4
            pivot = pivot if act == 'L' else (4 - pivot) % 4
            ew_pivot = (COMPASS_TO_INT[self.EW.action] + pivot) % 4
            ns_pivot = (COMPASS_TO_INT[self.NS.action] + pivot) % 4
            new_ew_action = Action(INT_TO_COMPASS[ew_pivot], self.EW.value)
            new_ns_action = Action(INT_TO_COMPASS[ns_pivot], self.NS.value)
            self.EW = new_ew_action if new_ew_action.action in ['E', 'W'] else new_ns_action
            self.NS = new_ns_action if new_ns_action.action in ['N', 'S'] else new_ew_action
        elif action.action in ['N', 'S']:
            direction = self.NS.action if self.NS.action == act or self.NS.value >= val else act
            value = self.NS.value + val if self.NS.action == act else abs(self.NS.value - val)
            self.NS = Action(direction, value)
        elif action.action in ['E', 'W']:
            direction = self.EW.action if self.EW.action == act or self.EW.value >= val else act
            value = self.EW.value + val if self.EW.action == act else abs(self.EW.value - val)
            self.EW = Action(direction, value)

        print(f'EW: {self.EW}')
        print(f'NS: {self.NS}')


class WaypointShip:
    def __init__(self, actions: List[str], waypoint_ew: Action, waypoint_ns: Action):
        self._actions = actions
        self._waypoint = Waypoint(waypoint_ew, waypoint_ns)
        self._compass = {'E': 0, 'N': 0, 'W': 0, 'S': 0}

    def move(self) -> int:
        for act in self._actions:
            action = Action(act[0], int(act[1:]))
            self._process_single_action(action)

        distance = abs(self._compass['E'] - self._compass['W']) + abs(self._compass['N'] - self._compass['S'])
        return distance

    def _process_single_action(self, action: Action) -> None:
        print(f'Action: {action.action}{action.value}')

        if action.action == 'F':
            self._compass[self._waypoint.EW.action] += self._waypoint.EW.value * action.value
            self._compass[self._waypoint.NS.action] += self._waypoint.NS.value * action.value
        else:
            self._waypoint.move(action)

        print(self._compass)


def part1(actions: List[str]) -> int:
    ship = Ship(actions, 'E')
    return ship.move()


def part2(actions: List[str]) -> int:
    ship = WaypointShip(actions, waypoint_ew=Action('E', 10), waypoint_ns=Action('N', 1))
    return ship.move()


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test(25, part1([
    'F10',
    'N3',
    'F7',
    'R90',
    'F11',
]))


test(286, part2([
    'F10',
    'N3',
    'F7',
    'R90',
    'F11',
]))


file_path = os.path.join(os.path.dirname(__file__), 'data/day12.txt')
with open(file_path, 'r') as f:
    input_data = [line.strip() for line in f.readlines()]

    print('Day 12, part 1: %r' % (part1(input_data)))
    print('Day 12, part 2: %r' % (part2(input_data)))
