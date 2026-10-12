import pytest
from unittest.mock import patch
from core.parser import parse_function, ParseError

def test_valid_simple():
    expr, f = parse_function("x**2")
    assert abs(f(3.0) - 9.0) < 1e-9


def test_valid_trig():
    expr, f = parse_function("sin(x) + cos(x)")
    assert abs(f(0.0) - 1.0) < 1e-9


def test_valid_exp():
    expr, f = parse_function("exp(x)")
    assert abs(f(0.0) - 1.0) < 1e-9


def test_empty():
    with pytest.raises(ParseError):
        parse_function("")


def test_whitespace():
    with pytest.raises(ParseError):
        parse_function("   ")


def test_forbidden_import():
    with pytest.raises(ParseError):
        parse_function("__import__('os').system('ls')")


def test_forbidden_eval():
    with pytest.raises(ParseError):
        parse_function("eval('1+1')")


def test_unknown_symbol():
    with pytest.raises(ParseError):
        parse_function("y + 1")


def test_syntax_error():
    with pytest.raises(ParseError):
        parse_function("x**")
        


def test_unknown_function():
    with pytest.raises(ParseError):
        parse_function("foo(x)")


def test_uppercase_sin():
    expr, f = parse_function("Sin(x)")
    assert abs(f(0.0)) < 1e-9





def test_ln_alias():
    expr, f = parse_function("ln(x)")
    assert abs(f(1.0)) < 1e-9
    assert abs(f(2.718281828) - 1.0) < 1e-6



    

        
def test_lambdify_raises():
    with patch("core.parser.sp.lambdify", side_effect=Exception("mock")):
        with pytest.raises(ParseError, match="Не удалось преобразовать"):
            parse_function("x**2")


def test_function_fails_at_one():
    def bad_func(_):
        raise Exception("mock")

    with patch("core.parser.sp.lambdify", return_value=bad_func):
        with pytest.raises(ParseError, match="не вычисляется в точке"):
            parse_function("x**2")        
            
       