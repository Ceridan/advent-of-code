import os


# Solution
def part1(data, input_parameter):
    opcodes = [int(x) for x in data.split(',')]
    results = execute_opcodes(opcodes, input_parameter)
    return results[-1]


def part2(data, input_parameter):
    opcodes = [int(x) for x in data.split(',')]
    results = execute_opcodes(opcodes, input_parameter)
    return results[-1]


def execute_opcodes(opcodes, input_param):
    results = []
    k = 0
    while opcodes[k] != 99:
        opcode, param_modes = get_opcode_and_param_modes(opcodes[k])
        p1 = get_param_position_by_mode(
            opcodes, param_modes[0], k + 1) if len(param_modes) > 0 else 0
        p2 = get_param_position_by_mode(
            opcodes, param_modes[1], k + 2) if len(param_modes) > 1 else 0
        p3 = get_param_position_by_mode(
            opcodes, param_modes[2], k + 3) if len(param_modes) > 2 else 0

        if opcode == 1:
            opcodes[p3] = opcodes[p1] + opcodes[p2]
        elif opcode == 2:
            opcodes[p3] = opcodes[p1] * opcodes[p2]
        elif opcode == 3:
            opcodes[p1] = input_param
        elif opcode == 4:
            results.append(opcodes[p1])
        elif opcode == 5:
            if opcodes[p1] != 0:
                k = opcodes[p2]
                continue
        elif opcode == 6:
            if opcodes[p1] == 0:
                k = opcodes[p2]
                continue
        elif opcode == 7:
            opcodes[p3] = 1 if opcodes[p1] < opcodes[p2] else 0
        elif opcode == 8:
            opcodes[p3] = 1 if opcodes[p1] == opcodes[p2] else 0

        k += len(param_modes) + 1

    return results


def get_param_position_by_mode(opcodes, mode, position):
    if mode == 0:
        return opcodes[position]
    else:
        return position


def get_opcode_and_param_modes(instruction):
    opcode = instruction % 100
    opcode_params_length = get_opcode_param_length(opcode)
    param_modes = [0 for x in range(0, opcode_params_length - 1)]
    instruction = int(instruction / 100)
    i = 0
    while (instruction > 0):
        param_modes[i] = instruction % 10
        instruction = int(instruction / 10)
        i += 1
    return (opcode, param_modes)


def get_opcode_param_length(opcode):
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
    elif opcode == 99:
        return 1


# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)


test(10, part1('3,0,4,0,99', 10))

test(1, part2('3,9,8,9,10,9,4,9,99,-1,8', 8))
test(0, part2('3,9,8,9,10,9,4,9,99,-1,8', 10))
test(1, part2('3,9,7,9,10,9,4,9,99,-1,8', 5))
test(0, part2('3,9,7,9,10,9,4,9,99,-1,8', 9))
test(1, part2('3,3,1108,-1,8,3,4,3,99', 8))
test(0, part2('3,3,1108,-1,8,3,4,3,99', 10))
test(1, part2('3,3,1107,-1,8,3,4,3,99', 5))
test(0, part2('3,3,1107,-1,8,3,4,3,99', 9))
test(0, part2('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', 0))
test(1, part2('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', 10))
test(0, part2('3,3,1105,-1,9,1101,0,0,12,4,12,99,1', 0))
test(1, part2('3,3,1105,-1,9,1101,0,0,12,4,12,99,1', 10))
test(999, part2('3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99', 7))
test(1000, part2('3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99', 8))
test(1001, part2('3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99', 9))


# Solve real puzzle
dir_path = os.path.dirname(__file__) 
file_path = os.path.join(dir_path, 'data/day05.txt')
input_data = [line.rstrip('\n') for line in open(file_path, 'r')][0]

print('Day 05, part 1: %r' % (part1(input_data, input_parameter=1)))
print('Day 05, part 2: %r' % (part2(input_data, input_parameter=5)))
