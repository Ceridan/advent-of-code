from collections import deque

# Solution
def part1(data):
    board, goblins, elves = init_board(data)
    rounds = 0
    while len(goblins) > 0 and len(elves) > 0:
        if rounds < 10:
            print(rounds)
            print_board(data, goblins, elves)
        current_units = list(goblins.keys()) + list(elves.keys())
        current_units.sort(key=lambda x: (x[1], x[0]))       
        for unit_coords in current_units:   
            if unit_coords not in goblins and unit_coords not in elves:
                continue
            allies = elves if unit_coords in elves else goblins
            enemies = goblins if unit_coords in elves else elves
            if len(enemies) == 0:
                rounds -= 1
                break                     
            unit = allies.pop(unit_coords)
            if not try_attack(unit_coords, unit, enemies):
                step = unit_next_step(unit_coords, allies, enemies, board)
                unit_coords = step
                try_attack(unit_coords, unit, enemies)
            allies[unit_coords] = unit
        rounds += 1
    hits = sum(goblins[x].hits for x in goblins) + sum(elves[x].hits for x in elves)
    print_board(data, goblins, elves)
    print (rounds, hits, rounds * hits)
    return rounds * hits
                
def part2(data):
    pass

def try_attack(unit_coords, unit, enemies):
    enemy_coords = check_fight(unit_coords, enemies)
    if enemy_coords is not None:
        enemies[enemy_coords].hits -= unit.damage
        if enemies[enemy_coords].hits <= 0:
            enemies.pop(enemy_coords)
        return True
    return False

def unit_next_step(unit_coords, allies, enemies, board):
    target_tiles = get_target_tiles(allies, enemies, board)
    if len(target_tiles) == 0:
        return unit_coords
    units = {}
    units.update(allies)
    units.update(enemies)
    tile_map = create_tile_map(unit_coords, board, units)
    min_dist = None
    for tile in target_tiles:
        if tile in tile_map:
            target_tiles[tile] = tile_map[tile]
            if min_dist is None or min_dist > tile_map[tile]:
                min_dist = tile_map[tile]
    if min_dist is None:
        return unit_coords
    targets = [x for x in target_tiles if target_tiles[x] == min_dist]
    targets.sort(key=lambda x: (x[1], x[0]))
    target_point = targets[0]
    target_point_tile_map = create_tile_map(target_point, board, units)
    return calculate_best_path(unit_coords, target_point, target_point_tile_map)

def calculate_best_path(current, target, target_map):
    x, y = current
    dist = None
    best_step = current
    steps = [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]
    for step in steps:
        if step in target_map:
            if dist is None or dist > target_map[step]:
                best_step = step
                dist = target_map[step]
    return best_step

def create_tile_map(tile, board, units):
    tiles = deque([(tile[0], tile[1], 0)])
    tile_map = { tile: 0 }
    while len(tiles) > 0:
        x, y, d = tiles.popleft()
        steps = [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]
        for step in steps:
            if step in board and (step not in tile_map or tile_map[step] > d + 1) and step not in units:
                tile_map[step] = d + 1
                tiles.append((step[0], step[1], d + 1))
    return tile_map

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

def get_target_tiles(allies, enemies, board):
    target_tiles = {}
    for unit_coords in enemies:
        x, y = unit_coords
        steps = [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]
        for step in steps:
            if step in board and step not in allies and step not in enemies:
                target_tiles[step] = None  
    return target_tiles

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
