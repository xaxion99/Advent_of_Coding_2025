from aoc25.christmas.helpers.loader import Loader
from typing import List, Tuple, Optional


class Day9:
    RED_TILE_COORDINATES = 'aoc25/resources/red_tile_coordinates.txt'

    def __init__(self, path: str | None = None):
        self._path = path or self.RED_TILE_COORDINATES
        self._red_tile_coordinates = Loader.load_lines(self._path)
        self._points: List[tuple[int, int]] = self._parse_red_tile_points(self._red_tile_coordinates)
        self._edges: List[tuple[tuple[int, int], tuple[int, int]]] = self._build_polygon_edges(self._points)

    # ===== Private methods =====

    @staticmethod
    def _parse_red_tile_points(lines: List[str]) -> List[tuple[int, int]]:
        points: List[tuple[int, int]] = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            x_str, y_str = line.split(",")
            points.append((int(x_str), int(y_str)))
        return points

    @staticmethod
    def _rectangle_area(p1: tuple[int, int], p2: tuple[int, int]) -> int:
        x1, y1 = p1
        x2, y2 = p2
        width = abs(x1 - x2) + 1
        height = abs(y1 - y2) + 1
        return width * height

    @staticmethod
    def _build_polygon_edges(points: List[tuple[int, int]]) -> List[tuple[tuple[int, int], tuple[int, int]]]:
        edges: List[tuple[tuple[int, int], tuple[int, int]]] = []
        n = len(points)
        if n < 2:
            return edges

        for i in range(n):
            a = points[i]
            b = points[(i + 1) % n]
            edges.append((a, b))

        return edges

    @staticmethod
    def _point_on_segment(p: tuple[float, float], a: tuple[int, int], b: tuple[int, int]) -> bool:
        x, y = p
        x1, y1 = a
        x2, y2 = b

        if (x2 - x1) * (y - y1) != (y2 - y1) * (x - x1):
            return False

        return min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2)

    @staticmethod
    def _rect_edges_from_corners(p1: tuple[int, int], p2: tuple[int, int]) -> List[tuple[tuple[int, int], tuple[int, int]]]:
        x1, y1 = p1
        x2, y2 = p2

        min_x = min(x1, x2)
        max_x = max(x1, x2)
        min_y = min(y1, y2)
        max_y = max(y1, y2)

        bl = (min_x, min_y)
        br = (max_x, min_y)
        tl = (min_x, max_y)
        tr = (max_x, max_y)

        return [
            (bl, br),
            (br, tr),
            (tr, tl),
            (tl, bl)
        ]

    @staticmethod
    def _segments_cross_strict(a1: tuple[int, int], a2: tuple[int, int], b1: tuple[int, int], b2: tuple[int, int]) -> bool:
        x1, y1 = a1
        x2, y2 = a2
        x3, y3 = b1
        x4, y4 = b2

        if x1 == x2 and y3 == y4:
            vx = x1
            hy = y3
            vy_min, vy_max = sorted((y1, y2))
            hx_min, hx_max = sorted((x3, x4))

            if (hx_min < vx < hx_max) and (vy_min < hy < vy_max):
                return True
            return False

        if y1 == y2 and x3 == x4:
            hy = y1
            vx = x3
            hx_min, hx_max = sorted((x1, x2))
            vy_min, vy_max = sorted((y3, y4))

            if (hx_min < vx < hx_max) and (vy_min < hy < vy_max):
                return True
            return False

        return False

    def _is_inside_polygon(self, point: tuple[float, float], points: List[tuple[int, int]]) -> bool:
        x, y = point
        n = len(points)
        if n < 3:
            return False

        for i in range(n):
            a = points[i]
            b = points[(i + 1) % n]
            if self._point_on_segment(point, a, b):
                return True

        inside = False
        for i in range(n):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % n]

            if (y1 > y) != (y2 > y):
                x_intersect = x1 + (x2 - x1) * (y - y1) / (y2 - y1)
                if x_intersect > x:
                    inside = not inside

        return inside

    def _rectangle_inside_polygon(self, p1: tuple[int, int], p2: tuple[int, int]) -> bool:
        x1, y1 = p1
        x2, y2 = p2

        min_x = min(x1, x2)
        max_x = max(x1, x2)
        min_y = min(y1, y2)
        max_y = max(y1, y2)

        bl = (min_x, min_y)
        br = (max_x, min_y)
        tl = (min_x, max_y)
        tr = (max_x, max_y)

        corners = (bl, br, tl, tr)
        for c in corners:
            if not self._is_inside_polygon(c, self._points):
                return False

        rect_edges = self._rect_edges_from_corners(p1, p2)

        for e1 in self._edges:
            for e2 in rect_edges:
                if self._segments_cross_strict(e1[0], e1[1], e2[0], e2[1]):
                    return False

        return True

    def _find_max_area_rectangle(self) -> int:
        points = self._points
        n = len(points)
        if n <= 1:
            return 0

        max_area = 0

        for i in range(n):
            for j in range(i + 1, n):
                p1 = points[i]
                p2 = points[j]

                if p1[0] == p2[0] or p1[1] == p2[1]:
                    continue

                area = self._rectangle_area(p1, p2)
                if area > max_area:
                    max_area = area

        return max_area

    def _find_max_area_rectangle_red_green(self) -> int:
        points = self._points
        n = len(points)
        if n <= 1:
            return 0

        max_area = 0

        for i in range(n):
            for j in range(i + 1, n):
                p1 = points[i]
                p2 = points[j]

                if p1[0] == p2[0] or p1[1] == p2[1]:
                    continue

                area = self._rectangle_area(p1, p2)

                if area <= max_area:
                    continue

                if self._rectangle_inside_polygon(p1, p2):
                    max_area = area

        return max_area

    # ===== Public methods =====

    def day_9_run_p1(self) -> int:
        max_area = self._find_max_area_rectangle()
        print(f"Part 1: Largest rectangle area is {max_area}.")
        return max_area

    def day_9_run_p2(self) -> int:
        max_area = self._find_max_area_rectangle_red_green()
        print(f"Part 2: Largest rectangle area using only red and green tiles is {max_area}.")
        return max_area
