# Solution
def part1(data):
    twos_count = 0
    threes_count = 0
    for line in data:
        letters = {}
        for c in line:
            letters[c] = letters[c] + 1 if c in letters else 1 
        twos = sum(i == 2 for i in list(letters.values()))
        threes = sum(i == 3 for i in list(letters.values()))
        twos_count += 1 if twos > 0 else 0
        threes_count += 1 if threes > 0 else 0
    return twos_count * threes_count

def part2(data):
    for i in range(len(data[0])):
        line_dict = {}
        for line in data:
            sub_line = line[:i] + line[i + 1:]
            line_dict[sub_line] = line_dict[sub_line] + 1 if sub_line in line_dict else 1
        for key in line_dict:
            if line_dict[key] > 1:
                return key

# Test
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)

test(12, part1(['abcdef', 'bababc', 'abbcde', 'abcccd', 'aabcdd', 'abcdee', 'ababab']))
test('fgij', part2(['abcde', 'fghij', 'klmno', 'pqrst', 'fguij', 'axcye', 'wvxyz']))

# Solve real puzzle 
filename = 'data/day02.txt'
data = [line.rstrip('\n') for line in open(filename, 'r')]

print('Day 01, part 1: %r' % (part1(data)))
print('Day 01, part 2: %r' % (part2(data)))