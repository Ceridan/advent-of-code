import re


# Solution
def part1(data):
    return process_find_divisors_algorithm(data)


def part2(data):
    return process_find_divisors_algorithm(data, [1, 0, 0, 0, 0, 0])


def process_commands_naive(data, initial_state=None):
    ip, commands = read_data(data)
    cpu = CPU(initial_state)
    ip_value = 0
    while ip_value < len(commands):
        op, ra, rb, rc = commands[ip_value]
        cpu.registers[ip] = ip_value
        cpu.commands[op](ra, rb, rc)
        ip_value = cpu.registers[ip] + 1
    return cpu.registers[0]


def process_find_divisors_algorithm(data, initial_state=None):
    ip, commands = read_data(data)
    cpu = CPU(initial_state)
    ip_value = 0
    prev_ip_value = 0
    ip_sequence = []
    prev_ip_sequence = []
    while ip_value < len(commands):
        op, ra, rb, rc = commands[ip_value]
        cpu.registers[ip] = ip_value
        cpu.commands[op](ra, rb, rc)
        ip_value = cpu.registers[ip] + 1
        if ip_value < prev_ip_value:
            if ip_sequence == prev_ip_sequence:
                break
            prev_ip_sequence = ip_sequence[:]
            ip_sequence = []
        else:
            ip_sequence.append(ip_value)
            prev_ip_value = ip_value
    mx = max(cpu.registers)
    div_sum = sum(x for x in range(1, mx + 1) if mx % x == 0)    
    return div_sum   


def read_data(data):
    commands = []
    ip = int(re.findall(r'(\d)', data[0])[0])
    pattern = r'^([a-z]+) (\d+) (\d+) (\d+)'
    for i in range(1, len(data)):
        op, ra, rb, rc = re.findall(pattern, data[i])[0]
        cmd = (op, int(ra), int(rb), int(rc))
        commands.append(cmd)
    return ip, commands


class CPU:
    def __init__(self, initial_state=None):
        self._registers = initial_state[:] if initial_state is not None else [0, 0, 0, 0, 0, 0]
        self._commands = {
            'addr': self.addr,
            'addi': self.addi, 
            'mulr': self.mulr, 
            'muli': self.muli,
            'banr': self.banr,
            'bani': self.bani, 
            'borr': self.borr, 
            'bori': self.bori, 
            'setr': self.setr, 
            'seti': self.seti, 
            'gtir': self.gtir, 
            'gtri': self.gtri, 
            'gtrr': self.gtrr, 
            'eqir': self.eqir, 
            'eqri': self.eqri, 
            'eqrr': self.eqrr,
        }

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
        for i in range(6):
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

    def setr(self, ra, _, rc):
        self._registers[rc] = self._registers[ra]

    def seti(self, ra, _, rc):
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


# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)


test(6, process_commands_naive([
    '#ip 0',
    'seti 5 0 1',
    'seti 6 0 2',
    'addi 0 1 0',
    'addr 1 2 3',
    'setr 1 0 0',
    'seti 8 0 4',
    'seti 9 0 5',
]))


# Solve real puzzle 
filename = 'data/day19.txt'
input_data = [line.rstrip('\n') for line in open(filename, 'r')]

print('Day 19, part 1: %r' % (part1(input_data)))
print('Day 19, part 2: %r' % (part2(input_data)))
