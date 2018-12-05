from datetime import datetime
import re

# Solution
def part1(data):
    ids = calculate_guard_duty(data)
    (guard_id, sleeping_time_array) = max(ids.items(), key=lambda x: sum(x[1]))
    minute = sleeping_time_array.index(max(sleeping_time_array))
    return guard_id * minute

def part2(data):
    ids = calculate_guard_duty(data)
    (guard_id, sleeping_time_array) = max(ids.items(), key=lambda x: max(x[1]))
    minute = sleeping_time_array.index(max(sleeping_time_array))
    return guard_id * minute

def calculate_guard_duty(data):
    pattern = r'\[([0-9-:\ ]+)\] (falls\ asleep|wakes\ up|Guard\ \#([0-9]+)\ begins\ shift)'
    data.sort()
    ids = {}
    current_id = 0
    sleep_start = 0
    for line in data:
        (dt, command, id) = re.findall(pattern, line)[0]
        date = datetime.strptime(dt, '%Y-%m-%d %H:%M')
        if command == 'falls asleep':
            sleep_start = date.minute
        elif command == 'wakes up':
            if current_id not in ids:
                ids[current_id] = [0] * 60
            for t in range(sleep_start, date.minute):
                ids[current_id][t] += 1
        else:
            current_id = int(id)
    return ids

# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)

test(240, part1([
    '[1518-11-01 00:00] Guard #10 begins shift',
    '[1518-11-01 00:05] falls asleep',
    '[1518-11-01 00:25] wakes up',
    '[1518-11-01 00:30] falls asleep',
    '[1518-11-01 00:55] wakes up',
    '[1518-11-01 23:58] Guard #99 begins shift',
    '[1518-11-02 00:40] falls asleep',
    '[1518-11-02 00:50] wakes up',
    '[1518-11-03 00:05] Guard #10 begins shift',
    '[1518-11-03 00:24] falls asleep',
    '[1518-11-03 00:29] wakes up',
    '[1518-11-04 00:02] Guard #99 begins shift',
    '[1518-11-04 00:36] falls asleep',
    '[1518-11-04 00:46] wakes up',
    '[1518-11-05 00:03] Guard #99 begins shift',
    '[1518-11-05 00:45] falls asleep',
    '[1518-11-05 00:55] wakes up'    
]))

test(4455, part2([
    '[1518-11-01 00:00] Guard #10 begins shift',
    '[1518-11-01 00:05] falls asleep',
    '[1518-11-01 00:25] wakes up',
    '[1518-11-01 00:30] falls asleep',
    '[1518-11-01 00:55] wakes up',
    '[1518-11-01 23:58] Guard #99 begins shift',
    '[1518-11-02 00:40] falls asleep',
    '[1518-11-02 00:50] wakes up',
    '[1518-11-03 00:05] Guard #10 begins shift',
    '[1518-11-03 00:24] falls asleep',
    '[1518-11-03 00:29] wakes up',
    '[1518-11-04 00:02] Guard #99 begins shift',
    '[1518-11-04 00:36] falls asleep',
    '[1518-11-04 00:46] wakes up',
    '[1518-11-05 00:03] Guard #99 begins shift',
    '[1518-11-05 00:45] falls asleep',
    '[1518-11-05 00:55] wakes up'    
]))


# Solve real puzzle 
filename = 'data/day04.txt'
data = [line.rstrip('\n') for line in open(filename, 'r')]

print('Day 04, part 1: %r' % (part1(data)))
print('Day 04, part 2: %r' % (part2(data)))
