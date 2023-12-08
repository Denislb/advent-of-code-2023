import re
import math

class Node:
    def __init__(self, name):
        self.left = None
        self.right = None
        self.name = name
      
    def addLeftNode(self, node):
        self.left = node

    def addRightNode(self, node):
        self.right = node

    def printNode(self):
        print(f"Name: {self.name}")
        print(f"Left: {self.left}")
        print(f"Right: {self.right}")

    def getLeft(self):
        return self.left
    
    def getRight(self):
        return self.right

    def getName(self):
        return self.name
    
    def getNextNodesName(self):
        return self.left.getName(), self.right.getName()

def parse_input(filename):
    nodes = {}
    root = None
    last = None
    with open(filename) as f:
        instructions = f.readline().strip()
        f.readline()
        for node in f:
            node_infos = re.search(r"(\w*) = \((\w*), (\w*)\)", node)
            node_name = node_infos.group(1)
            left_node = node_infos.group(2)
            right_node = node_infos.group(3)
            if node_name not in nodes:
                nodes[node_name] = Node(node_name)
            if left_node not in nodes:
                nodes[left_node] = Node(left_node)
            if right_node not in nodes:
                nodes[right_node] = Node(right_node)
            nodes[node_name].addLeftNode(nodes[left_node])
            nodes[node_name].addRightNode(nodes[right_node])
    return instructions, nodes

def part_one(instructions, nodes):
    root = nodes["AAA"]
    last = nodes["ZZZ"]
    current = root
    steps = 0
    while True:
        found = False
        for inst in instructions:
            steps += 1
            if inst == "L":
                current = current.getLeft()
            else:
                current = current.getRight()
            if current == last:
                found = True
                break
        if found:
            break
    return steps

def part_two(instructions, nodes):
    roots = [nodes[node] for node in nodes if node.endswith("A")]
    steps_list = []
    max = 0
    for current in roots:
        steps = 0
        while True:
            found = False
            for inst in instructions:
                steps += 1
                if inst == "L":
                    current = current.getLeft()
                else:
                    current = current.getRight()
                if current.getName().endswith("Z"):
                    found = True
                    steps_list.append(steps)
                    break
            if found:
                break

    return math.lcm(*steps_list)


if __name__ == "__main__":
    input_path = "./day_08/input.txt"
    instructions, nodes = parse_input(input_path)

    print("---Part One---")
    print(part_one(instructions, nodes))

    print("---Part Two---")
    print(part_two(instructions, nodes))