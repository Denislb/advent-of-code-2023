def parse_input(filename):
    seeds = []
    maps = {
        "seed-to-soil": [],
        "soil-to-fertilizer": [],
        "fertilizer-to-water": [],
        "water-to-light": [],
        "light-to-temperature": [],
        "temperature-to-humidity": [],
        "humidity-to-location": []
    }
    with open(filename) as f:
        seeds = [int(x) for x in f.readline().split(":")[1].split()]
        current_map = None
        for line in f:
            if not line.strip():
                continue
            if line.strip().strip(" map:") in maps:
                current_map = line.strip().strip(" map:")
                continue
            maps[current_map].append([int(x) for x in line.strip().split()])
    return seeds, maps

def part_one(seeds, maps):
    min_seed = None
    for seed in seeds:
        for map in maps:
            for values in maps[map]:
                if seed in range(values[1], values[1] + values[2]):
                    seed = values[0] + (seed - values[1])
                    break
        if not min_seed or seed < min_seed:
            min_seed = seed
    return min_seed

def Merge(dict1, dict2):
    return({**dict1, **dict2})

def generate_new_ranges(range_map, seed, seed_range):
    new_seeds = {}
    need_reprocess = {}
    found = False
    for range in range_map:
        if seed >= range[1] and seed + seed_range <= range[1] + range[2]:
            new_seeds[range[0] + (seed - range[1])] = seed_range
            found = True
            break
        elif seed >= range[1] and seed + seed_range >= range[1] + range[2] and seed <= range[1] + range[2]:
            found = True
            new_range = (range[1] + range[2]) - seed or 1
            new_seeds[range[0] + (seed - range[1])] = new_range
            need_reprocess[seed + new_range] = seed_range - new_seeds[range[0] + (seed - range[1])] ## Need to reprocess this part
        elif seed < range[1] and seed + seed_range <= range[1] + range[2] and seed + seed_range >= range[1]:
            found = True
            need_reprocess[seed] = range[1] - seed - 1 or 1 ## Need to reprocess this part
            new_seeds[range[0]] = seed_range - need_reprocess[seed]
        elif seed < range[1] and seed + seed_range >= range[1] + range[2]:
            found = True
            need_reprocess[seed] = range[1] - seed or 1  ## Need to reprocess this part
            new_seeds[range[0]] = range[2]
            need_reprocess[range[1] + range[2]] = seed_range - new_seeds[range[0]] ## Need to reprocess this part
    if not found:
        new_seeds[seed] = seed_range
        need_reprocess = {}
    if need_reprocess:
        for s in need_reprocess:
            ret = generate_new_ranges(range_map, s, need_reprocess[s])
            new_seeds = Merge(new_seeds, ret)

    return new_seeds



def part_two(seeds, maps):
    min_seed = None
    ranges = {}
    idx = 0
    while idx < len(seeds):
        ranges[seeds[idx]] = seeds[idx+1]
        idx += 2
    for map in maps:
        news = {}
        found = False
        for seeds_min in ranges:
            ret = generate_new_ranges(maps[map], seeds_min, ranges[seeds_min])
            news = Merge(news, ret)
        ranges = news
    m = None
    for r in ranges:
        if m is None or (r < m and r > 1):
            m = r
    return m


if __name__ == "__main__":
    input_path = "./day_05/input.txt"
    seeds, maps = parse_input(input_path)
    print("---Part One---")
    print(part_one(seeds, maps))

    print("---Part Two---")
    print(part_two(seeds, maps))