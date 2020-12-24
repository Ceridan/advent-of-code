import os

from typing import List, Tuple, Dict

# Coordinates image: http://devmag.org.za/blog/wp-content/uploads/2013/08/screen_136.png
DIRECTIONS_TO_COORDS = {
    'e': (1, 0),
    'se': (1, -1),
    'sw': (0, -1),
    'w': (-1, 0),
    'nw': (-1, 1),
    'ne': (0, 1),
}


class Tile:
    def __init__(self, coords: (int, int)):
        self.x = coords[0]
        self.y = coords[1]
        self.color = True

    def flip(self):
        self.color = not self.color


def part1(tiles_list: List[str]) -> int:
    tiles = _parse_tiles_list(tiles_list)
    black = sum([1 if tile.color else 0 for tile in tiles.values()])
    return black


def part2(tiles_list: List[str], days: int) -> int:
    pass


def _parse_tiles_list(tiles_list: List[str]) -> Dict[Tuple[int, int], Tile]:
    tiles = {}

    for line in tiles_list:
        x, y, i = 0, 0, 0

        while i < len(line):
            ch = line[i]
            if ch in 'sn':
                i += 1
                ch += line[i]
            dx, dy = DIRECTIONS_TO_COORDS[ch]
            x += dx
            y += dy
            i += 1

        if (x, y) in tiles:
            tiles[(x, y)].flip()
        else:
            tiles[(x, y)] = Tile((x, y))

    return tiles


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test(10, part1([
    'sesenwnenenewseeswwswswwnenewsewsw',
    'neeenesenwnwwswnenewnwwsewnenwseswesw',
    'seswneswswsenwwnwse',
    'nwnwneseeswswnenewneswwnewseswneseene',
    'swweswneswnenwsewnwneneseenw',
    'eesenwseswswnenwswnwnwsewwnwsene',
    'sewnenenenesenwsewnenwwwse',
    'wenwwweseeeweswwwnwwe',
    'wsweesenenewnwwnwsenewsenwwsesesenwne',
    'neeswseenwwswnwswswnw',
    'nenwswwsewswnenenewsenwsenwnesesenew',
    'enewnwewneswsewnwswenweswnenwsenwsw',
    'sweneswneswneneenwnewenewwneswswnese',
    'swwesenesewenwneswnwwneseswwne',
    'enesenwswwswneneswsenwnewswseenwsese',
    'wnwnesenesenenwwnenwsewesewsesesew',
    'nenewswnwewswnenesenwnesewesw',
    'eneswnwswnwsenenwnwnwwseeswneewsenese',
    'neswnwewnwnwseenwseesewsenwsweewe',
    'wseweeenwnesenwwwswnew',
]))

# test(2208, part2([
#     'sesenwnenenewseeswwswswwnenewsewsw',
#     'neeenesenwnwwswnenewnwwsewnenwseswesw',
#     'seswneswswsenwwnwse',
#     'nwnwneseeswswnenewneswwnewseswneseene',
#     'swweswneswnenwsewnwneneseenw',
#     'eesenwseswswnenwswnwnwsewwnwsene',
#     'sewnenenenesenwsewnenwwwse',
#     'wenwwweseeeweswwwnwwe',
#     'wsweesenenewnwwnwsenewsenwwsesesenwne',
#     'neeswseenwwswnwswswnw',
#     'nenwswwsewswnenenewsenwsenwnesesenew',
#     'enewnwewneswsewnwswenweswnenwsenwsw',
#     'sweneswneswneneenwnewenewwneswswnese',
#     'swwesenesewenwneswnwwneseswwne',
#     'enesenwswwswneneswsenwnewswseenwsese',
#     'wnwnesenesenenwwnenwsewesewsesesew',
#     'nenewswnwewswnenesenwnesewesw',
#     'eneswnwswnwsenenwnwnwwseeswneewsenese',
#     'neswnwewnwnwseenwseesewsenwsweewe',
#     'wseweeenwnesenwwwswnew',
# ], days=100))


file_path = os.path.join(os.path.dirname(__file__), 'data/day24.txt')
with open(file_path, 'r') as f:
    input_data = [line.strip() for line in f.readlines()]

    print('Day 24, part 1: %r' % (part1(input_data)))
    print('Day 24, part 2: %r' % (part2(input_data, days=100)))
