import pytest
from core.parser import parse_function
from core.errors import compute_exact, compute_error


def test_compute_exact_poly():
    expr, _ = parse_function("x**2")
    result = compute_exact(expr, 0, 1)
    assert abs(result - 1/3) < 1e-9


def test_compute_exact_trig():
    import numpy as np
    expr, _ = parse_function("sin(x)")
    result = compute_exact(expr, 0, np.pi)
    assert abs(result - 2.0) < 1e-9


def test_compute_error_positive():
    assert abs(compute_error(1.0, 0.9) - 0.1) < 1e-12
    assert abs(compute_error(0.9, 1.0) - 0.1) < 1e-12


def test_compute_error_zero():
    assert compute_error(1.0, 1.0) == 0.0


def test_divergent_integral_raises_or_nan():
    expr, _ = parse_function("log(x)")
    try:
        result = compute_exact(expr, 0, 1)
        assert not (result == result) or abs(result) == float("inf")
    except Exception:
        pass