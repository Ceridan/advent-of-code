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
            memory[instr.address] = _apply_mask(mask, instr.value)

    return sum(memory.values())


def part2(raw_instructions: List[str]) -> int:
    pass


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




def _apply_mask(mask: str, value: int) -> int:
    n = len(mask)
    result = value

    for i in range(n):
        if mask[i] == '0':
            result &= ~(2 ** (n - i - 1))
        elif mask[i] == '1':
            result |= 2 ** (n - i - 1)

    return result


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test(73, _apply_mask('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', 11))
test(101, _apply_mask('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', 101))
test(64, _apply_mask('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', 0))

test(165, part1([
    'mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X',
    'mem[8] = 11',
    'mem[7] = 101',
    'mem[8] = 0',
]))


file_path = os.path.join(os.path.dirname(__file__), 'data/day14.txt')
with open(file_path, 'r') as f:
    input_data = [line.strip() for line in f.readlines()]

    print('Day 14, part 1: %r' % (part1(input_data)))
    print('Day 14, part 2: %r' % (part2(input_data)))
