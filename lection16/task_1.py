from atf.ui import *
from pages.saby_pages.AuthOnline import AuthOnline
from atf import *
from pages.saby_pages.TransportDeliveriesMap import TransportDeliveriesMap
from atf.api.json_rpc import JsonRpcClient
from api.wrappers.staff_api_wrappers import StaffApiWrappers


class TestEmployee(TestCase):
    """Проверка сотрудника"""
    client = None
    name_employee = "Крошелев Александр Алексеевич"
    params_employee = {
        "Дата рождения": "1990-10-10",
        "Дата трудоустройства": "2021-07-20",
        "Должность": "Генеральный директор",
        "ID в облаке": 12511109,
        "Электронный адрес": "pp.muravev@tensor.ru",
        "Мобильный телефон": "8 (999) 999-99-99"
    }

    @classmethod
    def setUpClass(cls):
        """для всего класса тестов авторизация и создание экземпляра класса проверки карты и апи клиент"""
        cls.client = JsonRpcClient(url=cls.config.get('SITE'), verbose_log=2)
        cls.client.auth(login=cls.config.get("USER_LOGIN"), password=cls.config.get("USER_PASSWORD"))
        cls.staff_wrappers = StaffApiWrappers(cls.client)

    def test_01(self):
        """
        получает информацию о переданном сотруднике и сравнивает с эталонным значением:
            Дату рождения сотрудника (BirthDate)
            Дату приёма на работу (HiredDate)
            Должность (Position)
            Электронный адрес (Email)
            Мобильный телефон (MobilePhone)
            ID в облаке (User)
        """
        self.staff_wrappers.check_params_employee(self.name_employee, **self.params_employee)
