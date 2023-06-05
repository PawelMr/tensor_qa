# Напишите генератор generate_random_name(), используя модуль random,
# который генерирует два слова из латинских букв от 1 до 15 символов, разделенных пробелами
# Например при исполнении следующего кода:
# gen = generate_random_name()
# print(next(gen))
# print(next(gen))
# print(next(gen))
# print(next(gen))
#
# Выводится:
# tahxmckzexgdyt ocapwy
# dxqebbukr jg
# aym jpvezfqexlv
# iuy qnikkgxvxfxtxv

import random
import string


def generate_random_name():
    """
    генератор создающий случайные два слова из латинских букв от 1 до 15 символов, разделенных пробелами
    :return: строка из двух последовательности английских букв от 1 до 15 символов случайно разделенных пробелом
    """
    while True:
        letters = string.ascii_lowercase
        list_string = []
        for i in range(2):
            len_string = random.randint(1, 15)
            word = "".join(random.choices(letters, k=len_string))
            list_string.append(word)
        two_word = " ".join(list_string)
        yield two_word


gen = generate_random_name()
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
