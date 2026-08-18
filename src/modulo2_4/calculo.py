import time
import math
from concurrent.futures import ProcessPoolExecutor, as_completed
import cProfile

def heavy_computation(n: int) -> int:
    """A CPU-bound function that heavily uses the processor."""
    result = 0
    result = sum(math.sqrt(i) for i in range(n))
    return result

def run_with_map(numbers):
    """Pattern 1: Simple and preserves input order."""
    print("--- Using executor.map() ---")
    with ProcessPoolExecutor() as executor:
        # map handles the input iterable directly
        results = executor.map(heavy_computation, numbers)
        for num, res in zip(numbers, results):
            print(f"Input {num} -> Result: {res}")

def run_with_submit(numbers):
    """Pattern 2: Granular control; processes results as they finish."""
    print("\n--- Using executor.submit() ---")
    with ProcessPoolExecutor() as executor:
        # submit returns a Future object immediately
        futures = {executor.submit(heavy_computation, n): n for n in numbers}
        
        # as_completed yields futures the moment they finish
        for future in as_completed(futures):
            num = futures[future]
            try:
                res = future.result()
                print(f"Input {num} -> Result: {res}")
            except Exception as e:
                print(f"Task for {num} raised an exception: {e}")

if __name__ == "__main__":
    # Crucial protection guard for multiprocessing
    input_data = [15_000_000, 16_000_000, 17_000_000, 18_000_000]
    
    #start_time = time.perf_counter()
    cProfile.run('run_with_map(input_data)')
    #run_with_map(input_data)
    #print(f"\nTotal elapsed time: {time.perf_counter() - start_time:.2f} seconds")
    #start_time = time.perf_counter()
    #run_with_submit(input_data)
    cProfile.run('run_with_submit(input_data)')
    #print(f"\nTotal elapsed time: {time.perf_counter() - start_time:.2f} seconds")
