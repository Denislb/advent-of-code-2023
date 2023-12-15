def hash_func(str):
    value = 0
    for c in str:
        value = ((ord(c) + value) * 17) % 256
    return value

def part_one(filename):
    with open(filename) as f:
        splitted = f.read().strip().split(',')
    return sum(map(hash_func, splitted))

def part_two(filename):
    boxes = {}
    with open(filename) as f:
        splitted = f.read().strip().split(',')
    
    for lens in splitted:
        if '-' in lens:
            hash = hash_func(lens[:-1])
            if hash in boxes and lens[:-1] in boxes[hash]:
                boxes[hash].pop(lens[:-1], None)
        elif '=' in lens:
            s = lens.split('=')
            tag = s[0]
            v = s[1]
            hash = hash_func(tag)
            if hash in boxes:
                boxes[hash][tag] = v
            else:
                boxes[hash] = {tag: v}

    s = 0
    for box in boxes:
        x = 1
        for lens in boxes[box]:
            s += (box + 1) * x * int(boxes[box][lens])
            x += 1
    return s


if __name__ == "__main__":
    input_path = "./day_15/input.txt"
    print("---Part One---")
    print(part_one(input_path))

    print("---Part Two---")
    print(part_two(input_path))