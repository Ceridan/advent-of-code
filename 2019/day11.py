import os


# Solution
def part1(data):
    return run_program(data, 0)


def part2(data):
    return run_program(data, 1, print_result=True)


def run_program(program, initial_color, print_result=False):
    grid = {(0, 0): initial_color}
    computer = IntCodeComputer(program)
    try:
        icc_iter = iter(computer.run())
        direction = 'left'
        rotation = 0
        position = (0, 0)
        while True:
            input_color = grid[position] if position in grid else 0
            computer.add_input(input_color)
            new_color = next(icc_iter)
            grid[position] = new_color
            rotation = next(icc_iter)
            direction = calculate_direction(direction, rotation)
            position = calculate_position(position, direction)
    except StopIteration:
        if print_result:
            print(print_grid(grid))
        return len(grid)


def print_grid(grid):
    printed = '\n'
    min_x = min([item[0] for item in grid.keys()])
    max_x = max([item[0] for item in grid.keys()])
    min_y = min([item[1] for item in grid.keys()])
    max_y = max([item[1] for item in grid.keys()])
    for x in range(min_x, max_x + 1):
        printed += ''.join([('*' if (x, y) in grid and grid[(x, y)] == 1 else ' ') for y in range(min_y, max_y + 1)]) + '\n'
    return printed


def calculate_direction(current_direction, rotation):
    if current_direction == 'up':
        return 'left' if rotation == 0 else 'right'
    elif current_direction == 'right':
        return 'up' if rotation == 0 else 'down'
    elif current_direction == 'down':
        return 'right' if rotation == 0 else 'left'
    return 'down' if rotation == 0 else 'up'


def calculate_position(current_position, direction):
    x, y = current_position
    if direction == 'up':
        return (x, y + 1)
    elif direction == 'right':
        return (x + 1, y)
    elif direction == 'down':
        return (x, y - 1)
    return (x - 1, y)


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


grid = {
    (-2, -2): 0, (-1, -2): 0, (0, -2): 0, (1, -2): 0, (2, -2): 0,
    (-2, -1): 0, (-1, -1): 0, (0, -1): 0, (1, -1): 1, (2, -1): 0,
    (-2, 0): 0, (-1, 0): 0, (0, 0): 0, (1, 0): 1, (2, 0): 0,
    (-2, 1): 0, (-1, 1): 1, (0, 1): 1, (1, 1): 0, (2, 1): 0,
    (-2, 2): 0, (-1, 2): 0, (0, 2): 0, (1, 2): 0, (2, 2): 0,
}
test("""
     
   * 
   * 
 **  
     
""", print_grid(grid))


# Solve real puzzle
dir_path = os.path.dirname(__file__)
file_path = os.path.join(dir_path, 'data/day11.txt')
input_data = [line.rstrip('\n') for line in open(file_path, 'r')][0]

print('Day 11, part 1: %r' % (part1(input_data)))
print('Day 11, part 2: %r' % (part2(input_data)))
