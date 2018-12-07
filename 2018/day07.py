import re

# Solution
def part1(data):
    steps = read_steps(data)
    result = ''
    while len(steps) > 0:
        ready_steps = []
        for key in steps:
            step = steps[key]
            if (len(step.in_edges) == 0):
                ready_steps.append(step.name)
        ready_steps.sort()
        result += ready_steps[0]
        del_step(ready_steps[0], steps)
    return result
        
def part2(data, workers_count, base_step_time):
    steps = read_steps(data)
    time = 0
    workers_pool = workers_count
    steps_in_progress = []
    while len(steps) > 0:
        ready_steps = []
        for key in steps:
            step = steps[key]
            if (len(step.in_edges) == 0):
                ready_steps.append(step.name)
        ready_steps.sort()
        for step in ready_steps:
            if workers_pool == 0:
                break
            if len(list(filter(lambda x: x[0] == step, steps_in_progress))) > 0:
                continue
            steps_in_progress.append((step, base_step_time + ord(step) - 64))
            workers_pool -= 1        
        min_time = min(y for (x, y) in steps_in_progress)
        steps_in_progress = [(x, y - min_time) for (x, y) in steps_in_progress]
        for step in steps_in_progress:
            if step[1] == 0:
                del_step(step[0], steps)
        steps_in_progress = list(filter(lambda x: x[1] > 0, steps_in_progress))
        time += min_time
        workers_pool = workers_count - len(steps_in_progress)
    return time

def read_steps(data):
    pattern = r'Step ([A-Z]) must be finished before step ([A-Z]) can begin.'
    steps = {}
    for line in data:
        step1, step2 = re.findall(pattern, line)[0]
        if step1 not in steps: steps[step1] = Step(step1)
        steps[step1].out_edges.append(step2)
        if step2 not in steps: steps[step2] = Step(step2)
        steps[step2].in_edges.append(step1)
    return steps

def del_step(step_name, steps):    
    for edge in steps[step_name].out_edges:
        steps[edge].in_edges.remove(step_name)            
    del steps[step_name]

class Step:
    def __init__(self, name):
        self._name = name
        self._in = []
        self._out = []

    @property
    def name(self):
        return self._name

    @property
    def in_edges(self):
        return self._in

    @property
    def out_edges(self):
        return self._out

# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)

test('CABDFE', part1([
    'Step C must be finished before step A can begin.',
    'Step C must be finished before step F can begin.',
    'Step A must be finished before step B can begin.',
    'Step A must be finished before step D can begin.',
    'Step B must be finished before step E can begin.',
    'Step D must be finished before step E can begin.',
    'Step F must be finished before step E can begin.',
]))
test('CABDFE', part1([
    'Step F must be finished before step E can begin.',
    'Step C must be finished before step A can begin.',
    'Step D must be finished before step E can begin.',
    'Step C must be finished before step F can begin.',
    'Step A must be finished before step D can begin.',
    'Step B must be finished before step E can begin.',
    'Step A must be finished before step B can begin.',
]))

test(15, part2([
    'Step C must be finished before step A can begin.',
    'Step C must be finished before step F can begin.',
    'Step A must be finished before step B can begin.',
    'Step A must be finished before step D can begin.',
    'Step B must be finished before step E can begin.',
    'Step D must be finished before step E can begin.',
    'Step F must be finished before step E can begin.',
], 2, 0))
test(15, part2([
    'Step F must be finished before step E can begin.',
    'Step C must be finished before step A can begin.',
    'Step D must be finished before step E can begin.',
    'Step C must be finished before step F can begin.',
    'Step A must be finished before step D can begin.',
    'Step B must be finished before step E can begin.',
    'Step A must be finished before step B can begin.',
], 2, 0))

# Solve real puzzle
filename = 'data/day07.txt'
data = [line.rstrip('\n') for line in open(filename, 'r')]

print('Day 07, part 1: %r' % (part1(data)))
print('Day 07, part 2: %r' % (part2(data, 5, 60)))