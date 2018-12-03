import re

# # Solution
def part1(data):
    pattern = r'\#([0-9]+) \@ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)'
    tiles = {}
    for line in data:
        (id, left, top, width, height) = re.findall(pattern, line)[0]
        (id, left, top, width, height) = (int(id), int(left), int(top), int(width), int(height))
        for x in range(left, left + width):
            for y in range(top, top + height):
                tiles[(x, y)] = tiles[(x, y)] + 1 if (x, y) in tiles else 1
    result = sum(tiles[(x, y)] > 1 for (x, y) in tiles)        
    return result

def part2(data):       
    pattern = r'\#([0-9]+) \@ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)'
    tiles = {}
    ids = {}
    for line in data:
        (id, left, top, width, height) = re.findall(pattern, line)[0]
        (id, left, top, width, height) = (int(id), int(left), int(top), int(width), int(height))
        ids[id] = True
        for x in range(left, left + width):
            for y in range(top, top + height):
                if (x, y) in tiles:
                    ids[tiles[(x, y)]] = False
                    ids[id] = False
                else:
                    tiles[(x, y)] = id
    for tid in ids:
        if ids[tid]:
            return tid

# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)

test(4, part1([
    '#1 @ 1,3: 4x4',
    '#2 @ 3,1: 4x4',
    '#3 @ 5,5: 2x2'
]))
test(3, part2([
    '#1 @ 1,3: 4x4',
    '#2 @ 3,1: 4x4',
    '#3 @ 5,5: 2x2'
]))

# Solve real puzzle 
filename = 'data/day03.txt'
data = [line.rstrip('\n') for line in open(filename, 'r')]

print('Day 03, part 1: %r' % (part1(data)))
print('Day 03, part 2: %r' % (part2(data)))