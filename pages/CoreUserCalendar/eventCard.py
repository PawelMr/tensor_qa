from controls import *
from atf.ui import *


@templatename("CoreUserCalendar/eventCard:Card")
class Card(DialogTemplate):
    """Карточка создания события в календаре"""

    text_description = ControlsInputArea(rus_name='Ввод описания')
    save_button = Button(SabyBy.DATA_QA, 'WTM-EventCard__saveButton', 'Кнопка сохранения')

    start_time_inp = ControlsInputText(By.CSS_SELECTOR, '.TimeStart', "Время начала")
    start_time_elm = Element(By.CSS_SELECTOR, '.TimeStart', "Время начала")
    end_time_inp = ControlsInputText(By.CSS_SELECTOR, '.TimeEnd', "Время окончания")
    end_time_elm = Element(By.CSS_SELECTOR, '.TimeEnd', 'Время конца')
    del_btn = Button(SabyBy.DATA_QA, 'WTM-EventCard__deleteButton', "Удалить")
    date_elm = Element(By.CSS_SELECTOR, '.wtm-PeriodPicker__DatePicker', 'Дата события')

    def fill_event(self, ** kwargs):
        """
        Заполнять событие
        :param kwargs: 'заполняемые параметры'
        """
        if 'Время начала' in kwargs.keys():
            self.start_time_inp.type_in(kwargs['Время начала'], human=True)
        if 'Время окончания' in kwargs.keys():
            self.end_time_inp.type_in(kwargs['Время окончания'], human=True)
        if 'Комментарий' in kwargs.keys():
            self.text_description.type_in(kwargs['Комментарий'], human=True)

    def check_event(self, ** kwargs):
        """
        Проверить событие
        :param kwargs: 'заполняемые параметры'
        """
        if 'Время начала' in kwargs.keys():
            self.start_time_inp.should_be(ExactText(kwargs['Время начала']), msg="проверка времени начала")
        if 'Время окончания' in kwargs.keys():
            self.end_time_inp.should_be(ExactText(kwargs['Время окончания']), msg="время окончания не ввелось")
        if 'Комментарий' in kwargs.keys():
            self.text_description.should_be(ExactText(kwargs['Комментарий']), msg="Комментарий не ввелся")
        if "Дата" in kwargs.keys():
            self.date_elm.should_be(TextIgnoringCase(kwargs['Дата']), msg="дата в карточке события "
                                                                          "не совпала с ожидаемой")

    def save_event(self):
        """
        сохранить событие
        """
        self.save_button.click()
        self.check_close()

    def del_event(self):
        """удалить событие"""
        self.del_btn.click()

