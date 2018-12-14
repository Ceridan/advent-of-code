# Solution
def part1(data):
    skill_cap = data
    recipes = RecipesLinkedList(3, 7)
    k = 0
    while k < 10:
        (node1, node2) = recipes.generate_new_recipes()
        if node1 is not None:
            recipes.append(node1, skill_cap)
        recipes.append(node2, skill_cap)
        recipes.move_current()
        if recipes.skill_node is not None:
            k += 1
    result = ''
    current = recipes.skill_node.next
    for _ in range(10):      
        result += str(current.value)
        current = current.next
    return result

def part2(data):
    pass

class RecipesLinkedList:
    def __init__(self, value1, value2):
        node1 = RecipeNode(value1)
        node2 = RecipeNode(value2)
        node1.next = node2
        node2.next = node1
        self.current1 = node1
        self.current2 = node2
        self.head = node1
        self.tail = node2
        self.skill = 2
        self.skill_node = None
    
    def generate_new_recipes(self):
        new_value = self.current1.value + self.current2.value
        new_node1 = None
        if new_value > 9:
            new_node1 = RecipeNode(int(new_value / 10))
        new_node2 = RecipeNode(new_value % 10)
        return (new_node1, new_node2)

    def append(self, node, skill_cap):       
        self.tail.next = node
        node.next = self.head
        self.tail = node
        self.skill += 1
        if self.skill == skill_cap:
            self.skill_node = node

    def move_current(self):
        for _ in range(self.current1.value + 1):
            self.current1 = self.current1.next
        for _ in range(self.current2.value + 1):
            self.current2 = self.current2.next    

class RecipeNode:
    def __init__(self, value, next = None):
        self.value = value
        self.next = next

# Tests
def test(expected, actual):
    assert expected == actual, 'Expected: %r, Actual: %r' % (expected, actual)

test('0124515891', part1(5))
test('5158916779', part1(9))
test('9251071085', part1(18))
test('5941429882', part1(2018))

# test(5, part2('01245'))
# test(9, part2('51589'))
# test(18, part2('92510'))
# test(2018, part2('59414'))

# Solve real puzzle
filename = 'data/day14.txt'
data = int([line.rstrip('\n') for line in open(filename, 'r')][0])

print('Day 14, part 1: %r' % (part1(data)))
# print('Day 14, part 2: %r' % (part2(data)))
