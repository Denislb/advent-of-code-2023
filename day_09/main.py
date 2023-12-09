def get_distances(values):
    distances = []
    idx = 0
    while idx < len(values) - 1:
        distances.append(values[idx + 1]- values[idx])
        idx += 1
    return distances

def check_distances_equals(distances):
    return all(distance == distances[0] for distance in distances) 

def resolve(filename):
    result_1 = 0
    result_2 = 0
    with open(filename) as f:
        for l in f:
            distances_list = []
            values = [int(n) for n in l.split()]
            distances = get_distances(values)
            distances_list.append(distances)
            while not check_distances_equals(distances):
                distances = get_distances(distances)
                distances_list.append(distances)
            new_value_1 = 0
            new_value_2 = 0
            for distance in distances_list[::-1]:
                new_value_1 += distance[-1]
                new_value_2 = distance[0] - new_value_2
            result_1 += new_value_1 + values[-1]
            result_2 += values[0] - new_value_2
    return result_1, result_2


if __name__ == "__main__":
    input_path = "./day_09/input.txt"
    #print(part_one(input_path))

    results = resolve(input_path)
    print("---Part One---")
    print(results[0])
    print("---Part Two---")
    print(results[1])

