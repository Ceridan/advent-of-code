import string
import sys

# Solution
def part1(data):
    return process_sequence(data)

def part2(data):
    current_len = sys.maxsize
    for c in string.ascii_lowercase:
        tmp_len = process_sequence(data, c)
        if (tmp_len < current_len):
            current_len = tmp_len
    return current_len

def process_sequence(data, excluded_char = False):
    stack = []
    for c in data:
        if (excluded_char and excluded_char == c.lower()):
            continue
        if (len(stack) > 0 and stack[-1] != c and stack[-1].lower() == c.lower()):
            stack.pop()
        else:
            stack.append(c)
    return len(stack)

# Naive solution
def part1_naive(data):
    current_len = sys.maxsize
    while current_len > len(data):
        current_len = len(data)
        for i in range(26):           
            c1 = chr(i + 65)
            c2 = chr(i + 97)
            data = data.replace(c1 + c2, '')
            data = data.replace(c2 + c1, '')
    return current_len    

def part2_naive(data):   
    current_len = sys.maxsize
    for i in range(26):
        tmp = data
        tmp = tmp.replace(chr(i + 65), '')
        tmp = tmp.replace(chr(i + 97), '')
        tmp_len = part1(tmp)
        if (tmp_len < current_len):
            current_len = tmp_len
    return current_len

# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)

test(10, part1('dabAcCaCBAcCcaDA'))
test(4, part2('dabAcCaCBAcCcaDA'))

test(10, part1_naive('dabAcCaCBAcCcaDA'))
test(4, part2_naive('dabAcCaCBAcCcaDA'))

# Solve real puzzle 
filename = 'data/day05.txt'
data = [line.rstrip('\n') for line in open(filename, 'r')][0]

print('Day 05, part 1: %r' % (part1(data)))
print('Day 05, part 2: %r' % (part2(data)))


