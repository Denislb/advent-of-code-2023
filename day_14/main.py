def print_map(m):
    for r in m:
        for i in r:
            print(i, end="")
        print()

def parse_input(filename):
    m = []
    with open(filename) as f:
        for line in f:
            m.append([*line.strip()])
    return m

def calc_north(m):
    s = 0
    for y in range(len(m[0])):
        count = 0
        last = 0
        last = 0
        for x in range(len(m)):
            if m[x][y] == "O":
                count += 1
            elif m[x][y] == "#":
                s += (count / 2) * (len(m) - last + len(m) - last - count + 1)
                last = x + 1
                count = 0
        s += (count / 2) * (len(m) - last + len(m) - last - count + 1)
    return int(s)

def determine_type_pos(m, t):
    t_list = {}
    for i, r in enumerate(m):
        for y, c in enumerate(r):
            if c == t:
                if y in t_list:
                    t_list[y].append(i)
                else:
                    t_list[y] = [i]
    return t_list

def roll_north(m):
    solids_pos = determine_type_pos(m, "#")
    rocks_pos = determine_type_pos(m, "O")
    new_map = []
    for y in range(len(m)):
        new_row = []
        for x in range(len(m[0])):
            new_row.append('.')
            if x in solids_pos:
                if y in solids_pos[x]:
                    new_row[x] = '#'
        new_map.append(new_row)
    for rock_col in rocks_pos:
        for rock_row in rocks_pos[rock_col]:
            while rock_row > 0:
                if rock_row - 1 == -1 or new_map[rock_row - 1][rock_col] == '#' or new_map[rock_row - 1][rock_col] == 'O':
                    break
                rock_row -= 1
            new_map[rock_row][rock_col] = 'O'
    return new_map

def rotate_90_right(m):
    new_array = []
    for x in range(len(m[0])):
        new_row = []
        y = len(m[0]) - 1
        while y >= 0:
            new_row.append(m[y][x])
            y -= 1
        new_array.append(new_row)
    return new_array

def generate_hash(m):
    s = ""
    for line in m:
        s += "".join(line)
    return s

def part_two(m):
    passed = []
    idx = 0
    first = None
    num_cycles = 1000000000
    while idx < num_cycles:
        north_map = roll_north(m)
        west_map = roll_north(rotate_90_right(north_map))
        south_map = roll_north(rotate_90_right(west_map))
        east_map = roll_north(rotate_90_right(south_map))
        m = rotate_90_right(east_map)
        hash_map = generate_hash(m)
        if hash_map in passed and idx >= len(passed):
            if first is None:
                first = hash_map
            if idx - len(passed) + 1 == (num_cycles - passed.index(first)) % (len(passed) - passed.index(first)):
                break
        if hash_map not in passed:
            passed.append(hash_map)
        idx += 1
    count = 0
    for idx, r in enumerate(m):
        count += (r.count("O") * (len(m) - idx))
    return(count)

def part_one(m):
    return calc_north(m)

if __name__ == "__main__":
    input_path = "./day_14/input.txt"
    m = parse_input(input_path)
    print("---Part One---")
    print(part_one(m))

    print("---Part Two---")
    print(part_two(m))