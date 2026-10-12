import json
import numpy as np
from core.parser import parse_function
from core.methods import METHODS, method_rect_left
from core.errors import compute_exact, compute_error


def test_full_pipeline_poly():
    expr, f = parse_function("x**2 + 3*x - 1")
    exact = compute_exact(expr, 0, 1)
    approx = METHODS["Симпсона"](f, 0, 1, 100)
    assert compute_error(approx, exact) < 1e-8


def test_full_pipeline_trig():
    expr, f = parse_function("sin(x)")
    exact = compute_exact(expr, 0, np.pi)
    approx = METHODS["Трапеций"](f, 0, np.pi, 1000)
    assert abs(exact - 2.0) < 1e-6
    assert compute_error(approx, exact) < 1e-3


def test_full_pipeline_exp():
    expr, f = parse_function("exp(x)")
    exact = compute_exact(expr, 0, 1)
    approx = METHODS["Средних прямоугольников"](f, 0, 1, 1000)
    assert compute_error(approx, exact) < 1e-5


def test_all_methods_converge():
    expr, f = parse_function("x**3")
    exact = compute_exact(expr, 0, 2)

    tolerances = {
        "Левых прямоугольников": 1e-1,
        "Правых прямоугольников": 1e-1,
        "Средних прямоугольников": 1e-3,
        "Трапеций": 1e-3,
        "Симпсона": 1e-6,
    }

    for name, method in METHODS.items():
        n = 1000 if "прямоугольников" in name else 100
        approx = method(f, 0, 2, n)
        err = compute_error(approx, exact)
        assert err < tolerances[name], f"{name} не сошёлся: err={err}"


def test_left_rect_convergence_order():
    expr, f = parse_function("x**3")
    exact = compute_exact(expr, 0, 2)

    err_100 = compute_error(method_rect_left(f, 0, 2, 100), exact)
    err_200 = compute_error(method_rect_left(f, 0, 2, 200), exact)

    ratio = err_100 / err_200
    assert 1.8 < ratio < 2.2, f"Порядок сходимости не 1: ratio={ratio}"
    
def test_cases_from_json():
    with open("data/test_cases.json", encoding="utf-8") as f:
        cases = json.load(f)

    for case in cases:
        expr, func = parse_function(case["function"])
        exact = compute_exact(expr, case["a"], case["b"])
        approx = METHODS["Симпсона"](func, case["a"], case["b"], 1000)
        assert compute_error(approx, exact) < 1e-3, case["name"]