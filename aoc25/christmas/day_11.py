from aoc25.christmas.helpers.loader import Loader
from typing import Dict, List, Set, Tuple


class Day11:
    DEVICES_WITH_OUTPUTS = 'aoc25/resources/devices_with_outputs.txt'

    def __init__(self, path: str | None = None):
        self._path = path or self.DEVICES_WITH_OUTPUTS
        self._devices_with_outputs = Loader.load_lines(self._path)

    # ===== Private methods =====

    @staticmethod
    def _parse_devices(lines: List[str]) -> Dict[str, List[str]]:
        graph: Dict[str, List[str]] = {}
        for line in lines:
            line = line.strip()
            if not line:
                continue
            name, rhs = line.split(":")
            name = name.strip()
            targets = rhs.strip().split()
            graph[name] = targets
        return graph

    @staticmethod
    def _count_paths(graph: Dict[str, List[str]], start: str, target: str = "out") -> int:
        memo: Dict[str, int] = {}
        visiting: Set[str] = set()

        def dfs(node: str) -> int:
            if node == target:
                return 1
            if node in memo:
                return memo[node]
            if node in visiting:
                raise ValueError("Cycle detected in device graph")
            visiting.add(node)
            total = 0
            for nxt in graph.get(node, []):
                total += dfs(nxt)
            visiting.remove(node)
            memo[node] = total
            return total

        return dfs(start)

    @staticmethod
    def _count_paths_with_required(
        graph: Dict[str, List[str]],
        start: str,
        target: str,
        required: Set[str],
    ) -> int:
        req_list = list(required)
        req_index: Dict[str, int] = {name: i for i, name in enumerate(req_list)}
        full_mask = (1 << len(req_list)) - 1

        memo: Dict[Tuple[str, int], int] = {}
        visiting: Set[str] = set()

        def dfs(node: str, mask: int) -> int:
            key = (node, mask)
            if key in memo:
                return memo[key]
            if node in visiting:
                raise ValueError("Cycle detected in device graph")
            new_mask = mask
            if node in req_index:
                new_mask |= 1 << req_index[node]
            if node == target:
                result = 1 if new_mask == full_mask else 0
                memo[key] = result
                return result
            visiting.add(node)
            total = 0
            for nxt in graph.get(node, []):
                total += dfs(nxt, new_mask)
            visiting.remove(node)
            memo[key] = total
            return total

        return dfs(start, 0)

    def number_of_paths_to_out_p1(self, lines: List[str]) -> int:
        graph = self._parse_devices(lines)
        return self._count_paths(graph, "you", "out")

    def number_of_paths_to_out_p2(self, lines: List[str]) -> int:
        graph = self._parse_devices(lines)
        required = {"fft", "dac"}
        return self._count_paths_with_required(graph, "svr", "out", required)

    # ===== Public methods =====

    def day_11_run_p1(self) -> int:
        total_paths = self.number_of_paths_to_out_p1(self._devices_with_outputs)
        print(f"Part 1: Number of paths from 'you' to 'out' is {total_paths}.")
        return total_paths

    def day_11_run_p2(self) -> int:
        total_paths = self.number_of_paths_to_out_p2(self._devices_with_outputs)
        print(f"Part 2: Number of paths from 'svr' to 'out' through both 'fft' and 'dac' is {total_paths}.")
        return total_paths
