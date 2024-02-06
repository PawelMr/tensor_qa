from atf.ui import *
from atf import *
from api.clients.document_api import DocumentApi
from api.wrappers.WTD_api_wrappers import WTDApiWrapper
from pages.saby_pages.AuthOnline import AuthOnline
from pages.saby_pages.WorkScheduleDocuments import WorkScheduleDocuments
import datetime
from atf.api.json_rpc import JsonRpcClient


class TestDaysOff(TestCaseUI):
    """
    Tесты проверки Отгулов
    """
    client_api = None
    list_comment = ["Тестовая причина отгула", "Тестовая причина-2 отгула"]

    @classmethod
    def setUpClass(cls):
        """для всего класса тестов авторизация и создание экземпляра класса проверки Отгулов"""
        AuthOnline(cls.driver).auth(cls.config.get('USER_LOGIN'), cls.config.get('USER_PASSWORD'),
                                    cls.config.get('SITE'))
        cls.page_doc_schedule_works = WorkScheduleDocuments(cls.driver)
        cls.client_api = JsonRpcClient(url=cls.config.get('SITE'), verbose_log=0)
        cls.client_api.auth(login=cls.config.get("USER_LOGIN"), password=cls.config.get("USER_PASSWORD"))

        cls.wtd_wrappers = WTDApiWrapper(cls.client_api)

    def setUp(self):
        """для каждого теста проверка прогрузки документов"""
        self.page_doc_schedule_works.open_page()
        self.page_doc_schedule_works.check_page_load_wasaby()

    def tearDownClass(self):
        """ удаляем отгулы с комментарием из списка """
        self.wtd_wrappers.del_doc_by_comment(*self.list_comment)

    def test_01(self):
        """
        -Создать отгул
        -Выбрать сотрудника через автодополнение, которому создаем отгул
        -Выставить дату - завтра
        -Выбрать тип отгула "С оплатой"
        -Заполнить причину
        -Запустить в ДО
        -Убедиться, что появился в реестре и при переоткрытии значения в полях сохранились
        -Удалить отгул
        """

        text_off_dey = f'Тестовая причина отгула {datetime.datetime.now()}'
        date_off_dey = datetime.date.today() + datetime.timedelta(days=1)
        off_dey_data = {'Исполнитель': 'Крошелев Александр Алексеевич',
                        'Причина': text_off_dey,
                        'Дата': date_off_dey,
                        "Тип": "с оплатой"}
        log(f"Данные для заполнения отгула {off_dey_data}")
        log("создаем отгул")
        self.page_doc_schedule_works.create_document('Отгул')

        from pages.WorkTimeDocuments.timeoff import Dialog
        off_day_card = Dialog(self.driver)
        off_day_card.check_open()

        log("заполняем отгул")
        off_day_card.fill_doc(**off_dey_data)

        log("Запускаем ДО")
        off_day_card.to_run_doc()

        log("открыто окно запуска")
        from pages.EDO3.passage import Panel
        panel_to_run = Panel(self.driver)

        log("выбираем исполнителя согласования")
        panel_to_run.executor_cl.autocomplete_search('Крошелев Александр Алексеевич')

        log("нажимаем кнопку согласовать")
        panel_to_run.button_coordinate_day_off.click()
        panel_to_run.check_close()

        log("закрываем окно отгула")
        off_day_card.close()
        off_day_card.check_close()

        log(f"открываем его дя проверки ищем по сообщению: '{text_off_dey}'")
        self.page_doc_schedule_works.open_doc(text_off_dey)
        off_day_card_for_check = Dialog(self.driver)
        off_day_card_for_check.check_open()

        log("получаем формат даты для проверки")
        date_off_dey = date_off_dey.strftime("%d.%m.%y")
        off_dey_data['Дата'] = date_off_dey

        log("Проверяем отгул")
        off_day_card_for_check.check_doc(**off_dey_data)
        off_day_card_for_check.close()
        off_day_card_for_check.check_close()

        log("удаляем")
        self.wtd_wrappers.del_doc_by_comment(text_off_dey)
        self.page_doc_schedule_works.open_page()
        self.page_doc_schedule_works.check_page_load_wasaby()

        log("проверяем что в списке его нет")
        self.page_doc_schedule_works.check_availability_doc(text_off_dey)

    def test_02(self):
        """
        -Создать отгул
        -Выбрать сотрудника через справочник
        -Выставить время завтра с 12 до 14 часов
        -Заполнить описание
        -Сохранить
        -Убедиться, что появился в реестре и при переоткрытии значения в полях сохранились
        -Удалить отгул
        """

        text_off_dey = f'Тестовая причина-2 отгула {datetime.datetime.now()}'
        date_off_dey = datetime.date.today() + datetime.timedelta(days=1)
        off_dey_data = {'Причина': text_off_dey,
                        'Дата': date_off_dey,
                        "Время": ["12:00", "14:00"]}
        log(f"Данные для заполнения отгула {off_dey_data}")

        log("создаем отгул")
        self.page_doc_schedule_works.create_document('Отгул')

        from pages.WorkTimeDocuments.timeoff import Dialog
        off_day_card = Dialog(self.driver)
        off_day_card.check_open()

        log("Выбор исполнителя из справочника")
        off_day_card.executor_cl.click().select('Крошелев Александр Алексеевич')

        log("заполняем отгул")
        off_day_card.fill_doc(**off_dey_data)

        log("сохраняем отгул")
        off_day_card.save_button.click()
        off_day_card.check_close()

        log(f"открываем его дя проверки ищем по сообщению: '{text_off_dey}'")
        self.page_doc_schedule_works.open_doc(text_off_dey)
        off_day_card_for_check = Dialog(self.driver)
        off_day_card_for_check.check_open()

        log("получаем формат даты для проверки")
        date_off_dey = date_off_dey.strftime("%d.%m.%y")
        off_dey_data['Дата'] = date_off_dey
        off_dey_data.update({'Исполнитель': 'Крошелев Александр Алексеевич'})

        log("Проверяем отгул")
        off_day_card_for_check.check_doc(**off_dey_data)
        off_day_card_for_check.close()
        off_day_card_for_check.check_close()

        log("удаляем")
        self.wtd_wrappers.del_doc_by_comment(text_off_dey)
        self.page_doc_schedule_works.open_page()
        self.page_doc_schedule_works.check_page_load_wasaby()

        log("проверяем что в списке его нет")
        self.page_doc_schedule_works.check_availability_doc(text_off_dey)
