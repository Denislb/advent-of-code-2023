import re

def part_one(filename):
    with open(filename) as f:
        times = list(map(int, re.findall(r'(\d+)', f.readline())))
        dists = list(map(int, re.findall(r'(\d+)', f.readline())))
    ret_value = 1
    for race in range(0, len(times)):
        records = 0
        for t in range(0, times[race]):
            dist = t * (times[race] - t)
            if dist > dists[race]:
                records += 1
        ret_value *= records
    return ret_value


def part_two(filename):
    with open(filename) as f:
        max_time = int(''.join(re.findall(r'(\d+)', f.readline())))
        max_dist = int(''.join(re.findall(r'(\d+)', f.readline())))
    records = 0
    for t in range(0, max_time):
        dist = t * (max_time - t)
        if dist > max_dist:
            records += 1
    return records

if __name__ == "__main__":
    input_path = "./day_06/input.txt"
    print("---Part One---")
    print(part_one(input_path))

    print("---Part Two---")
    print(part_two(input_path))