from atf.ui import *
from atf import *

import datetime


sbis_site = "https://fix-online.sbis.ru/"
login = 'курсБазовогоЭдо'
password = "курсБазовогоЭдо123"
name_user = "Крошелев"
# login = "Демо"
# password = "Демо123"
# name_user = "йцу"
message_sender = "Тестовое сообщение " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")


class AuthorizationOnlineSbis(Region):
    """страница авторизации"""
    login_field = TextField(By.CSS_SELECTOR, '[name="Login"]', "Ввод логина")
    accept_login = Button(SabyBy.DATA_QA, 'auth-AdaptiveLoginForm__checkSignInTypeButton',
                          "Кнопка окончания ввода логина")
    password_field = TextField(By.CSS_SELECTOR, '[name="Password"]', "Ввод Пароля")
    accept_password = Button(SabyBy.DATA_QA, 'auth-AdaptiveLoginForm__signInButton',
                             "Кнопка окончания ввода пароля")
    job_choice_home = Button(By.CSS_SELECTOR, '.controls-Button_outlined_style-secondary',
                             "Кнопка выбора типа рабочего места - Личное")


class Accordion(Region):
    """Аккордеон Сбис"""
    contacts_accordion_button = Button(SabyBy.DATA_QA, 'Контакты', "кнопка аккардиона - Контакты")
    contacts_button_submenu = Button(By.CSS_SELECTOR, '[data-qa="NavigationPanels-SubMenu__head"] [data-qa="Контакты"]',
                                     "кнопка подменю аккардиона - Контакты")

    task_accordion_button = Button(SabyBy.DATA_QA, 'Задачи', "кнопка аккардиона - Задачи")
    task_button_submenu = Button(By.CSS_SELECTOR, '[data-qa="NavigationPanels-SubMenu__head"] [data-qa="Задачи"]',
                                 "кнопка подменю аккардиона - Задачи")


class Messages(Region):
    """список сообщений"""
    plus_button = Button(SabyBy.DATA_QA, 'sabyPage-addButton', "кнопка плюс (создать)")
    list_message = CustomList(By.CSS_SELECTOR, '.msg-dialogs-detail [data-qa="items-container"] [data-qa="item"]',
                              "Список сообщений на странице")

    def find_message(self, item_number=1):
        """
        получаем элемент содержащий сообщение из списка по номеру
        :param item_number: 'номер сообщения'
        :return: элемент сообщения
        """
        message_in_list = self.list_message.item(item_number)
        return message_in_list

    def find_text_message(self, item_number=1):
        """
        получаем элемент содержащий Текст сообщения из списка
        :param item_number: 'номер сообщения'
        :return: элемент содержащий текст сообщения
        """
        message_txt = self.find_message(item_number).element('.msg-entity-text p')
        return message_txt

    def find_sender_message(self, item_number=1):
        """
        получаем элемент содержащий Отправителя сообщения из списка
        :param item_number: 'номер сообщения'
        :return: элемент содержащий текст сообщения
        """
        message = self.find_message(item_number).element('[data-qa="msg-dialogs-item__addressee"]')
        return message

    def delete_message(self, item_number=1):
        """
        удаляем сообщение
        :param item_number: 'номер сообщения'
        :return:
        """
        message_in_list = self.find_message(item_number)
        message_in_list.mouse_over()
        message_in_list.element('[data-qa="controls-itemActions__action deleteToArchive"]').click()


class SendingWindow(Region):
    """окно отправки сообщений"""
    message_field = TextField(By.CSS_SELECTOR, '[data-qa="textEditor_slate_Field"] [data-slate-leaf="true"] span',
                              "поле ввода текста в сообщение")
    submit_button = Button(SabyBy.DATA_QA, 'msg-send-editor__send-button',
                           "кнопка отправки сообщения")

    close_message = Button(SabyBy.DATA_QA, 'controls-stack-Button__close',
                           "Кнопка закрытия окна отправки")


class Staff(Region):
    """окно выбора сотрудника получателя сообщения"""
    search_box = TextField(By.CSS_SELECTOR,
                           '[data-qa="addressee-selector-root"] [data-qa="controls-Render__field"] input',
                           "строка поиска сотрудников")
    find_button = TextField(By.CSS_SELECTOR,
                            '[data-qa="addressee-selector-root"] [data-qa="Search__searchButton"]',
                            "Кнопка поиска в строке поиска")
    list_employee = CustomList(By.CSS_SELECTOR,
                               '[data-qa="addressee-selector-root"] [data-qa="controls-Scroll__content"] '
                               '[data-qa="items-container"].controls-BaseControl_showActions_onhover',
                               "список найденных сотрудников")


class TestSendingMessage(TestCaseUI):

    def test(self):
        """
        -Авторизоваться на сайте https://fix-online.sbis.ru/
        -Перейти в реестр Контакты
        -Отправить сообщение самому себе
        -Убедиться, что сообщение появилось в реестре
        -Удалить это сообщение и убедиться, что удалили
        """
        self.browser.open(sbis_site)
        log("Вводим логин")
        authorization = AuthorizationOnlineSbis(self.driver)
        authorization.login_field.type_in(login)
        authorization.accept_login.click()
        log("вводим пароль")
        authorization.password_field.type_in(password)
        authorization.accept_password.click()

        if authorization.job_choice_home.is_displayed:
            authorization.job_choice_home.click()
            log("Выбрали тип рабочего мета домашнее")

        log("проверяем адрес открытой страницы")
        self.browser.should_be(UrlExact(sbis_site), msg=f'Не перешли на сайт {sbis_site}' )

        log("в аккордеоне выбираем раздел контакты")
        accordion = Accordion(self.driver)
        accordion.contacts_accordion_button.click()
        accordion.contacts_button_submenu.click()

        log("нажимаем плюс - создать сообщение")
        messages = Messages(self.driver)
        messages.plus_button.click()

        log("в боковом меню вводим фамилию сотрудника под кем авторизовались")
        staff = Staff(self.driver)
        staff.search_box.type_in(name_user)
        log("запускаем поиск, проверяем что нашелся только один сотрудник")
        staff.find_button.click()
        staff.list_employee.should_be(CountElements(1), msg="ожидали только одного сотрудника в результате поиска")
        log("кликаем по найденному сотруднику, выбираем его как получателя")
        employee = staff.list_employee.item(item_number=1)
        employee.click()

        log("заполняем и отправляем сообщение")
        sending_window = SendingWindow(self.driver)
        sending_window.message_field.type_in(message_sender)
        sending_window.submit_button.click()
        log("в аккаунте демо сообщения не закрываются автоматом")
        if login == "Демо":
            sending_window.close_message.click()

        log("проверяем текст верхнего сообщения")
        messages.find_text_message().should_be(ExactText(message_sender),
                                               msg=f"текст сообщения совпал с введенным: {message_sender}")
        log("проверяем отправителя верхнего сообщения")
        my_sender = messages.find_sender_message().text
        assert_that(name_user, is_in(my_sender), f"отправитель сообщения не совпал с ожидаемым \n"
                                                 f"ждали: {name_user}\n"
                                                 f"пришел: {my_sender}")
        log("удаляем верхнее сообщение")
        messages.delete_message()

        if messages.find_message(item_number=1).is_present:
            log("проверяем есть ли сообщения остались, сообщение с удаленным совпасть не должны")
            messages.find_text_message().should_not_be(ExactText(message_sender),
                                                       msg="текст сообщения совпал с удаленным")
        else:
            log("сообщений нет")
