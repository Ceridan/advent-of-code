# Solution
def part1(data):
    skill_cap = data
    recipes = [3, 7]
    cur1 = 0
    cur2 = 1
    k = 0
    while k < skill_cap + 10:
        val = recipes[cur1] + recipes[cur2]
        if val > 9:
            recipes.append(int(val / 10))
            k += 1
        recipes.append(val % 10)
        k += 1
        cur1 = (cur1 + recipes[cur1] + 1) % len(recipes)
        cur2 = (cur2 + recipes[cur2] + 1) % len(recipes)
    return ''.join(str(x) for x in recipes[skill_cap:skill_cap + 10])

def part2(data):
    skill_cap = data
    recipes = [3, 7]
    cur1 = 0
    cur2 = 1
    skill_array = [int(c) for c in str(skill_cap)]
    l = len(skill_array)
    while True:
        val = recipes[cur1] + recipes[cur2]
        if val > 9:
            recipes.append(int(val / 10))
            if skill_array == recipes[-l:]:
                return len(recipes) - l
        recipes.append(val % 10)
        if skill_array == recipes[-l:]:
            return len(recipes) - l
        cur1 = (cur1 + recipes[cur1] + 1) % len(recipes)
        cur2 = (cur2 + recipes[cur2] + 1) % len(recipes)

# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)

test('0124515891', part1(5))
test('5158916779', part1(9))
test('9251071085', part1(18))
test('5941429882', part1(2018))

test(5, part2('01245'))
test(9, part2('51589'))
test(18, part2('92510'))
test(2018, part2('59414'))

# Solve real puzzle
filename = 'data/day14.txt'
data = int([line.rstrip('\n') for line in open(filename, 'r')][0])

print('Day 14, part 1: %r' % (part1(data)))
print('Day 14, part 2: %r' % (part2(data)))
