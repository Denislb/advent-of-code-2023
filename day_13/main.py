def parse_input(filename):
    maps_list = []
    with open(filename) as f:
        new_map = []
        for line in f:
            if not line.strip():
                maps_list.append([*new_map])
                new_map = []
                continue
            new_map.append(line.strip())
    
    maps_list.append(new_map)
    return maps_list

def rotate_island(island):
    new_array = []
    for x in range(len(island[0])):
        new_row = []
        for y in range(len(island)):
            new_row.append(island[y][x])
        new_array.append(new_row)
    return new_array

def find_reflection_row(island, smudge_pos = 0, pos_2 = 0, part_2 = False):
    curr = 0
    matches = []
    start = {}
    while curr < len(island):
        count = 0
        before = curr
        after = curr + 1
        founded = False
        while before >= 0 and after < len(island):
            start[curr] = before
            if island[before] != island[after]:
                founded = False
                break
            founded = True
            count += 1
            before -= 1
            after += 1
        if founded:
            if (part_2 and smudge_pos >= start[curr] and smudge_pos <= curr and curr <= pos_2) or not part_2:
                matches.append(curr)
        curr += 1
    if not matches:
        return 0
    return matches[0] + 1

def print_island(island):
    for l in island:
        for idx, i in enumerate(l):
            print(i, end="")
        print("")

def part_one(map_list):
    rows = []
    cols = []
    for island in map_list:
        row_idx = find_reflection_row(island)
        col_idx = find_reflection_row(rotate_island(island))
        rows.append(row_idx)
        cols.append(col_idx)
    return sum(rows) * 100 + sum(cols)


def diff_by_one(map_list):
    diffs = []
    for idx, value in enumerate(map_list):
        i = idx + 1
        while i < len(map_list):
            diff_size = 0
            pos = 0
            for x in range(len(value)):
                if map_list[i][x] != value[x]:
                    diff_size += 1
                    pos = x
                    if diff_size > 1:
                        break
            if diff_size == 1:
                diffs.append((idx, i))
            i += 1
    return diffs

def part_two(map_list):
    s = 0
    for i, island in enumerate(map_list):
        diffs = diff_by_one(island)
        founded = False
        for d in diffs:
            new_island = [*island]
            new_island[d[0]] = new_island[d[1]]
            row_idx = find_reflection_row(new_island, d[0], d[1], True)
            if row_idx != 0:
                founded = True
                s += row_idx * 100
                break
        if not founded:
            r_island = rotate_island(island)
            diffs = diff_by_one(r_island)
            for d in diffs:
                new_island = [*r_island]
                new_island[d[0]] = new_island[d[1]]
                col_idx = find_reflection_row(new_island, d[0], d[1], True)
                if col_idx != 0:
                    s += col_idx
                    break
    return s

if __name__ == "__main__":
    input_path = "./day_13/input.txt"
    map_list = parse_input(input_path)
    print("---Part One---")
    print(part_one(map_list))

    print("---Part Two---")
    print(part_two(map_list))