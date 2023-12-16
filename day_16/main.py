def parse_input(filename):
    grid = []
    with open(filename) as f:
        for l in f:
            grid.append([*l.strip()])
    return grid

def print_grid(grid):
    for row in grid:
        print("".join(row))

RIGHT = (0, 1)
LEFT = (0, -1)
DOWN = (1, 0)
UP = (-1, 0)

matrix_dir = {
    LEFT:  { "/": DOWN,  "\\": UP, '-': LEFT},
    RIGHT: { "/": UP,    "\\": DOWN, '-': RIGHT},
    UP:    { "/": RIGHT, "\\": LEFT, '|': UP},
    DOWN:  { "/": LEFT,  "\\": RIGHT, '|': DOWN}
}

def energize_tiles(grid, start, direction):
    energized = []
    beams = [{"pos": start, "dir": direction}]
    passed = []
    
    while beams:
        for idx, beam in enumerate(beams):
            if (beam["pos"][0] + beam["dir"][0] >= len(grid)
                    or beam["pos"][0] + beam["dir"][0] < 0 
                    or beam["pos"][1] + beam["dir"][1] >= len(grid[0])
                    or beam["pos"][1] + beam["dir"][1] < 0):
                beams.pop(idx)
                continue
            beam["pos"] = beam["pos"][0] + beam["dir"][0], beam["pos"][1] + beam["dir"][1]
            if (beam["pos"], beam["dir"]) in passed:
                beams.pop(idx)
                continue
            if beam["pos"] not in energized:
                energized.append(beam["pos"])
            if grid[beam["pos"][0]][beam["pos"][1]] == '|' and (beam["dir"] == RIGHT or beam["dir"] == LEFT):
                passed.append((beam["pos"], beam["dir"]))
                beam["dir"] = DOWN
                beams.append({"pos": beam["pos"], "dir": UP})
            elif grid[beam["pos"][0]][beam["pos"][1]] == '-' and (beam["dir"] == DOWN or beam["dir"] == UP):
                passed.append((beam["pos"], beam["dir"]))
                beam["dir"] = RIGHT
                beams.append({"pos": beam["pos"], "dir": LEFT})
            elif grid[beam["pos"][0]][beam["pos"][1]] in ['/', '\\', '|', '-']:
                passed.append((beam["pos"], beam["dir"]))
                mirror = grid[beam["pos"][0]][beam["pos"][1]]
                beam["dir"] = matrix_dir[beam["dir"]][mirror]
        if not beams:
            break
    return len(energized)

def part_one(grid):
    return energize_tiles(grid, (0, -1), RIGHT)

def part_two(grid):
    r = 0
    for y in range(len(grid)):
        r = max(r, energize_tiles(grid, (y, len(grid[0])), LEFT))
        r = max(r, energize_tiles(grid, (y, -1), RIGHT))
    for x in range(len(grid[0])):
        r = max(r, energize_tiles(grid, (-1, x), DOWN))
        r = max(r, energize_tiles(grid, (len(grid), x), UP))
    return r

if __name__ == "__main__":
    input_path = "./day_16/input.txt"
    grid = parse_input(input_path)
    print("---Part One---")
    print(part_one(grid))

    print("---Part Two---")
    print(part_two(grid))