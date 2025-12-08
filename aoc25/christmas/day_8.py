from aoc25.christmas.helpers.loader import Loader
from collections import defaultdict
from math import prod
from typing import List, Tuple, Optional


class Day8:
    JUNCTION_BOX_COORDINATES = 'aoc25/resources/junction_box_coordinates.txt'

    def __init__(self, path: str | None = None):
        self._path = path or self.JUNCTION_BOX_COORDINATES
        self._junction_box_coordinates = Loader.load_lines(self._path)

    # ===== Private methods =====

    @staticmethod
    def _parse_junction_points(lines: List[str]) -> List[tuple[int, int, int]]:
        points: List[tuple[int, int, int]] = []
        for line in lines:
            x_str, y_str, z_str = line.split(",")
            points.append((int(x_str), int(y_str), int(z_str)))
        return points

    @staticmethod
    def _build_sorted_distance_pairs(points: List[tuple[int, int, int]]) -> List[tuple[int, int, int]]:
        pairs: List[tuple[int, int, int]] = []
        n = len(points)

        for i in range(n):
            x1, y1, z1 = points[i]
            for j in range(i + 1, n):
                x2, y2, z2 = points[j]
                dx = x1 - x2
                dy = y1 - y2
                dz = z1 - z2
                dist2 = dx * dx + dy * dy + dz * dz
                pairs.append((dist2, i, j))

        pairs.sort(key=lambda p: p[0])
        return pairs

    @staticmethod
    def _run_union_find(n: int, pairs: List[Tuple[int, int, int]], max_connections: Optional[int] = None, stop_when_single_circuit: bool = False) -> Tuple[List[int], Optional[Tuple[int, int]]]:
        if n == 0:
            return [], None

        parent = list(range(n))
        size = [1] * n
        components = n
        last_merge: Optional[Tuple[int, int]] = None

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int) -> bool:
            nonlocal components, last_merge
            ra, rb = find(a), find(b)
            if ra == rb:
                return False
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]
            components -= 1
            last_merge = (a, b)
            return True

        limit = len(pairs) if max_connections is None else min(max_connections, len(pairs))

        for idx in range(limit):
            _, i, j = pairs[idx]
            merged = union(i, j)
            if stop_when_single_circuit and merged and components == 1:
                break

        counts = defaultdict(int)
        for i in range(n):
            counts[find(i)] += 1

        sizes_desc = sorted(counts.values(), reverse=True)
        return sizes_desc, last_merge

    def _prepare_points_and_pairs(self, lines: List[str]) -> Tuple[int, List[Tuple[int, int, int]], List[Tuple[int, int, int]]]:
        if not lines:
            return 0, [], []

        points = self._parse_junction_points(lines)
        n = len(points)
        if n <= 1:
            return n, points, []

        pairs = self._build_sorted_distance_pairs(points)
        return n, points, pairs

    def _union_and_count_circuits(self, n: int, pairs: List[Tuple[int, int, int]], connections_to_consider: int) -> List[int]:
        sizes, _ = self._run_union_find(n=n, pairs=pairs, max_connections=connections_to_consider, stop_when_single_circuit=False)
        return sizes

    def _calculate_circuit_product(self, lines: List[str], connections_to_consider: int = 1000) -> int:
        n, points, pairs = self._prepare_points_and_pairs(lines)
        if n <= 1:
            return 0

        sizes = self._union_and_count_circuits(n, pairs, connections_to_consider)
        top_three = sizes[:3]
        return prod(top_three) if top_three else 0

    def _find_last_connection_x_product(self, lines: List[str]) -> int:
        n, points, pairs = self._prepare_points_and_pairs(lines)
        if n <= 1:
            return 0

        _, last_merge = self._run_union_find(n=n, pairs=pairs, max_connections=None, stop_when_single_circuit=True)
        if last_merge is None:
            return 0

        i, j = last_merge
        x1 = points[i][0]
        x2 = points[j][0]
        return x1 * x2

    # ===== Public methods =====

    def day_8_run_p1(self) -> int:
        circuit_product = self._calculate_circuit_product(self._junction_box_coordinates)
        print(f"Part 1: Product of three largest circuits is {circuit_product}.")
        return circuit_product

    def day_8_run_p2(self) -> int:
        final_product = self._find_last_connection_x_product(self._junction_box_coordinates)
        print(f"Part 2: Product of X coordinates of the final connection is {final_product}.")
        return final_product
