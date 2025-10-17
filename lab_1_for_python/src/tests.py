import pytest
from src.main import evaluate_rpn, tokenize_rpn, RPNError


def test_add():
    tokens = tokenize_rpn("3 4 +")
    assert evaluate_rpn(tokens) == 7


def test_sub():
    tokens = tokenize_rpn("3 4 -")
    assert evaluate_rpn(tokens) == -1


def test_mul():
    tokens = tokenize_rpn("3 4 *")
    assert evaluate_rpn(tokens) == 12


def test_div():
    tokens = tokenize_rpn("8 2 /")
    assert evaluate_rpn(tokens) == 4.0


def test_power():
    tokens = tokenize_rpn("2 3 **")
    assert evaluate_rpn(tokens) == 8


def test_floor_div():
    tokens = tokenize_rpn("7 2 //")
    assert evaluate_rpn(tokens) == 3


def test_div_with_remainder():
    tokens = tokenize_rpn("10 3 %")
    assert evaluate_rpn(tokens) == 1


def test_unar_operations():
    tokens = tokenize_rpn("4 ~")
    assert evaluate_rpn(tokens) == -4
    tokens = tokenize_rpn("5 $")
    assert evaluate_rpn(tokens) == 5


def test_complex_expression():
    tokens = tokenize_rpn("3 4 2 * +")
    assert evaluate_rpn(tokens) == 11


def test_float_numbers():
    tokens = tokenize_rpn("2.5 1.5 +")
    assert evaluate_rpn(tokens) == 4.0


def test_dev_by_zero():
    tokens = tokenize_rpn("5 0 /")
    with pytest.raises(RPNError, match="деление на ноль"):
        evaluate_rpn(tokens)


def test_mod_with_float():
    tokens = tokenize_rpn("5.5 2 %")
    with pytest.raises(RPNError, match="только с целыми числами"):
        evaluate_rpn(tokens)


def test_not_enough_operands():
    tokens = tokenize_rpn("5 +")
    with pytest.raises(RPNError, match="не хватает операндов"):
        evaluate_rpn(tokens)


def test_too_many_operands():
    tokens = tokenize_rpn("1 2 3 +")
    with pytest.raises(RPNError, match="слишком много чисел"):
        evaluate_rpn(tokens)


def test_invalid_token():
    with pytest.raises(RPNError, match="недопустимый токен"):
        tokenize_rpn("3 4 a")


def test1():
    tokens = tokenize_rpn("2 3 + 4 * 2 **")
    assert evaluate_rpn(tokens) == 400


def test2():
    tokens = tokenize_rpn("5 ~ 2 *")
    assert evaluate_rpn(tokens) == -10


def test3():
    tokens = tokenize_rpn("5 ~ ~")
    assert evaluate_rpn(tokens) == 5


def test4():
    tokens = tokenize_rpn("2 3*4+")
    assert evaluate_rpn(tokens) == 10
