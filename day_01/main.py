import re

matrice = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9 , "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9 }


def calibration(filename, regex):
    total = 0
    with open(filename) as f:
        for line in f:
            result = re.findall(f"{regex}", line)
            total += 10 * {result[0]} + {result[-1]}
    return total

def part_one(filename):
    return calibration(filename, "\\d")


def part_two(filename):
    return calibration(filename, "(?=(\\d|one|two|three|four|five|six|seven|eight|nine|ten))")


if __name__ == "__main__":
    input_path = "./day_01/input.txt"
    print("---Part One---")
    print(part_one(input_path))

    print("---Part Two---")
    print(part_two(input_path))
    