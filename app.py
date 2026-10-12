import math
import io

import streamlit as st
import numpy as np
import sympy as sp
import pandas as pd
import matplotlib.pyplot as plt

from core.parser import parse_function, ParseError
from core.methods import METHODS
from core.errors import compute_exact, compute_error
from io_utils.exporter import export_csv, export_json
from plots.plotting import plot_function

STUDENT = "Иванов И.И."

st.set_page_config(page_title="Численное интегрирование", layout="wide")
st.title("Численное интегрирование")
st.write(f"Студент: {STUDENT}")

st.sidebar.header("Параметры")

func_str = st.sidebar.text_input("Функция f(x):", value="x**2 + 3*x - 1")
a = st.sidebar.number_input("Нижний предел a:", value=0.0, format="%.6f")
b = st.sidebar.number_input("Верхний предел b:", value=1.0, format="%.6f")
method_name = st.sidebar.selectbox("Метод:", list(METHODS.keys()))
n = st.sidebar.number_input(
    "Число разбиений n:", min_value=2, max_value=100000, value=10, step=1
)
n_max = st.sidebar.number_input(
    "Максимум n для таблицы:", min_value=10, max_value=10000, value=100, step=10
)

compute = st.sidebar.button("Вычислить")

if "results" not in st.session_state:
    st.session_state.results = None


if compute:
    try:
        if a >= b:
            raise ValueError("Должно быть a < b")

        expr, f = parse_function(func_str)

        try:
            exact_val = compute_exact(expr, a, b)
        except Exception:
            exact_val = float("nan")

        method_func = METHODS[method_name]

        try:
            approx = method_func(f, a, b, int(n))
        except Exception:
            approx = float("nan")

        try:
            approx_float = float(approx)
        except (TypeError, ValueError):
            approx_float = float("nan")

        try:
            exact_float = float(exact_val)
        except (TypeError, ValueError):
            exact_float = float("nan")

        is_finite = math.isfinite(approx_float) and math.isfinite(exact_float)

        n_values = [2 ** k for k in range(1, 12) if 2 ** k <= n_max]
        if int(n) not in n_values:
            n_values.append(int(n))
            n_values.sort()

        rows = []
        for ni in n_values:
            try:
                val = method_func(f, a, b, ni)
                val_float = float(val)
                if not math.isfinite(val_float):
                    rows.append([ni, None, None])
                else:
                    err = compute_error(val_float, exact_float)
                    rows.append([ni, val_float, err])
            except Exception:
                rows.append([ni, None, None])

        st.session_state.results = {
            "expr": expr,
            "f": f,
            "a": a,
            "b": b,
            "n": int(n),
            "method_name": method_name,
            "exact_float": exact_float,
            "approx_float": approx_float,
            "is_finite": is_finite,
            "rows": rows,
            "columns": ["n", "Значение", "Погрешность"],
        }

    except ParseError as e:
        st.session_state.results = None
        st.error(f"Ошибка ввода: {e}")
    except ValueError as e:
        st.session_state.results = None
        st.error(f"Ошибка: {e}")
    except Exception as e:
        st.session_state.results = None
        st.error(f"Непредвиденная ошибка: {e}")


res = st.session_state.results

if res is None:
    st.info("Введите параметры слева и нажмите «Вычислить»")

elif not res["is_finite"]:
    st.warning(
        "Функция имеет особенность на отрезке — интеграл расходится или "
        "не может быть вычислен численно. Попробуйте изменить пределы "
        "интегрирования (например, a > 0 для log(x))."
    )

    st.subheader("График разбиения")
    fig = plot_function(
        res["f"], res["a"], res["b"], res["n"], res["expr"], STUDENT,
        method_name=res["method_name"],
    )
    st.pyplot(fig)
    plt.close(fig)

else:
    error = compute_error(res["approx_float"], res["exact_float"])

    st.subheader("Результат")
    col1, col2, col3 = st.columns(3)
    col1.metric("Точное значение", f"{res['exact_float']:.10f}")
    col2.metric(res["method_name"], f"{res['approx_float']:.10f}")
    col3.metric("Погрешность", f"{error:.3e}")

    st.subheader("График разбиения")
    fig = plot_function(
        res["f"], res["a"], res["b"], res["n"], res["expr"], STUDENT,
        method_name=res["method_name"],
    )
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Таблица значений и погрешностей")
    df = pd.DataFrame(res["rows"], columns=res["columns"])

    try:
        st.dataframe(df, width="stretch")
    except TypeError:
        st.dataframe(df, use_container_width=True)

    csv_data = export_csv(res["rows"], res["columns"])
    json_data = export_json(res["rows"], res["columns"])

    st.download_button(
        "Скачать CSV", csv_data, file_name="results.csv", mime="text/csv"
    )
    st.download_button(
        "Скачать JSON",
        json_data,
        file_name="results.json",
        mime="application/json",
    )