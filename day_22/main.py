class Brick:
    def __init__(self):
        self.blocks = set()
        self.supported_by = set()
        self.support = set()

    def generate_blocks(self, start, end):
        for z in range(min(start[2], end[2]), max(start[2], end[2]) + 1):
            for y in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                for x in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
                    self.blocks.add((x, y, z))

    def calc_supports(self, bricks, idx):
        found = False
        while idx > 0:
            if idx in bricks:
                for brick in bricks[idx]:
                    for block in self.blocks:
                        if (block[0], block[1], idx) in brick.blocks:
                            found = True
                            self.supported_by.add(brick)
                            brick.support.add(self)
            idx -= 1
            if found:
                break

    def fall(self, bricks):
        current_fall = 0
        while True:
            can_fall = True
            for block in self.blocks:
                x, y, z = block
                if z - current_fall - 1 == 0:
                    can_fall = False
                    break
                if z - current_fall - 1 in bricks:
                    for brick in bricks[z - current_fall - 1]:
                        if (x, y, z - current_fall - 1) in brick.blocks:
                            can_fall = False
                            break
                if not can_fall:
                    break
            if not can_fall:
                new_blocks = set()
                for block in self.blocks:
                    new_blocks.add((block[0], block[1], block[2] - current_fall))
                self.blocks = new_blocks
                best_block = None
                for b in self.blocks:
                    if not best_block or best_block[2] < b[2]:
                        best_block = b
                if best_block[2] not in bricks:
                    bricks[best_block[2]] = [ self ]
                else:
                    bricks[best_block[2]].append(self)
                break
            current_fall += 1

    def is_multi_support(self):
        for support in self.support:
            if len(support.supported_by) < 2:
                return False
        return True

    def collapse(self, removed, count):
        removed.add(self)
        for support in self.support:
            c = 0
            for supported_by in support.supported_by:
                if supported_by not in removed:
                    c += 1
            if c == 0:
                count = support.collapse(removed, count + 1)
        return count

def parse_input(filename):
    bricks = {}
    with open(filename) as f:
        for line in f:
            curr_brick = line.strip().split('~')
            start_brick = [int(i) for i in curr_brick[0].split(',')]
            end_brick = [int(i) for i in curr_brick[1].split(',')]
            new_brick = Brick()
            new_brick.generate_blocks(start_brick, end_brick)
            if end_brick[2] not in bricks:
                bricks[end_brick[2]] = [new_brick]
            else:
                bricks[end_brick[2]].append(new_brick)

    new_bricks = {}
    for b in sorted(bricks):
        for brick in bricks[b]:
            brick.fall(new_bricks)
    for b in sorted(new_bricks, reverse=True):
        if b == 1:
            break
        for brick in new_bricks[b]:
            brick.calc_supports(new_bricks, b - 1)
    return new_bricks   


def part_one(bricks):
    count = 0
    for _, brick in bricks.items():
        for b in brick:
            if b.is_multi_support():
                count += 1
    return count

def part_two(bricks):
    count = 0
    for _, brick in bricks.items():
        for b in brick:
            count += b.collapse(set(), 0)
    return count

if __name__ == "__main__":
    input_path = "./day_22/input.txt"
    bricks = parse_input(input_path)
    print("---Part One---")
    print(part_one(bricks))
    print("---Part Two---")
    print(part_two(bricks))