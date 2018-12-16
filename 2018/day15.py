from collections import deque

# Solution
def part1(data):
    board, goblins, elves = init_board(data)
    rounds = 0
    while len(goblins) > 0 and len(elves) > 0:
        current_units = list(goblins.keys()) + list(elves.keys())
        current_units.sort(key=lambda x: (x[1], x[0]))
        killed = []       
        for unit_coords in current_units:   
            if unit_coords in killed:
                continue
            allies = elves if unit_coords in elves else goblins
            enemies = goblins if unit_coords in elves else elves
            if len(enemies) == 0:
                rounds -= 1
                break                     
            unit = allies.pop(unit_coords)
            step = next_step(unit_coords, allies, enemies, board)
            unit_coords = step
            try_attack(unit_coords, unit, enemies, killed)
            allies[unit_coords] = unit
        rounds += 1
    hits = sum(goblins[x].hits for x in goblins) + sum(elves[x].hits for x in elves)
    return rounds * hits
                
def part2(data):
    pass

def try_attack(unit_coords, unit, enemies, killed):
    enemy_coords = check_fight(unit_coords, enemies)
    if enemy_coords is None:
        return False
    enemies[enemy_coords].hits -= unit.damage
    if enemies[enemy_coords].hits <= 0:
        killed.append(enemy_coords)
        enemies.pop(enemy_coords)
    return True

def check_fight(unit_coords, enemies):
    x, y = unit_coords
    steps = [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]
    current_hits = 201
    current_step = None
    for step in steps:
        if step in enemies and enemies[step].hits < current_hits:
            current_hits = enemies[step].hits
            current_step = step
    return current_step

def next_step(unit_coords, allies, enemies, board):
    step_map = { unit_coords: [] }
    queue = deque([unit_coords])
    while len(queue) > 0:
        possible_solution = []
        new_queue = deque()
        while len(queue) > 0:
            x, y = queue.popleft()
            path = step_map[(x, y)]
            steps = [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]
            for step in steps:
                if step not in board or step in allies or step in step_map:
                    continue
                if step in enemies:
                    solution = [(x, y), path[1]] if len(path) > 1 else [(x, y), (x, y)]
                    possible_solution.append(solution)
                else:
                    new_queue.append(step)
                    step_map[step] = path + [(x, y)]
        if len(possible_solution) > 0:
            possible_solution.sort(key = lambda x: (x[0][1], x[0][0], x[1][1], x[1][0]))
            return possible_solution[0][1]
        queue = new_queue
    return unit_coords

def init_board(data):
    board = {}
    goblins = {}
    elves = {}
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == '#':
                continue
            if data[y][x] in 'G':
                goblins[(x, y)] = Unit(data[y][x])
            elif data[y][x] in 'E':
                elves[(x, y)] = Unit(data[y][x])                
            board[(x, y)] = []
            if x - 1 >= 0 and data[y][x - 1] != '#': board[(x, y)].append((x - 1, y))
            if x + 1 < len(data[y]) and data[y][x + 1] != '#': board[(x, y)].append((x + 1, y))
            if y - 1 >= 0 and data[y - 1][x] != '#': board[(x, y)].append((x, y - 1))
            if x + 1 < len(data) and data[y + 1][x] != '#': board[(x, y)].append((x, y + 1))
    return (board, goblins, elves)

def print_board(data, goblins, elves):
    units = {}
    units.update(goblins)
    units.update(elves)
    for y in range(len(data)):
        line_arr = ['.'] * len(data[y])
        line_add = ''
        for x in range(len(data[y])):
            if data[y][x] == '#':
                line_arr[x] = '#'
            elif (x, y) in units:
                unit = units[(x, y)]
                line_arr[x] = unit.type
                line_add += unit.type + '(' + str(unit.hits) + '), '
            line = ''.join(line_arr)
            if line_add:
                line += '   ' + line_add
        print(line)

class Unit:
    def __init__(self, unit_type):
        self.type = unit_type
        self.hits = 200
        self.damage = 3

# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)

test(27730, part1([
    '#######',   
    '#.G...#',
    '#...EG#',
    '#.#.#G#',
    '#..G#E#',
    '#.....#',   
    '#######',
]))
test(36334, part1([
    '#######',
    '#G..#E#',
    '#E#E.E#',
    '#G.##.#',
    '#...#E#',
    '#...E.#',
    '#######', 
]))
test(39514, part1([
    '#######',
    '#E..EG#',
    '#.#G.E#',
    '#E.##E#',
    '#G..#.#',
    '#..E#.#',
    '#######',
]))
test(27755, part1([
    '#######',
    '#E.G#.#',
    '#.#G..#',
    '#G.#.G#',
    '#G..#.#',
    '#...E.#',
    '#######',
]))
test(28944, part1([
    '#######',
    '#.E...#',
    '#.#..G#',
    '#.###.#',
    '#E#G#G#',
    '#...#G#',
    '#######',
]))
test(18740, part1([
    '#########',
    '#G......#',
    '#.E.#...#',
    '#..##..G#',
    '#...##..#',
    '#...#...#',
    '#.G...G.#',
    '#.....G.#',
    '#########',
]))

# Solve real puzzle
filename = 'data/day15.txt'
data = [line.rstrip('\n') for line in open(filename, 'r')]

print('Day 15, part 1: %r' % (part1(data)))
# print('Day 15, part 2: %r' % (part2(data)))
