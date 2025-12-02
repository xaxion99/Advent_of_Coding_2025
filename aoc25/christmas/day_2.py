from aoc25.christmas.helpers.loader import Loader


class Day2:
    PRODUCT_ID_RANGES = 'aoc25/resources/product_id_ranges.txt'

    def __init__(self, path: str | None = None):
        self._path = path or self.PRODUCT_ID_RANGES
        self._product_id_ranges = Loader.load_csv_row(self._path)

    # ===== Private methods =====

    @staticmethod
    def _is_pattern_id(n: int, *, min_repeats: int = 2, exact_repeats: int | None = None) -> bool:
        s = str(n)
        length = len(s)

        for sub_len in range(1, length // 2 + 1):
            if length % sub_len != 0:
                continue

            repeats = length // sub_len
            if repeats < min_repeats:
                continue
            if exact_repeats is not None and repeats != exact_repeats:
                continue

            chunk = s[:sub_len]
            if chunk * repeats == s:
                return True

        return False

    @staticmethod
    def _parse_range(range_str: str) -> tuple[int, int]:
        start_str, end_str = range_str.split("-")
        return int(start_str), int(end_str)

    def _invalid_ids_in_range(self, range_str: str, *, part2: bool = False) -> list[int]:
        start, end = self._parse_range(range_str)
        invalids: list[int] = []

        for value in range(start, end + 1):
            if part2:
                if self._is_pattern_id(value):
                    invalids.append(value)
            else:
                if self._is_pattern_id(value, exact_repeats=2):
                    invalids.append(value)

        return invalids

    @staticmethod
    def _sum_invalid_ids(invalid_lists: list[list[int]]) -> int:
        total = 0
        for lst in invalid_lists:
            total += sum(lst)
        return total

    # ===== Public methods =====

    def day_2_run_p1(self):
        all_invalid: list[list[int]] = []

        for range_str in self._product_id_ranges:
            invalids = self._invalid_ids_in_range(range_str, part2=False)
            all_invalid.append(invalids)

        total_sum = self._sum_invalid_ids(all_invalid)
        print(f'Part 1: Invalid IDs Sum - {total_sum}')
        return total_sum

    def day_2_run_p2(self):
        all_invalid: list[list[int]] = []

        for range_str in self._product_id_ranges:
            invalids = self._invalid_ids_in_range(range_str, part2=True)
            all_invalid.append(invalids)

        total_sum = self._sum_invalid_ids(all_invalid)
        print(f'Part 2: Invalid IDs Sum - {total_sum}')
        return total_sum
