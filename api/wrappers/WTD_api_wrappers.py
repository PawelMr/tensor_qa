from atf.api.base_api_ui import BaseApiUI
from api.clients.WTD_api import WTDApi
from api.clients.document_api import DocumentApi
from atf.api.helpers import *


class WTDApiWrapper(BaseApiUI):
    """
    WTD
    документы графика работ
    """
    def __init__(self,client):
        super().__init__(client=client)
        self.wtd = WTDApi(client)
        self.document = DocumentApi(client)

    def get_id_doc_by_comment(self, comment):
        """
        получить список id документов по маске комментария
        Фильтр по комментарию срабатывает некорректно, отбираем вручную
        :param comment: Часть комментария (маска)
        :return: в ответе список описания документов
        """

        params_list = dict(flServerRendering=False,
                           iterative_list=True,
                           new_navigation=True,
                           translit_search=False,
                           УчитыватьИерархиюНО=True,
                           ФильтрДатаП=(None, 'Строка'),
                           ФильтрДатаПериод='Период',
                           ФильтрДатаС=(None, 'Строка'),
                           ФильтрДокументНашаОрганизация='-2',
                           ФильтрМоиДокументы='Все',
                           ФильтрПодтипДокумента=(None, 'Строка'),
                           ФильтрПоиска=(None, 'Строка'),
                           ФильтрСостояние='-1')
        list_doc = self.wtd.list(**params_list)

        list_id_doc = [i["DocID"] for i in list_doc if comment in i["NoteText"]]

        return list_id_doc

    def del_doc_by_comment(self, *args):
        """
        удаляем отгул по маске комментария
        :param args: комментарии к удалению (маска)
        """
        list_full_id = []
        for text_mask in args:
            list_id = self.get_id_doc_by_comment(text_mask)
            list_full_id.extend(list_id)
        for i in list_full_id:
            self.document.delete_doc(i)
