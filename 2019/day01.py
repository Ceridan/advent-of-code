import os


# Solution
def part1(data):
    fuels = [int(x) // 3 - 2 for x in data]
    return sum(fuels)


def part2(data):
    mass = [int(x) for x in data]
    result = 0
    for x in mass:
        fuel = x // 3 - 2
        if fuel > 0:
            result += fuel
            mass.append(fuel)
    return result


# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)


test(2, part1([12]))
test(2, part1([14]))
test(654, part1([1969]))
test(33583, part1([100756]))
test(34241, part1([12, 14, 1969, 100756]))

test(2, part2([14]))
test(966, part2([1969]))
test(50346, part2([100756]))
test(51314, part2([14, 1969, 100756]))


# Solve real puzzle
dir_path = os.path.dirname(__file__) 
file_path = os.path.join(dir_path, 'data/day01.txt')
input_data = [line.rstrip('\n') for line in open(file_path, 'r')]

print('Day 01, part 1: %r' % (part1(input_data)))
print('Day 01, part 2: %r' % (part2(input_data)))
