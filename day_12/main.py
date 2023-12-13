import re

def clean_dots(str):
    last_is_dot = False
    new_str = ""
    for i in range(len(str)):
        if str[i] == '.' and last_is_dot:
            continue
        elif str[i] == '.':
            last_is_dot = True
        else:
            last_is_dot = False
        new_str += str[i]
    return new_str

def find_matches(line, infos, idx = 0, idx_infos = 0, count = 0, last_is_dot = False, hash_map = {}):
    if clean_dots("".join(line)) in hash_map:
        return hash_map[clean_dots("".join(line))]
    if idx < len(line) and line[idx::].count('.') == len(line[idx::]):
        idx = len(line)
    if idx >= len(line):
        if idx_infos == len(infos) - 1 and count == infos[idx_infos]:
            hash_map[clean_dots("".join(line))] = 1
            return 1
        hash_map[clean_dots("".join(line))] = 0
        return 0
    if idx_infos == len(infos) - 1 and count == infos[idx_infos] and line[idx::].count('?') + line[idx::].count('.') == len(line[idx::]):
        hash_map[clean_dots("".join(line))] = 1
        return 1
    if idx_infos >= len(infos) or count > infos[idx_infos]:
        hash_map[clean_dots("".join(line))] = 0
        return 0
    if line[idx::].count('?') + line[idx::].count('#') + count < sum(infos[idx_infos::]):
        hash_map[clean_dots("".join(line))] = 0
        return 0
    if line[idx] == "?":
        new_line = [*line]
        new_line[idx] = '.'
        r1 = find_matches(new_line, infos, idx + 1, idx_infos, count, True, hash_map)
        if last_is_dot and count != 0:
            if count != infos[idx_infos]:
                hash_map[clean_dots("".join(line))] = 0
                return 0
            idx_infos += 1
            count = 0
        new_line = [*line]
        new_line[idx] = '#'
        r2 = find_matches(new_line, infos, idx + 1, idx_infos, count + 1, False, hash_map)
        hash_map[clean_dots("".join(line))] = r1 + r2
        return r1 + r2
    else:
        if line[idx] == '#':
            if last_is_dot and count != 0:
                if count != infos[idx_infos]:
                    hash_map[clean_dots("".join(line))] = 0
                    return 0
                idx_infos += 1
                count = 0
            last_is_dot = False
            count += 1
        if line[idx] == '.':
            last_is_dot = True
        r = find_matches(line, infos, idx + 1, idx_infos, count, last_is_dot, hash_map)
        hash_map[clean_dots("".join(line))] = r
        return r

def part_one(filename):
    r = 0
    with open(filename) as f:
        for line in f:
            hash_map = {}
            record, infos = line.split()
            splitted_infos = [int(i) for i in infos.split(',')]
            splitted_record = list(record)
            r += find_matches(splitted_record, splitted_infos, hash_map = hash_map)
    return r

def unfold_records(str, infos):
    return f"{str}?{str}?{str}?{str}?{str}", f"{infos},{infos},{infos},{infos},{infos}"

def part_two(filename):
    r = 0
    with open(filename) as f:
        for line in f:
            hash_map = {}
            record, infos = unfold_records(*line.split())
            splitted_infos = [int(i) for i in infos.split(',')]
            splitted_record = list(record)
            r += find_matches(splitted_record, splitted_infos, hash_map = hash_map)
    return r



if __name__ == "__main__":
    input_path = "./day_12/input.txt"
    print("---Part One---")
    print(part_one(input_path))

    print("---Part Two---")
    print(part_two(input_path))