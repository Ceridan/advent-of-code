import re

# Solution
def part1(data, multiplier = 1):
    pattern = r'\d+'
    (player_count, marble_count) = re.findall(pattern, data)
    (player_count, marble_count) = (int(player_count), int(marble_count) * multiplier)
    players = [0] * player_count
    marbles = DoubleLinkedList(0)
    k = 0
    for i in range(1, marble_count + 1):
        if i % 23 == 0:
            players[k] += (i + marbles.remove_node())
        else:
            marbles.add_node(i)
        k = (k + 1) % player_count
    return max(x for x in players)

def part2(data, multiplier):
    return part1(data, 100)

class DoubleLinkedList:
    def __init__(self, initial_value):
        initial_node = DoubleLinkedListNode(initial_value)
        initial_node.prev = initial_node
        initial_node.next = initial_node
        self.current = initial_node
    
    def add_node(self, node_value):
        left = self.current.next
        right = self.current.next.next
        new_node = DoubleLinkedListNode(node_value, left, right)
        left.next = new_node
        right.prev = new_node
        self.current = new_node

    def remove_node(self):
        for _ in range(7):
            self.current = self.current.prev
        val = self.current.value
        self.current.prev.next = self.current.next
        self.current.next.prev = self.current.prev
        self.current = self.current.next
        return val
        
class DoubleLinkedListNode:
    def __init__(self, value, prev = None, next = None):
        self.value = value
        self.prev = prev
        self.next = next

# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)

test(32, part1('9 players; last marble is worth 25 points'))
test(8317, part1('10 players; last marble is worth 1618 points'))
test(146373, part1('13 players; last marble is worth 7999 points'))
test(2764, part1('17 players; last marble is worth 1104 points'))
test(54718, part1('21 players; last marble is worth 6111 points'))
test(37305, part1('30 players; last marble is worth 5807 points'))
test(8317, part1('10 players; last marble is worth 1618 points'))

# Solve real puzzle 
filename = 'data/day09.txt'
data = [line.rstrip('\n') for line in open(filename, 'r')][0]

print('Day 09, part 1: %r' % (part1(data)))
print('Day 09, part 2: %r' % (part2(data, 100)))
