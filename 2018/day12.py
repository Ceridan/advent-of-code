import re

# Solution
def part1(data, generation_number):
    state, rules = parse_data(data)
    offset = 4
    for _ in range(generation_number):
        state, offset = calculate_new_state(state, rules, offset)
    pots_sum = 0
    for i in range(len(state)):
        if state[i] == '#':
            pots_sum += i - offset
    return pots_sum

def part2(data, generation_number, stable_modifier):
    state, rules = parse_data(data)
    offset = 4
    for _ in range(stable_modifier):
        state, offset = calculate_new_state(state, rules, offset)
    pots_sum = 0
    for i in range(len(state)):
        if state[i] == '#':
            pots_sum += i - offset + generation_number - stable_modifier
    return pots_sum

def calculate_new_state(state, rules, offset):
    tmp = ['.'] * len(state)
    for rule in rules:
        pattern = re.compile('(?=' + re.escape(rule[0]) + ')')
        match = pattern.finditer(state)
        for m in match:
            tmp[m.start() + 2] = rule[1]
    state = ''.join(tmp)
    if not state.startswith('....'):
        state = '....' + state
        offset += 4
    if not state.endswith('....'):
        state = state + '....'
    return (state, offset)

def parse_data(data):
    rules = []
    initial_state = '....' + data[0].replace('initial state: ', '') + '....'
    for i in range(2, len(data)):
        rule = data[i].split(' => ')
        rules.append((rule[0], rule[1]))
    return (initial_state, rules) 

# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)

test(325, part1([
    'initial state: #..#.#..##......###...###',
    '',
    '...## => #',
    '..#.. => #',
    '.#... => #',
    '.#.#. => #',
    '.#.## => #',
    '.##.. => #',
    '.#### => #',
    '#.#.# => #',
    '#.### => #',
    '##.#. => #',
    '##.## => #',
    '###.. => #',
    '###.# => #',
    '####. => #',
], 20))

# Solve real puzzle 
filename = 'data/day12.txt'
data = [line.rstrip('\n') for line in open(filename, 'r')]

print('Day 12, part 1: %r' % (part1(data, 20)))
print('Day 12, part 2: %r' % (part2(data, 50000000000, 200)))