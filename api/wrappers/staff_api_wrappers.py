from atf.api.base_api_ui import BaseApiUI
from atf.api.helpers import *
from atf import *
from  api.clients.staff_api import StaffApi


class StaffApiWrappers(BaseApiUI):
    """
    Управление персоналом
    """

    def __init__(self, client):
        super().__init__(client=client)
        self.staff = StaffApi(client)

    def get_list_id_by_search(self, search):
        """
        получение списка EmplId сотрудников
        :param search: Маска для поиска
        :return: список параметров сотрудников
        """
        params = dict(Access=(None, 'Строка'),
                      AccrualTypes=(None, 'Строка'),
                      ActivePeriod=(None, 'Строка'),
                      Age=(None, 'Строка'),
                      Birthday=(None, 'Строка'),
                      Breadcrumbs=True,
                      CalcFields=(['WorkState', 'FiredDate', 'Contact', 'CanEdit', 'Motivation'],
                                  {'n': 'Массив', 't': 'Строка'}),
                      City=(None, 'Строка'),
                      ColorMark=(None, 'Строка'),
                      DepNameSort=False,
                      EmptyActual=False,
                      Expansion=False,
                      Gender=(None, 'Строка'),
                      Maternity=(None, 'Строка'),
                      Nationality=(None, 'Строка'),
                      OnlyChiefs=(None, 'Строка'),
                      Organization=-2,
                      Parent=(None, 'Строка'),
                      Position=(None, 'Строка'),
                      Schedule=(None, 'Строка'),
                      ScopesAreas=(['Сотрудники'], {'n': 'Массив', 't': 'Строка'}),
                      SearchString=search,
                      TypeTree='All',
                      Wanted=(['FIO', 'DepName'], {'n': 'Массив', 't': 'Строка'}),
                      WithWorkgroup=(None, 'Строка'),
                      Working=(None, 'Строка'),
                      usePages='full',
                      Разворот='С разворотом')
        list_res = self.staff.wasaby_list_api(**params)
        list_user = [i for i in list_res if i.get("Employee")]
        return list_user

    def check_params_employee(self, search, **kwargs):
        """
        проверяем параметры сотрудника найденного по маске
        :param search: Маска для поиска
        :param: kwargs: Параметры проверки, если параметр не входит в dict_equivalent или dict_equivalent_list_value
                        надо передать как в ответе метода Staff.WasabyList
        """
        log("Находим сотрудника по маске ожидаем что результат поиска один")
        list_employee = self.get_list_id_by_search(search)
        assert_that(1, equal_to(len(list_employee)),
                    "ожидаем только одного сотрудника в результате поиска")

        log("словарь эквивалента русских названий ключам метода ")
        dict_equivalent = {'Дата рождения': "BirthDate",
                           'Дата трудоустройства': "HiredDate",
                           'Должность': "Position",
                           'ID в облаке': "User"}
        log("словарь эквивалента русских названий ключам метода вложения Contacts")
        dict_equivalent_list_value = {'Электронный адрес': "Email",
                                      'Мобильный телефон': "MobilePhone"}

        log("Составляем стандарт значений полей сотрудника из переданных параметров")
        params_standard = {'Contacts': kwargs.get('Contacts', {})}
        for key, value in kwargs.items():

            log("если передан русский эквивалент заменяем на поле метода")
            if key in dict_equivalent:
                params_standard.update({dict_equivalent[key]: value})

            log("если передан русский эквивалент Контактов заменяем на поле метода")
            if key in dict_equivalent_list_value:
                value = [{'Value': value}]
                params_standard['Contacts'].update({dict_equivalent_list_value[key]: value})

        assert_that(params_standard, is_in_json(list_employee[0]["Employee"]),
                    "параметры сотрудников не совпадают с ожидаемыми")

    def get_wan_private_person_by_search(self, search):
        """
        получение PrivatePerson одного сотрудника
        :param search: Маска уникальная для одного сотрудника
        :return: PrivatePerson
        """
        list_employee = self.get_list_id_by_search(search)
        assert_that(1, equal_to(len(list_employee)),
                    "ожидаем только одного сотрудника в результате поиска")
        user_private_person = list_employee[0]["Employee"]["PrivatePerson"]
        return user_private_person
