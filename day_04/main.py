import re

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
    with open(input_path) as f:
        num_games = len(f.readlines())
    
    cards = {x: 1 for x in range(1, num_games + 1)}
    with open(input_path) as f:
        for idx, line in enumerate(f):
            wins = 0
            splitted = line.split('|')
            winnings = re.findall(r"(\d+) ", splitted[0])
            numbers = re.findall(r"(\d+)", splitted[1])
            for winning_num in winnings:
                if winning_num in numbers:
                    wins += 1
            curr = idx + 2
            while wins > 0:
                cards[curr] += cards[idx + 1]
                wins -= 1
                curr += 1
    return sum(cards.values())


if __name__ == "__main__":
    input_path = "./day_04/input.txt"
    print("---Part One---")
    print(part_one(input_path))

    print("---Part Two---")
    print(part_two(input_path))