def parse_input(filename):
    starting_map = []
    max_x, max_y, max_z = 0, 0, 0
    blocks = {}
    idx = 0
    with open(filename) as f:
        for line in f:
            curr_block = line.strip().split('~')
            start_block = [int(i) for i in curr_block[0].split(',')]
            end_block = [int(i) for i in curr_block[1].split(',')]
            max_x = max(max_x, start_block[0], end_block[0])
            max_y = max(max_y, start_block[1], end_block[1])
            max_z = max(max_z, start_block[2], end_block[2])
            blocks[idx] = (start_block, end_block)
            idx += 1
    starting_map = generate_map(blocks, max_x, max_y, max_z)
    return starting_map, blocks

def print_map_z_y(map):
    z = len(map) - 1
    while z > 0:
        for r in map[z]:
            found = False
            for c in r:
                if c != '.':
                    found = True
                    print(c, end="")
                    break
            if found == False:
                print('.', end="")
        print()
        z -= 1

def print_map_z_x(map):
    z = len(map) - 1
    while z > 0:
        x = 0
        while x < len(map[z][0]):
            y = 0
            found = False
            while y < len(map[z]):
                if map[z][y][x] != '.':
                    found = True
                    print(map[z][y][x], end="")
                    break
                y += 1
            if found == False:
                print('.', end="")
            x += 1
        print("")
        z -= 1

def print_raw(map):
    z = len(map) - 1
    while z > 0:
        print(map[z])
        z -= 1

def generate_map(blocks, max_x, max_y, max_z):
    starting_map = []
    for z in range(max_z + 1):
        row_y = []
        for y in range(max_y + 1):
            row_x = []
            for x in range(max_x + 1):
                row_x.append('.')
            row_y.append(row_x)
        starting_map.append(row_y)

    for idx, block in blocks.items():
        for z in range(block[0][2], block[1][2] + 1):
            for y in range(block[0][1], block[1][1] + 1):
                for x in range(block[0][0], block[1][0] + 1):
                    starting_map[z][y][x] = idx
    return starting_map

def fall(starting_map, blocks):
    fall = True
    while fall:
        new_blocks = {}
        fall = False
        for idx, block in blocks.items():
            z = min(block[0][2], block[1][2])
            found = False
            if z == 1:
                found = True
            for y in range(block[0][1], block[1][1] + 1):
                for x in range(block[0][0], block[1][0] + 1):
                    if starting_map[z - 1][y][x] != '.':
                        found = True
                        break
                if found:
                    break
            if not found:
                fall = True
                new_blocks[idx] = ([block[0][0], block[0][1], block[0][2] - 1], [block[1][0], block[1][1], block[1][2] - 1])
            else:
                new_blocks[idx] = (block)
        blocks = new_blocks
        starting_map = generate_map(blocks, len(starting_map[0][0]) - 1, len(starting_map[0]) - 1, len(starting_map) - 1)
    return starting_map, blocks

def check_multiple_supports(starting_map, blocks, b, removed_support = []):
    block = blocks[b]
    z = min(block[0][2], block[1][2])
    supported_by = set()
    for y in range(block[0][1], block[1][1] + 1):
        for x in range(block[0][0], block[1][0] + 1):
            if starting_map[z - 1][y][x] != '.' and starting_map[z - 1][y][x] not in removed_support:
                supported_by.add(starting_map[z - 1][y][x])
    return supported_by

def part_one(starting_map, blocks):
    count = 0
    for _, block in blocks.items():
        support = set()
        z = max(block[0][2], block[1][2])
        for y in range(block[0][1], block[1][1] + 1):
            for x in range(block[0][0], block[1][0] + 1):
                if z + 1 < len(starting_map):
                    if starting_map[z + 1][y][x] != '.':
                        support.add(starting_map[z + 1][y][x])
        f = True
        for s in support:
            if len(check_multiple_supports(starting_map, blocks, s)) <= 1:
                f = False
                break
        if f:
            count += 1
    return count


def remove_blocks(blocks, to_remove):
    to_check = {}
    ret = set()
    if len(to_remove) == 0:
        return
    for tr in to_remove:
        block = blocks[tr]
        ret.add(tr)
        support = set()
        z = max(block[0][2], block[1][2])
        for y in range(block[0][1], block[1][1] + 1):
            for x in range(block[0][0], block[1][0] + 1):
                if z + 1 < len(starting_map):
                    if starting_map[z + 1][y][x] != '.':
                        support.add(starting_map[z + 1][y][x])
        # print(f"[{tr}] ==> {support} wth {to_remove}")
        for s in support:
            if len(check_multiple_supports(starting_map, blocks, s, to_remove)) <= 0:
                if tr not in to_check:
                    to_check[tr] = [s]
                else:
                    to_check[tr].append(s)
        if tr in to_check:
            ret = ret.union(remove_blocks(blocks, to_check[tr]))
    return ret

def part_two(starting_map, blocks): # 91530 to high - 1265 to low
    to_check = {}
    for idx, block in blocks.items():
        support = set()
        z = max(block[0][2], block[1][2])
        for y in range(block[0][1], block[1][1] + 1):
            for x in range(block[0][0], block[1][0] + 1):
                if z + 1 < len(starting_map):
                    if starting_map[z + 1][y][x] != '.':
                        support.add(starting_map[z + 1][y][x])
        for s in support:
            if len(check_multiple_supports(starting_map, blocks, s)) <= 1:
                if idx not in to_check:
                    to_check[idx] = [s]
                else:
                    to_check[idx].append(s)
    print_raw(starting_map)
    # print_map_z_y(starting_map)
    # print("----")
    # print(to_check)
    ret = 0
    idx = 0
    print(len(to_check))
    for b in to_check:
        r = remove_blocks(blocks, to_check[b])
        print(r)
        ret += len(r)
        idx += 1
    #print(ret)
    return ret

if __name__ == "__main__":
    input_path = "./day_22/exemple.txt"
    starting_map, blocks = parse_input(input_path)
    starting_map, blocks = fall(starting_map, blocks)
    print("---Part One---")
    print(part_one(starting_map, blocks))

    print("---Part Two---")
    print(part_two(starting_map, blocks))