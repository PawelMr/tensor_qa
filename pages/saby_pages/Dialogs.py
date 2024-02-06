from atf.ui import *
from controls import *


class Dialogs(Region):
    """Реестр Сообщений"""

    folders = ControlsTreeGridView(rus_name='Папки в окне Контакты')
    messages = ControlsListView(By.CSS_SELECTOR,
                                '.controls-MasterDetail_details .controls-ListViewV',
                                'Список сообщений')

    list_msg_text = CustomList(By.CSS_SELECTOR, '.controls-MasterDetail_details .controls-ListViewV '
                                                '.msg-dialogs-item__content .msg-entity-text p',
                               "Список Текстов сообщений")

    list_msg_date = CustomList(By.CSS_SELECTOR,
                               '.controls-MasterDetail_details .controls-ListViewV .msg-dialogs-item__date',
                               "Список дат сообщений")

    list_folder_to_move = ControlsMoveDialog()
    _counter_messages_in_folder = Element(SabyBy.DATA_QA, 'msg-folders-counter_total',
                                          'Счетчик сообщений в папке')

    tabs = ControlsTabsButtons(rus_name='вкладки в окне Контакты')

    list_tags_to_move = ControlsListView(By.CSS_SELECTOR,
                                         '.msg-tags-aggregate__tags [data-qa="items-container"]',
                                         "выбор тега для сообщения")
    tags = ControlsListView(By.CSS_SELECTOR, '.msg-tag-list .controls-ListViewV', 'Список тегов')
    counter_tag_message = Element(SabyBy.DATA_QA, 'tag-count-entities', 'Счетчик сообщений у тега')

    tag_message = Element(By.CSS_SELECTOR, '.tag-base', 'тег сообщения')

    def check_load_message(self):
        """Проверка загрузки реестра"""

        self.folders.check_load()
        self.messages.check_load()

    def get_message_counter_in_folder(self, folder):
        """
        получить счетчик сообщений в папке
        :param folder: 'название папки'
        :return: значение счетчика int
        """
        self.folders.check_load()
        self._counter_messages_in_folder.add_parent(self.folders.get_row(folder))
        if self._counter_messages_in_folder.is_present:
            counter = self._counter_messages_in_folder.text
        else:
            counter = 0
        return int(counter)

    def get_message_text(self, item_number):
        """
        получить текст сообщения по номеру
        :param item_number: номер сообщения
        :return: текст сообщения
        """
        text = self.list_msg_text.item(item_number).text
        return text

    def get_message_date(self, item_number=None, contains_text=None):
        """
        получить дату сообщения по номеру или тексту сообщения
        :param item_number: номер сообщения
        :param contains_text: текс сообщения
        :return: текст сообщения
        """
        if not (item_number or contains_text) or (item_number and contains_text):
            raise ValueError("Для получения даты надо передать что то одно: номер или текст")
        if not item_number:
            item_number = self.messages.item(contains_text=contains_text).position
        date = self.list_msg_date.item(item_number).text
        return date

    def select_folder(self, folder):
        """Переключение по папкам"""
        self.folders.get_row(folder).click()
        self.messages.check_load()

    def select_tab(self, tab):
        """Переключение по вкладкам"""

        self.tabs.select(contains_text=tab)
        self.messages.check_load(wait_time=20)

    def get_message_counter_in_tag(self, tag):
        """
        получить счетчик сообщений у тега
        :param tag: 'название тега'
        :return: значение счетчика int
        """
        self.tags.check_load()
        self.counter_tag_message.add_parent(self.tags.item(contains_text=tag))
        if self.counter_tag_message.is_present:
            counter = self.counter_tag_message.text
        else:
            counter = 0
        return int(counter)

    def get_message_tag(self, item_number):
        """
        получить тег сообщения
        :param item_number: 'номер сообщения'
        :return: тег сообщения
        """
        self.messages.check_load()
        self.tag_message.add_parent(self.messages.item(item_number))
        if self.tag_message.is_present:
            tag = self.tag_message.text
        else:
            tag = None
        return tag

    def move_message(self, name_folder, item_number=None, contains_text=None):

        """
        переместить сообщение в папку через контекстное меню
        :param name_folder: название папки для перемещения
        :param item_number: номер сообщения
        :param contains_text: текс сообщения
        :return: текст сообщения
        """
        if not (item_number or contains_text) or (item_number and contains_text):
            raise ValueError("Для получения даты надо передать что то одно: номер или текст")
        message = self.messages.item(item_number) if item_number else self.messages.item(contains_text=contains_text)
        message.select_menu_actions("Переместить")
        self.list_folder_to_move.check_open()
        self.list_folder_to_move.select(contains_text=name_folder)
