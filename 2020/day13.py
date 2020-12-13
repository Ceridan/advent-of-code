import os
import sys
from typing import List


def part1(earliest_timestamp: int, bus_schedule: str) -> int:
    ids = [int(bus_id) for bus_id in bus_schedule.split(',') if bus_id != 'x']
    best_id = 0
    timestamp_diff = sys.maxsize

    for bus_id in ids:
        if earliest_timestamp % bus_id == 0:
            return 0

        diff = (bus_id * (earliest_timestamp // bus_id + 1)) % earliest_timestamp

        if diff < timestamp_diff:
            timestamp_diff = diff
            best_id = bus_id

    return best_id * timestamp_diff


def part2(bus_schedule: str, watermark: int = 0) -> int:
    all_ids = [int(bus_id) if bus_id != 'x' else 0 for bus_id in bus_schedule.split(',')]
    known_ids = [bus_id for bus_id in all_ids if bus_id > 0]

    first_id = all_ids[0]
    max_id = max(known_ids)
    first_max_id_diff = abs(all_ids.index(first_id) - all_ids.index(max_id))

    current = max_id * (watermark // max_id) if watermark > 0 else max_id
    t = current - first_max_id_diff

    while not _check_order(all_ids, t):
        current += max_id
        t = current - first_max_id_diff

    return t


def _check_order(all_ids: List[int], t: int) -> bool:
    for i in range(len(all_ids)):
        bus_id = all_ids[i]
        if bus_id == 0:
            continue

        if (t + i) % bus_id != 0:
            return False

    return True


def _gcd(a: int, b: int) -> int:
    return _gcd(b, a % b) if b else a


def _lcm(a: int, b: int) -> int:
    if a > b:
        a, b = b, a
    return a // _gcd(a, b) * b


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test(295, part1(939, '7,13,x,x,59,x,31,19'))

test(1068781, part2('7,13,x,x,59,x,31,19'))
test(3417, part2('17,x,13,19'))
test(754018, part2('67,7,59,61'))
test(779210, part2('67,x,7,59,61'))
test(1261476, part2('67,7,x,59,61'))
test(1202161486, part2('1789,37,47,1889'))


file_path = os.path.join(os.path.dirname(__file__), 'data/day13.txt')
with open(file_path, 'r') as f:
    timestamp = int(f.readline().strip())
    input_data = f.readline().strip()

    print('Day 13, part 1: %r' % (part1(timestamp, input_data)))
    print('Day 13, part 2: %r' % (part2(input_data, watermark=100000000000000)))
