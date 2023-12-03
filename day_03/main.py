import numpy

def parse_input(filename):
    with open(input_path) as f:
        lines = f.read().splitlines()
        map = ([list(l) for l in lines])
    return map

def check_areas(map, l_num, c_num):
    for y in range(l_num - 1, l_num + 2):
        for x in range(c_num - 1, c_num + 2):
            if y >= 0 and x >= 0 and y < len(map) and x < len(map[0]):
                if map[y][x] and not map[y][x].isdigit() and map[y][x] != ".":
                    return True
    return False

def get_gear_coords(map, l_num, c_num):
    for y in range(l_num - 1, l_num + 2):
        for x in range(c_num - 1, c_num + 2):
            if y >= 0 and x >= 0 and y < len(map) and x < len(map[0]):
                if map[y][x] and map[y][x] == "*":
                    return (y, x)
    return None

def part_one(map):
    valid_numbers = []
    for l_num, lines in enumerate(map):
        new_num = ""
        symbol_found = False
        for c_num, char in enumerate(lines):
            if char.isdigit():
                new_num += char
                if check_areas(map, l_num, c_num):
                    symbol_found = True
            else:
                if symbol_found:
                    valid_numbers.append(int(new_num))
                symbol_found = False
                new_num = ""
        if symbol_found:
            valid_numbers.append(int(new_num))
    return sum(valid_numbers)


def part_two():
    gears = {}
    for l_num, lines in enumerate(map):
        new_num = ""
        gear_found = False
        new_gear = None
        for c_num, char in enumerate(lines):
            if char.isdigit():
                new_num += char
                gear_coords = get_gear_coords(map, l_num, c_num)
                if gear_coords:
                    new_gear = gear_coords
            else:
                if new_gear:
                    if new_gear not in gears:
                        gears[new_gear] = [ int(new_num) ]
                    else:
                        gears[new_gear].append(int(new_num))
                new_num = ""
                new_gear = None
        if new_gear:
            if new_gear not in gears:
                    gears[new_gear] = [ int(new_num) ]
            else:
                gears[new_gear].append(int(new_num))
    v = 0
    for g in gears.values():
        n = 0
        if (len(g) > 1):
            n = numpy.prod(g)
            v += n
    return v


if __name__ == "__main__":
    input_path = "./day_03/input.txt"
    map = parse_input(input_path)
    print("---Part One---")
    print(part_one(map))

    print("---Part Two---")
    print(part_two())