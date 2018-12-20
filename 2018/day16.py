import re

# Solution
def part1(data):
    dump, _ = read_data(data)
    cpu = CPU()
    total_count = 0
    for dump_row in dump:    
        total_count += 1 if calculate_possible_opcode(cpu, dump_row) >= 3 else 0
    return total_count

def part2(data):
    dump, commands = read_data(data)
    cpu = CPU()
    possible_opcodes = {}
    for dump_row in dump:
        check_opcode(cpu, dump_row, possible_opcodes)
    opcodes = determine_opcodes(possible_opcodes)
    cpu.reset()
    for command in commands:
        opcode, ra, rb, rc = command
        cpu.commands[opcodes[opcode]](ra, rb, rc)
    return cpu.registers[0]

def calculate_possible_opcode(cpu, dump_row):
    _, ra, rb, rc = dump_row.command
    count = 0
    for i in range(16):
        cpu.registers = dump_row.before[:]
        cpu.commands[i](ra, rb, rc)
        if cpu.registers == dump_row.after:
            count += 1
    return count

def check_opcode(cpu, dump_row, possible_opcodes):
    opcode, ra, rb, rc = dump_row.command
    if opcode not in possible_opcodes:
        possible_opcodes[opcode] = [set(), set()]
    for i in range(16):
        cpu.registers = dump_row.before[:]
        cpu.commands[i](ra, rb, rc)
        if cpu.registers == dump_row.after:
            if i not in possible_opcodes[opcode][1]:
                possible_opcodes[opcode][0].add(i)
        else:
            possible_opcodes[opcode][1].add(i)
            if i in possible_opcodes[opcode][0]:
                possible_opcodes[opcode][0].remove(i)

def determine_opcodes(possible_opcodes):
    opcodes = {}
    po = [(key, possible_opcodes[key][0]) for key in possible_opcodes if len(possible_opcodes[key][0]) == 1]
    while len(po) > 0:
        for item in po:
            opcode, val = item[0], item[1].pop()
            opcodes[opcode] = val
            del possible_opcodes[opcode]
            for key in possible_opcodes:
                if val in possible_opcodes[key][0]:
                    possible_opcodes[key][0].remove(val)
        po = [(key, possible_opcodes[key][0]) for key in possible_opcodes if len(possible_opcodes[key][0]) == 1]
    return opcodes

def read_data(data):
    dump = []
    current_dump_row = None
    commands = []
    is_dump = False
    pattern = r'(\d+),* (\d+),* (\d+),* (\d+)'
    for line in data:
        if line == '':
            continue
        v1, v2, v3, v4 = re.findall(pattern, line)[0]
        op = [int(v1), int(v2), int(v3), int(v4)]
        if line.startswith('Before'):
            current_dump_row = CpuDumpRow()
            current_dump_row.before = op
            is_dump = True
        elif line.startswith('After'):
            current_dump_row.after = op
            dump.append(current_dump_row)
            is_dump = False
        else:
            if is_dump:
                current_dump_row.command = op
            else:
                commands.append(op)
    return (dump, commands)
            
class CPU:
    def __init__(self):
        self._registers = [0, 0, 0, 0]
        self._commands = [
            self.addr, self.addi, self.mulr, self.muli, self.banr, self.bani, self.borr, self.bori, 
            self.setr, self.seti, self.gtir, self.gtri, self.gtrr, self.eqir, self.eqri, self.eqrr,
        ]

    @property
    def registers(self):
        return self._registers

    @registers.setter
    def registers(self, registers):
        self._registers = registers

    @property
    def commands(self):
        return self._commands          

    def reset(self):
        for i in range(4):
            self._registers[i] = 0

    def addr(self, ra, rb, rc):
        self._registers[rc] = self._registers[ra] + self._registers[rb]

    def addi(self, ra, rb, rc):
        self._registers[rc] = self._registers[ra] + rb   

    def mulr(self, ra, rb, rc):
        self._registers[rc] = self._registers[ra] * self._registers[rb]

    def muli(self, ra, rb, rc):
        self._registers[rc] = self._registers[ra] * rb     
    
    def banr(self, ra, rb, rc):
        self._registers[rc] = self._registers[ra] & self._registers[rb]

    def bani(self, ra, rb, rc):
        self._registers[rc] = self._registers[ra] & rb      

    def borr(self, ra, rb, rc):
        self._registers[rc] = self._registers[ra] | self._registers[rb]

    def bori(self, ra, rb, rc):
        self._registers[rc] = self._registers[ra] | rb        

    def setr(self, ra, rb, rc):
        self._registers[rc] = self._registers[ra]

    def seti(self, ra, rb, rc):
        self._registers[rc] = ra      

    def gtir(self, ra, rb, rc):
        self._registers[rc] = 1 if ra > self._registers[rb] else 0       

    def gtri(self, ra, rb, rc):
        self._registers[rc] = 1 if self._registers[ra] > rb else 0

    def gtrr(self, ra, rb, rc):
        self._registers[rc] = 1 if self._registers[ra] > self._registers[rb] else 0       

    def eqir(self, ra, rb, rc):
        self._registers[rc] = 1 if ra == self._registers[rb] else 0       

    def eqri(self, ra, rb, rc):
        self._registers[rc] = 1 if self._registers[ra] == rb else 0

    def eqrr(self, ra, rb, rc):
        self._registers[rc] = 1 if self._registers[ra] == self._registers[rb] else 0            

class CpuDumpRow:
    def __init__(self, before = [], after = [], command = []):
        self.before = before
        self.after = after
        self.command = command     

# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)

test(3, calculate_possible_opcode(CPU(), CpuDumpRow([3, 2, 1, 1], [3, 2, 2, 1], [9, 2, 1, 2])))

# Solve real puzzle 
filename = 'data/day16.txt'
data = [line.rstrip('\n') for line in open(filename, 'r')]

print('Day 16, part 1: %r' % (part1(data)))
print('Day 16, part 2: %r' % (part2(data)))