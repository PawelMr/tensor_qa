from atf.ui import *
from controls import *
from atf import *


class Calendar(Region):
    """Календарь"""

    hours_cslst = CustomList(By.CSS_SELECTOR, '.WTM-Days__HoursItem', 'заголовки строк часов в календаре ')
    hover_day = Element(By.CSS_SELECTOR, '.WTM-Days__DayGrid_HoverBlock', 'Подсветка дня в календаре')
    hours_panel = Element(By.CSS_SELECTOR, '.WTM-Days__Hours', 'Полоска с часам слева')
    time_display = Element(By.CSS_SELECTOR, ".WTM-Days__DayGrid_HoverBlock_caption",
                           'элемент отображения времени в наведенной ячейки')
    object_display = Element(By.CSS_SELECTOR, ".wtm-EndlessPanel__glass",
                           'элемент принимающий клик')
    container_table_calendar = Element(By.CSS_SELECTOR, '.wtm-EndlessPanel__scroll-container', "Контейнер календаря")
    container_table_heading_calendar = Element(By.CSS_SELECTOR, '.DaysHeader', "Контейнер шапки календаря")

    popup_menu = ControlsPopup(rus_name="Меню создания события в календаре")
    list_event = CustomList(SabyBy.DATA_QA, 'WTM-Days__Event', "Список Событий календаря")

    def open_page(self):
        """открыть страницу календаря"""
        site = self.config.get('SITE') + "/page/calendar/#"
        self.browser.open(site)

    def check_load_calendar(self):
        """Проверка загрузки реестра"""
        self.hours_panel.should_be(Displayed, wait_time=True, msg="Страница календаря не загружена")

    @staticmethod
    def get_date_attr_format(date_):
        """
        Получаем Атрибут data-qa, нужный для аттрибута даты в верстке календаря
        :param date_: дата формата datetime
        :return: значение атрибута data-qa
        """
        return f'WTM-Days__Day_{date_.strftime("%a %b %d %Y")} 00:00:00 GMT+0300 (Москва, стандартное время)'

    def get_day_col(self, day_date):
        """Получить элемент колонки дня
        :param day_date: дата формата datetime
        :return: element
        """

        col_pos = self.get_date_attr_format(day_date)
        day_col = Element(SabyBy.DATA_QA, col_pos, f'Колонка дня {day_date}')
        day_col.init(self.driver)
        return day_col

    def mouse_over_on_day_and_hour(self, day, hour, click = False):
        """Навести мышкой на определённый час дня при передачи click кликнуть
        :param day: дата формата datetime
        :param hour: Час Формата hh:00
        :param click: кликнуть в наведенную ячейку
        """

        hour_elm = self.hours_cslst.item(contains_text=hour)
        day_elm = self.get_day_col(day)
        self.hover_day.add_parent(day_elm)
        day_elm.should_be(Visible, wait_time=True, msg="элемент дня не отображается")
        offset_x = day_elm.coordinates.get('x') - day_elm.size.get('width') / 2
        hour_elm.mouse_over_with_offset(x=offset_x)
        if click:
            chain = ActionChainsATF(self.driver)
            chain.click(self.hover_day).perform()

    def check_there_are_no_events_day(self, day):
        """
        проверяем что в переданном дне нет событий
        :param day: дата формата datetime
        :return:
        """
        day_elm = self.get_day_col(day)
        event = day_elm.element('[data-qa="WTM-Days__Event"]')
        event.should_not_be(Present, msg="в переданом дне есть событие")

    def scroll_time(self, time, direction_up=True):
        """
        проверяем отображается ли время в календаре и прокручиваем вверх или в низ
        :param time: время
        :param direction_up: скрол вверх False-вниз
        """
        hour_elm = self.hours_cslst.item(contains_text=time)
        if not hour_elm.is_displayed:
            direction = 1 if direction_up else -1
            chain = ActionChainsATF(self.driver)
            chain.click_and_hold(self.hours_panel).pause(1).move_by_offset(0, direction * 300).release().perform()

    def create_event(self, *args):
        """
        создать событие
        :param args: путь в меню до события
        """
        self.popup_menu.select(*args)

    def find_event(self, comment):
        """
        найти событие по комментарию
        :param comment: комментарий
        :return событие
        """
        my_event = self.list_event.item(with_text=comment)
        return my_event

    def drag_event(self, event, number_days, data):
        """
        перетащить событие на количество дней
        :param event: событие
        :param number_days: количество дней (меньше нуля тащим влево, больше нуля в право)
        :param data: дата для на экране для определения ширины столбца формата datetime
        """
        chain = ActionChainsATF(self.driver)
        width = self.get_day_col(data).size.get('width') * number_days
        chain.click_and_hold(event).pause(3).move_by_offset(width, 0).release().perform()

    def open_event(self, comment):
        """
        открыть событие по комментарию
        :param comment: комментарий
        """
        chain = ActionChainsATF(self.driver)
        my_event = self.list_event.item(with_text=comment)
        chain.pause(1).click(my_event).perform()

