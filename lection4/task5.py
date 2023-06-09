# Задача Иосифа Флавия
# https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B4%D0%B0%D1%87%D0%B0_%D0%98%D0%BE%D1%81%D0%B8%D1%84%D0%B0_%D0%A4%D0%BB%D0%B0%D0%B2%D0%B8%D1%8F
# Задача заключается в следующем: по кругу стоит num_people воинов,
# начиная с первого воина они выводят из круга каждого kill_num по счёту.
# Вы должны правильно указать, кто является «выжившим», то есть: последний элемент списка.
#
# num_people=7, kill_num=3 => Значит 7 человек в кругу и каждый третий из него выходит
# [1,2,3,4,5,6,7] - начальный круг
# [1,2,4,5,6,7] => 3 вышел
# [1,2,4,5,7] => 6 вышел
# [1,4,5,7] => 2 вышел
# [1,4,5] => 7 вышел
# [1,4] => 5 вышел
# [4] => 1 вышел, 4 остался последним т.е. выжившим - это наш ответ survivor.

def josephus_task(num_people: int, kill_num: int):
    """
    Решение Задачи Иосифа Флавия
    Задача заключается в следующем: по кругу стоит num_people воинов,
    начиная с первого воина они выводят из круга каждого kill_num по счёту.
    Вернуть последний элемент списка.
    :param num_people: количество элементов
    :param kill_num: номер удаляемых элементов
    :return: последний оставшийся элемент
    """
    if num_people <= 0 and kill_num <= 1:
        return "Некорректные входные данные!"
    list_people = [j for j in range(1, num_people + 1)]
    while len(list_people) > 1:
        kill_index = kill_num-1 if kill_num <= len(list_people) else kill_num % len(list_people)-1
        if kill_index != - 1:
            list_people = list_people[kill_index + 1:] + list_people[:kill_index]
        else:
            list_people = list_people[:kill_index]
    survivor = list_people[0]
    return survivor


def josephus_task_2(num_people, kill_num):
    """способ производительней но  сложнее в понимании, составил после гугла
    сделан по двум статьям
    https://habr.com/ru/articles/709540/
    - развернул рекурсию так как глубина рекурсии в питоне 1000 у нас есть задания больше
    http://school6.tgl.ru/old/made/calk/3.html
    - тут объяснения почему рекурсия так идет
    """
    survivor = 0
    for i in range(1, num_people + 1):
        survivor = (survivor + kill_num) % i
    return survivor + 1


# Ниже НИЧЕГО НЕ НАДО ИЗМЕНЯТЬ

data = [(7, 3), (11, 19), (1, 300), (14, 2), (100, 1), (1234, 56), (987, 11)]

test_data = [4, 10, 1, 13, 100, 1130, 379]


for i, d in enumerate(data):
    assert josephus_task(*d) == test_data[i], f'С набором {d} есть ошибка, не проходит проверку'
    print(f'Тестовый набор {d} прошёл проверку')
print('Всё ок')
