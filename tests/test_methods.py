import numpy as np
import pytest
from core.methods import (
    method_rect_left, method_rect_right, method_rect_mid,
    method_trapezoid, method_simpson
)


def f1(x):
    return x ** 2


def test_rect_left_poly():
    result = method_rect_left(f1, 0, 1, 1000)
    assert abs(result - 1 / 3) < 1e-3


def test_rect_right_poly():
    result = method_rect_right(f1, 0, 1, 1000)
    assert abs(result - 1 / 3) < 1e-3


def test_rect_mid_poly():
    result = method_rect_mid(f1, 0, 1, 1000)
    assert abs(result - 1 / 3) < 1e-6


def test_trapezoid_poly():
    result = method_trapezoid(f1, 0, 1, 1000)
    assert abs(result - 1 / 3) < 1e-6


def test_simpson_poly():
    result = method_simpson(f1, 0, 1, 100)
    assert abs(result - 1 / 3) < 1e-9


def test_simpson_odd_n():
    with pytest.raises(ValueError):
        method_simpson(f1, 0, 1, 11)


def test_all_methods_constant():
    def fc(x):
        return np.ones_like(x)

    for m in [method_rect_left, method_rect_right, method_rect_mid,
              method_trapezoid, method_simpson]:
        if m is method_simpson:
            result = m(fc, 0, 1, 10)
        else:
            result = m(fc, 0, 1, 10)
        assert abs(result - 1.0) < 1e-9


def test_simpson_accuracy_vs_trapezoid():
    def fs(x):
        return np.sin(x)

    exact = 2.0
    err_trap = abs(method_trapezoid(fs, 0, np.pi, 100) - exact)
    err_simp = abs(method_simpson(fs, 0, np.pi, 100) - exact)
    assert err_simp < err_trap
    
def test_rect_left_n_one():
    result = method_rect_left(f1, 0, 1, 1)
    assert abs(result - 0.0) < 1e-12


def test_rect_right_n_one():
    result = method_rect_right(f1, 0, 1, 1)
    assert abs(result - 1.0) < 1e-12


def test_trapezoid_n_one():
    result = method_trapezoid(f1, 0, 1, 1)
    assert abs(result - 0.5) < 1e-12


def test_log_at_zero_nonfinite():
    import numpy as np

    def f(x):
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.log(x)

    result = method_rect_left(f, 0, 1, 10)
    assert not np.isfinite(result)