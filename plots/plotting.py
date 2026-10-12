import numpy as np
import matplotlib.pyplot as plt
import sympy as sp


METHOD_KEYS = {
    "left": "Левых прямоугольников",
    "right": "Правых прямоугольников",
    "mid": "Средних прямоугольников",
    "trap": "Трапеций",
    "simp": "Симпсона",
}


def _plot_rectangles(ax, f, a, b, n, side):
    x = np.linspace(a, b, n + 1)
    h = (b - a) / n
    if side == "left":
        xs = x[:-1]
        ys = f(xs)
    elif side == "right":
        xs = x[1:]
        ys = f(xs)
    else:
        xs = (x[:-1] + x[1:]) / 2
        ys = f(xs)

    for xi, yi in zip(xs, ys):
        if not np.isfinite(yi):
            continue
        if side == "left":
            left = xi
        elif side == "right":
            left = xi - h
        else:
            left = xi - h / 2
        rect = plt.Rectangle(
            (left, 0), h, yi,
            linewidth=0.8, edgecolor="royalblue",
            facecolor="lightskyblue", alpha=0.35,
        )
        ax.add_patch(rect)


def _plot_trapezoids(ax, f, a, b, n):
    x = np.linspace(a, b, n + 1)
    y = f(x)
    for i in range(n):
        xi, xi1 = x[i], x[i + 1]
        yi, yi1 = y[i], y[i + 1]
        if not (np.isfinite(yi) and np.isfinite(yi1)):
            continue
        poly_x = [xi, xi, xi1, xi1]
        poly_y = [0, yi, yi1, 0]
        ax.fill(poly_x, poly_y, color="lightskyblue", alpha=0.35,
                edgecolor="royalblue", linewidth=0.8)


def _plot_simpson_parabolas(ax, f, a, b, n):
    x = np.linspace(a, b, n + 1)
    y = f(x)
    for i in range(0, n, 2):
        if i + 2 > n:
            break
        xi, xi1, xi2 = x[i], x[i + 1], x[i + 2]
        yi, yi1, yi2 = y[i], y[i + 1], y[i + 2]
        if not (np.isfinite(yi) and np.isfinite(yi1) and np.isfinite(yi2)):
            continue
        try:
            coeffs = np.polyfit([xi, xi1, xi2], [yi, yi1, yi2], 2)
            xs_local = np.linspace(xi, xi2, 30)
            ys_local = np.polyval(coeffs, xs_local)
            ax.fill_between(xs_local, 0, ys_local,
                            color="lightskyblue", alpha=0.35,
                            edgecolor="royalblue", linewidth=0.8)
        except Exception:
            continue


def _make_label(expr):
    try:
        tex = sp.latex(expr)
        return f"$f(x) = {tex}$"
    except Exception:
        return f"f(x) = {sp.sstr(expr)}"


def plot_function(f, a, b, n, expr, student, method_name=None):
    fig, ax = plt.subplots(figsize=(11, 5.5))

    x_plot = np.linspace(a, b, 800)
    y_plot = f(x_plot)
    ax.plot(x_plot, y_plot, "b-", linewidth=2,
            label=_make_label(expr), zorder=5)

    if method_name is not None:
        if method_name == METHOD_KEYS["left"]:
            _plot_rectangles(ax, f, a, b, n, "left")
        elif method_name == METHOD_KEYS["right"]:
            _plot_rectangles(ax, f, a, b, n, "right")
        elif method_name == METHOD_KEYS["mid"]:
            _plot_rectangles(ax, f, a, b, n, "mid")
        elif method_name == METHOD_KEYS["trap"]:
            _plot_trapezoids(ax, f, a, b, n)
        elif method_name == METHOD_KEYS["simp"]:
            _plot_simpson_parabolas(ax, f, a, b, n)

    x_nodes = np.linspace(a, b, n + 1)
    y_nodes = f(x_nodes)
    ax.plot(x_nodes, y_nodes, "ro", markersize=4, zorder=6)

    if n <= 50:
        for xi in x_nodes:
            ax.axvline(xi, color="gray", linestyle="--",
                       linewidth=0.3, alpha=0.4, zorder=1)

    ax.axhline(0, color="black", linewidth=0.8)

    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title(student)
    ax.legend(loc="upper right", fontsize=11)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig