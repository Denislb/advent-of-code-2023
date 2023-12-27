from sympy import symbols, Eq, solve


def parse_input(filename):
    datas = {}
    with open(filename) as f:
        for line in f:
            splitted = line.strip().split('@')
            datas[tuple([int(x) for x in splitted[0].strip().split(', ')])] = tuple([int(x) for x in splitted[1].strip().split(', ')])
    return datas

def calc_intersection(position_1, vector_1, position_2, vector_2, mini, maxi):
    x1, y1, z1 = position_1
    x2, y2, z2 = position_2

    m1 = vector_1[1] / vector_1[0]
    m2 = vector_2[1] / vector_2[0]
    b1 = y1 - (m1 * x1)
    b2 = y2 - (m2 * x2)

    if (m1 - m2) == 0:
        return False
    x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1
    if mini <= x <= maxi and mini <= y <= maxi:
        if (((x - x1 < 0 and vector_1[0] < 0) or (x - x1 > 0 and vector_1[0] > 0)) and ((x - x2  < 0 and vector_2[0] < 0) or (x - x2 > 0 and vector_2[0] > 0))
                and ((y - y1  < 0 and vector_1[1] < 0) or (y - y1 > 0 and vector_1[1] > 0)) and ((y - y2  < 0 and vector_2[1] < 0) or (y - y2 > 0 and vector_2[1] > 0))):
            return True
    return False


def part_one(datas):
    already_process = set()
    count = 0
    for position, vector in datas.items():
        already_process.add((position, vector))
        for p2, v2 in datas.items():
            if (p2, v2) in already_process:
                continue
            if calc_intersection(position, vector, p2, v2, 200000000000000, 400000000000000):
                count += 1
    return count


def part_two(datas):
    t0, t1, t2, p0x, p0y, p0z, v0x, v0y, v0z = symbols('t0 t1 t2 p0x p0y p0z v0x v0y v0z')
    eq = []
    t = [t0, t1, t2]
    idx = 0
    for position, vector in datas.items():
        x, y, z = position
        vx, vy, vz = vector
        eq.append(Eq(x + t[idx] * vx, p0x + t[idx] * v0x))
        eq.append(Eq(y + t[idx] * vy, p0y + t[idx] * v0y))
        eq.append(Eq(z + t[idx] * vz, p0z + t[idx] * v0z))
        if idx == 2:
            break
        idx += 1
    solutions = solve(eq, [p0x, p0y, p0z, v0x, v0y, v0z, t0, t1, t2])
    return sum(solutions[0][:3])


if __name__ == "__main__":
    input_path = "./day_24/input.txt"
    datas = parse_input(input_path)
    print("---Part One---")
    print(part_one(datas))

    print("---Part Two---")
    print(part_two(datas))