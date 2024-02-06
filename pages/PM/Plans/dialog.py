from controls import *
from atf.ui import *
from atf import *
from pages.PM.Plans._scheduling.Selector import Selector


@templatename("PM/Plans/dialog:Dialog")
class Dialog(DocumentTemplate):
    """окно диалога плана работ"""
    planning_object = ControlsLookupInput(By.CSS_SELECTOR, '.controls-Render__wrapper', 'Выбор объекта планирования',
                                          catalog=Selector)

    list_status_plan_item = CustomList(By.CSS_SELECTOR, '[data-qa="cell_content"] .controls-icon_size-s',
                                       "статус пункта плана")
    list_plan_item = ControlsTreeGridView(By.CSS_SELECTOR, '.plan-PointList__body .controls-Grid',
                                          'Список пунктов плана')
    list_adding_in_plan = ControlsMenuControl(By.CSS_SELECTOR, '.controls-ListViewV__itemsContainer',
                                              'Список элементов для добавления в пустом плане')
    button_running = Button(By.CSS_SELECTOR,'.edo3-PassageButton', "Кнопка запуска и перехода ЭДО")

    def select_executor(self, executor):
        """
        выбрать исполнителя плана
        :param executor: исполниель
        """
        self.planning_object.click().select(executor)

    def check_executor(self, executor):
        """
        проверить исполнителя плана
        :param executor: исполниель
        """
        self.planning_object.should_be(ExactText(executor),
                                       msg="исполнитель не совпал с ожидаемым\n")

    def enter_comment(self, comment):
        """
        ввести комментарий
        :param comment: комментарий
        """
        self.planning_object.type_in(comment)

    def get_list_item_plan_statuses(self):
        """
        получить список статусов пунктов плана
        """
        self.list_plan_item.check_load()
        number_statuses = self.list_status_plan_item.size
        list_item_plan_statuses = []
        for i in range(1, number_statuses+1):
            list_item_plan_statuses.append(self.list_status_plan_item.item(i).get_attribute("title"))
        return list_item_plan_statuses

    def choose_employer(self, employer):
        """
        выбрать заказчика плана
        :param employer: заказчик которого надо выбрать
        """
        from pages.EDO3.Document.Sticker import Sticker
        old_employer = Sticker(self.driver, inherit_parent=True)
        old_employer.choose_responsible(employer)

    def check_employer(self, employer_standard):
        """
        проверить заказчика плана
        :param employer_standard: заказчик
        """
        employer = self.get_employer()
        assert_that(employer_standard, equal_to(employer), "заказчик не совпал с ожидаемым\n"
                                                           f"ждали {employer_standard}\n"
                                                           f"в плане: {employer}")

    def get_employer(self):
        """
        получить значение заказчика из стикера документа
        :return:
        """
        from pages.EDO3.Document.Sticker import Sticker
        old_employer = Sticker(self.driver, inherit_parent=True)
        return old_employer.employer.text

    def add_element_in_empty_plan(self, element):
        """
        создание элемента в пустом плане
        :param element: пункт из списка
        """
        self.list_adding_in_plan.select(element)

    def launch_plan(self, name_button="На выполнение", close=True):
        """
        запустить план в работу
        :param name_button: название кнопки ДО
        :param close: закрыть после запуска
        """
        self.button_running.should_be(ExactText(name_button), msg="ожидали название кнопки 'На выполнение'")
        self.button_running.click()
        self.button_running.should_not_be(ExactText(name_button), msg="Кнопка 'На выполнение' должна была сменится")
        if close:
            self.close()
            self.check_close()

    def check_point(self, comment):
        """
        проверка наличия пункта плана по комментарию
        :param comment: комментарий
        """
        self.list_plan_item.row(contains_text=comment)\
            .should_be(Present, wait_time=5, msg=f"ожидали отображения пункта с комментарием\n{comment}")
