from src.errors import *


def tokenize_rpn(raw_input: str) -> list[str]:
    """Разбивает строку(выражение) на список токенов(чисел и операторов)

    Допустимые операторы:
    1) Бинарные: '+', '-', '*', '/', '**', '//', '%'
    2) Унарные: '~', '$'

    Принимаются целые и вещественные числа.
    Допускаются пробелы между токенами.

    Args:
        raw_input (str): Строка с выражением формата RPN.
    Returns:
        List[str]: Список токенов (операторы как строки, числа как строки сочетиания цифр и точек).
    Raises:
        RPNError: Если входная строка содержит недопустимые символы или некорректное число
        (например: '..', 'a')
    """
    tokens = []
    i = 0
    n = len(raw_input)
    while i < n:
        char = raw_input[i]

        #Пропуск пробелов
        if char == ' ':
            i += 1
            continue

        #Проверка на двусимвольные операторы
        if i + 1 < n:
            two = raw_input[i:i + 2]
            if two in ("**", "//"):
                tokens.append(two)
                i += 2
                continue

        if char in "+-*/%~$":
            tokens.append(char)
            i += 1
            continue
        #Начало обработки числа(определяем начало)
        if char.isdigit() or char == '.':
            start = i
            has_dot = False
            if char == '.':
                has_dot = True
                i += 1
                #После точки должно идти число
                if i >= n or not raw_input[i].isdigit():
                    raise RPNError(ERROR_INVALID_TOKEN)
            #Продолжаем "собирать" число
            while i < n:
                c = raw_input[i]
                if c.isdigit():
                    i += 1
                elif c == '.':
                    if has_dot:
                        raise RPNError(ERROR_INVALID_TOKEN)
                    has_dot = True
                    i += 1
                else:
                    break
            num_str = raw_input[start:i]
            tokens.append(num_str)
            continue

        #При вводе любого другого символа будет ошибка через созданный класс RPNError
        raise RPNError(ERROR_INVALID_TOKEN)
    return tokens


def evaluate_rpn(tokens: list[str]) -> float:
    """Вычисляет значение выражения.
    Используется стек:
    1)Сначала числа кладутся в список.
    2)Затем операторы извлекают нужное количество операндов.
    3)Затем выполняется операция двух последних чисел.
    4)Результат операции помещается обратно в стек.

    Особенности программы:
    1)Результат всегда возвращается как float.
    2)Деление на ноль даст ошибку.
    3)Операции // и % требуют целых операндов.

    Args:
        tokens (List[str]): Список токенов, полученных из функции tokenize_rpn.
    Returns:
        float: Результат выражения.
    Raises:
        RPNError: При ошибках:
        -Пустой стек при попытке извлечь операнд.
        -Деление на ноль.
        -Операции // и % с нецелыми числами.
        -Оставшиеся элементы в стеке после вычислений(должен быть ровно 1).
    """
    stack = []
    #Обработка токенов
    for token in tokens:
        if token in ("+", "-", "*", "/", "**", "//", "%"):
            if len(stack) < 2:
                raise RPNError(ERROR_EMPTY_STACK)
            #Из-за того что  a b + = a + b, сначала возьмем b потом a
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                res = a + b
            elif token == "-":
                res = a - b
            elif token == "*":
                res = a * b
            elif token == "/":
                if b == 0:
                    raise RPNError(ERROR_DIVISION_BY_ZERO)
                res = a / b
            elif token == "**":
                res = a ** b
            elif token == "//":
                #Проверка на целочисленность
                if not (a.is_integer() and b.is_integer()):
                    raise RPNError(ERROR_MODULO_FLOAT)
                if b == 0:
                    raise RPNError(ERROR_DIVISION_BY_ZERO)
                res = int(a) // int(b)
            elif token == "%":
                #Проверка на целочисленность
                if not (a.is_integer() and b.is_integer()):
                    raise RPNError(ERROR_MODULO_FLOAT)
                if b == 0:
                    raise RPNError(ERROR_DIVISION_BY_ZERO)
                res = int(a) % int(b)
            else:
                #Если будет неизвестный токен
                raise RPNError(ERROR_INVALID_TOKEN)
            stack.append(res)
        #Меняем знак верхнего элемента стека
        elif token == "~":
            if len(stack) < 1:
                raise RPNError(ERROR_EMPTY_STACK)
            num = stack.pop()
            stack.append(-num)
        #Проверяем, что стек не пустой
        elif token == "$":
            if len(stack) < 1:
                raise RPNError(ERROR_EMPTY_STACK)
            pass
        else:
            try:
                num = float(token)
                stack.append(num)
            except ValueError:
                raise RPNError(ERROR_INVALID_TOKEN)
    #После обработки токенов в стеке должке остаться один элемент
    if len(stack) != 1:
        raise RPNError(ERROR_TOO_MANY_OPERANDS)
    return stack[0]
