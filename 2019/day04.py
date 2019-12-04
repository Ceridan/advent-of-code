import os


# Solution
def part1(data):
    return digit_loop(data, 1)


def part2(data):
    return digit_loop(data, 2)


def digit_loop(data, validation_rule_number):
    bounds = data.split('-')
    passwords = dict()
    for a in range(int(bounds[0][0]), 10):
        if a > int(bounds[1][0]): break
        for b in range(a, 10):
            if b < a: continue
            for c in range(b, 10):
                if c < b: continue
                for d in range(c, 10):
                    if d < c: continue
                    for e in range(d, 10):
                        if e < d: continue
                        for f in range(e, 10):
                            if f < e: continue
                            if (validation_rule_number == 1 and range_rule_1(a, b, c, d, e, f)) \
                                    or (validation_rule_number == 2 and range_rule_2(a, b, c, d, e, f)):
                                value = a * 100000 + b * 10000 + c * 1000 + d * 100 + e * 10 + f
                                passwords[value] = True
    lbound = int(bounds[0])
    rbound = int(bounds[1])
    result = len([x for x in passwords.keys() if lbound <= x <= rbound])
    return result


def range_rule_1(a, b, c, d, e, f):
    return a == b or b == c or c == d or d == e or e == f


def range_rule_2(a, b, c, d, e, f):
    return (a == b and b != c) \
           or (b == c and a != b and c != d) \
           or (c == d and b != c and d != e) \
           or (d == e and c != d and e != f) \
           or (e == f and d != e)


# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)


test(1, part1('111111-111111'))
test(0, part1('223450-223450'))
test(0, part1('123789-123789'))

test(1, part2('112233-112233'))
test(0, part2('123444-123444'))
test(1, part2('111122-111122'))

# Solve real puzzle
file_path = os.path.abspath('data/day04.txt')
input_data = [line.rstrip('\n') for line in open(file_path, 'r')][0]

print('Day 04, part 1: %r' % (part1(input_data)))
print('Day 04, part 2: %r' % (part2(input_data)))
