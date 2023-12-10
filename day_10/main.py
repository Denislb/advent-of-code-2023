class Node:
    def __init__(self, positions, type):
        self.next = None
        self.positions = positions
        self.type = type

    def setNext(self, next):
        self.next = next

    def getNext(self):
        return self.next

    def getPositons(self):
        return self.positions
    
    def getType(self):
        return self.type

def generate_tree(filename):
    map = []
    pipe_pos = []
    with open(filename) as f:
        for line in f.readlines():
            map.append([*line[:-1].replace(".", "0")])
    
    for y, row in enumerate(map):
        for x, char in enumerate(row):
            if char == "S":
                start = Node((y, x), "S")
    y, x = start.getPositons()
    if y - 1 >= 0 and map[y - 1][x] in ["|", "7", "F"]:
        start.setNext(Node((y - 1, x), map[y - 1][x]))
    elif y + 1 < len(map) and map[y + 1][x] in ["|", "J", "L"]:
        start.setNext(Node((y + 1, x), map[y + 1][x]))
    elif x - 1 >= 0 and map[y][x - 1] in ["-", "F", "L"]:
        start.setNext(Node((y, x - 1), map[y][x - 1]))
    elif x + 1 < len(row) and map[y][x + 1] in ["-", "7", "J"]:
        start.setNext(Node((y, x + 1), map[y][x + 1]))

    curr = start.getNext()
    prev_y, prev_x = start.getPositons()
    pipe_pos.append((prev_y, prev_x))
    while curr != start:
        y, x = curr.getPositons()
        pipe_pos.append((y, x))
        if y - 1 >= 0 and y - 1 != prev_y and map[y - 1][x] in ["|", "7", "F"] and map[y][x] in ["|", "J", "L"]:
            curr.setNext(Node((y - 1, x), map[y - 1][x]))
        elif y + 1 < len(map) and y + 1 != prev_y and map[y + 1][x] in ["|", "J", "L"] and map[y][x] in ["|", "F", "7"]:
            curr.setNext(Node((y + 1, x), map[y + 1][x]))
        elif x - 1 >= 0 and x - 1 != prev_x and map[y][x - 1] in ["-", "F", "L"] and map[y][x] in ["-", "J", "7"] :
            curr.setNext(Node((y, x - 1), map[y][x - 1]))
        elif x + 1 < len(row) and x + 1 != prev_x and map[y][x + 1] in ["-", "7", "J"] and map[y][x] in ["-", "F", "L"]:
            curr.setNext(Node((y, x + 1), map[y][x + 1]))
        else:
            curr.setNext(start)
        prev_y, prev_x = curr.getPositons()
        curr = curr.getNext()
    for y, row in enumerate(map):
        for x, col in enumerate(row):
            if (y, x) not in pipe_pos:
                map[y][x] = "0"
    return start, map

def part_one(start_node):
    count = 1
    curr = start_node.getNext()
    while curr != start_node:
        count += 1
        curr = curr.getNext()
    return count // 2

def part_two(map):
    count = 0
    for row in map:
        inside = False
        x = 0
        while x < len(row):
            if row[x] == '0' and inside:
                count += 1
            elif row[x] == '|':
                inside = not inside
            elif row[x] == 'L' or row[x] == 'F':
                start = row[x]
                x += 1
                while row[x] == '-':
                    x += 1
                if (start == 'F' and row[x] == 'J') or (start == 'L' and row[x] == '7'):
                    inside = not inside
            x += 1
    return count


if __name__ == "__main__":
    input_path = "./day_10/input.txt"
    start_node, map = generate_tree(input_path)
    print("---Part One---")
    print(part_one(start_node))

    print("---Part Two---")
    print(part_two(map))