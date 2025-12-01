SAFE_ROTATIONS = 'aoc25/resources/safe_rotations.txt'


# Part 1
def load_rotations(path):
    rotations = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            rotations.append(line)

    return rotations

def apply_rotations(rotations, start=50, size=100):
    pos = start
    results = []

    for rot in rotations:
        direction = rot[0]
        amount = int(rot[1:])

        if direction == 'R':
            pos = (pos + amount) % size
        elif direction == 'L':
            pos = (pos - amount) % size
        else:
            raise ValueError(f"Invalid rotation: {rot}")

        results.append(pos)

    return results


def count_zeros(values):
    return sum(1 for v in values if v == 0)


def day_1_run_p1():
    rotations = load_rotations(SAFE_ROTATIONS)
    results = apply_rotations(rotations)
    count = count_zeros(results)
    print(count)


# Part 2
def count_zero_passes(rotations, start=50, size=100):
    pos = start
    count = 0

    for rot in rotations:
        direction = rot[0]
        amount = int(rot[1:])

        for _ in range(amount):
            if direction == 'R':
                pos = (pos + 1) % size
            else:
                pos = (pos - 1) % size

            if pos == 0:
                count += 1

    return count


def day_1_run_p2():
    rotations = load_rotations(SAFE_ROTATIONS)
    zero_passes = count_zero_passes(rotations)
    print(zero_passes)
