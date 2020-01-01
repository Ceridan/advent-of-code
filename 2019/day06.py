import os


# Solution
def part1(data):
    orbits = create_orbits_dict(data)
    result = 0
    for key in orbits.keys():
        result += calculate_orbits(orbits, key)
    return result


def part2(data):
    orbits = create_orbits_dict(data)
    you_path = traverse_path(orbits, 'YOU')
    san_path = traverse_path(orbits, 'SAN')
    for i in range(len(you_path)):
        for j in range(len(san_path)):
            if you_path[i] == san_path[j]:
                return i + j
    return 0


def create_orbits_dict(data):
    orbits = dict()
    orbits['COM'] = None
    for orbit in data:
        root, satellite = orbit.split(')')
        orbits[satellite] = root
    return orbits


def calculate_orbits(orbits, key):
    result = 0
    while orbits[key] is not None:
        result += 1
        key = orbits[key]
    return result


def traverse_path(orbits, key):
    path = []
    while orbits[key] is not None:
        path.append(orbits[key])
        key = orbits[key]
    return path


# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)


test(42, part1(['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L']))
test(4, part2(['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L', 'K)YOU', 'I)SAN']))

# Solve real puzzle
file_path = os.path.abspath('data/day06.txt')
input_data = [line.rstrip('\n') for line in open(file_path, 'r')]

print('Day 06, part 1: %r' % (part1(input_data)))
print('Day 06, part 2: %r' % (part2(input_data)))
