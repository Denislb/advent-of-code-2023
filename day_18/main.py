def parse_input(filename):
    instructions = []
    with open(filename) as f:
        for l in f:
            instruction = l.split()
            instructions.append(instruction)
    return instructions

def calc_shoelace_formula(vertices, border_length):
    s = 0
    for idx, vertice in enumerate(vertices):
        if idx + 1 < len(vertices):
            s += (vertice[0] * vertices[idx + 1][1]) - (vertice[1] * vertices[idx + 1][0])
    s += vertices[len(vertices) - 1][0] * vertices[0][1] - vertices[0][0] * vertices[len(vertices) - 1][1] 
    return((abs(s) + border_length) // 2) + 1

def generate_dir_from_hexa(hexa):
    dir = ''
    if hexa[-2] == '0':
        dir = 'R'
    elif hexa[-2] == '1':
        dir = 'D'
    elif hexa[-2] == '2':
        dir = 'L'
    elif hexa[-2] == '3':
        dir = 'U'
    return dir, int(hexa[2:-2], 16)

def part_two(instructions):
    vertices = []
    col, row = 0, 0
    border_length = 0
    for instruction in instructions:
        dir, len = generate_dir_from_hexa(instruction[2])
        if dir == 'R':
            col += len
            vertices.append((row, col))
        elif dir == 'L':
            col -= len
            vertices.append((row, col))
        elif dir == 'U':
            row -= len
            vertices.append((row, col))
        elif dir == 'D':
            row += len
            vertices.append((row, col))
        border_length += len
    return calc_shoelace_formula(vertices, border_length)

def part_one(instructions):
    vertices = []
    col, row = 0, 0
    border_length = 0
    for instruction in instructions:
        if instruction[0] == 'R':
            col += int(instruction[1])
            vertices.append((row, col))
        elif instruction[0] == 'L':
            col -= int(instruction[1])
            vertices.append((row, col))
        elif instruction[0] == 'U':
            row -= int(instruction[1])
            vertices.append((row, col))
        elif instruction[0] == 'D':
            row += int(instruction[1])
            vertices.append((row, col))
        border_length += int(instruction[1])
    return calc_shoelace_formula(vertices, border_length)

if __name__ == "__main__":
    input_path = "./day_18/input.txt"
    instructions = parse_input(input_path)
    print("---Part One---")
    print(part_one(instructions))

    print("---Part Two---")
    print(part_two(instructions))