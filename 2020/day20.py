import os
from collections import namedtuple, Counter
from copy import deepcopy
from math import sqrt

from typing import List, Dict, Tuple, Set, Union


TileVariants = namedtuple('TileVariants', ['id', 'position'])


class Tile:
    def __init__(self, id_: int, data: List[List[str]]):
        self.id = id_
        self.data = data
        self.borders = {
            'top': int(''.join(self.data[0]), 2),
            'right': int(''.join(list(zip(*self.data))[-1]), 2),
            'bottom': int(''.join(self.data[-1]), 2),
            'left': int(''.join(list(zip(*self.data))[0]), 2),
        }

    @property
    def top(self):
        return self.borders['top']

    @property
    def right(self):
        return self.borders['right']

    @property
    def bottom(self):
        return self.borders['bottom']

    @property
    def left(self):
        return self.borders['left']

    def rotate(self, angle: int) -> 'Tile':
        angle = angle % 360
        data = deepcopy(self.data)

        while angle > 0:
            data = list(zip(*data[::-1]))
            angle -= 90

        return Tile(self.id, data)

    def flip(self) -> 'Tile':
        data = deepcopy(self.data)
        data = data[::-1]
        return Tile(self.id, data)

    def print(self) -> None:
        for line in self.data:
            print(''.join(['#' if ch == '1' else '.' for ch in line]))

    def __repr__(self):
        return f'{self.id}'


def part1(tile_data: str) -> int:
    tiles = _parse_data(tile_data)
    size = int(sqrt(len(tiles)))
    variants = {}

    for tile in tiles:
        flipped_tile = tile.flip()
        variants[tile.id] = [tile, tile.rotate(90), tile.rotate(180), flipped_tile.rotate(270),
                             flipped_tile, flipped_tile.rotate(90), flipped_tile.rotate(180), flipped_tile.rotate(270)]

    result = _dfs_search((0, 0), size, variants, set(variants.keys()), [[None for _ in range(size)] for _ in range(size)])

    return result[0][0].id * result[0][-1].id * result[-1][0].id * result[-1][-1].id


def _dfs_search(pos: Tuple[int, int], size: int, tiles: Dict[int, List[Tile]], unused: Set[int], puzzle: List[List[Union[TileVariants, None]]]) -> Union[List[List[TileVariants]], None]:
    if not unused:
        return puzzle

    x, y = pos

    for tile_id in list(unused):
        for i, tile in enumerate(tiles[tile_id]):
            if x > 0 and tiles[puzzle[y][x - 1].id][puzzle[y][x - 1].position].right != tile.left:
                continue

            if y > 0 and tiles[puzzle[y - 1][x].id][puzzle[y - 1][x].position].bottom != tile.top:
                continue

            puzzle[y][x] = TileVariants(tile.id, i)

            new_x = (x + 1) % size
            new_y = y + 1 if x == size - 1 else y

            res = _dfs_search((new_x, new_y), size, tiles, unused - {tile_id}, puzzle)

            if res:
                return res
            else:
                puzzle[y][x] = None

    return None


def part2(tile_data: str) -> int:
    pass


def _parse_data(tile_data: str) -> List[Tile]:
    tiles = []
    current_tile_id = 0
    current_tile = []

    for line in tile_data.split('\n'):
        if not line:
            continue

        if line.startswith('Tile'):
            if current_tile_id:
                tiles.append(Tile(current_tile_id, current_tile))
            current_tile_id = int(line[5:9])
            current_tile = []
        else:
            current_tile.append(['1' if ch == "#" else '0' for ch in line])

    tiles.append(Tile(current_tile_id, current_tile))
    return tiles


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test(20899048083289, part1("""
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
"""))


file_path = os.path.join(os.path.dirname(__file__), 'data/day20.txt')
with open(file_path, 'r') as f:
    input_data = f.read()

    print('Day 20, part 1: %r' % (part1(input_data)))
    print('Day 20, part 2: %r' % (part2(input_data)))
