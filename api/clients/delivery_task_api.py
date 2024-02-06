from atf.api.base_api_ui import BaseApiUI
from atf.api.helpers import *


class DocumentTaskApi(BaseApiUI):
    """
    DeliveryTask
    операции над документами доставки
    """

    def delete_doc(self, id_doc):
        """
        DeliveryTask.УдалитьДокументы
        :param id_doc: ИдО документа (id:int)
        :return: словарь списков {"УдаленыВКорзину":[Массив id],"УдаленыНасовсем":[Массив id]}
        """
        params = {'ИдО': [str(id_doc)]}
        return self.client.call_rrecord("DeliveryTask.УдалитьДокументы", **params).result
