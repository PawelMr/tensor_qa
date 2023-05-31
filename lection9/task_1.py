# Дан текстовый файл test_file/task1_data.txt
# Он содержит текст, в словах которого есть цифры.
# Необходимо удалить все цифры и записать получившийся текст в файл test_file/task1_answer.txt


def delete_numbers_from_file_via_import(path_to_file):
    """
    Читаем текст из файла и возвращаем этот текст без файла
    Функция отрабатывает через ИМПОРТ Регулярных вырожений
    :param path_to_file: путь файла с исходным текстом
    :return: текст без цифр
    """
    import re
    with open(path_to_file, mode="r", encoding="utf-8") as test_file:
        txt = test_file.read()
        txt_not_number = re.sub(r"\d+", "", txt)
    return txt_not_number


def delete_numbers_from_file(path_to_file):
    """
    Читаем текст из файла и возвращаем этот текст без файла
    Функция отрабатывает БЕЗ импорта
    :param path_to_file: путь файла с исходным текстом
    :return: текст без цифр
    """
    with open(path_to_file, mode="r", encoding="utf-8") as test_file:
        txt = test_file.read()
        txt.isalnum()
        txt_not_number = "".join(i for i in txt if not i.isdigit())
    return txt_not_number


new_txt = delete_numbers_from_file_via_import(r"test_file/task1_data.txt")
with open(r"test_file/task1_answer.txt", mode="w", encoding="utf-8") as new_test_file:
    new_test_file.write(new_txt)

# Ниже НИЧЕГО НЕ НАДО ИЗМЕНЯТЬ


with open("test_file/task1_answer.txt", 'r', encoding='utf-8') as file1:
    with open("test_file/task1_ethalon.txt", 'r', encoding='utf-8') as file2:
        answer = file1.readlines()
        ethalon = file2.readlines()
        assert answer == ethalon, "Файл ответа не совпадает с эталонном"
print('Всё ок')
