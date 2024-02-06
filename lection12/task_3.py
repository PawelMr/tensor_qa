from atf.ui import *
from atf import *
from atf.exceptions import *
from lection12.task_1 import AuthorizationOnlineSbis


sbis_site = "https://fix-online.sbis.ru/"
sbis_task = "https://fix-online.sbis.ru/opendoc.html?guid=ce2a675d-e129-43e5-853e-e7056878a87b&client=12511108"
login = 'курсБазовогоЭдо'
password = "курсБазовогоЭдо123"
executor = autor = "Крошелев А.А."
date = "14.02.21"
number = "437"
descript = "123"


class Task(Region):
    """карточка задачи открытая в отдельном окне"""
    date_task = Element(By.CSS_SELECTOR, '.controls-Tabs__content_text .controls-EditableArea__Text__inner',
                        "дата задачи")
    number_task = Element(By.CSS_SELECTOR, '.controls-Tabs__content_additionaltext .controls-EditableArea__Text__inner',
                          "номер задачи")
    descript_task = Element(By.CSS_SELECTOR, '[data-qa="controls-Render__field"] p',
                            "Содержание задачи")
    executor_task = Element(By.CSS_SELECTOR, '.edws-StaffChooser__itemTpl-name',
                            "исполнитель задачи")
    autor_task = Element(By.CSS_SELECTOR, '[data-qa="edo3-Sticker__mainInfo"]',
                         "автор задачи")


class TestTaskReference(TestCaseUI):

    def test(self):
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

        log("открываем новую вкладку")
        new_window = lambda: self.browser.create_new_tab(sbis_task)
        self.browser.switch_to_new_window(action=new_window)
        self.browser.should_be(TitleExact(f"Задача №{number} от {date}"), msg="не совпал заголовок страницы, ожидали: "
                                                                              f"Задача №{number} от {date}")

        log("проверяем параметры задачи")
        task = Task(self.driver)
        task.descript_task.should_be(ExactText(descript), msg="описание не совпало с ожидаемым значением")
        task.executor_task.should_be(ExactText(executor), msg="исполнитель не совпал с ожидаемым значением")
        task.autor_task.should_be(ExactText(autor), msg="автор не совпал с ожидаемым значением")
        task.date_task.should_be(ExactText(date), msg="дата не совпала с ожидаемым значением")
        task.number_task.should_be(ExactText(number), msg="номер не совпал с ожидаемым значением")
