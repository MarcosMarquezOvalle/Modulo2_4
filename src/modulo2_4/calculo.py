from __future__ import annotations

import cProfile
import math
from concurrent.futures import as_completed
from concurrent.futures import ProcessPoolExecutor


def heavy_computation(n: int) -> int:
    result = 0
    result = sum(math.sqrt(i) for i in range(n))
    return result


def run_with_map(numbers):
    with ProcessPoolExecutor() as executor:
        results = executor.map(heavy_computation, numbers)
        for num, res in zip(numbers, results):
            print(f"Input {num} -> Result: {res}")


def run_with_submit(numbers):
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(heavy_computation, n): n for n in numbers}

        for future in as_completed(futures):
            num = futures[future]
            try:
                res = future.result()
                print(f"Input {num} -> Result: {res}")
            except Exception as e:
                print(f"Task for {num} raised an exception: {e}")


if __name__ == "__main__":
    input_data = [15_000_000, 16_000_000, 17_000_000, 18_000_000]

    cProfile.run("run_with_map(input_data)")
    cProfile.run("run_with_submit(input_data)")
