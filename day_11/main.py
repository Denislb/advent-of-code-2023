def parse_input(filename):
    map = []
    with open(filename) as f:
        for line in f:
            map.append([*line[:-1]])
    return map


def get_empties(map):
    new_map = []
    empty_rows = []
    empty_cols = []
    for idx, line in enumerate(map):
        if line.count(".") == len(line):
            empty_rows.append(idx)
    to_add = []
    for idx in range(len(map[0])):
        founded = False
        for y in range(len(map)):
            if map[y][idx] != ".":
                founded = True
                break
        if founded == False:
            empty_cols.append(idx)

    return empty_rows, empty_cols

def len_empties(empty_map, idx_1, idx_2):
    count = 0
    for v in empty_map:
        if v > idx_1 and v < idx_2:
            count += 1
        if v > idx_2:
            break
    return count


def solve(map, empty_rows, empty_cols, expansion):
    galaxies = []
    sum = 0
    for y, row in enumerate(map):
        for x, c in enumerate(row):
            if c != ".":
                galaxies.append((y, x))
    for idx, galaxie in enumerate(galaxies):
        new_idx = idx + 1
        while new_idx < len(galaxies):
            nb_row = len_empties(empty_rows, min(galaxies[new_idx][0], galaxie[0]), max(galaxies[new_idx][0], galaxie[0]))
            nb_col = len_empties(empty_cols, min(galaxies[new_idx][1], galaxie[1]), max(galaxies[new_idx][1], galaxie[1]))
            sum += abs(galaxies[new_idx][0] - galaxie[0]) + (nb_row * expansion - 1) + abs(galaxies[new_idx][1] - galaxie[1]) + (nb_col * expansion - 1)
            new_idx += 1
    return sum


if __name__ == "__main__":
    input_path = "./day_11/input.txt"
    map = parse_input(input_path)
    empty_rows, empty_cols = get_empties(map)
    print("---Part One---")
    print(solve(map, empty_rows, empty_cols, 2))

    print("---Part Two---")
    print(solve(map, empty_rows, empty_cols, 1000000))
