# Напишите 5 тестов на функцию all_division. Обязательно должен быть тест деления на ноль.
# Промаркируйте часть тестов. Например, smoke.
# В консоли с помощью pytest сделайте вызов:
# 1) Всех тестов
# 2) Только с маркером smoke
# 3) По маске. Выберите такую маску, чтобы под неё подпадали не все тесты, но больше одного
# Пришлите на проверку файл с тестами и скрины с вызовами и их результаты

import pytest


def all_division(*arg1):


    division = arg1[0]
    for i in arg1[1:]:
        division /= i
    return division


def test_positive_01():
    """
    Проверка деления нуля на число
    """
    result = all_division(0, 1, 1)
    assert result == 0, f"при делении 0 на число в результате ожидаем ноль \n" \
                        f"входящие данные (0, 1, 1) \n" \
                        f"функция вернула {result}"


@pytest.mark.smoke
def test_positive_02():
    """
    Проверка деления натуральных чисел
    """
    result = all_division(10, 2, 5)
    assert result == 1, f"при делении натуральных чисел в результате ожидаем 1\n" \
                        f"входящие данные (10, 2, 5)  \n" \
                        f"функция вернула {result}"


def test_positive_03():
    """
    Проверка деления дробных чисел
    """
    result = all_division(10.2, 0.5)
    assert result == 20.4, f"при делении дробных чисел в результате ожидаем 20.4\n" \
                           f"входящие данные (10.2, 0.5)  \n" \
                           f"функция вернула {result}"


def test_negative_01():
    """
    Передача в функцию данных отличных от числа
    """
    with pytest.raises(TypeError):
        all_division("10", 2)


@pytest.mark.smoke
def test_negative_02():
    """
    Проверка исключения при делении на ноль
    """
    with pytest.raises(ZeroDivisionError):
        all_division(10, 0)




