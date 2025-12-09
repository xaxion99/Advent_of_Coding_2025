from aoc25.christmas.helpers.loader import Loader


class Day10:
    PLACEHOLDER = 'aoc25/resources/placeholder.txt'

    def __init__(self, path: str | None = None):
        self._path = path or self.PLACEHOLDER
        self._placeholder = Loader.load_lines(self._path)

    # ===== Private methods =====



    # ===== Public methods =====

    def day_10_run_p1(self) -> int:
        pass

    def day_10_run_p2(self) -> int:
        pass