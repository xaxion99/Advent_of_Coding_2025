from aoc25.christmas.helpers.loader import Loader
from collections import deque
from fractions import Fraction
from itertools import product
import re
from typing import List, Tuple


class Day10:
    FACTORY_MACHINES_MANUAL = 'aoc25/resources/factory_machines_manual.txt'

    def __init__(self, path: str | None = None):
        self._path = path or self.FACTORY_MACHINES_MANUAL
        self._factory_machines_manual = Loader.load_lines(self._path)

    # ===== Private methods =====

    @staticmethod
    def _parse_manual(lines: List[str]) -> List[Tuple[str, List[Tuple[int, ...]], List[int]]]:
        results = []
        for line in lines:
            indicator_lights = re.search(r'\[(.*?)]', line).group(1)

            schematics = re.findall(r'\((.*?)\)', line)
            button_wiring_schematics: List[Tuple[int, ...]] = []
            for p in schematics:
                if p.strip() == "":
                    button_wiring_schematics.append(())
                else:
                    button_wiring_schematics.append(tuple(int(x) for x in p.split(",")))

            j = re.search(r'\{(.*?)}', line).group(1)
            joltages = [int(x) for x in j.split(",")]

            results.append((indicator_lights, button_wiring_schematics, joltages))

        return results

    @staticmethod
    def _min_presses(pattern: str, button_groups: List[Tuple[int, ...]]) -> int:
        n = len(pattern)
        target = 0
        for i, ch in enumerate(pattern):
            if ch == '#':
                target |= 1 << i
        if target == 0:
            return 0
        btn_masks = []
        for group in button_groups:
            mask = 0
            for idx in group:
                mask |= 1 << idx
            btn_masks.append(mask)
        max_state = 1 << n
        dist = [-1] * max_state
        start = 0
        dist[start] = 0
        q = deque([start])
        while q:
            s = q.popleft()
            d = dist[s]
            for mask in btn_masks:
                ns = s ^ mask
                if dist[ns] == -1:
                    nd = d + 1
                    dist[ns] = nd
                    if ns == target:
                        return nd
                    q.append(ns)
        raise ValueError("Unreachable light configuration")

    @staticmethod
    def _build_joltage_system(buttons: List[Tuple[int, ...]], joltages: List[int]):
        n = len(joltages)
        m = len(buttons)
        A: List[List[Fraction]] = []
        for j in range(n):
            row = [0] * m
            for i, b in enumerate(buttons):
                if j in b:
                    row[i] = 1
            row.append(joltages[j])
            A.append([Fraction(x) for x in row])
        return A

    @staticmethod
    def _rref(A: List[List[Fraction]]):
        nrows = len(A)
        if nrows == 0:
            return A, [], 0
        ncols = len(A[0])
        m = ncols - 1
        pivots = [-1] * m
        row = 0
        for col in range(m):
            pivot = None
            for r in range(row, nrows):
                if A[r][col] != 0:
                    pivot = r
                    break
            if pivot is None:
                continue
            A[row], A[pivot] = A[pivot], A[row]
            f = A[row][col]
            for c in range(col, ncols):
                A[row][c] /= f
            for r in range(nrows):
                if r != row and A[r][col] != 0:
                    factor = A[r][col]
                    for c in range(col, ncols):
                        A[r][c] -= factor * A[row][c]
            pivots[col] = row
            row += 1
            if row == nrows:
                break
        rank = sum(1 for p in pivots if p != -1)
        return A, pivots, rank

    @staticmethod
    def _min_presses_joltage(buttons: List[Tuple[int, ...]], joltages: List[int]) -> int:
        n = len(joltages)
        m = len(buttons)
        if n == 0:
            return 0
        A = Day10._build_joltage_system(buttons, joltages)
        A, pivots, rank = Day10._rref(A)
        mcols = m

        for r in range(n):
            if all(A[r][c] == 0 for c in range(mcols)) and A[r][mcols] != 0:
                raise ValueError("Unsolvable joltage configuration")

        ub: List[int] = []
        total_j = sum(joltages)
        for i, b in enumerate(buttons):
            if not b:
                ub.append(0)
            else:
                v = min(joltages[j] for j in b)
                if v > total_j:
                    v = total_j
                ub.append(v)

        if rank == mcols:
            x: List[Fraction] = [Fraction(0)] * mcols
            for col, row in enumerate(pivots):
                if row != -1:
                    x[col] = A[row][mcols]
            vals: List[int] = []
            for v in x:
                if v < 0 or v.denominator != 1:
                    raise ValueError("Unsolvable joltage configuration")
                vals.append(int(v))
            return sum(vals)

        free_cols = [i for i in range(mcols) if pivots[i] == -1]
        ranges = [range(0, ub[c] + 1) for c in free_cols]
        best: int | None = None

        for choice in product(*ranges):
            x: List[Fraction] = [Fraction(0)] * mcols
            for col, v in zip(free_cols, choice):
                x[col] = Fraction(v)

            feasible = True
            for col, row in enumerate(pivots):
                if row == -1:
                    continue
                rhs = A[row][mcols]
                for c in free_cols:
                    rhs -= A[row][c] * x[c]
                if rhs < 0:
                    feasible = False
                    break
                x[col] = rhs
            if not feasible:
                continue

            total = 0
            ok = True
            for i, v in enumerate(x):
                if v < 0 or v.denominator != 1:
                    ok = False
                    break
                iv = int(v)
                if iv > ub[i]:
                    ok = False
                    break
                total += iv
            if not ok:
                continue
            if best is None or total < best:
                best = total

        if best is None:
            raise ValueError("Unsolvable joltage configuration")
        return best

    def least_button_presses_p1(self, lines: List[str]) -> int:
        manual = self._parse_manual(lines)
        results: List[int] = []
        for light_pattern, buttons, _ in manual:
            results.append(self._min_presses(light_pattern, buttons))
        return sum(results)

    def least_button_presses_p2(self, lines: List[str]) -> int:
        manual = self._parse_manual(lines)
        results: List[int] = []
        for _, buttons, joltages in manual:
            results.append(self._min_presses_joltage(buttons, joltages))
        return sum(results)

    # ===== Public methods =====

    def day_10_run_p1(self) -> int:
        sum_of_button_presses = self.least_button_presses_p1(self._factory_machines_manual)
        print(f"Part 1: Sum of least button presses is {sum_of_button_presses}.")
        return sum_of_button_presses

    def day_10_run_p2(self) -> int:
        sum_of_button_presses = self.least_button_presses_p2(self._factory_machines_manual)
        print(f"Part 2: Sum of least button presses is {sum_of_button_presses}.")
        return sum_of_button_presses
