from src.hard import tokenize_rpn, evaluate_rpn, RPNError
from src.errors import ERROR_DIVISION_BY_ZERO, ERROR_EMPTY_STACK, ERROR_INVALID_TOKEN, ERROR_TOO_MANY_OPERANDS, \
    ERROR_MODULO_FLOAT


def main() -> None:
    """Основная функция программы.
    Функция запрашивает у пользователя RPN-выражения, обрабатывает его, вычисляет и выводит результат.
    Поддерживает прерывание программы.
    """
    print("Введите выражение в обратной польской  нотации через пробел:")
    try:
        user_input = input().strip()
    except KeyboardInterrupt:
        print("\nВыход")
        return

    if not user_input:
        print("Пустой ввод")
        return

    try:
        #Разбиение строки(выражения) на токены
        tokens = tokenize_rpn(user_input)
        #Вычисление выражения
        result = evaluate_rpn(tokens)
        if isinstance(result, float) and result.is_integer():
            print(int(result))
        else:
            print(result)
    #Все ошибки обрабатываются и выводятся на экран
    except RPNError as e:
        print(e)
    #В случае непредвиденной ошибки
    except Exception:
        print(ERROR_INVALID_TOKEN)


if __name__ == "__main__":
    main()
