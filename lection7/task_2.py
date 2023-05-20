
# Напишите класс PersonInfo
# Экземпляр класса создается из следующих атрибутов:
# 1. Строка - "Имя Фамилия"
# 2. Число - возраст сотрудника
# 3. Подразделения от головного до того, где работает сотрудник.
# Реализуйте методы класса:
# 1. short_name, который возвращает строку Фамилия И.
# 2. path_deps, возвращает путь "Головное подразделение --> ... --> Конечное подразделение"
# 3. new_salary, Директор решил проиндексировать зарплаты, и новая зарпалата теперь вычисляет по формуле:
# 1337*Возраст*суммарное кол-во вхождений трех наиболее часто встречающихся букв из списка подразделений
# (регистр имеет значение "А" и "а" - разные буквы)
# Например (Ввод --> Вывод) :
# PersonInfo('Александр Шленский',
#            32,
#            'Разработка', 'УК', 'Автотесты').short_name() --> 'Шленский А.'
# PersonInfo('Александр Шленский',
#            32,
#            'Разработка', 'УК', 'Автотесты').path_deps() -->
#            'Разработка --> УК --> Автотесты'
# PersonInfo('Александр Шленский', 32, 'Разработка', 'УК', 'Автотесты').new_salary() --> 385056 т.к.
# т.к. буква "т" встречается 4 раза, "а" 3 раза, 'о' 2 раза, остальные по одной. Сумма трёх самых частых букв 4+3+2 = 9.
# 1337*32*9 = 385056


class PersonInfo:
    """
    Класс обработки информации о сотруднике
    """

    def __init__(self, ful_name: str, age: int, *args: str):
        """
        Инициализация класса
        :param ful_name: Имя Фамилия
        :param age: Возраст сотрудника
        :param args: Подразделения от головного до того, где работает сотрудник
        """
        self.ful_name = ful_name
        self.age = age
        self.subdivision = args

    def short_name(self):
        """
        Возвращает Фамилию и инициал имени сотрудника
        :return: строка формата "Фамилия И."
        """
        list_name = self.ful_name.split()
        return f"{list_name[1]} {list_name[0][:1]}."

    def path_deps(self):
        """
        Возвращает путь "Головное подразделение --> ... --> Конечное подразделение"
        :return: строка
        """
        return " --> ".join(self.subdivision)

    # Вариант без импорта
    def new_salary_2(self):
        """
        Вычисление зарплаты после Индексации
        зарплата теперь вычисляет по формуле:
        1337*Возраст*суммарное кол-во вхождений трех наиболее часто встречающихся букв из списка подразделений
        (регистр имеет значение "А" и "а" - разные буквы)
        :return:
        """
        list_characters_our_str = list("".join(self.subdivision))
        letters_dict = {}
        for characters in list_characters_our_str:
            if characters not in letters_dict:
                letters_dict.update({characters: 1})
            else:
                letters_dict[characters] += 1
        list_number_occurrences = [value for key, value in letters_dict.items()]
        list_number_occurrences.sort(reverse=True)
        new_salary = 1337 * self.age * sum(list_number_occurrences[:3])
        return new_salary

    def new_salary(self):
        """
        Вычисление зарплаты после Индексации
        зарплата теперь вычисляет по формуле:
        1337*Возраст*суммарное кол-во вхождений трех наиболее часто встречающихся букв из списка подразделений
        (регистр имеет значение "А" и "а" - разные буквы)

        Используя импорт из задачи 5 лекции
        from lection5.task_1 import letter_stat
        с условием выкаченного всего репозитория
        в случае отсутствия импорта возьмет функцию new_salary_2
        :return:
        """
        try:
            from lection5.task_1 import letter_stat
            letters_dict = letter_stat("".join(self.subdivision))
            list_number_occurrences = [value for key, value in letters_dict.items()]
            list_number_occurrences.sort(reverse=True)
            new_salary = 1337 * self.age * sum(list_number_occurrences[:3])
        except NameError:
            new_salary = self.new_salary_2()
        return new_salary


# Ниже НИЧЕГО НЕ НАДО ИЗМЕНЯТЬ


first_person = PersonInfo('Александр Шленский', 32, 'Разработка', 'УК', 'Автотесты')
fourth_person = PersonInfo('Иван Иванов', 26, 'Разработка')
second_person = PersonInfo('Пётр Валерьев', 47, 'Разработка', 'УК')
third_person = PersonInfo('Макар Артуров', 51, 'Разработка', 'УК', 'Нефункциональное тестирование', 'Автотестирование')

data = [first_person.short_name,
        second_person.short_name,
        third_person.short_name,
        fourth_person.short_name,

        first_person.path_deps,
        second_person.path_deps,
        third_person.path_deps,
        fourth_person.path_deps,

        first_person.new_salary,
        second_person.new_salary,
        third_person.new_salary,
        fourth_person.new_salary
        ]


test_data = ['Шленский А.', 'Валерьев П.', 'Артуров М.', 'Иванов И.',

             'Разработка --> УК --> Автотесты',
             'Разработка --> УК',
             'Разработка --> УК --> Нефункциональное тестирование --> Автотестирование',
             'Разработка',
             385056, 314195, 1227366, 173810]

for i, d in enumerate(data):
    assert_error = f'Не прошла проверка для метода {d.__qualname__} экземпляра с атрибутами {d.__self__.__dict__}'
    assert d() == test_data[i], assert_error
    print(f'Набор для метода {d.__qualname__} экземпляра класса с атрибутами {d.__self__.__dict__} прошёл проверку')
print('Всё ок')
