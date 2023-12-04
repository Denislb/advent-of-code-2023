import re
from collections import defaultdict


def part_one(filename):
    points = 0
    with open(input_path) as f:
        for idx, line in enumerate(f):
            cur_points = 0
            splitted = line.split('|')
            winnings = re.findall(r"(\d+) ", splitted[0])
            numbers = re.findall(r"(\d+)", splitted[1])
            for winning_num in winnings:
                if winning_num in numbers:
                    if cur_points == 0:
                        cur_points = 1
                    else:
                        cur_points = cur_points * 2
            points += cur_points
    return points



def part_two(input_path):
    cards = defaultdict(int)
    with open(input_path) as f:
        for idx, line in enumerate(f):
            cards[idx] += 1
            splitted = line.split('|')
            winnings = re.findall(r"(\d+) ", splitted[0])
            numbers = re.findall(r"(\d+)", splitted[1])
            curr = idx + 1
            for winning_num in winnings:
                if winning_num in numbers:
                    cards[curr] += cards[idx]
                    curr += 1
    return sum(cards.values())


if __name__ == "__main__":
    input_path = "./day_04/input.txt"
    print("---Part One---")
    print(part_one(input_path))

    print("---Part Two---")
    print(part_two(input_path))