from atf.api.base_api_ui import BaseApiUI
from atf.api.helpers import *
from api.clients.work_plan_api import WorkPlanApi


class WorkPlanApiWrappers(BaseApiUI):
    """
    WorkPlan
    планы работ
    """

    def __init__(self, client):
        super().__init__(client=client)
        self.works_plan = WorkPlanApi(client)

    def get_list_id_plans(self, mask_comment=None, item_comment=None):
        """
        получение списка id документов планов работ
        :param mask_comment: комментарий плана (значение None не проверяем)
        :param item_comment: комментарий пункта плана полное совпадение (значение None не проверяем)
        :return: в ответе метода список id документов с совпадающим комментарием плана или комментарием пункта
        """
        params = dict(iterative_list=True,
                      new_navigation=True,
                      translit_search=False,
                      МастерФильтр=6,
                      СостояниеПлана=-1,
                      СостояниеПунктов=0,
                      ФильтрДатаП=(None, 'Строка'),
                      ФильтрДатаС=(None, 'Строка'),
                      ФильтрПоМаске=(mask_comment, 'Строка'),
                      ФильтрПринадлежность=0)
        list_doc = self.works_plan.plans_list_api(**params)
        id_list = []
        if mask_comment:
            id_doc_mask_comment = [i["@Документ"] for i in list_doc if mask_comment in i["Проект.Описание"]]
            id_list.extend(id_doc_mask_comment)
        if item_comment:
            id_doc_item_comment = [i["@Документ"] for i in list_doc if item_comment in i["Пункты"]]
            id_list.extend(id_doc_item_comment)
        return id_list
