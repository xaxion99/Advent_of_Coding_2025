from aoc25.christmas.helpers.loader import Loader
from typing import List, Tuple
import re


class Day12:
    PRESENT_SITUATION_DOC = 'aoc25/resources/present_situation_doc.txt'

    def __init__(self, path: str | None = None):
        self._path = path or self.PRESENT_SITUATION_DOC
        self._present_situation_doc = Loader.load_lines(self._path)

    # ===== Private methods =====

    @staticmethod
    def _parse_input(lines: List[str]) -> Tuple[List[List[str]], List[Tuple[int, int, List[int]]]]:
        shape_header_re = re.compile(r'^(\d+):\s*$')
        region_re = re.compile(r'^(\d+)x(\d+):\s*(.*)$')

        shapes: List[List[str]] = []
        regions: List[Tuple[int, int, List[int]]] = []

        n = len(lines)
        i = 0

        while i < n:
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            m_region = region_re.match(line)
            if m_region:
                break
            m_shape = shape_header_re.match(line)
            if not m_shape:
                break
            i += 1
            grid: List[str] = []
            while i < n:
                raw = lines[i].rstrip("\n")
                s = raw.strip()
                if not s:
                    i += 1
                    if grid:
                        break
                    continue
                if shape_header_re.match(s) or region_re.match(s):
                    break
                grid.append(raw)
                i += 1
            shapes.append(grid)

        while i < n:
            line = lines[i].strip()
            i += 1
            if not line:
                continue
            m_region = region_re.match(line)
            if not m_region:
                continue
            w = int(m_region.group(1))
            h = int(m_region.group(2))
            rest = m_region.group(3).strip()
            counts = [int(x) for x in rest.split()] if rest else []
            regions.append((w, h, counts))

        return shapes, regions

    @staticmethod
    def _shape_areas(shapes: List[List[str]]) -> List[int]:
        areas: List[int] = []
        for grid in shapes:
            area = 0
            for row in grid:
                area += sum(1 for ch in row if ch == '#')
            areas.append(area)
        return areas

    @staticmethod
    def _region_can_fit_by_area(width: int, height: int, areas: List[int], counts: List[int]) -> bool:
        region_area = width * height
        presents_area = sum(a * c for a, c in zip(areas, counts))
        return presents_area <= region_area

    def christmas_trees_full_of_presents(self, lines: List[str]) -> int:
        shapes, regions = self._parse_input(lines)
        areas = self._shape_areas(shapes)
        count = 0
        for w, h, counts in regions:
            if self._region_can_fit_by_area(w, h, areas, counts):
                count += 1
        return count

    # ===== Public methods =====

    def day_12_run_p1(self) -> int:
        trees = self.christmas_trees_full_of_presents(self._present_situation_doc)
        print(f"Part 1: Number of Christmas trees that can fit all presents is {trees}.")
        return trees

    def day_12_run_p2(self) -> int:
        pass
