from atf.ui import *
from pages.saby_pages.AuthOnline import AuthOnline
from pages.saby_pages.Calendar import Calendar
from atf import *
import datetime
from atf.api.json_rpc import JsonRpcClient


class TestPlane(TestCaseUI):
    """Проверка страницы календарь"""
    client_api = None

    @classmethod
    def setUpClass(cls):
        """для всего класса тестов авторизация и создание экземпляра класса проверки календаря"""
        AuthOnline(cls.driver).auth(cls.config.get('USER_LOGIN'), cls.config.get('USER_PASSWORD'),
                                    cls.config.get('SITE'))
        cls.page_calendar = Calendar(cls.driver)
        cls.client_api = JsonRpcClient(url=cls.config.get('SITE'), verbose_log=0)
        cls.client_api.auth(login=cls.config.get("USER_LOGIN"), password=cls.config.get("USER_PASSWORD"))

    def setUp(self):
        """для каждого теста проверка прогрузку календаря"""
        self.page_calendar.open_page()
        self.page_calendar.check_load_calendar()

    def test_01(self):
        """
        Открыть календарь на вкладке "Дни"
        Создать рабочее событие на 07:00 текущего дня, кликнув по сетке в нужную ячейку (Это не обычный реестр, тут надо проявить смекалку)
        Убедиться, что при создании время начала события в диалоге 07:00
        Заполнить время окончания 09:00 и описание и сохранить
        Перетащить событие на завтра
        Открыть и проверить, что дата в диалоге события изменилась, а за сегодня нет в сетке событий
        Удалить событие
        """
        log("задаем параметры теста")
        time_start = "07:00"
        time_end = "09:00"
        comment = f'очень сложное задание {datetime.datetime.now()}'
        # на карточке дата с руским месяцем а в селекторах месяца английские поэтому локализации передергиваем туда
        # обратно. по умолчанию конечно и так должна стоить русская но особенность питона пока не переустановишь
        # остается на английской
        import locale
        locale.setlocale(locale.LC_ALL, 'Russian_Russia')
        date_today = datetime.date.today()
        date_tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%d %b")
        locale.setlocale(locale.LC_ALL, 'en_US')

        log("если нужного времени нет в календаре прокручиваем (перетаскиваем) время вверх")
        self.page_calendar.scroll_time(time_start)

        log("кликаем по календарб в сегодняшнюю дату в время старта события")
        self.page_calendar.mouse_over_on_day_and_hour(date_today, time_start, True)

        log("создаем рабочее событие")
        self.page_calendar.create_event("Событие", "Рабочее")

        log("проверяем время начала события, заполняем время конца и коментарий события")
        from pages.CoreUserCalendar.eventCard import Card
        cart_event = Card(self.driver)
        cart_event.check_open()
        dict_params = {
            "Время окончания": time_end,
            "Комментарий": comment
        }
        cart_event.fill_event(**dict_params)
        dict_params.update({"Время начала":time_start})
        cart_event.check_event(**dict_params)

        log("сохраняем событие")
        cart_event.save_event()

        log("ищем в календаре")
        my_event = self.page_calendar.find_event(comment)

        log("перетаскиваем на 1 день вперед")
        number_days = 1
        self.page_calendar.drag_event(my_event, number_days, date_today)

        log("проверяем что в текущем дне нет событий")
        self.page_calendar.check_there_are_no_events_day(date_today)

        log("открываем заведенное событие, проверяем что дата изменилась")
        self.page_calendar.open_event(comment)
        cart_event.check_open()
        cart_event.check_event(**{"Дата": date_tomorrow})

        log("Ищем сотрудника чей календарь открыт")
        from api.wrappers.staff_api_wrappers import StaffApiWrappers
        staff_wrappers = StaffApiWrappers(self.client_api)
        user_private_person = staff_wrappers.get_wan_private_person_by_search("Крошелев Александр Алексеевич")

        log("ищем и удаляем события календаря")
        date_event = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

        from api.wrappers.event_aggregator_api_wrappers import EventAggregatorApiWrappers
        event_aggregator_api = EventAggregatorApiWrappers(self.client_api)
        event_aggregator_api.get_and_del_event(comment, user_private_person, date_event)
