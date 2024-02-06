from atf.ui import *
from pages.saby_pages.AuthOnline import AuthOnline
from atf import *
from pages.saby_pages.TransportDeliveriesMap import TransportDeliveriesMap
from atf.api.json_rpc import JsonRpcClient


class TestMap(TestCaseUI):
    """Проверка страницы планы"""
    client = None

    @classmethod
    def setUpClass(cls):
        """для всего класса тестов авторизация и создание экземпляра класса проверки карты и апи клиент"""
        AuthOnline(cls.driver).auth(cls.config.get('USER_LOGIN'), cls.config.get('USER_PASSWORD'),
                                    cls.config.get('SITE'))
        cls.page_map = TransportDeliveriesMap(cls.driver)
        cls.client = JsonRpcClient(url=cls.config.get('SITE'), verbose_log=0)
        cls.client.auth(login=cls.config.get("USER_LOGIN"), password=cls.config.get("USER_PASSWORD"))

    def setUp(self):
        """открываем и прогружаем карту"""
        self.page_map.open_page()
        self.page_map.check_load_map()

    def test_01(self):
        """
        Перейти в реестр Бизнес-Транспорт, вкладка "На карте"
        ПКМ по карте - Создать доставку - Сохранить
        Проверить, что появилась метка
        Создать вторую доставку
        Открыть вторую доставку
        Удалить через API первую доставку
        Убедиться, что на карте осталась именно вторая метка
        Удалить через API вторую доставку
        Убедиться, что на карте нет метки по второй доставке
        """
        log("кликаем по карте ПКМ ")
        self.page_map.create_point_on_map(-200, 100)

        log("Создаем доставку, сохраняем id документа, номер дату, сохраняем документ")
        self.page_map.create_doc("Доставка")
        from pages.WorksManagement.Wasaby.Transport.DeliveryTask.dialog import Dialog
        doc = Dialog(self.driver)
        doc.check_open()
        id_doc_1 = doc.get_id_doc()
        date_number_doc_1 = doc.get_date_number()
        doc.save_doc()
        doc.check_close()

        self.page_map.refresh_page()
        log("проверяем что появилась метка соответствующая 1 документу")
        self.page_map.check_visible_mark_by_id_doc(id_doc_1, True)

        log("кликаем по карте ПКМ ")
        self.page_map.create_point_on_map(500, 200)

        log("Создаем доставку, сохраняем id документа, номер дату, сохраняем документ")
        self.page_map.create_doc("Доставка")
        doc.check_open()
        id_doc_2 = doc.get_id_doc()
        date_number_doc_2 = doc.get_date_number()
        doc.save_doc()
        doc.check_close()

        self.page_map.refresh_page()
        log("проверяем что появилась метка соответствующая 2 документу")
        self.page_map.check_visible_mark_by_id_doc(id_doc_2, True)

        log("открываем документ по второй марке, проверяем соответствие id, номера и даты с присвоенными при создании")
        self.page_map.open_doc_by_mark(id_doc_2)
        doc.check_open()
        params = {'Дата и номер': date_number_doc_2,
                  "ID": id_doc_2}
        doc.check_parameter_doc(**params)

        log("удаляем первую метку обновляем страницу")
        from api.clients.delivery_task_api import DocumentTaskApi
        api_delivery_task = DocumentTaskApi(self.client)
        api_delivery_task.delete_doc(id_doc_1)
        self.page_map.refresh_page()

        log("проверяем что первой марки нет а вторая все еще на карте")
        self.page_map.check_visible_mark_by_id_doc(id_doc_1, False)
        self.page_map.check_visible_mark_by_id_doc(id_doc_2, True)

        log("удаляем вторую метку обновляем страницу, проверяем что второй марки нет на карте")
        api_delivery_task.delete_doc(id_doc_2)
        self.page_map.refresh_page()
        self.page_map.check_visible_mark_by_id_doc(id_doc_2, False)
