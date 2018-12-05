import sys

# Solution
def part1(data):
    current_len = sys.maxsize
    while current_len > len(data):
        current_len = len(data)
        for i in range(26):           
            c1 = chr(i + 65)
            c2 = chr(i + 97)
            data = data.replace(c1 + c2, '')
            data = data.replace(c2 + c1, '')
    return current_len    

def part2(data):   
    current_length = sys.maxsize
    for i in range(26):
        tmp = data
        tmp = tmp.replace(chr(i + 65), '')
        tmp = tmp.replace(chr(i + 97), '')
        tmp_length = part1(tmp)
        if (tmp_length < current_length):
            current_length = tmp_length
    return current_length

# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)

test(10, part1('dabAcCaCBAcCcaDA'))
test(4, part2('dabAcCaCBAcCcaDA'))

# Solve real puzzle 
filename = 'data/day05.txt'
data = [line.rstrip('\n') for line in open(filename, 'r')][0]

print('Day 05, part 1: %r' % (part1(data)))
print('Day 05, part 2: %r' % (part2(data)))


