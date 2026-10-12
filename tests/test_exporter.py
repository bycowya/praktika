import json
import csv
import io

from io_utils.exporter import export_csv, export_json


def test_export_csv_basic():
    rows = [[10, 0.5, 0.01], [100, 0.49, 0.001]]
    columns = ["n", "Значение", "Погрешность"]
    data = export_csv(rows, columns)
    text = data.decode("utf-8")
    assert "n,Значение,Погрешность" in text
    assert "10,0.5,0.01" in text
    assert "100,0.49,0.001" in text


def test_export_csv_empty():
    data = export_csv([], ["n", "Значение", "Погрешность"])
    text = data.decode("utf-8")
    assert "n,Значение,Погрешность" in text


def test_export_json_basic():
    rows = [[10, 0.5, 0.01]]
    columns = ["n", "Значение", "Погрешность"]
    data = export_json(rows, columns)
    parsed = json.loads(data.decode("utf-8"))
    assert len(parsed) == 1
    assert parsed[0]["n"] == 10
    assert abs(parsed[0]["Значение"] - 0.5) < 1e-12


def test_export_json_empty():
    data = export_json([], ["n", "Значение", "Погрешность"])
    parsed = json.loads(data.decode("utf-8"))
    assert parsed == []


def test_export_csv_none_values():
    rows = [[10, None, None]]
    columns = ["n", "Значение", "Погрешность"]
    data = export_csv(rows, columns)
    text = data.decode("utf-8")
    assert "10,," in text