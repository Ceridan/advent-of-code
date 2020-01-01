import os


# Solution
def part1(data, replaces=dict()):
    base_opcodes = [int(x) for x in data.split(',')]
    opcodes = initialize_opcodes(base_opcodes, replaces)
    return execute_opcodes(opcodes)


def part2(data, output):
    base_opcodes = [int(x) for x in data.split(',')]
    replaces = dict()
    for x in range(100):
        for y in range(100):
            replaces[1] = x
            replaces[2] = y
            opcodes = initialize_opcodes(base_opcodes, replaces)
            result = execute_opcodes(opcodes)
            if result == output:
                return 100 * replaces[1] + replaces[2]


def execute_opcodes(opcodes):
    k = 0
    while opcodes[k] != 99:
        if opcodes[k] == 1:
            opcodes[opcodes[k + 3]] = opcodes[opcodes[k + 1]] + opcodes[opcodes[k + 2]]
        elif opcodes[k] == 2:
            opcodes[opcodes[k + 3]] = opcodes[opcodes[k + 1]] * opcodes[opcodes[k + 2]]
        k += 4
    return opcodes[0]


def initialize_opcodes(base_opcodes, replaces):
    opcodes = [x for x in base_opcodes]
    for key in replaces:
        opcodes[key] = replaces[key]
    return opcodes


# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)


test(3500, part1('1,9,10,3,2,3,11,0,99,30,40,50'))
test(2, part1('1,0,0,0,99'))
test(2, part1('2,3,0,3,99'))
test(2, part1('2,4,4,5,99,0'))
test(30, part1('1,1,1,4,99,5,6,0,99'))


# Solve real puzzle
dir_path = os.path.dirname(__file__) 
file_path = os.path.join(dir_path, 'data/day02.txt')
input_data = [line.rstrip('\n') for line in open(file_path, 'r')][0]

print('Day 02, part 1: %r' % (part1(input_data, replaces={1: 12, 2: 2})))
print('Day 02, part 2: %r' % (part2(input_data, output=19690720)))
