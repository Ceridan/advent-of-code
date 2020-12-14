import itertools
import os
import re
from abc import ABC, abstractmethod

from typing import List, Union


class Instruction(ABC):
    @property
    @abstractmethod
    def type(self):
        pass


class MemInstruction(Instruction):
    def __init__(self, address: int, value: int):
        self.address = address
        self.value = value

    @property
    def type(self):
        return 'mem'


class MaskInstruction(Instruction):
    def __init__(self, mask: str):
        self.mask = mask

    @property
    def type(self):
        return 'mask'


def part1(raw_instructions: List[str]) -> int:
    instructions = _parse_instructions(raw_instructions)
    memory = {}
    mask = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    for instr in instructions:
        if instr.type == 'mask':
            mask = instr.mask
        else:
            memory[instr.address] = _apply_mask_v1(mask, instr.value)

    return sum(memory.values())


def part2(raw_instructions: List[str]) -> int:
    instructions = _parse_instructions(raw_instructions)
    memory = {}
    mask = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    for instr in instructions:
        if instr.type == 'mask':
            mask = instr.mask
        else:
            masked_address = _apply_mask_v2(mask, instr.address)
            for address in _generate_addresses(masked_address):
                memory[address] = instr.value

    return sum(memory.values())


def _parse_instructions(raw_instructions: List[str]) -> List[Union[MemInstruction, MaskInstruction]]:
    regex = re.compile(r'(\d+)')
    instructions = []

    for instr in raw_instructions:
        if instr.startswith('mask'):
            mask = instr.split('=')[1].strip()
            instructions.append(MaskInstruction(mask))
        else:
            mem_values = regex.findall(instr)
            instructions.append(MemInstruction(address=int(mem_values[0]), value=int(mem_values[1])))

    return instructions


def _apply_mask_v1(mask: str, value: int) -> int:
    n = len(mask)
    result = value

    for i in range(n):
        if mask[i] == '0':
            result &= ~(2 ** (n - i - 1))
        elif mask[i] == '1':
            result |= 2 ** (n - i - 1)

    return result


def _apply_mask_v2(mask: str, value: int) -> str:
    bin_val = format(value, '#038b')[2:]
    result = []
    for m, v in zip(mask, bin_val):
        if m == 'X':
            result.append('X')
        else:
            result.append(str(int(m) | int(v)))

    return ''.join(result)


def _generate_addresses(masked_address: str) -> List[int]:
    if 'X' not in masked_address:
        return [int(masked_address, 2)]

    addresses = []
    x_positions = []
    for i, ch in enumerate(masked_address):
        if ch == 'X':
            x_positions.append(i)

    products = itertools.product('01', repeat=len(x_positions))

    next_address = list(masked_address)
    for p in products:
        for j, pos in enumerate(x_positions):
            next_address[pos] = p[j]
        addresses.append(int(''.join(next_address), 2))

    return addresses


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test(73, _apply_mask_v1('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', 11))
test(101, _apply_mask_v1('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', 101))
test(64, _apply_mask_v1('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', 0))

test('000000000000000000000000000000X1101X', _apply_mask_v2('000000000000000000000000000000X1001X', 42))
test('00000000000000000000000000000001X0XX', _apply_mask_v2('00000000000000000000000000000000X0XX', 26))

test([18, 19, 50, 51], _generate_addresses('000000000000000000000000000000X1001X'))

test(165, part1([
    'mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X',
    'mem[8] = 11',
    'mem[7] = 101',
    'mem[8] = 0',
]))

test(208, part2([
    'mask = 000000000000000000000000000000X1001X',
    'mem[42] = 100',
    'mask = 00000000000000000000000000000000X0XX',
    'mem[26] = 1',
]))

file_path = os.path.join(os.path.dirname(__file__), 'data/day14.txt')
with open(file_path, 'r') as f:
    input_data = [line.strip() for line in f.readlines()]

    print('Day 14, part 1: %r' % (part1(input_data)))
    print('Day 14, part 2: %r' % (part2(input_data)))
