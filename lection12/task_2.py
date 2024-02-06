from atf.ui import *
from atf import *
from atf.exceptions import *
from lection12.task_1 import AuthorizationOnlineSbis, Accordion

import datetime


sbis_site = "https://fix-online.sbis.ru/"
login = 'курсБазовогоЭдо'
password = "курсБазовогоЭдо123"
name_folders = "тест папка " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")


class ListTask(Region):
    """раздел задач, список задач и папки с задачами"""
    list_task = CustomList(By.CSS_SELECTOR, '.Hint-ListWrapper [data-qa="row"]',
                           "список задач для просмотра")
    list_folders = CustomList(By.CSS_SELECTOR,
                              '.controls-MasterDetail_master [data-qa="items-container"] [data-qa="cell"]',
                              "список папок на вкладке задач")

    plus_button = Button(SabyBy.DATA_QA, 'sabyPage-addButton', "кнопка плюс (создать)")
    plus_folders = Button(By.CSS_SELECTOR, '[key="list-render-folderItem"]', "в меню создания пункт папка (папка плюс)")
    input_name = Button(By.CSS_SELECTOR, '.controls-InputBase__nativeField_caretFilled', "поле ввода названия папки")
    save_folders = Button(By.CSS_SELECTOR,
                          '.controls-DialogTemplate__top-area .controls-Button__text_viewMode-outlined',
                          "кнопка сохранения создаваемой папки")
    delete_folders = Button(By.CSS_SELECTOR, '[title="Удалить папку"]', "Удалить папку")
    confirm_delete_folders = Button(SabyBy.DATA_QA, 'controls-ConfirmationDialog__button-true',
                                    "подтвердить удаление")

    def find_folder(self, item_number=1):
        """
        получаем элемент содержащий папку из списка по номеру
        :param item_number: 'номер папки'
        :return: элемент сообщения
        """
        element_folder = self.list_folders.item(item_number)
        return element_folder

    def check_folder_marker_style_name(self, name_standard, item_number=1):
        """
        проверка наличия выделения и маркера на папке а так же ее название
        :param item_number: 'номер папки которую проверяем'
        :param name_standard: 'название папки'
        """
        element_folder = self.find_folder(item_number)
        element_folder.should_be(CssClass("controls-StickyBlock"), msg="ожидали класс выделения")
        element_folder.element('[data-qa="marker"]').should_be(Visible, wait_time=5, msg=" ждали маркер")
        element_folder.element(' .controls-ListEditor__columns').should_be(Attribute(title=name_standard),
                                                                           msg="название папки не совпало с ожидаемым")

    def check_folder_not_marker_not_style_name(self, name_standard, item_number=1):
        """
        проверка отсутствие выделения и маркера на папке, а так же ее название
        :param item_number: 'номер папки которую проверяем'
        :param name_standard: 'название папки'
        """
        element_folder = self.find_folder(item_number)
        element_folder.should_not_be(CssClass("controls-StickyBlock"), msg="не должно быть класса активного выделения")
        element_folder.element('[data-qa="marker"]').should_not_be(Present, wait_time=5,
                                                                   msg="маркера не должно быть")
        element_folder.element(' .controls-ListEditor__columns').should_be(Attribute(title=name_standard),
                                                                           msg="название папки не совпало с ожидаемым")

    def menu_folders(self):
        """
        вызываем контекстное меню у активной папки
        """
        active_folders = self.list_folders.find_item(By.CSS_SELECTOR, ".controls-StickyBlock")
        active_folders.element('.controls-BaseButton__wrapper').click()


class TestFolderTask(TestCaseUI):

    def test(self):
        """
        -Авторизоваться на сайте https://fix-online.sbis.ru/
        -Перейти в реестр Задачи на вкладку "В работе"
        -Убедиться, что выделена папка "Входящие" и стоит маркер.
        -Убедиться, что папка не пустая (в реестре есть задачи)
        -Перейти в другую папку, убедиться, что теперь она выделена, а со "Входящие" выделение снято.
        -Создать новую папку и перейти в неё
        -Убедиться, что она пустаяУдалить новую папку, проверить, что её нет в списке папок
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
        self.browser.should_be(UrlExact(sbis_site), msg=f'Не перешли на сайт {sbis_site}')

        log("в аккордеоне выбираем раздел Задачи")
        accordion = Accordion(self.driver)
        accordion.task_accordion_button.click()
        accordion.task_button_submenu.click()

        log("проверяем что активна папка входящие")
        list_task = ListTask(self.driver)
        list_task.check_folder_marker_style_name("Входящие", item_number=1)
        log("проверяем что есть задачи")
        list_task.list_task.should_not_be(CountElements(0), msg="задач нет")
        log("переключаемся на другую папку")
        list_task.list_folders.item(item_number=2).click()
        log("проверяем что активна другая папка, а входящие не активна")
        list_task.check_folder_marker_style_name("Не входящие", item_number=2)
        list_task.check_folder_not_marker_not_style_name("Входящие", item_number=1)
        log("создаем новую папку")
        list_task.plus_button.click()
        list_task.plus_folders.click()
        list_task.input_name.type_in(name_folders)
        list_task.save_folders.click()
        log("Проверяем что в созданной папке нет задач")
        new_folders = list_task.list_folders.find_item(By.CSS_SELECTOR, f' [title="{name_folders}"]').click()
        list_task.list_task.should_be(CountElements(0), msg="есть записи задач")
        log("удаляем созданную папку")
        new_folders.mouse_over()
        list_task.menu_folders()
        list_task.delete_folders.click()
        list_task.confirm_delete_folders.click()
        list_task.list_folders.find_item(By.CSS_SELECTOR, f' [title="{name_folders}"]')\
            .should_not_be(Present, wait_time=5)
