import numpy as np


def method_rect_left(f, a, b, n):
    with np.errstate(divide="ignore", invalid="ignore"):
        x = np.linspace(a, b, n + 1)
        h = (b - a) / n
        return h * np.sum(f(x[:-1]))


def method_rect_right(f, a, b, n):
    with np.errstate(divide="ignore", invalid="ignore"):
        x = np.linspace(a, b, n + 1)
        h = (b - a) / n
        return h * np.sum(f(x[1:]))


def method_rect_mid(f, a, b, n):
    with np.errstate(divide="ignore", invalid="ignore"):
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        mid = (x[:-1] + x[1:]) / 2
        return h * np.sum(f(mid))


def method_trapezoid(f, a, b, n):
    with np.errstate(divide="ignore", invalid="ignore"):
        x = np.linspace(a, b, n + 1)
        h = (b - a) / n
        y = f(x)
        return h * (y[0] / 2 + np.sum(y[1:-1]) + y[-1] / 2)


def method_simpson(f, a, b, n):
    if n % 2 != 0:
        raise ValueError("Для метода Симпсона число разбиений должно быть чётным")
    with np.errstate(divide="ignore", invalid="ignore"):
        x = np.linspace(a, b, n + 1)
        h = (b - a) / n
        y = f(x)
        return h / 3 * (y[0] + 4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-1:2]) + y[-1])


METHODS = {
    "Левых прямоугольников": method_rect_left,
    "Правых прямоугольников": method_rect_right,
    "Средних прямоугольников": method_rect_mid,
    "Трапеций": method_trapezoid,
    "Симпсона": method_simpson,
}