# Напишите функцию to_roman, которая преобразуют арабское число (val) в римское (roman_str).
#
# Современные римские цифры записываются, выражая каждую цифру отдельно,
# начиная с самой левой цифры и пропуская цифру со значением нуля.
# Римскими цифрами 1990 отображается: 1000=М, 900=СМ, 90=ХС; в результате MCMXC.
# 2023 записывается как 2000=MM, 20=XX, 3=III; или MMXXIII.
# В 1666 используется каждый римский символ в порядке убывания: MDCLXVI.
#
# Например (Ввод --> Вывод) :
# 2008 --> MMVIII


def to_roman(val):
    """
    Функция перевода арабских цифр в римские
    :param val: арабское число
    :return: римское число
    """
    translation_dict = {1: "I",
                        5: "V",
                        10: "X",
                        50: "L",
                        100: "C",
                        500: "D",
                        1000: "M"}
    # словарь не позиционный тип, поэтому перебирать будем список ключей развернутого по убыванию
    list_key = list(translation_dict.keys())
    list_key.sort(reverse=True)
    roman_str = str()
    for index, key in enumerate(list_key):
        new_characters = val // key * translation_dict[key]
        val %= key
        roman_str = roman_str + new_characters
        if key != 1:
            #  проверяю цифру 4*Е^10
            if "5" in str(key):
                number = translation_dict[list_key[index + 1]] + translation_dict[key]
                new_characters = val // (key - list_key[index + 1]) * number
                val %= (key - list_key[index + 1])
                roman_str = roman_str + new_characters
            #  проверяю цифру 9*Е^10
            else:
                number = translation_dict[list_key[index + 2]] + translation_dict[key]
                new_characters = val // (key - list_key[index + 2]) * number
                val %= (key - list_key[index + 2])
                roman_str = roman_str + new_characters
    return roman_str


def to_roman_option_2(val):
    """
    Тот же самый алгоритм, но исходный словарь больше, меньше условий на проверку кратных 4 и 9 чисел
    Функция перевода арабских цифр в римские
    :param val: арабское число
    :return: римское число
    """
    translation_dict = {1: "I",
                        4: "IV",
                        5: "V",
                        9: "IX",
                        10: "X",
                        40: "XL",
                        50: "L",
                        90: "XC",
                        100: "C",
                        400: "CD",
                        500: "D",
                        900: "CM",
                        1000: "M"}
    list_key = list(translation_dict.keys())
    list_key.sort(reverse=True)
    roman_str = str()
    for index, key in enumerate(list_key):
        new_characters = val // key * translation_dict[key]
        val %= key
        roman_str = roman_str + new_characters
    return roman_str

# Ниже НИЧЕГО НЕ НАДО ИЗМЕНЯТЬ


data = [1133, 2224, 1938, 1817, 2505, 391, 3743, 1634, 699, 1666, 1494, 1444]

test_data = [
    "MCXXXIII", "MMCCXXIV", "MCMXXXVIII", "MDCCCXVII", "MMDV", "CCCXCI", 'MMMDCCXLIII', 'MDCXXXIV', 'DCXCIX', 'MDCLXVI',
    'MCDXCIV', 'MCDXLIV']


for i, d in enumerate(data):
    assert to_roman(d) == test_data[i], f'С набором {d} есть ошибка, не проходит проверку'
    print(f'Тестовый набор {d} прошёл проверку')
print('Всё ок')
