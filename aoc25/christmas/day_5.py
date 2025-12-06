from aoc25.christmas.helpers.loader import Loader
from typing import List


class Day5:
    INGREDIENT_IDS = 'aoc25/resources/ingredient_ids.txt'
    INGREDIENT_ID_RANGES = 'aoc25/resources/ingredient_id_ranges.txt'

    def __init__(self, path_1: str | None = None, path_2: str | None = None):
        self._path_1 = path_1 or self.INGREDIENT_ID_RANGES
        self._ingredient_id_ranges = Loader.load_lines(self._path_1)
        self._path_2 = path_2 or self.INGREDIENT_IDS
        self._ingredient_ids = Loader.load_lines(self._path_2)

    # ===== Private methods =====

    @staticmethod
    def _is_ingredient_fresh(ranges: List[str], values: List[str]) -> List[bool]:
        parsed_ranges = []
        for r in ranges:
            start_str, end_str = r.split('-')
            parsed_ranges.append((int(start_str), int(end_str)))

        results = []
        for v in values:
            n = int(v)
            found = any(start <= n <= end for start, end in parsed_ranges)
            results.append(found)

        return results

    @staticmethod
    def _count_fresh_values(ranges: List[str]) -> int:
        if not ranges:
            return 0

        intervals = []
        for r in ranges:
            start_str, end_str = r.split('-')
            start = int(start_str)
            end = int(end_str)
            intervals.append((start, end))

        intervals.sort(key=lambda x: x[0])

        total = 0
        cur_start, cur_end = intervals[0]

        for start, end in intervals[1:]:
            if start <= cur_end + 1:
                cur_end = max(cur_end, end)
            else:
                total += (cur_end - cur_start + 1)
                cur_start, cur_end = start, end

        total += (cur_end - cur_start + 1)

        return total

    # ===== Public methods =====

    def day_5_run_p1(self) -> int:
        ingredient_freshnesses = self._is_ingredient_fresh(self._ingredient_id_ranges, self._ingredient_ids)
        fresh_count = sum(ingredient_freshnesses)
        print(f'Part 1: Fresh Ingredients - {fresh_count}')
        return fresh_count

    def day_5_run_p2(self) -> int:
        fresh_value_count = self._count_fresh_values(self._ingredient_id_ranges)
        print(f'Part 2: Fresh Ingredient ID Values - {fresh_value_count}')
        return fresh_value_count
