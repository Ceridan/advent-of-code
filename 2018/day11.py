# Solution
def part1(serial_number):
    best_coords = (1, 1)
    best_power_level = -45
    grid = [[None for x in range(301)] for y in range(301)]
    for y in range(1, 298):
        for x in range(1, 298):
            current_power_level = 0
            for dy in range(3):
                for dx in range(3):
                    if grid[y + dy][x + dx] is None:
                        grid[y + dy][x + dx] = cell_power_level(x + dx, y + dy, serial_number)
                    current_power_level += grid[y + dy][x + dx]
            if current_power_level > best_power_level:
                best_coords = (x, y)
                best_power_level = current_power_level
    return best_coords

def part2(serial_number):
    result = (1, 1, 1)
    best_power_level = -450000
    grid = [[None for x in range(301)] for y in range(301)]
    for y in range(1, 301):
        for x in range(1, 301):
            grid[y][x] = cell_power_level(x, y, serial_number)
    for ly in range(1, 301):
        current_sums = [0] * 301
        for ry in range(ly, 301):
            for i in range(1, 301):
                current_sums[i] += grid[ry][i]
            k_left, k_right, k_sum = kadane_max_array_sum(current_sums, ry - ly + 1)
            if k_sum > best_power_level:
                best_power_level = k_sum
                result = (k_left, ly, k_right - k_left + 1)
    return result

def cell_power_level(x, y, serial_number):
    rack_id = x + 10
    power_level_base = (rack_id * y + serial_number) * rack_id
    hundred_digit = int((power_level_base % 1000) / 100)
    return hundred_digit - 5

def kadane_max_array_sum(arr, size):
    best_sum = -450000
    left = 1
    right = -1
    for i in range(1, len(arr) - size + 1):
        current_sum = 0
        for k in range(0, size):
            current_sum += arr[i + k]
        if current_sum < 0:
            current_sum = 0
        elif current_sum > best_sum:
            best_sum = current_sum
            left = i
            right = i + size - 1
    return (left, right, best_sum)

# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)

test(4, cell_power_level(x = 3, y = 5, serial_number = 8))
test(-5, cell_power_level(x = 122, y = 79, serial_number = 57))
test(0, cell_power_level(x = 217, y = 196, serial_number = 39))
test(4, cell_power_level(x = 101, y = 153, serial_number = 71))

test((5, 5, 4), kadane_max_array_sum([None, 3, 2, 0, -1, 4], 1))
test((1, 2, 5), kadane_max_array_sum([None, 3, 2, 0, -1, 4], 2))
test((1, 3, 5), kadane_max_array_sum([None, 3, 2, 0, -1, 4], 3))
test((2, 5, 5), kadane_max_array_sum([None, 3, 2, 0, -1, 4], 4))

test((33, 45), part1(18))
test((21, 61), part1(42))

test((90, 269, 16), part2(18))
test((232, 251, 12), part2(42))

# Solve real puzzle 
filename = 'data/day11.txt'
data = int([line.rstrip('\n') for line in open(filename, 'r')][0])

print('Day 11, part 1: (%r, %r)' % (part1(data)))
print('Day 11, part 2: (%r, %r, %r)' % (part2(data)))
