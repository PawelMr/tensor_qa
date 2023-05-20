# Напишите класс RomanNums
# Экземпляр класса создается из строки - Римского числа.
# Реализуйте методы класса:
# 1. from_roman, который переводит римскую запись числа в арабскую
# 2. is_palindrome, метод определяет, является ли арабское число палиндромом (True - является, иначе False)
# т.е. имеет ли одинаковое значение число при чтении слева направо и справа налево
# Например (Ввод --> Вывод) :
# RomanNums('MMMCCLXIII').from_roman() --> 3263
# RomanNums('CMXCIX').is_palindrome() --> True
import copy


class RomanNums:
    """
    Класс работы с римскими числами
    """
    translation_dict_one_sign = {"I": 1,
                                 "V": 5,
                                 "X": 10,
                                 "L": 50,
                                 "C": 100,
                                 "D": 500,
                                 "CM": 900,
                                 "M": 1000}
    translation_dict_two_sign = {"IV": 4,
                                 "IX": 9,
                                 "XL": 40,
                                 "XC": 90,
                                 "CD": 400,
                                 "CM": 900}

    def __init__(self, roman_number: str):
        """
        Инициализация класса
        :param roman_number: Римское число
        """
        self.roman_number = roman_number

    def from_roman(self):
        """
        Переводит римскую запись числа в арабскую
        :return: int число
        """
        arabic_number = 0
        roman_number = self.roman_number

        for key, value in self.translation_dict_two_sign.items():
            if key in roman_number:
                arabic_number += value
                roman_number = roman_number.replace(key, "", 1)

        for key, value in self.translation_dict_one_sign.items():
            while key in roman_number:
                arabic_number += value
                roman_number = roman_number.replace(key, "", 1)

        return arabic_number

    def is_palindrome(self):
        """
        Определяет, является ли арабское число палиндромом
        :return: bool (True - является, иначе False)
        """
        arabic_number = self.from_roman
        return str(arabic_number) == str(arabic_number)[::-1]

# Ниже НИЧЕГО НЕ НАДО ИЗМЕНЯТЬ


data = [RomanNums('MMMCCLXIII').from_roman,
        RomanNums('CXXXIV').from_roman,
        RomanNums('LXXXVI').from_roman,
        RomanNums('MCDV').from_roman,
        RomanNums('CMLXXVIII').from_roman,
        RomanNums('MMMCDIV').from_roman,
        RomanNums('CMX').from_roman,
        RomanNums('MMCCCLXXXVIII').from_roman,
        RomanNums('MMVIII').from_roman,
        RomanNums('MCLXXIX').from_roman,
        RomanNums('MMMDCCXCV').from_roman,
        RomanNums('CMLXXXVIII').from_roman,
        RomanNums('CMXCIX').from_roman,
        RomanNums('CDXLIV').from_roman,
        RomanNums('CMXCIX').is_palindrome,
        RomanNums('CDXLIV').is_palindrome,
        RomanNums('MMMCCLXIII').is_palindrome,
        RomanNums('CXXXIV').is_palindrome,
        RomanNums('V').is_palindrome,
        RomanNums('MI').is_palindrome,
        RomanNums('XXX').is_palindrome,
        RomanNums('D').is_palindrome,
        ]


test_data = [3263, 134, 86, 1405, 978, 3404, 910, 2388, 2008, 1179, 3795, 988, 999, 444,
             True, True, False, False, True, True, False, False]

for i, d in enumerate(data):
    assert_error = f'Не прошла проверка для метода {d.__qualname__} экземпляра с атрибутами {d.__self__.__dict__}'
    assert d() == test_data[i], assert_error
    print(f'Набор для метода {d.__qualname__} экземпляра класса с атрибутами {d.__self__.__dict__} прошёл проверку')
print('Всё ок')
