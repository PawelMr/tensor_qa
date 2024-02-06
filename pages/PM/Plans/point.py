from controls import *
from atf.ui import *


@templatename("PM/Plans/point:Dialog")
class Dialog(DocumentTemplate):
    """Диалог создания пункта плана"""
    list_works = ControlsInputArea(rus_name='Перечень работ / Описание')
    add_executor = Element(By.CSS_SELECTOR, '.plan-PointImplementers__addBtn',
                           "Добавить исполнителя, если списка исполнителя в пункте нет")
    save_button = Button(By.XPATH, '//*[@class="extControls-doubleButton_bordered-m_captionPosition-start"]'
                                   '//*[text()="Сохранить"]',
                         'кнопка сохранения')

    def enter_comment(self, comment):
        """
        ввести комментарий
        :param comment: комментарий
        """
        self.list_works.type_in(comment)

    def save_point(self):
        """ сохранить пункт плана"""
        self.save_button.click()
