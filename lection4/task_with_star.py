# Задача со ЗВЁЗДОЧКОЙ. Решать НЕ обязательно.
# Программа получает на вход натуральное число num.
# Программа должна вывести другое натуральное число, удовлетворяющее условиям:
# Новое число должно отличаться от данного ровно одной цифрой
# Новое число должно столько же знаков как исходное
# Новое число должно делиться на 3
# Новое число должно быть максимально возможным из всех таких чисел
# Например (Ввод --> Вывод) :
#
# 379 --> 879
# 15 --> 75
# 4974 --> 7974
import copy


def max_division_by_3(num):
    """
    получаем число, удовлетворяющее условиям:
    -Новое число должно отличаться от данного ровно одной цифрой
    -Новое число должно столько же знаков как исходное
    -Новое число должно делиться на 3
    -Новое число должно быть максимально возможным из всех таких чисел
    :param num:
    :return: полученное число
    """
    list_new_num = []
    list_old_digits = [int(j) for j in str(num)]
    # перебираю все разряды числа с лева направо через индексы списка из цифр числа
    for index in range(len(list_old_digits)):
        # всего скорее start_digits всегда может быть ноль так как мы ищем максимальная а не минимальное значение,
        # но если у первого индекса зануляем цифру в выборку попадут значения меньшего разряда
        start_digits = 0 if index != 0 else 1
        # составляю возможные варианты цифр для данного индекса
        new_list_digits = [j for j in range(start_digits, 10) if j != list_old_digits[index]]
        # копия списка начальных цифр что бы не затереть их
        changeable_copy_list_old_digits = copy.copy(list_old_digits)
        # перебор вариантов замены цифры с индексом
        for digits in new_list_digits:
            changeable_copy_list_old_digits[index] = digits
            # проверяю делится ли число на 3 (оно делится если сумма цифр кратна трем) если делится то в общий список
            if sum(changeable_copy_list_old_digits) % 3 == 0:
                list_new_num.append(int(''.join([str(j) for j in changeable_copy_list_old_digits])))
    # выбираю максимальное
    new_num = max(list_new_num)
    return new_num

# Ниже НИЧЕГО НЕ НАДО ИЗМЕНЯТЬ


data = [
    379, 810, 981, 4974, 996, 9000, 15, 0, 9881, 9984, 9876543210, 98795432109879543210
]

test_data = [
    879, 870, 987, 7974, 999, 9900, 75, 9, 9981, 9987, 9879543210, 98798432109879543210
]


for i, d in enumerate(data):
    assert max_division_by_3(d) == test_data[i], f'С набором {d} есть ошибка, не проходит проверку'
    print(f'Тестовый набор {d} прошёл проверку')
print('Всё ок')

