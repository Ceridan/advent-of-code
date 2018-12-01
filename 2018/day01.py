def task01_1(data):
    frequency = sum(int(x) for x in data)
    return frequency

def task01_2(data):
    known_frequency = { 0: True }
    frequency = 0
    while True:
        for x in data:
            frequency += int(x)
            if frequency in known_frequency:
                return frequency
            known_frequency[frequency] = True


filename = 'data/day01.txt'
content = [line.rstrip('\n') for line in open(filename, 'r')]

print('Day 01, task 1: %r' % (task01_1(content)))
print('Day 01, task 2: %r' % (task01_2(content)))
