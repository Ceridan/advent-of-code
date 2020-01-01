import os


# Solution
def part1(data, settings):
    perms = get_permutations([x for x in settings])
    result = 0
    for x in perms:
        val = 0
        for i in range(len(settings)):
            val = next(execute_opcodes(data, [x[i], val]))
        if val > result:
            result = val
    return result


def part2(data, settings):
    perms = get_permutations([x for x in settings])
    result = 0
    for x in perms:
        vals = []
        ampfs = []
        for i in range(len(settings)):
            vals.append([x[i]])
            ampfs.append(execute_opcodes(data, vals[i]))
        val = 0
        k = 0
        try:
            while True:
                vals[k].append(val)
                val = next(ampfs[k])
                k = (k + 1) % 5
        except StopIteration:
            if vals[0][-1] > result:
                result = vals[0][-1]
    return result


def get_permutations(settings):
    result = [[settings.pop()]]
    while len(settings) > 0:
        nxt = settings.pop()
        new_result = []
        for x in result:
            for i in range(len(x) + 1):
                new_result.append(x[i:] + [nxt] + x[:i])
        result = new_result
    return result


def execute_opcodes(data, input_params):
    opcodes = [int(x) for x in data.split(',')]
    k = 0
    input_index = 0
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
            opcodes[p1] = input_params[input_index]
            input_index += 1
        elif opcode == 4:
            yield opcodes[p1]
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
    return


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


test(43210, part1('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0', settings=[0, 1, 2, 3, 4]))
test(54321, part1('3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0', settings=[0, 1, 2, 3, 4]))
test(65210, part1('3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0', settings=[0, 1, 2, 3, 4]))

test(139629729, part2('3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5', settings=[5, 6, 7, 8, 9]))
test(18216, part2('3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10', settings=[5, 6, 7, 8, 9]))


# Solve real puzzle
file_path = os.path.abspath('data/day07.txt')
input_data = [line.rstrip('\n') for line in open(file_path, 'r')][0]

print('Day 07, part 1: %r' % (part1(input_data, settings=[0, 1, 2, 3, 4])))
print('Day 07, part 2: %r' % (part2(input_data, settings=[5, 6, 7, 8, 9])))
