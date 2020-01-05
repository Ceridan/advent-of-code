import itertools
import math
import os
import re


# Solution
def part1(data, steps):
    moons = load_initial_data(data)
    result = 0
    pairs = [pair for pair in itertools.combinations(range(len(moons)), 2)]
    for _ in range(steps):
        calculate_step(moons, pairs)
    for k in moons.keys():
        pot = 0
        kin = 0
        for i in range(3):
           pot += abs(moons[k]['pos'][i])
           kin += abs(moons[k]['vel'][i])
        result += pot * kin
    return result


def part2(data):
    moons = load_initial_data(data)
    pairs = [pair for pair in itertools.combinations(range(len(moons)), 2)]
    initial_state = [[], [], []]
    for j in range(3):
        for i in range(len(moons)):
            initial_state[j].append(moons[i]['pos'][j])
            initial_state[j].append(moons[i]['vel'][j])
    step_state = [0, 0, 0]
    steps = 0
    while not all(step_state):
        calculate_step(moons, pairs)
        steps += 1
        for j in range(3):
            if step_state[j] == 0:
                arr = []
                for i in range(len(moons)):
                    arr.append(moons[i]['pos'][j])
                    arr.append(moons[i]['vel'][j])
                if initial_state[j] == arr:
                    step_state[j] = steps
    result = 1
    for j in range(3):
        result = lcm(result, step_state[j])
    return result


def calculate_step(moons, pairs):
    for pair in pairs:
        for i in range(3):
            if moons[pair[0]]['pos'][i] > moons[pair[1]]['pos'][i]:
                moons[pair[0]]['vel'][i] += -1
                moons[pair[1]]['vel'][i] += 1
            elif moons[pair[0]]['pos'][i] < moons[pair[1]]['pos'][i]:
                moons[pair[0]]['vel'][i] += 1
                moons[pair[1]]['vel'][i] += -1
    for k in moons.keys():
        for i in range(3):
            moons[k]['pos'][i] += moons[k]['vel'][i]


def load_initial_data(data):
    moons = dict()
    pattern = r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>'
    for i in range(len(data)):
        x, y, z = [int(m) for m in re.findall(pattern, data[i])[0]]
        moons[i] = {'pos': [x, y, z], 'vel': [0, 0, 0]}
    return moons


def lcm(a, b):
    return int(a / math.gcd(a, b)) * b


# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)


test(179, part1([
    '<x=-1, y=0, z=2>',
    '<x=2, y=-10, z=-7>',
    '<x=4, y=-8, z=8>',
    '<x=3, y=5, z=-1>',
], steps=10))

test(1940, part1([
    '<x=-8, y=-10, z=0>',
    '<x=5, y=5, z=10>',
    '<x=2, y=-7, z=3>',
    '<x=9, y=-8, z=-3>',
], steps=100))

test(2772, part2([
    '<x=-1, y=0, z=2>',
    '<x=2, y=-10, z=-7>',
    '<x=4, y=-8, z=8>',
    '<x=3, y=5, z=-1>',
]))

test(4686774924, part2([
    '<x=-8, y=-10, z=0>',
    '<x=5, y=5, z=10>',
    '<x=2, y=-7, z=3>',
    '<x=9, y=-8, z=-3>',
]))


# Solve real puzzle
dir_path = os.path.dirname(__file__)
file_path = os.path.join(dir_path, 'data/day12.txt')
input_data = [line.rstrip('\n') for line in open(file_path, 'r')]

print('Day 12, part 1: %r' % (part1(input_data, steps=1000)))
print('Day 12, part 2: %r' % (part2(input_data)))
