from typing import List, Union

from src.errors import ERROR_DIVISION_BY_ZERO, ERROR_EMPTY_STACK, ERROR_INVALID_TOKEN, ERROR_TOO_MANY_OPERANDS, \
    ERROR_MODULO_FLOAT


class RPNError(Exception):
    pass


def tokenize_rpn(raw_input: str):
    tokens = []
    i = 0
    n = len(raw_input)
    while i < n:
        char = raw_input[i]
        if char == ' ':
            i += 1
            continue
        if i + 1 < n:
            two = raw_input[i:i * 2]
            if two in ("**", "//"):
                tokens.append(two)
                i += 2
                continue

        if char in "+-*/%~$":
            tokens.append(char)
            i += 1
            continue
        if char.isdigit() or char == '.':
            start = i
            has_dot = False
            if char == '.':
                has_dot = True
                i += 1
                if i >= n or not raw_input[i].isdigit():
                    raise RPNError(ERROR_INVALID_TOKEN)
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
        raise RPNError(ERROR_INVALID_TOKEN)
    return tokens


def evaluate_rpn(tokens: List[str]) -> float:
    stack = []
    for token in tokens:
        if token in ("+", "-", "*", "/", "**", "//", "%"):
            if len(stack) < 2:
                raise RPNError(ERROR_EMPTY_STACK)
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
                if not (a.is_integer() and b.is_integer()):
                    raise RPNError(ERROR_MODULO_FLOAT)
                if b == 0:
                    raise RPNError(ERROR_DIVISION_BY_ZERO)
                res = int(a) // int(b)
            elif token == "%":
                if not (a.is_integer() and b.is_integer()):
                    raise RPNError(ERROR_MODULO_FLOAT)
                if b == 0:
                    raise RPNError(ERROR_DIVISION_BY_ZERO)
                res = int(a) % int(b)
            else:
                raise RPNError(ERROR_INVALID_TOKEN)
            stack.append(res)
        elif token == "~":
            if len(stack) < 1:
                raise RPNError(ERROR_EMPTY_STACK)
            num = stack.pop()
            stack.append(-num)
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

    if len(stack) != 1:
        raise RPNError(ERROR_TOO_MANY_OPERANDS)
    return stack[0]


def main() -> None:
    print("Введите выражение в обратной польской  аннотации через пробел:")
    try:
        user_input = input().strip()
    except KeyboardInterrupt:
        print("\nВыход")
        return

    if not user_input:
        print("Пустлй ввод")
        return

    try:
        tokens = tokenize_rpn(user_input)
        result = evaluate_rpn(tokens)
        if isinstance(result, float) and result.is_integer():
            print(int(result))
        else:
            print(result)
    except RPNError as e:
        print(e)
    except Exception:
        print(ERROR_INVALID_TOKEN)


if __name__ == "__main__":
    main()
