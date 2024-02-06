from atf.ui import *
from pages.saby_pages.AuthOnline import AuthOnline
from pages.saby_pages.Dialogs import Dialogs
from atf import *


class TestMessage(TestCaseUI):
    """
    Tесты проверки страницы 'контакты'
    """

    @classmethod
    def setUpClass(cls):
        """для всего класса тестов авторизация и создание экземпляра класса проверки сообщений"""
        AuthOnline(cls.driver).auth(cls.config.get('USER_LOGIN'), cls.config.get('USER_PASSWORD'))
        cls.page_messages = Dialogs(cls.driver)

    def setUp(self):
        """для каждого теста проверка прогрузки сообщений"""
        self.page_messages.check_load_message()

    def test_01(self):
        """
        -Переместить запись в другую папку
        -проверить перемещение (убедиться в: наличии в папке и увеличении счётчика).
        -вернуть обратно.
        """
        log("получаем счетчик сообщений для папки Папка_1")
        count_messages_old = self.page_messages.get_message_counter_in_folder("Папка_1")

        log("запоминаем текст первого сообщения")
        text_message = self.page_messages.messages.item(1).text
        self.page_messages.move_message("Папка_1", 1)

        log("получаем счетчик сообщений для папки Папка_1 и сравнить с предыдущим значением")
        count_messages_new = lambda: self.page_messages.get_message_counter_in_folder("Папка_1")
        assert_that(count_messages_old+1, equal_to(count_messages_new),
                    "после переноса сообщения счетчик отличается на не 1\n"
                    f"был: {count_messages_old}\n"
                    f"стал: {count_messages_new}",
                    and_wait(5))

        log("Перейти в папку Папка_1, проверить наличие сообщения")
        self.page_messages.select_folder("Папка_1")
        self.page_messages.messages.item(1).should_be(ExactText(text_message),
                                                      msg=f"верхнее сообщение в папке не совпадает с перенесенным\n"
                                                          f"переносили: {text_message}")

        log("Вернуть сообщение в 'Все сообщения' переместиться в 'Все сообщения'")
        self.page_messages.move_message("Все сообщения", 1)
        self.page_messages.select_folder("Все сообщения")

    def test_02(self):
        """
        Проверить, что дата сообщения в реестре Диалоги совпадает с датой в Чатах
        """
        log("открыть вкладку Диалоги у первого сообщения получить текст и дату")
        self.page_messages.select_tab("Диалоги")
        text = self.page_messages.get_message_text(1)
        date = self.page_messages.get_message_date(1)

        log("перейти в вкладку чаты, получить дату сообщения с тем же текстом, сравнить")
        self.page_messages.select_tab("Чаты")
        date_in_chat = self.page_messages.get_message_date(contains_text=text)
        assert_that(date, equal_to(date_in_chat),
                    f"у сообщения с текстом '{text}' не совпали даты"
                    f"в диалоге : {date}\n"
                    f"в чате: {date_in_chat}",)

        log("вернуться в Диалоги")
        self.page_messages.select_tab("Диалоги")

    def test_03(self):
        """
        -Пометить сообщение эталонным тегом.
        -Убедиться, что тег появился на сообщении,
        -Cчётчик тегов увеличился.
        -Снять тег и проверить.
        """
        old_counter_teg = self.page_messages.get_message_counter_in_tag("Эталонный тег")
        log("ставим пометку эталонного тега на первое сообщение")
        self.page_messages.messages.item(1).select_menu_actions("Пометить")
        self.page_messages.list_tags_to_move.item(contains_text="Эталонный тег").click()

        log("Проверяем наличие тега на сообщении")
        tag_message = lambda: self.page_messages.get_message_tag(1)
        assert_that("Эталонный тег", equal_to(tag_message), f"Ожидали на сообщении тег 'Эталонный тег' \n"
                                                            f"на сообщении тег: {tag_message}",
                    and_wait(5))
        log("проверяем счетчик сообщений тега")
        new_counter_teg = self.page_messages.get_message_counter_in_tag("Эталонный тег")
        assert_that(old_counter_teg + 1, equal_to(new_counter_teg),
                    "после пометки сообщения тегом счетчик отличается на не 1\n"
                    f"был: {old_counter_teg}\n"
                    f"стал: {new_counter_teg}")

        log("снимаем пометку эталонного тега на первое сообщение")
        self.page_messages.messages.item(1).select_menu_actions("Пометить")
        self.page_messages.list_tags_to_move.item(contains_text="Эталонный тег").click()
        log("Проверяем наличие тега на сообщении")
        tag_message = lambda: self.page_messages.get_message_tag(1)
        assert_that(None, equal_to(tag_message), f"Ожидали на сообщении отсутствие тега \n"
                                                 f"на сообщении тег: {tag_message}",
                    and_wait(5))
        log("проверяем счетчик сообщений тега")
        new_counter_teg = self.page_messages.get_message_counter_in_tag("Эталонный тег")
        assert_that(old_counter_teg, equal_to(new_counter_teg),
                    "после пометки сообщения тегом счетчик отличается на не 1\n"
                    f"был: {old_counter_teg}\n"
                    f"стал: {new_counter_teg}")
