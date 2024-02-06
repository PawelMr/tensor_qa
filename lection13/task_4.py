from atf.ui import *
from pages.saby_pages.AuthOnline import AuthOnline
from pages.saby_pages.Plans import Plans
from atf import *


class TestPlane(TestCaseUI):
    """Проверка страницы планы"""

    @classmethod
    def setUpClass(cls):
        """для всего класса тестов авторизация и создание экземпляра класса проверки планов"""
        AuthOnline(cls.driver).auth(cls.config.get('USER_LOGIN'), cls.config.get('USER_PASSWORD'),
                                    cls.config.get('SITE_PLANS'))
        cls.page_planes = Plans(cls.driver)

    def setUp(self):
        """для каждого теста проверка прогрузки списка планов"""
        self.page_planes.check_load_plans()

    def test_01(self):
        """
        Проверить, что в реестре отображается шкала выполнения (2 зеленых прямоугольника, 2 жёлтых и 4 серых)
        Получить ссылку в буфер обмена и открыть её в новой вкладке (эталонный url НЕ использовать).
        Проверить наличие 4 пунктов и их статусы.
        """
        log("Проверяем индикатор выполнения плана по цветам")
        standard_dict_colors = {
            "Все": 8,
            "Зеленые": 2,
            "Желтые": 2,
            "Серые": 4,

        }
        dict_colors = self.page_planes.receive_dict_indicator_bax("Крошелев Александр Алексеевич /"
                                                                  " проверка индикатора выполнения")
        assert_that(standard_dict_colors, equal_to(dict_colors), f"проверка цветов индикатора пришло: {dict_colors}")

        log("открываем план в новой вкладке")
        self.page_planes.select_menu_item("Крошелев Александр Алексеевич / проверка индикатора выполнения",
                                          "Скопировать в буфер")
        link = self.page_planes.get_link()
        self.browser.switch_to_opened_window(lambda: self.browser.create_new_tab(link))

        log("проверяем Статусы")
        from pages.PM.Plans.dialog import Dialog
        plan = Dialog(self.driver)
        plan.check_open()
        list_item_statuses = plan.get_list_item_plan_statuses()
        assert_that(['Выполнен', 'Готово', 'Не выполнен', 'В работе'], equal_to(list_item_statuses),
                    "проверяем список статусов пунктов плана")
