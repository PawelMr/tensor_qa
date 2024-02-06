from atf.api.base_api_ui import BaseApiUI
from atf.api.helpers import *


class DocumentApi(BaseApiUI):
    """
    Document
    операции над документами
    """

    def delete_doc(self, id_doc):
        """
        Document.УдалитьДокументы
        :param id_doc: ИдО документа (id:int)
        :return: словарь списков {"УдаленыВКорзину":[Массив id],"УдаленыНасовсем":[Массив id]}
        """
        params = {'ИдО': [str(id_doc)]}
        return self.client.call_rrecord("DeliveryTask.УдалитьДокументы", **params).result
