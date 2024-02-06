from controls import *
from atf.ui import *


class Sticker(Region):
    """
    стикер ответственного/заказчика на документе

    EDO3/Document/Sticker
    """

    employer = Link(SabyBy.DATA_QA, 'edo3-Sticker__mainInfo', 'Ответственный / Заказчик')

    def choose_responsible(self, employee):
        """
        выбрать Ответственного / Заказчика плана
        :param employee: ответственный /заказчик которого надо выбрать
        """
        self.employer.click()
        from pages.Addressee.popup import Stack
        menu_employer = Stack(self.driver)
        menu_employer.check_open()
        menu_employer.select(employee)
        menu_employer.check_close()
