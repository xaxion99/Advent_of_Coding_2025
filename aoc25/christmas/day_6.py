from aoc25.christmas.helpers.loader import Loader
from typing import List


class Day6:
    MATH_HOMEWORK = 'aoc25/resources/cephalopod_homework.txt'

    def __init__(self, path: str | None = None):
        self._path = path or self.MATH_HOMEWORK
        self._math_homework_lines = Loader.load_lines(self._path)
        self._math_homework = [line.split() for line in self._math_homework_lines]

    # ===== Private methods =====

    @staticmethod
    def _complete_homework(data: List[List[str]]) -> List[int]:
        results = []
        rows = len(data) - 1
        ops_row = data[-1]

        cols = len(data[0])

        for c in range(cols):
            op = ops_row[c]
            if op == '*':
                val = 1
                for r in range(rows):
                    val *= int(data[r][c])
            elif op == '+':
                val = 0
                for r in range(rows):
                    val += int(data[r][c])
            else:
                raise ValueError(f"Unknown operator {op}")

            results.append(val)

        return results

    @staticmethod
    def _split_into_bands(lines: List[str]) -> List[tuple[int, int, str]]:
        if not lines:
            return []

        ops_line = lines[-1]
        num_rows = len(lines) - 1
        width = len(ops_line)

        last_used = -1
        for c in range(width):
            if ops_line[c] in ("*", "+"):
                last_used = c
            else:
                for r in range(num_rows):
                    if lines[r][c].isdigit():
                        last_used = c
                        break

        if last_used == -1:
            return []

        width = last_used + 1

        def is_separator(col: int) -> bool:
            if ops_line[col] in ("*", "+"):
                return False
            for r in range(num_rows):
                if not lines[r][col].isspace():
                    return False
            return True

        bands: List[tuple[int, int, str]] = []
        col = 0

        while col < width:
            while col < width and is_separator(col):
                col += 1
            if col >= width:
                break

            start = col
            while col < width and not is_separator(col):
                col += 1
            end = col

            op_char = None
            for c in range(start, end):
                if ops_line[c] in ("*", "+"):
                    op_char = ops_line[c]
                    break

            if op_char is None:
                continue

            bands.append((start, end, op_char))

        return bands

    @staticmethod
    def _rechunk_band(band_rows: List[str]) -> List[int]:
        if not band_rows:
            return []

        width = len(band_rows[0])
        for i in range(1, len(band_rows)):
            if len(band_rows[i]) < width:
                band_rows[i] = band_rows[i].ljust(width)

        new_nums: List[int] = []

        for col in range(width - 1, -1, -1):
            digits = "".join(
                row[col] for row in band_rows
                if row[col].isdigit()
            )
            if digits:
                new_nums.append(int(digits))

        return new_nums

    def _complete_homework_in_cephalopod(self, lines: List[str]) -> List[int]:
        if not lines:
            return []

        max_width = max(len(line) for line in lines)
        norm_lines = [line.ljust(max_width) for line in lines]

        bands = self._split_into_bands(norm_lines)
        if not bands:
            return []

        num_rows = len(norm_lines) - 1
        results: List[int] = []

        for start_col, end_col, op_char in bands:
            band_rows = [
                norm_lines[r][start_col:end_col]
                for r in range(num_rows)
            ]

            new_nums = self._rechunk_band(band_rows)

            if not new_nums:
                results.append(0)
                continue

            if op_char == "*":
                acc = 1
                for v in new_nums:
                    acc *= v
            elif op_char == "+":
                acc = sum(new_nums)
            else:
                raise ValueError(f"Unknown operator {op_char!r}")

            results.append(acc)

        return results

    # ===== Public methods =====

    def day_6_run_p1(self) -> int:
        answers = self._complete_homework(self._math_homework)
        total = sum(answers)
        print(f'Part 1: Answers Total - {total}')
        return total

    def day_6_run_p2(self) -> int:
        answers = self._complete_homework_in_cephalopod(self._math_homework_lines)
        total = sum(answers)
        print(f"Part 2: Answers Total - {total}")
        return total
