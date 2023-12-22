def parse_input(filename):
    rocks = set()
    start = None
    row = 0
    with open(filename) as f:
        for line in f:
            col = 0
            for char in line:
                if char == "#":
                    rocks.add((row, col))
                elif char == "S":
                    start = (row, col)
                col += 1
            row += 1
    return rocks, start, row, col - 1

def part_one(rocks, start):
    pos = {start}
    for steps in range(64):
        new_pos = set()
        for p in pos:
            for dir in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if (p[0] + dir[0], p[1] + dir[1]) not in rocks:
                    new_pos.add((p[0] + dir[0], p[1] + dir[1]))
        pos = new_pos
    return len(pos)

def expand_map(rocks, start, rows, cols, size):
    new_rocks = set()
    for rock in rocks:
        for row in range(size):
            for col in range(size):
                new_rocks.add((rock[0] + row * rows, rock[1] + col * cols))
    start_pos = size // 2
    new_start = (start[0] + start_pos * rows, start[1] + start_pos * cols)
    return new_rocks, new_start, rows * size, cols * size

def part_two(rocks, start, rows, cols):
    pos = {start}
    m = set()
    for x in range(rows):
        for y in range(cols):
            if ((x, y) not in rocks):
                ok = False
                for dir in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    if (x + dir[0], y + dir[1]) not in rocks:
                        ok = True
                if ok:
                    m.add((x, y))
    values = []
    for idx in range(328):
        new_pos = set()
        for p in pos:
            for dir in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if (p[0] + dir[0], p[1] + dir[1]) not in rocks:
                    new_pos.add((p[0] + dir[0], p[1] + dir[1]))
        if idx in [65, 196, 327]:
            values.append(len(pos))
        pos = new_pos

    t = 26501365 // 131
    return(values[0] + (values[1] - values[0]) * t + (t * (t - 1) // 2) * ((values[2] - values[1]) - (values[1] - values[0])))


if __name__ == "__main__":
    input_path = "./day_21/input.txt"
    rocks, start, rows, cols = parse_input(input_path)
    print("---Part One---")
    print(part_one(rocks, start))
    rocks, start, rows, cols = expand_map(rocks, start, rows, cols, 7)
    print("---Part Two---")
    print(part_two(rocks, start, rows, cols))