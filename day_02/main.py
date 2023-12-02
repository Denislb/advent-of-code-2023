import re

RED = 12
GREEN = 13
BLUE = 14

if __name__ == "__main__":
    input_path = "./day_02/input.txt"
    sum_1 = 0
    sum_2 = 0
    with open(input_path) as f:
        for idx, line in enumerate(f):
            max_red = max(map(int, re.findall(r'(\d+) red', line)))
            max_green = max(map(int, re.findall(r'(\d+) green', line)))
            max_blue = max(map(int, re.findall(r'(\d+) blue', line)))
            if max_red <= RED and max_green <= GREEN and max_blue <= BLUE:
                sum_1 += idx + 1
            sum_2 += max_red * max_green * max_blue
            
    print("---Part One---")
    print(sum_1)
    print("---Part Two---")
    print(sum_2)