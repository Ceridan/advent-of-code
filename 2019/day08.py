import os
import sys


# Solution
def part1(data, image_wide, image_tall):
    result_zeros = sys.maxsize
    result = 0
    i = 0
    while i < len(data):
        layer = [0, 0, 0]
        for _ in range(image_wide * image_tall):
            x = int(data[i])
            if x in [0, 1, 2]:
                layer[x] += 1
            i += 1
        if layer[0] < result_zeros:
            result_zeros = layer[0]
            result = layer[1] * layer[2]
    return result


def part2(data, image_wide, image_tall):
    image = [[] for _ in range(image_tall)]
    for y in range(image_tall):
        for x in range(image_wide):
            k = x + y * image_wide
            v = int(data[k])
            while v == 2:
                k += image_wide * image_tall
                v = int(data[k])
            image[y].append(v)
    return print_image(image, image_wide, image_tall)


def print_image(image, image_wide, image_tall):
    printed = '\n'
    for y in range(image_tall):
        printed += ' '.join([str(v) for v in image[y]]) + '\n'
    return printed


# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)


test(1, part1('123456789012', image_wide=3, image_tall=2))
test(6, part1('000121011122', image_wide=3, image_tall=2))

test("""
0 1
1 0
""", part2('0222112222120000', image_wide=2, image_tall=2))


# Solve real puzzle
file_path = os.path.abspath('data/day08.txt')
input_data = [line.rstrip('\n') for line in open(file_path, 'r')][0]

print('Day 08, part 1: %r' % (part1(input_data, image_wide=25, image_tall=6)))
print('Day 08, part 2:', part2(input_data, image_wide=25, image_tall=6).replace('0', ' ').replace('1', '*'))
