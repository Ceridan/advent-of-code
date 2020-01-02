import os


# Solution
def part1(data, input_params=[]):
    return run_program(data, input_params)


def part2(data, input_params=[]):
    return run_program(data, input_params)


def run_program(program, input_params=[]):
    computer = IntCodeComputer(program, input_params)
    result = []
    try:
        icc_iter = iter(computer.run())
        while True:
            result.append(next(icc_iter))
    except StopIteration:
        if len(result) > 0:
            return result[-1]
    return


class IntCodeComputer:
    def __init__(self, program, input=[]):
        self.program = [int(x) for x in program.split(',')]
        self.opcodes = dict(zip(range(len(self.program)), self.program))
        self.rel_base = 0
        self.current_index = 0
        self.input_index = -1
        self.input = input
        

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
        while self.get_opcode(self.current_index) != 99:
            insturction = self.get_opcode(self.current_index)
            opcode, param_modes = self.get_opcode_and_param_modes(insturction)
            p1 = self.get_param_position_by_mode(param_modes[0], self.current_index + 1) if len(param_modes) > 0 else 0
            p2 = self.get_param_position_by_mode(param_modes[1], self.current_index + 2) if len(param_modes) > 1 else 0
            p3 = self.get_param_position_by_mode(param_modes[2], self.current_index + 3) if len(param_modes) > 2 else 0

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

            self.current_index += len(param_modes) + 1
        return


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


test(99, part1('109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'))
test(1219070632396864, part1('1102,34915192,34915192,7,4,7,99,0'))
test(1125899906842624, part1('104,1125899906842624,99'))


# Solve real puzzle
dir_path = os.path.dirname(__file__) 
file_path = os.path.join(dir_path, 'data/day09.txt')
input_data = [line.rstrip('\n') for line in open(file_path, 'r')][0]

print('Day 09, part 1: %r' % (part1(input_data, input_params=[1])))
print('Day 09, part 2: %r' % (part2(input_data, input_params=[2])))
