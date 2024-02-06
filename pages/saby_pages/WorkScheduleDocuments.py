from atf.ui import *
from controls import *


class WorkScheduleDocuments(Region):
    """Реестр Документов графика работ"""

    create_doc = ExtControlsDropdownAddButton(rus_name="выпадающее меню создание документа")
    list_doc = ControlsTreeGridView(By.CSS_SELECTOR, '[data-qa="wtd-List"] .controls-Grid',
                                    "Список документов графика работ")

    def open_page(self):
        """открыть страницу Документов графика работ"""
        site = self.config.get('SITE') + "/page/work-schedule-documents"
        self.browser.open(site)

    def create_document(self, regulation='Отгул'):
        """
        открываем карточку создания диалога
        :param regulation: название регламента по которому создаем документ
        """
        self.create_doc.select(regulation)

    def open_doc(self, contains_text):
        """
        открыть документ из списка
        :param contains_text: примечание документа
        """
        self.list_doc.item(contains_text=contains_text).click()

    def delete_doc(self, contains_text):
        """
        удалить документ из списка
        :param contains_text: примечание документа
        :return: 'элемент карточки'
        """
        self.list_doc.row(contains_text=contains_text).open_context_menu()
        menu = self.list_doc.row(contains_text=contains_text).popup_menu
        menu.select("Удалить")
        from pages.Controls.popupTemplate import ConfirmationDialog
        confirm = ConfirmationDialog(self.driver)
        confirm.yes_button.should_be(Visible, msg="не отображается кнопка подтверждения")
        confirm.yes_button.click()
        confirm.check_close()

    def check_availability_doc(self, contains_text, availability=False):
        """
        проверяем наличие документа в списке
        :param contains_text: примечание документа
        :param availability False- должен отсутствовать, True -должен присутствовать
        """
        doc = self.list_doc.item(contains_text=contains_text)
        if availability:
            doc.should_be(Present, wait_time=5, msg="ожидали что документ есть на странице")
        else:
            doc.should_not_be(Present, wait_time=5, msg="ожидали что документа нет на странице")
