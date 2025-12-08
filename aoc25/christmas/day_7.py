from aoc25.christmas.helpers.loader import Loader
from collections import deque
from typing import List


class Day7:
    TACHYON_MANIFOLD_DIAGRAM = 'aoc25/resources/tachyon_manifold_diagram.txt'

    def __init__(self, path: str | None = None):
        self._path = path or self.TACHYON_MANIFOLD_DIAGRAM
        self._tachyon_manifold_diagram = Loader.load_lines(self._path)

    # ===== Private methods =====

    @staticmethod
    def _count_splits_in_manifold(lines: List[str]) -> int:
        if not lines:
            return 0

        height = len(lines)
        width = max(len(line) for line in lines)
        grid = [list(line.ljust(width, ".")) for line in lines]

        start_row = start_col = None
        for r in range(height):
            for c in range(width):
                if grid[r][c] == "S":
                    start_row, start_col = r, c
                    break
            if start_row is not None:
                break

        if start_row is None:
            raise ValueError("No starting point 'S' found in tachyon manifold.")

        queue = deque()
        queue.append((start_row, start_col))

        visited: set[tuple[int, int]] = set()
        split_count = 0

        while queue:
            r, c = queue.popleft()

            if r < 0 or r >= height or c < 0 or c >= width:
                continue

            if (r, c) in visited:
                continue
            visited.add((r, c))

            ch = grid[r][c]

            if ch == "^":
                split_count += 1

                queue.append((r, c - 1))
                queue.append((r, c + 1))

                continue

            queue.append((r + 1, c))

        return split_count

    @staticmethod
    def _count_timelines_in_quantum_manifold(lines: List[str]) -> int:
        if not lines:
            return 0

        height = len(lines)
        width = max(len(line) for line in lines)
        grid = [list(line.ljust(width, ".")) for line in lines]

        start_row = start_col = None
        for r in range(height):
            for c in range(width):
                if grid[r][c] == "S":
                    start_row, start_col = r, c
                    break
            if start_row is not None:
                break

        if start_row is None:
            raise ValueError("No starting point 'S' found in tachyon manifold.")

        frontier: dict[tuple[int, int], int] = {(start_row, start_col): 1}
        total_timelines = 0

        while frontier:
            next_frontier: dict[tuple[int, int], int] = {}

            for (r, c), count in frontier.items():
                ch = grid[r][c]

                if ch == "^":
                    for dc in (-1, +1):
                        nc = c + dc
                        if nc < 0 or nc >= width:
                            total_timelines += count
                        else:
                            key = (r, nc)
                            next_frontier[key] = next_frontier.get(key, 0) + count
                else:
                    nr = r + 1
                    if nr >= height:
                        total_timelines += count
                    else:
                        key = (nr, c)
                        next_frontier[key] = next_frontier.get(key, 0) + count

            frontier = next_frontier

        return total_timelines

    # ===== Public methods =====

    def day_7_run_p1(self) -> int:
        splits = self._count_splits_in_manifold(self._tachyon_manifold_diagram)
        print(f"Part 1: Beam is split {splits} times.")
        return splits

    def day_7_run_p2(self):
        timelines = self._count_timelines_in_quantum_manifold(self._tachyon_manifold_diagram)
        print(f"Part 2: Quantum tachyon particle ends up on {timelines} timelines.")
        return timelines
