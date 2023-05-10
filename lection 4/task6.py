import re


# Напишите функцию, которая принимает кортеж num_tuple из 10 цифр num_tuple,
# и возвращает строку этих чисел в виде номера телефона str_phone.
# Например (Ввод --> Вывод) :
# (1, 2, 3, 4, 5, 6, 7, 8, 9, 0)  => "(123) 456-7890"

# def create_phone_number(num_tuple):
#     """ можно тоже самое без регулярного выражения не нужен импорт import re"""
#     list_num_tuple = [str(i) for i in num_tuple]
#     list_num_tuple.insert(0, "(")
#     list_num_tuple.insert(4, ") ")
#     list_num_tuple.insert(8, "-")
#     str_phone = ''.join(list_num_tuple)
#     return str_phone


def create_phone_number(num_tuple: tuple):
    """
    Форматирование кортежа в строку - номер телефона
    :param num_tuple: кортеж цифр
    :return: строка вида "(123) 456-7890"
    """
    list_num_tuple = [str(j) for j in num_tuple]
    str_phone = re.sub(r'(\d{3})(\d{3})(\d{4})', r'(\1) \2-\3', ''.join(list_num_tuple))
    return str_phone

# Ниже НИЧЕГО НЕ НАДО ИЗМЕНЯТЬ


data = [
    (1, 2, 3, 4, 5, 6, 7, 8, 9, 0),
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    (0, 2, 3, 0, 5, 6, 0, 8, 9, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
]

test_data = [
    "(123) 456-7890", "(111) 111-1111", "(023) 056-0890", "(000) 000-0000"
]


for i, d in enumerate(data):
    assert create_phone_number(d) == test_data[i], f'С набором {d} есть ошибка, не проходит проверку'
    print(f'Тестовый набор {d} прошёл проверку')
print('Всё ок')
