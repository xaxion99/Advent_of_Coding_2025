from aoc25.christmas.helpers.loader import Loader
from typing import List, Tuple


class Day4:
    PAPER_ROLLS_GRID = 'aoc25/resources/paper_rolls_grid.txt'

    def __init__(self, path: str | None = None):
        self._path = path or self.PAPER_ROLLS_GRID
        self._paper_rolls_grid = Loader.load_lines(self._path)

    # ===== Private methods =====

    @staticmethod
    def _find_accessible_paper_rolls(grid: List[str], max_neighbors: int = 3) -> List[Tuple[int, int]]:
        if not grid:
            return []

        rows = len(grid)
        cols = len(grid[0])

        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1),]
        result: List[Tuple[int, int]] = []

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != '@':
                    continue

                same = 0
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if grid[nr][nc] == '@':
                            same += 1

                if same <= max_neighbors:
                    result.append((r, c))

        return result

    def _prune_accessible_paper_rolls(self, grid: List[str], max_neighbors: int = 3) -> int:
        grid_chars: List[List[str]] = [list(row) for row in grid]
        total_removed = 0

        while True:
            current_grid = [''.join(row) for row in grid_chars]
            accessible = self._find_accessible_paper_rolls(grid=current_grid, max_neighbors=max_neighbors)

            if not accessible:
                break

            total_removed += len(accessible)

            for r, c in accessible:
                grid_chars[r][c] = '.'

        return total_removed

    # ===== Public methods =====

    def day_4_run_p1(self) -> int:
        paper_rolls = len(self._find_accessible_paper_rolls(self._paper_rolls_grid))
        print(f'Part 1: Paper Rolls - {paper_rolls}')
        return paper_rolls

    def day_4_run_p2(self) -> int:
        total_removed = self._prune_accessible_paper_rolls(self._paper_rolls_grid)
        print(f'Part 2: Total Removed Paper Rolls - {total_removed}')
        return total_removed
