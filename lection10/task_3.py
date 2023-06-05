# Из набора тестов задания task_2 создайте один тест с параметрами, используя @pytest.mark.parametrize
# Промаркируйте 1 параметр из выборки как smokе, а 1 набор данных скипните

import pytest


def all_division(*arg1):

    division = arg1[0]
    for i in arg1[1:]:
        division /= i
    return division

@pytest.mark.parametrize("set_value,result",
                         [
                                 pytest.param((10, 2, 5), 1, marks=pytest.mark.skip("плохие данные")),
                                 pytest.param((0, 1, 1), 0, marks=pytest.mark.smoke),
                                 ((10.2, 0.5), 20.4),
                         ])
def test_positive(set_value,result):
    """
    Проверка all_division через parametrize позитивные сценарии
    """
    result_res = all_division(*set_value)
    assert result == result_res, f"при делении натуральных чисел в результате ожидаем 1\n" \
                                 f"входящие данные {set_value}  \n" \
                                 f"функция вернула {result}"

@pytest.mark.parametrize("set_value,type_error",
                         [
                                 pytest.param(("10", "2", "5"), TypeError, marks=pytest.mark.skip("плохие данные")),
                                 pytest.param(("10", 1, ), TypeError, marks=pytest.mark.smoke),
                                 ((10, 0), ZeroDivisionError),
                         ], ids=["lot bad data", "TypeError", "ZeroDivisionError"])
def test_negative(set_value,type_error):
    """
    Проверка all_division через parametrize негативные сценарии
    """
    with pytest.raises(type_error):
        all_division(*set_value)


