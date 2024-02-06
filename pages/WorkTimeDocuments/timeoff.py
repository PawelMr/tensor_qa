from controls import *
from atf.ui import *
from pages.Staff.selection import Stack


@templatename("WorkTimeDocuments/timeoff:Dialog")
class Dialog(DocumentTemplate):
    """Окно диалога создания документа графика работ (отгул)"""

    executor_cl = ControlsLookupInput(By.CSS_SELECTOR, '.staffCommon-Lookup__wrapper', 'исполнитель', catalog=Stack)
    note = RichEditorExtendedEditor(By.CSS_SELECTOR, '.richEditor_Base_textContainer', 'описание причины отгула')
    # self.note.text не срабатывал в check_doc. завел отдельный элемент
    note_read_only = Element(By.CSS_SELECTOR, '.richEditor_Base_textContainer',
                             'описание причины отгула в карточке закрытой от редактирования')
    date_in_off_day = ControlsInputDate(rus_name="Ввод даты в окне календаря")
    # self.date_in_off_day.text престало срабатывать
    # на билде online-inside_23.3220 (ver 23.3220) - 12 (21.06.2023 - 21:30:03)
    # возвращает только день недели теперь дата в атрибуте
    date_in_off_day_read_only = Element(By.CSS_SELECTOR, '.controls-Input-DatePicker input',
                                        rus_name="Ввод даты в окне календаря в карточке закрытой от редактирования")
    reason_taking_time_off = ControlsDropdownSelector(rus_name='кнопка выбора типа отгула')
    # self.reason_taking_time_off.text не срабатывал в check_doc. завел отдельный элемент
    reason_taking_time_off_read_only = Element(By.CSS_SELECTOR, '.controls-Dropdown .wtd-TimeOff__type-text',
                                               'кнопка выбора типа отгула в карточке закрытой от редактирования')
    button_to_run = ControlsButton(caption='На выполнение')
    time_start = ControlsInputMask(SabyBy.DATA_QA, 'wtd-TimeIntervalMinutes__start', 'Время начала отгула')
    time_end = ControlsInputMask(SabyBy.DATA_QA, 'wtd-TimeIntervalMinutes__end', 'Время окончания отгула')
    button_time = Button(By.CSS_SELECTOR, '.icon-TimeSkinny', 'Кнопка ввода времени')
    save_button = Button(By.CSS_SELECTOR, '[title="Сохранить"]', 'Сохранить карточку документа')

    def to_run_doc(self):
        """
        Запускаем в документооборот
        :param executor: исполнитель
        :param to_send: клик по кнопке отправить
        """
        self.button_to_run.should_be(Visible, msg="на документе нет кнопки выполнить")
        self.button_to_run.click()

    def fill_doc(self, **kwargs):
        """Заполнять задачу
        :param kwargs: 'заполняемые параметры'
        """
        if 'Исполнитель' in kwargs.keys():
            self.executor_cl.autocomplete_search(kwargs['Исполнитель'])
        if 'Причина' in kwargs.keys():
            self.note.type_in(kwargs['Причина'])
        if "Дата" in kwargs.keys():
            self.date_in_off_day.input_date(kwargs['Дата'])
        if "Тип" in kwargs.keys():
            self.choose_type_time_off(kwargs['Тип'])
        if "Время" in kwargs.keys():
            self.fill_in_time(kwargs['Время'])

    def check_doc(self, **kwargs):
        """проверяет заполненность отгула
        :param kwargs: 'заполняемые параметры'
        """
        if 'Исполнитель' in kwargs.keys():
            self.executor_cl.should_be(ExactText(kwargs['Исполнитель']))
        if 'Причина' in kwargs.keys():
            self.note_read_only.should_be(ExactText(kwargs['Причина']))
        if "Дата" in kwargs.keys():
            if self.time_start.is_displayed:
                self.date_in_off_day_read_only.should_be(Attribute(value=kwargs['Дата']))
            else:
                self.date_in_off_day.should_be(ContainsText(kwargs['Дата']))
        if "Тип" in kwargs.keys():
            self.reason_taking_time_off_read_only.should_be(ExactText(kwargs['Тип']))
        if "Время" in kwargs.keys():
            self.check_in_time(kwargs['Время'])

    def fill_in_time(self, time_period):
        """
        заполняем отгула
        :param time_period: список из строк начало времени и конец
        """
        self.button_time.click()
        self.time_start.should_be(Visible, msg="начало времени отгула не отображается")
        self.time_end.should_be(Visible, msg="начало времени отгула не отображается")
        self.time_start.type_in(time_period[0])
        self.time_end.type_in(time_period[1])

    def check_in_time(self, time_period):
        """
        проверяем время отгула
        :param time_period: список из строк начало времени и конец
        """
        self.time_start.should_be(ExactText(time_period[0]), msg="время начала отгула не совпало с ожидаемым")
        self.time_end.should_be(ExactText(time_period[1]), msg="время начала конца не совпало с ожидаемым")

    def choose_type_time_off(self, type_str):
        """
        заполняем тип отгула в окне заполнения отгула
        :param type_str: 'тип отгула'
        """
        self.reason_taking_time_off.click()
        self.reason_taking_time_off.popup_vcp.popup_cslst.item(contains_text=type_str).click()
