def task1(side_of_square: float):
    """
    Функция по стороне квадрата выводит периметр, площадь и диагональ этого квадрата.
    :param side_of_square: Сторона квадрата
    :return:
    """
    print(f"Периметр квадрата: {4 * side_of_square}")
    print(f"Площадь Квадрата: {side_of_square ** 2}")
    print(f"Диагональ квадрата: {2 ** 0.5 * side_of_square}")


def task2(a: float, b: float, c: float):
    """
    Ищет корни квадратного уровнения вида ax^2 + bx + c =0
    Дискриминант должен быть больше нуля
    :return:
    """
    discr = b ** 2 - 4 * a * c
    if discr > 0:
        x1 = (-b + discr ** 0.5) / (2 * a)
        x1 = round(x1, 2)
        x2 = (-b - discr ** 0.5) / (2 * a)
        x2 = round(x2, 2)
        print(f"x1 = {x1}\n"
              f"x2 = {x2}")
    else:
        print("Условие не выполнено Дискриминант меньше или равен 0")


def task3(string1: str, string2: str):
    """
    Объединяем две строки в одну меняя два первых символа первой строки на два первых символа второй строки
    и наоборот
    :param string1: строка 1
    :param string2: строка 2
    :return:
    """
    first_characters_string1 = string1[0:2]
    first_characters_string2 = string2[0:2]
    new_string1 = " ".join([string1.replace(first_characters_string1, first_characters_string2, 1),
                            string2.replace(first_characters_string2, first_characters_string1, 1)])
    print(new_string1)

    # Альтернативный способ решения
    print(f"{string2[0:2]}{string1[2:]} {string1[0:2]}{string2[2:]}")


def task4(path: str):
    """
    Из пути к файлу выделяем название файла без расширения название диска и корневую папку
    :param path: путь до файла
    :return:
    """
    list_element_path = path.split("\\")
    if len(list_element_path) > 1:
        if len(list_element_path[0]) == 2:
            disk = list_element_path[0][0:1]
        else:
            disk = "Диск не определен путь не Локальный, не Виндовс или некорректный"
        if len(list_element_path) != 2:
            root_folder = list_element_path[1]
        else:
            root_folder = "корневой папки нет файл лежит на диске"
        name_file = list_element_path[-1]
        index_point = name_file.rfind(".")
        if index_point != -1:
            name_file = name_file[0:index_point]
        print(f"локальный диск: {disk}\n"
              f"корневая папка: {root_folder}\n"
              f"имя файла без расширения: {name_file}")
    else:
        print("путь не корректный")


def task5(a: float, b: float):
    """
    Выводим сумму и произведение двух чисел
    :param a: первое число
    :param b: второе число
    :return:
    """
    print(f"a + b = {a + b}\n"
          f"a * b = {a * b}")


def task6(string):
    """
    Удаляем все символы в строке с нечетными индексами
    :param string: строка
    :return:
    """
    new_string = ""
    for i in range(len(string)):
        if i % 2 == 0:
            new_string = new_string + string [i]
    print(new_string)


def task7(string1: str, string2: str):
    """

    :param string1:
    :param string2:
    :return:
    """
    # условия только для контроля входных данных, можно удалить но данные в ручную контролировать надо будет
    if len(string1) != 3:
        print("длинна 1 строки должна быть равна 3")
    elif string1[0] not in string2 or string1[1] not in string2 or string1[2] not in string2:
        print(" во второй строке должны быть все символы первой строки")
    else:
        symbol_0_index = string2.find(string1[0])
        symbol_1_index = string2.find(string1[1])
        symbol_2_index = string2.find(string1[2])
        beginning_segment = min([symbol_0_index, symbol_1_index, symbol_2_index])
        end_segment = max([symbol_0_index, symbol_1_index, symbol_2_index])
        print(f"минимальный срез: {string2[beginning_segment:end_segment + 1]}")


task1(1)
task2(1, 4, 1)
task3("1234", "qwer")
task4("C:\\123\\qwe.txt")
task5(2, 1)
task6("0123456789")
task7("153", "02345678")
