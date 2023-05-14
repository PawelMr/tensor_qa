# Игра "Эрудит"
# Нужно написать программу scrabble, которая помогает считать кол-во очков (points), полученное за слово (word)
# По одному очку вы получите за буквы а, в, е=ё, и, н, о, р, с, т.
# Два очка стоит д, к, л, м, п, у.
# Три балла получают за б, г, ь, а также я.
# Четыре балла стоят буквы й, ы.
# 5 очков засчитывается за ж, з, х, ц, ч.
# 6 и 7 очков не предусмотрено.
# Восемь можно получить за букву ф, ш, э, ю.
# 10 баллов стоит буква щ,
# а 15 - ъ
# Например (Ввод --> Вывод):
# курс --> 6 (к=2, у=2, р=1, с=1)


def scrabble(word):
    """

    Функция подсчитывает количество баллов за переданную строку
    каждый символ строки сравнивается с заданной ценностью, и вычисляется сумма баллов,
    если у символа нет заданной ценности он расценивается как ноль
    :param word: исходная строка
    :return: количество баллов
    """
    # ВНИМАНИЕ!!! при попадание не описанны символов их ценность 0 в 3 варианте
    # "e" - английская судя по ответам считать не нужно но в условии не прописано

    # эффективнее сразу ввести словарь с ключем в один символ тогда можно убрать функцию compiling_dict_score(),
    # но печатать дольше и больше шансов опечататься
    dict_characters_score = compiling_dict_score()
    points = 0
    for characters in word:
        if characters in dict_characters_score:
            points += dict_characters_score[characters]
    return points


def compiling_dict_score():
    """
    Получение словаря типа {символ: количество баллов}
    :return: словарь баллов
    """
    dict_str_score = {1: "а, в, е, ё, и, н, о, р, с, т",
                      2: "д, к, л, м, п, у",
                      3: "б, г, ь, я",
                      4: "й, ы",
                      5: "ж, з, х, ц, ч",
                      8: "ф, ш, э, ю",
                      10: "щ",
                      15: "ъ"}
    dict_characters_score = dict()
    for score, string in dict_str_score.items():
        list_characters = string.split(", ")
        dict_characters_score.update({j: score for j in list_characters})
    return dict_characters_score

# Ниже НИЧЕГО НЕ НАДО ИЗМЕНЯТЬ


data = ["курс", 'авеинорстё', 'дклмпeу', 'бгья', 'йы', 'жзхцч', 'фшэю', 'щъ', "карабасбарабас", "околоводопроводного",
        "еженедельное", 'эхоэнцефалограф', 'человеконенавистничество', 'делопроизводительница']

test_data = [6, 10, 12, 12, 8, 25, 32, 25, 21, 26, 20, 54, 34, 36]

for i, d in enumerate(data):
    assert scrabble(d) == test_data[i], f'С набором {d} есть ошибка, не проходит проверку'
    print(f'Тестовый набор {d} прошёл проверку')
print('Всё ок')