import requests

DAY = 5
YEAR = 2023
with open("cookie.txt", "r") as f:
  COOKIE = f.read().splitlines()[0]
INPUT_URL = f"https://adventofcode.com/{YEAR}/day/{DAY}/input"

headers = {
    "Cookie": f"session={COOKIE}"
}

puzzle = requests.get(INPUT_URL, headers = headers).content.decode('ASCII')

with open(f"day_{DAY:02}/input.txt", "w") as f:
  f.write(puzzle)