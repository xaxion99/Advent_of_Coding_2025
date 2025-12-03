from aoc25.christmas.helpers.loader import Loader


class Day3:
    BATTERY_BANKS = 'aoc25/resources/battery_banks.txt'

    def __init__(self, path: str | None = None):
        self._path = path or self.BATTERY_BANKS
        self._battery_banks = Loader.load_lines(self._path)

    # ===== Private methods =====
    @staticmethod
    def _max_joltage(row: str, k: int) -> int:
        digits = [int(c) for c in row]
        stack = []
        n = len(digits)

        for i, d in enumerate(digits):
            while (
                    stack
                    and d > stack[-1]
                    and (len(stack) - 1 + (n - i)) >= k
            ):
                stack.pop()

            stack.append(d)

        chosen = stack[:k]

        val = 0
        for d in chosen:
            val = val * 10 + d
        return val

    def _find_max_joltages(self, rows: list[str], k: int) -> list[int]:
        return [self._max_joltage(row, k) for row in rows]

    # ===== Public methods =====

    def day_3_run_p1(self):
        max_joltages = self._find_max_joltages(self._battery_banks, 2)
        total_joltage = sum(max_joltages)
        print(f'Part 1: Total Joltage - {total_joltage}')

    def day_3_run_p2(self):
        max_joltages = self._find_max_joltages(self._battery_banks, 12)
        total_joltage = sum(max_joltages)
        print(f'Part 2: Total Joltage - {total_joltage}')
