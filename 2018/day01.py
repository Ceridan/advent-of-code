def part1(data):
    frequency = sum(int(x) for x in data)
    return frequency

def part2(data):
    known_frequency = { 0: True }
    frequency = 0
    while True:
        for x in data:
            frequency += int(x)
            if frequency in known_frequency:
                return frequency
            known_frequency[frequency] = True

# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)

test(3, part1(['+1', '-2', '+3', '+1']))
test(3, part1(['+1', '+1', '+1']))
test(0, part1(['+1', '+1', '-2']))
test(-6, part1(['-1', '-2', '-3']))

test(2, part2(['+1', '-2', '+3', '+1']))
test(0, part2(['+1', '-1']))
test(10, part2(['+3', '+3', '+4', '-2', '-4']))
test(5, part2(['-6', '+3', '+8', '+5', '-6']))
test(14, part2(['+7', '+7', '-2', '-7', '-4']))

# Solve real puzzle 
filename = 'data/day01.txt'
content = [line.rstrip('\n') for line in open(filename, 'r')]

print('Day 01, part 1: %r' % (part1(content)))
print('Day 01, part 2: %r' % (part2(content)))
