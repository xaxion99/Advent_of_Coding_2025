from aoc25.christmas.helpers.loader import Loader


class Day1:
    SAFE_ROTATIONS = 'aoc25/resources/safe_rotations.txt'

    def __init__(self, path: str | None = None, start: int = 50, size: int = 100):
        self._path = path or self.SAFE_ROTATIONS
        self._start = start
        self._size = size
        self._rotations = Loader.load_lines(self._path)

    # ===== Private methods =====

    def _step(self, pos: int, direction: str) -> int:
        if direction == 'R':
            return (pos + 1) % self._size
        elif direction == 'L':
            return (pos - 1) % self._size
        else:
            raise ValueError(f"Invalid rotation direction: {direction}")

    def _simulate(self, track_zero_passes: bool = False):
        pos = self._start
        results = []
        zero_passes = 0

        for rot in self._rotations:
            direction = rot[0]
            amount = int(rot[1:])

            for _ in range(amount):
                pos = self._step(pos, direction)
                if track_zero_passes and pos == 0:
                    zero_passes += 1

            results.append(pos)

        return results, zero_passes

    def _count_zero_landings(self):
        landings, _ = self._simulate(track_zero_passes=False)
        return landings

    def _count_zero_passes(self):
        _, zero_passes = self._simulate(track_zero_passes=True)
        return zero_passes

    # ===== Public methods =====

    def day_1_run_p1(self) -> int:
        landings = self._count_zero_landings()
        zero_count = landings.count(0)
        print(f'Part 1: Zero Count - {zero_count}')
        return zero_count

    def day_1_run_p2(self) -> int:
        zero_passes = self._count_zero_passes()
        print(f'Part 2: Zero Passes Count - {zero_passes}')
        return zero_passes
