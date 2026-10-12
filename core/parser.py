import re
import numpy as np
import sympy as sp

ALLOWED_FUNCS = {
    "sin": sp.sin, "cos": sp.cos, "tan": sp.tan,
    "asin": sp.asin, "acos": sp.acos, "atan": sp.atan,
    "sinh": sp.sinh, "cosh": sp.cosh, "tanh": sp.tanh,
    "exp": sp.exp, "log": sp.log, "ln": sp.log,
    "sqrt": sp.sqrt, "abs": sp.Abs,
    "pi": sp.pi, "e": sp.E
}

FORBIDDEN = {"import", "exec", "eval", "open", "os", "sys", "lambda"}


class ParseError(Exception):
    pass


def _normalize(func_str):
    def repl(match):
        word = match.group(0)
        lower = word.lower()
        if lower in ALLOWED_FUNCS and word != "x":
            return lower
        return word
    return re.sub(r"[A-Za-z_][A-Za-z0-9_]*", repl, func_str)


def _check_forbidden(func_str):
    tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", func_str)
    for token in tokens:
        if token in FORBIDDEN:
            raise ParseError(f"Запрещённое выражение: {token}")
        if token.startswith("__") or token.endswith("__"):
            raise ParseError(f"Запрещённое выражение: {token}")


def parse_function(func_str):
    if not func_str or not func_str.strip():
        raise ParseError("Функция не введена")

    _check_forbidden(func_str)

    normalized = _normalize(func_str)

    x = sp.Symbol("x")
    local_dict = {"x": x, **ALLOWED_FUNCS}

    try:
        expr = sp.sympify(normalized, locals=local_dict)
    except (sp.SympifyError, SyntaxError, TypeError):
        raise ParseError("Не удалось разобрать выражение")

    for sym in expr.free_symbols:
        if str(sym) != "x":
            raise ParseError(f"Неизвестный символ: {sym}")

    for func in expr.atoms(sp.Function):
        name = func.func.__name__
        if name not in ALLOWED_FUNCS:
            raise ParseError(f"Неизвестная функция: {name}")

    try:
        f_raw = sp.lambdify(x, expr, "numpy")
    except Exception:
        raise ParseError("Не удалось преобразовать выражение в функцию")

    def f(xv):
        try:
            result = f_raw(xv)
        except Exception:
            raise ParseError("Функция не вычисляется в указанной точке")
        if np.isscalar(result):
            arr = np.asarray(xv, dtype=float)
            return np.full_like(arr, float(result), dtype=float)
        return result

    try:
        f(1.0)
    except Exception:
        raise ParseError("Функция не вычисляется в точке x=1")

    return expr, f