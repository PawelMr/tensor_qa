from atf.ui import *
from controls import *


class Plans(Region):
    """Реестр Планов"""

    list_plans = ControlsTreeGridView(By.CSS_SELECTOR, '.Hint-ListWrapper .controls-Grid', 'Список планов')
    list_plans_indicator_box = CustomList(By.CSS_SELECTOR, '.controls-StateIndicator__box', "индикаторы исполнения")
    list_plans_indicator_box_green = CustomList(By.CSS_SELECTOR, '.controls-StateIndicator__sector1',
                                                "зеленые индикаторы исполнения")
    list_plans_indicator_box_yellow = CustomList(By.CSS_SELECTOR, '.controls-StateIndicator__sector2',
                                                 "желтые индикаторы исполнения")
    list_plans_indicator_box_grey = CustomList(By.CSS_SELECTOR, '.controls-StateIndicator__emptySector',
                                               "серые индикаторы исполнения")

    search_bar = ControlsSearchInput(rus_name='Строка поиска')

    button_plus = ExtControlsDropdownAddButton(rus_name='Кнопка "плюс" создать')

    def open_page(self):
        """открыть страницу реестра планов"""
        site = self.config.get('SITE') + "/page/plans"
        self.browser.open(site)

    def check_load_plans(self):
        """Проверка загрузки реестра"""
        self.list_plans.check_load()

    def create_document(self, menu_item='План работ'):
        """
        открываем карточку создания плана/объекта планирования
        :param menu_item: название пункта меню
        """
        self.button_plus.select(menu_item)

    def receive_dict_indicator_bax(self, contains_text):
        """
        получить словарь цветов бокса индикатора
        :param contains_text: текст для поиска плана
        :return: словарь цветов
        """
        dict_class_colors = {
            "Все": self.list_plans_indicator_box,
            "Зеленые": self.list_plans_indicator_box_green,
            "Желтые": self.list_plans_indicator_box_yellow,
            "Серые": self.list_plans_indicator_box_grey,

        }
        cell = self.list_plans.item(contains_text=contains_text)
        dict_colors = {}
        for key, value in dict_class_colors.items():
            value.add_parent(cell)
            dict_colors.update({key: value.size})
        return dict_colors

    def select_menu_item(self, contains_text, menu_item):
        """
        выбираем пункт из контекстного меню
        :param contains_text: текст для поиска плана
        :param menu_item: пункт меню
        :return: словарь цветов
        """
        self.list_plans.row(contains_text=contains_text).select_menu_actions(menu_item)

    def get_link(self):
        """получить ссылку из буфера обмена"""

        self.search_bar.clear()
        self.search_bar.send_keys(Keys.CONTROL, 'v')
        link = self.search_bar.text
        return link

    def delete_doc(self, contains_text):
        """
        удалить документ из списка
        :param contains_text: примечание документа
        :return: 'элемент карточки'
        """
        self.select_menu_item(contains_text, "Удалить")
        from pages.Controls.popupTemplate import ConfirmationDialog
        confirm = ConfirmationDialog(self.driver)
        confirm.yes_button.should_be(Visible, msg="не отображается кнопка подтверждения")
        confirm.yes_button.click()
        confirm.check_close()

    def open_plans(self, comment):
        """
        открываем карточку плана по комментарию
        :param comment: комментарий
        """
        self.list_plans.find_cell_by_column_number(comment, 2).click()

    def check_list_plans(self, comment, presence=True):
        """
        проверяем наличие плана по комментарию
        :param comment: комментарий
        :param presence: наличия пункта плана
        """
        plan = self.list_plans.row(contains_text=comment)
        if presence:
            plan.should_be(Present, wait_time=5, msg="ожидали что документ есть на странице")
        else:
            plan.should_not_be(Present, wait_time=5, msg="ожидали что документа нет на странице")