import heapq

def parse_input(filename):
    grid = []
    with open(filename) as f:
        for l in f:
            grid.append([int(x) for x in l.strip()])
    return grid

def djikstra(grid, min_steps = 0, max_steps = 3):
    visited = set()
    nodes = [(0, 0, 0, 0, 0, 0)]
    while nodes:
        weight, row, col, prev_row, prev_col, steps = heapq.heappop(nodes)
        if (row, col, prev_row, prev_col, steps) in visited:
            continue

        visited.add((row, col, prev_row, prev_col, steps))
        if (row, col) == (len(grid) - 1, len(grid[0]) - 1) and steps >= min_steps:
            return weight

        for dir_row, dir_col in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            if  (row + dir_row < 0 
                    or row + dir_row >= len(grid)
                    or col + dir_col >= len(grid[0])
                    or col + dir_col < 0
                    or (row + dir_row, col + dir_col) == (prev_row, prev_col)):
                continue
            if (row - prev_row, col - prev_col) == (dir_row, dir_col) and steps < max_steps:
                heapq.heappush(nodes, (weight + grid[row + dir_row][col + dir_col], row + dir_row, col + dir_col, row, col, steps + 1))    
            elif ((row - prev_row, col - prev_col) != (dir_row, dir_col) and steps >= min_steps) or (row, col) == (0, 0):
                heapq.heappush(nodes, (weight + grid[row + dir_row][col + dir_col], row + dir_row, col + dir_col, row, col, 1))

def part_one(grid):
    return djikstra(grid)


def part_two(filename):
    return djikstra(grid, 4, 10)


if __name__ == "__main__":
    input_path = "./day_17/input.txt"
    grid = parse_input(input_path)
    print("---Part One---")
    print(part_one(grid))

    print("---Part Two---")
    print(part_two(grid))