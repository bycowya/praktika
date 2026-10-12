import sympy as sp


def compute_exact(expr, a, b):
    x = sp.Symbol("x")
    exact = sp.integrate(expr, (x, a, b))
    return float(exact.evalf())


def compute_error(approx, exact):
    return abs(approx - exact)