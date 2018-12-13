# Solution
def part1(data):
    tracks, carts = parse_data(data)
    while True:
        current_carts = list(carts.keys())
        current_carts.sort()
        for coords in current_carts:
            cart = carts.pop(coords)
            if cart[0] in carts:
                return cart[0]
            update_cart_track(coords, cart, carts, tracks)            

def part2(data):
    tracks, carts = parse_data(data)
    while len(carts) > 1:
        current_carts = list(carts.keys())
        current_carts.sort()
        removed = []
        for coords in current_carts:
            if coords in removed:
                continue
            cart = carts.pop(coords)
            if cart[0] in carts:
                removed.append(cart[0])
                carts.pop(cart[0])
            else:   
                update_cart_track(coords, cart, carts, tracks)
    return list(carts.keys())[0]                

def update_cart_track(coords, cart, carts, tracks):
    track = tracks[cart[0]]            
    if len(track) == 2:
        if coords == track[0]:
            carts[cart[0]] = (track[1], cart[1])
        else:
            carts[cart[0]] = (track[0], cart[1])
    else:
        cross_turn = choose_cross_turn(coords, cart)
        carts[cart[0]] = (cross_turn, (cart[1] + 1) % 3)

def choose_cross_turn(current_coords, cart):
    current_x, current_y = current_coords
    new_x, new_y = cart[0]
    if current_x < new_x:
        if cart[1] == 0: return (new_x, new_y - 1)
        if cart[1] == 1: return (new_x + 1, new_y)
        if cart[1] == 2: return (new_x, new_y + 1)
    if current_x > new_x:
        if cart[1] == 0: return (new_x, new_y + 1)
        if cart[1] == 1: return (new_x - 1, new_y)
        if cart[1] == 2: return (new_x, new_y - 1)
    if current_y < new_y:
        if cart[1] == 0: return (new_x + 1, new_y)
        if cart[1] == 1: return (new_x, new_y + 1)
        if cart[1] == 2: return (new_x - 1, new_y)
    if current_y > new_y:
        if cart[1] == 0: return (new_x - 1, new_y)
        if cart[1] == 1: return (new_x, new_y - 1)
        if cart[1] == 2: return (new_x + 1, new_y)

def parse_data(data):
    tracks = {}
    carts = {}
    for y in range(len(data)):
        for x in range(len(data[y])):
            c = data[y][x]
            if c == '-':
                tracks[(x, y)] = [(x - 1, y), (x + 1, y)]
            elif c == '|':
                tracks[(x, y)] = [(x, y - 1), (x, y + 1)]
            elif c == '/':
                if x + 1 < len(data[y]) and data[y][x + 1] in '<>-+':
                    tracks[(x, y)] = [(x + 1, y), (x, y + 1)]
                else:
                    tracks[(x, y)] = [(x - 1, y), (x, y - 1)]
            elif c == '\\':
                if y + 1 < len(data) and data[y + 1][x] in '^v|+':
                    tracks[(x, y)] = [(x, y + 1), (x - 1, y)]
                else:
                    tracks[(x, y)] = [(x, y - 1), (x + 1, y)]
            elif c == '+':
                tracks[(x, y)] = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    for y in range(len(data)):
        for x in range(len(data[y])):
            c = data[y][x]    
            if c == '<':
                carts[(x, y)] = ((x - 1, y), 0)
            elif c == '>':
                carts[(x, y)] = ((x + 1, y), 0)
            elif c == '^':
                carts[(x, y)] = ((x, y - 1), 0)
            elif c == 'v':
                carts[(x, y)] = ((x, y + 1), 0)
            else:
                continue
            set_cart_track(x, y, tracks)
    return (tracks, carts)

def set_cart_track(x, y, tracks):
    tracks[(x, y)] = []
    if (x - 1, y) in tracks and (x, y) in tracks[x - 1, y]: tracks[(x, y)].append((x - 1, y))
    if (x, y + 1) in tracks and (x, y) in tracks[x, y + 1]: tracks[(x, y)].append((x, y + 1))
    if (x + 1, y) in tracks and (x, y) in tracks[x + 1, y]: tracks[(x, y)].append((x + 1, y))
    if (x, y - 1) in tracks and (x, y) in tracks[x, y - 1]: tracks[(x, y)].append((x, y - 1))
        
# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)

test((7, 3), part1([
'/->-\\        ',
'|   |  /----\\',
'| /-+--+-\\  |',
'| | |  | v  |',
'\\-+-/  \\-+--/',
'  \\------/',
]))

test((6, 4), part2([
'/>-<\\  ',
'|   |  ',
'| /<+-\\',
'| | | v',
'\\>+</ |',
'  |   ^',
'  \\<->/',
]))

# Solve real puzzle
filename = 'data/day13.txt'
data = [line.rstrip('\n') for line in open(filename, 'r')]

print('Day 13, part 1: (%r, %r)' % (part1(data)))
print('Day 13, part 2: (%r, %r)' % (part2(data)))
