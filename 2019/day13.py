import os


# Solution
def part1(data):
    grid = dict()
    computer = IntCodeComputer(data)
    icc_iter = iter(computer.run())
    try:
        while True:
            x = next(icc_iter)
            y = next(icc_iter)
            tile_id = next(icc_iter)
            grid[(x, y)] = tile_id
    except StopIteration:
        return sum([1 for x in grid.values() if x == 2])
    return 0


def part2(data):
    data = '2' + data[1:]
    computer = IntCodeComputer(data)
    icc_iter = iter(computer.run())
    pad = (0, 0)
    ball = (0, 0)
    score = 0
    tile_id = 0
    try:
        while True:
            px = pad[0]
            bx = ball[0]
            if px > bx:
                computer.new_input(-1)
            elif px < bx:
                computer.new_input(1)
            else:
                computer.new_input(0)

            x = next(icc_iter)
            y = next(icc_iter)
            if x == -1 and y == 0: 
                score = next(icc_iter)
            else:
                tile_id = next(icc_iter)
                
            if tile_id == 3:
                pad = (x, y)
            elif tile_id == 4:
                ball = (x, y)
    except StopIteration:
        return score
    return 0


def print_grid(grid):
    min_x = min([item[0] for item in grid.keys()])
    max_x = max([item[0] for item in grid.keys()])
    min_y = min([item[1] for item in grid.keys()])
    max_y = max([item[1] for item in grid.keys()])
    for y in range(min_y, max_y + 1):
        row = []
        for x in range(min_x, max_x + 1):
            if (x, y) not in grid or grid[(x, y)] == 0:
                row.append(' ')
            elif grid[(x, y)] == 1:
                row.append('|')
            elif grid[(x, y)] == 2:
                row.append('B')
            elif grid[(x, y)] == 3:
                row.append('=')
            else:
                row.append('O')
        print(''.join(row))


class IntCodeComputer:
    def __init__(self, program, input=None):
        self.program = [int(x) for x in program.split(',')]
        self.opcodes = dict(zip(range(len(self.program)), self.program))
        self.rel_base = 0
        self.current_index = 0
        self.input_index = -1
        self.input = input if input is not None else []

    def get_opcode(self, index):
        if index in self.opcodes:
            return self.opcodes[index]
        return 0

    def set_opcode(self, index, value):
        self.opcodes[index] = value

    def add_input(self, param):
        self.input.append(param)

    def new_input(self, param):
        self.input = [param]
        self.input_index = -1

    def is_input_processed(self):
        return len(self.input) == self.input_index + 1

    def read_input(self):
        self.input_index += 1
        return self.input[self.input_index]

    def run(self):
        while True:
            insturction = self.get_opcode(self.current_index)
            opcode, param_modes = self.get_opcode_and_param_modes(insturction)
            p1 = self.get_param_position_by_mode(
                param_modes[0], self.current_index + 1) if len(param_modes) > 0 else 0
            p2 = self.get_param_position_by_mode(
                param_modes[1], self.current_index + 2) if len(param_modes) > 1 else 0
            p3 = self.get_param_position_by_mode(
                param_modes[2], self.current_index + 3) if len(param_modes) > 2 else 0

            if opcode == 1:
                self.set_opcode(p3, self.get_opcode(p1) + self.get_opcode(p2))
            elif opcode == 2:
                self.set_opcode(p3, self.get_opcode(p1) * self.get_opcode(p2))
            elif opcode == 3:
                self.set_opcode(p1, self.read_input())
            elif opcode == 4:
                yield self.get_opcode(p1)
            elif opcode == 5:
                if self.get_opcode(p1) != 0:
                    self.current_index = self.get_opcode(p2)
                    continue
            elif opcode == 6:
                if self.get_opcode(p1) == 0:
                    self.current_index = self.get_opcode(p2)
                    continue
            elif opcode == 7:
                self.set_opcode(p3, 1 if self.get_opcode(p1) < self.get_opcode(p2) else 0)
            elif opcode == 8:
                self.set_opcode(p3, 1 if self.get_opcode(p1) == self.get_opcode(p2) else 0)
            elif opcode == 9:
                self.rel_base += self.get_opcode(p1)
            elif opcode == 99:
                return
            self.current_index += len(param_modes) + 1

    def get_param_position_by_mode(self, mode, position):
        if mode == 0:
            return self.get_opcode(position)
        elif mode == 1:
            return position
        else:
            return self.rel_base + self.get_opcode(position)

    def get_opcode_and_param_modes(self, instruction):
        opcode = instruction % 100
        opcode_params_length = self.get_opcode_param_length(opcode)
        param_modes = [0 for x in range(0, opcode_params_length - 1)]
        instruction = int(instruction / 100)
        i = 0
        while (instruction > 0):
            param_modes[i] = instruction % 10
            instruction = int(instruction / 10)
            i += 1
        return (opcode, param_modes)

    def get_opcode_param_length(self, opcode):
        if opcode == 1:
            return 4
        elif opcode == 2:
            return 4
        elif opcode == 3:
            return 2
        elif opcode == 4:
            return 2
        elif opcode == 5:
            return 3
        elif opcode == 6:
            return 3
        elif opcode == 7:
            return 4
        elif opcode == 8:
            return 4
        elif opcode == 9:
            return 2
        elif opcode == 99:
            return 1


# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)


# Solve real puzzle
dir_path = os.path.dirname(__file__)
file_path = os.path.join(dir_path, 'data/day13.txt')
input_data = [line.rstrip('\n') for line in open(file_path, 'r')][0]

print('Day 13, part 1: %r' % (part1(input_data)))
print('Day 13, part 2: %r' % (part2(input_data)))
