# Solution
def part1(data):
    stack = []
    meta_sum = 0
    gen = input_gen(data)
    for x in gen:
        if x != 0 or len(stack) % 2 == 1:
            stack.append(x)
            continue
        m = next(gen)
        while m > 0 or len(stack) > 0:
            for _ in range(m):
                meta_sum += next(gen)
            m = stack.pop() if len(stack) > 0 else 0
            node = stack.pop() - 1 if len(stack) > 0 else 0
            if node > 0:
                stack.append(node)
                stack.append(m)
                break
    return meta_sum

def part2(data):
    gen = input_gen(data)
    children_count = next(gen)
    metadata_count = next(gen)
    root = Tree(None, children_count, metadata_count)
    current_node = root
    while True:
        children_count = next(gen)
        metadata_count = next(gen)
        new_node = Tree(current_node, children_count, metadata_count)
        current_node.children[current_node.index] = new_node
        current_node = new_node
        if children_count == 0:
            get_metadata(gen, current_node.metadata)
            while current_node.parent is not None:
                current_node = current_node.parent
                current_node.index += 1
                if current_node.index < len(current_node.children):
                    break
                get_metadata(gen, current_node.metadata)                    
            if current_node.parent is None and current_node.index == len(current_node.children):
                break
    return calculate_node_value(root)

def input_gen(data):
    arr = data.split(' ')
    for x in arr:
        yield(int(x))

def get_metadata(gen, arr):
    for i in range(len(arr)):
        arr[i] = next(gen)

def calculate_node_value(node):
    if len(node.metadata) == 0:
        return 0
    if len(node.children) == 0:
        return sum(node.metadata)
    node_value = 0
    for i in node.metadata:
        if i <= len(node.children):
            node_value += calculate_node_value(node.children[i - 1])
    return node_value

class Tree:
    def __init__(self, parent, children_count, metadata_count):
        self._parent = parent
        self._children = [None] * children_count
        self._metadata = [None] * metadata_count
        self._index = 0
    
    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        self._index = value

    @property
    def parent(self):
        return self._parent

    @property
    def children(self):
        return self._children

    @property
    def metadata(self):
        return self._metadata

# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)

test(138, part1('2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'))
test(66, part2('2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'))

# Solve real puzzle 
filename = 'data/day08.txt'
data = [line.rstrip('\n') for line in open(filename, 'r')][0]

print('Day 08, part 1: %r' % (part1(data)))
print('Day 08, part 2: %r' % (part2(data)))
