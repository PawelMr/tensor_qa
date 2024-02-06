from controls import *
from atf.ui import *
from atf import *


@templatename("WorksManagement/Wasaby/Transport/DeliveryTask/dialog:Dialog")
class Dialog(DocumentTemplate):
    """окно создания доставки"""

    save_button = Button(By.CSS_SELECTOR, '[title="Сохранить"]', 'Сохранить карточку документа')
    content_container = Element(SabyBy.DATA_QA, "edo3-Dialog__tab-main", "Контейнер содержащий параметры документа")
    date_number_field = ControlsEditableAreaView(rus_name="Дата номер документа")

    def save_doc(self):
        """
        сохранить документ
        """
        self.save_button.click()

    def get_id_doc(self):
        """
        получить id документа
        :return: id документа в формате int
        """
        css_class = self.content_container.css_class
        list_css_class = css_class.split(" .")
        list_css_class_id = [i for i in list_css_class if "edo3-Dialog__drag-and-drop-area--" in i]
        assert_that(1, equal_to(len(list_css_class_id)), "елемент содержит больше одного класса с id")
        id_doc = int(list_css_class_id[0].replace("edo3-Dialog__drag-and-drop-area--",""))
        return id_doc

    def get_date_number(self):
        """
        получить дату номер документа
        :return: дата номер документа
        """
        return self.date_number_field.text

    def check_parameter_doc(self,**kwargs):
        """
        Проверить параметры документа
        :param kwargs: параметры документа
        """
        if 'Дата и номер' in kwargs.keys():
            date_number_doc_open = self.get_date_number()
            assert_that(kwargs['Дата и номер'], equal_to(date_number_doc_open),
                        "дата номер открытого документа не совпал с ожидаемыми")
        if 'ID' in kwargs.keys():
            id_doc_open = self.get_id_doc()
            assert_that(kwargs['ID'], equal_to(id_doc_open),
                        "id открытого документа не совпал с ожидаемым")
