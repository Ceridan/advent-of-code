# Solution
def part1(data, size, minutes):
    board = init_board(data, size)
    for _ in range(minutes):
        tile_transform(board)
    trees = sum([sum([1 for x in range(1, len(board[y]) - 1) if board[y][x][0] == '|']) for y in range(1, len(board) - 1)])
    lumberyards = sum([sum([1 for x in range(1, len(board[y]) - 1) if board[y][x][0] == '#']) for y in range(1, len(board) - 1)])
    return trees * lumberyards

def part2(data, size, minutes):
    pass

def tile_transform(board):
    for y in range(1, len(board) - 1):
        for x in range(1, len(board[0]) - 1):
            board[y][x][1] = board[y][x][0]            
    for y in range(1, len(board) - 1):
        for x in range(1, len(board[0]) - 1):
            trees, lumberyards, _ = calculate_adjacent((x, y), board)
            if board[y][x][0] == '.' and trees >= 3:
               board[y][x][0] = '|'
            elif board[y][x][0] == '|' and lumberyards >= 3:
               board[y][x][0] = '#'
            elif board[y][x][0] == '#' and (lumberyards == 0 or trees == 0):
               board[y][x][0] = '.' 

def calculate_adjacent(tile_coords, board):
    x, y = tile_coords
    trees = sum([sum([1 for ix in range(x - 1, x + 2) if (ix, iy) != (x, y) and board[iy][ix][1] == '|']) for iy in range(y - 1, y + 2)])
    lumberyards = sum([sum([1 for ix in range(x - 1, x + 2) if (ix, iy) != (x, y) and board[iy][ix][1] == '#']) for iy in range(y - 1, y + 2)]) 
    empty = 8 - trees - lumberyards
    return (trees, lumberyards, empty)    

def init_board(data, size):
    board = [[['-', '-'] for x in range(0, size[0] + 2)] for y in range(0, size[1] + 2)]
    for y in range(1, len(data) + 1):
        for x in range(1, len(data[0]) + 1):
            board[y][x] = [data[y - 1][x - 1], data[y - 1][x - 1]]
    return board

def print_board(board):
    for y in range(1, len(board) - 1):
        s = ''
        for x in range(1, len(board[y]) - 1):
            s += board[y][x][0]
        print(s)
    print('\n')


# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)

test(1147, part1([
    '.#.#...|#.',
    '.....#|##|',
    '.|..|...#.',
    '..|#.....#',
    '#.#|||#|#|',
    '...#.||...',
    '.|....|...',
    '||...#|.#|',
    '|.||||..|.',
    '...#.|..|.',
], (10,10), 10))

# Solve real puzzle 
filename = 'data/day18.txt'
data = [line.rstrip('\n') for line in open(filename, 'r')]

print('Day 18, part 1: %r' % (part1(data, (50, 50), 10)))
print('Day 18, part 2: %r' % (part2(data, (50, 50), 1000000000)))
