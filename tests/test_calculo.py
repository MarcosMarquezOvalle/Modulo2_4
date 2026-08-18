import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import modulo2_4.calculo as calculo
from modulo2_4.calculo import heavy_computation, run_with_map, run_with_submit


def test_heavy_computation_zero_returns_zero():
    assert heavy_computation(0) == 0


def test_heavy_computation_matches_expected_sum_for_small_value():
    n = 5
    expected = sum(math.sqrt(i) for i in range(n))

    assert math.isclose(heavy_computation(n), expected)


def test_heavy_computation_is_non_negative_for_positive_input():
    result = heavy_computation(10)

    assert result >= 0
    assert math.isfinite(result)


def test_run_with_map_prints_results_in_input_order(monkeypatch, capsys):
    class FakeExecutor:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            return False

        def map(self, func, numbers):
            assert func is calculo.heavy_computation
            return [n * 10 for n in numbers]

    monkeypatch.setattr(calculo, "ProcessPoolExecutor", FakeExecutor)

    run_with_map([1, 2, 3])

    output = capsys.readouterr().out
    assert "--- Using executor.map() ---" in output
    assert "Input 1 -> Result: 10" in output
    assert "Input 2 -> Result: 20" in output
    assert "Input 3 -> Result: 30" in output


def test_run_with_submit_prints_results_as_completed(monkeypatch, capsys):
    class FakeFuture:
        def __init__(self, value):
            self._value = value

        def result(self):
            return self._value

    class FakeExecutor:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            return False

        def submit(self, func, n):
            assert func is calculo.heavy_computation
            return FakeFuture(n * 100)

    monkeypatch.setattr(calculo, "ProcessPoolExecutor", FakeExecutor)
    monkeypatch.setattr(calculo, "as_completed", lambda futures: list(futures.keys()))

    run_with_submit([1, 2])

    output = capsys.readouterr().out
    assert "--- Using executor.submit() ---" in output
    assert "Input 1 -> Result: 100" in output
    assert "Input 2 -> Result: 200" in output
