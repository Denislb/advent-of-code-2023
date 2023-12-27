slopes = { ">" :(0, 1), "v": (1, 0), "^": (-1, 0), "<": (0, -1) }

class Node:
    def __init__(self, pos):
        self.pos = pos
        self.edges = {}
    
    def find_edges(self, maze, end, nodes, proceeds, restricted = False):
        if self.pos not in nodes:
            nodes[self.pos] = self
        proceeds[self.pos] = self
        self._find_edges(maze, end, self.pos, set(), 0, nodes, proceeds, restricted = restricted)
        for edge in self.edges:
            if edge.pos not in proceeds:
                edge.find_edges(maze, end, nodes, proceeds, restricted = restricted)
            
    
    def _find_edges(self, maze, end, pos, visited, count, nodes, proceeds, init = True, restricted = False):
        row, col = pos
        visited.add(pos)
        count += 1
        if init == False and row - 1 > 0 and row + 1 < len(maze) and col + 1 < len(maze[0]) and col - 1 > 0:
            if ([maze[row][col + 1], maze[row + 1][col], maze[row - 1][col], maze[row][col - 1]].count("#") < 2):
                if (row, col) in proceeds:
                    self.edges[proceeds[(row, col)]] = count - 1
                    return True
                if (row, col) in nodes:
                    self.edges[nodes[(row, col)]] = count - 1
                else:
                    new_edge = Node((row, col))
                    nodes[(row, col)] = new_edge
                    self.edges[new_edge] = count - 1
                return True
        for dir_row, dir_col in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            if  (row + dir_row < 0 
                    or row + dir_row >= len(maze)
                    or col + dir_col >= len(maze[0])
                    or col + dir_col < 0
                    or maze[row + dir_row][col + dir_col] == '#'):
                continue
            if restricted:
                if maze[row + dir_row][col + dir_col] in slopes and (dir_row, dir_col) != slopes[maze[row + dir_row][col + dir_col]]:
                    continue
            if (row + dir_row, col + dir_col) in visited:
                continue

            if (row + dir_row, col + dir_col) == end:
                if (row + dir_row, col + dir_col) in nodes:
                    self.edges[nodes[(row + dir_row, col + dir_col)]] = count
                else:
                    new_edge = Node((row + dir_row, col + dir_col))
                    self.edges[new_edge] = count
                    nodes[(row + dir_row, col + dir_col)] = new_edge
                return True
            self._find_edges(maze, end, (row + dir_row, col + dir_col), visited, count, nodes, proceeds, False, restricted = restricted)
        return False

    def find_longest(self, end, visited, idx = 0):
        longest = 0
        founded = False
        visited.add(self)
        if self == end:
            return True, 0
        for edge, val in self.edges.items():
            if edge in visited:
                continue
            f, r =  edge.find_longest(end, visited.copy(), idx + 1)
            if f:
                founded = f
                s = val + r
                longest = max(s, longest)
        return founded, longest

def parse_input(filename):
    maze = []
    start = None
    end = None
    with open(filename) as f:
        for line in f:
            maze.append([*line.strip()])
    min_row = 0
    while start is None:
        min_col = 0
        while min_col < len(maze[min_row]):
            if maze[min_row][min_col] == '.':
                start = (min_row, min_col)
                break
            min_col += 1
        min_row += 1
    
    max_row = len(maze) - 1
    while end is None:
        max_col = len(maze[max_row]) - 1
        while max_col > 0:
            if maze[max_row][max_col] == '.':
                end = (max_row, max_col)
                break
            max_col -= 1
    return maze, start, end

def part_one(maze, start, end):
    starting_node = Node(start)
    nodes = {}
    starting_node.find_edges(maze, end, {}, nodes, restricted = True)
    f, r = starting_node.find_longest(nodes[end], set())
    return r



def part_two(maze, start, end):
    starting_node = Node(start)
    nodes = {}
    starting_node.find_edges(maze, end, {}, nodes)
    f, r = starting_node.find_longest(nodes[end], set())
    return r


if __name__ == "__main__":
    input_path = "./day_23/input.txt"
    maze, start, end = parse_input(input_path)
    print("---Part One---")
    print(part_one(maze, start, end))

    print("---Part Two---")
    print(part_two(maze, start, end))