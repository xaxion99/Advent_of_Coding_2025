from aoc25.christmas.day_1 import Day1
from aoc25.christmas.day_2 import Day2
from aoc25.christmas.day_3 import Day3
from aoc25.christmas.day_4 import Day4
from aoc25.christmas.day_5 import Day5
from aoc25.christmas.day_6 import Day6
from aoc25.christmas.day_7 import Day7
from aoc25.christmas.day_8 import Day8
from aoc25.christmas.day_9 import Day9
from aoc25.christmas.day_10 import Day10
from aoc25.christmas.day_11 import Day11
from aoc25.christmas.day_12 import Day12
import time


def run_with_timing(label: str, func):
    if RUN_TIMES:
        start = time.perf_counter()
        result = func()
        elapsed = time.perf_counter() - start
        print(f"{label} runtime: {elapsed:.6f} seconds")
        return result
    else:
        return func()


def twelve_days_of_christmas():

    day1 = Day1()
    print(f'===== Day 1 =====')
    run_with_timing("Day 1 Part 1", day1.day_1_run_p1)
    run_with_timing("Day 1 Part 2", day1.day_1_run_p2)

    day2 = Day2()
    print(f'===== Day 2 =====')
    run_with_timing("Day 2 Part 1", day2.day_2_run_p1)
    run_with_timing("Day 2 Part 2", day2.day_2_run_p2)

    day3 = Day3()
    print(f'===== Day 3 =====')
    run_with_timing("Day 3 Part 1", day3.day_3_run_p1)
    run_with_timing("Day 3 Part 2", day3.day_3_run_p2)

    day4 = Day4()
    print(f'===== Day 4 =====')
    run_with_timing("Day 4 Part 1", day4.day_4_run_p1)
    run_with_timing("Day 4 Part 2", day4.day_4_run_p2)

    day5 = Day5()
    print(f'===== Day 5 =====')
    run_with_timing("Day 5 Part 1", day5.day_5_run_p1)
    run_with_timing("Day 5 Part 2", day5.day_5_run_p2)

    day6 = Day6()
    print(f'===== Day 6 =====')
    run_with_timing("Day 6 Part 1", day6.day_6_run_p1)
    run_with_timing("Day 6 Part 2", day6.day_6_run_p2)

    day7 = Day7()
    print(f'===== Day 7 =====')
    run_with_timing("Day 7 Part 1", day7.day_7_run_p1)
    run_with_timing("Day 7 Part 2", day7.day_7_run_p2)

    day8 = Day8()
    print(f'===== Day 8 =====')
    run_with_timing("Day 8 Part 1", day8.day_8_run_p1)
    run_with_timing("Day 8 Part 2", day8.day_8_run_p2)

    day9 = Day9()
    print(f'===== Day 9 =====')
    run_with_timing("Day 9 Part 1", day9.day_9_run_p1)
    run_with_timing("Day 9 Part 2", day9.day_9_run_p2)

    day10 = Day10()
    print(f'===== Day 10 =====')
    run_with_timing("Day 10 Part 1", day10.day_10_run_p1)
    run_with_timing("Day 10 Part 2", day10.day_10_run_p2)

    # day11 = Day11()
    # print(f'===== Day 11 =====')
    # run_with_timing("Day 11 Part 1", day11.day_11_run_p1)
    # run_with_timing("Day 11 Part 2", day11.day_11_run_p2)

    # day12 = Day12()
    # print(f'===== Day 12 =====')
    # run_with_timing("Day 12 Part 1", day12.day_12_run_p1)
    # run_with_timing("Day 12 Part 2", day12.day_12_run_p2)


if __name__ == '__main__':
    RUN_TIMES = True
    run_with_timing("Overall runtime", twelve_days_of_christmas)
