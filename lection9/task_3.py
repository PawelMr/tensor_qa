# Дан файл test_file/task_3.txt можно считать, что это запись покупок в магазине, где указана только цена товара
# В каждой строке файла записана цена товара.
# Покупки (т.е. несколько подряд идущих цен) разделены пустой строкой
# Нужно найти сумму трёх самых дорогих покупок, которые запишутся в переменную three_most_expensive_purchases

# вариант через генераторы не показал больше производительность даже на больших файлах
# with open(r"test_file/task_3.txt", mode="r") as test_file:
#     # читаем весь файл в строку
#     txt_string = test_file.read()
#     # получаем список из покупок в форме строк
#     list_purchasing = txt_string.split("\n\n")
#     # список из покупок представленных в виде списка позиций в формате строки
#     list_purchasing = [i.split("\n") for i in list_purchasing]
#     # позиции переводим в число суммируем по покупкам, получаем список из стоимости покупок
#     list_sum = [sum([int(j) for j in i if j]) for i in list_purchasing]
#     # находим трех наибольших
#     list_sum.sort(reverse=True)
#     three_most_expensive_purchases = sum(list_sum[0:3])


with open(r"test_file/task_31.txt", mode="r") as test_file:
    list_sum = [0]
    for line in test_file:
        if line == "\n":
            list_sum.append(0)
        else:
            list_sum[-1] += int(line.rstrip("\n"))
    list_sum.sort(reverse=True)
    three_most_expensive_purchases = sum(list_sum[0:3])

assert three_most_expensive_purchases == 202346
