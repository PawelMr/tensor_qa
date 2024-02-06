from atf.api.base_api_ui import BaseApiUI
from atf.api.helpers import *


class WorkPlanApi(BaseApiUI):
    """
    WorkPlan
    планы работ
    """

    def plans_list_api(self, **kwargs):
        """
        WorkPlan.PlansList
        получение списка сотрудников
        :param kwargs: Параметры поиска
        :return: в ответе метода список найденных сотрудников и подразделений
        """
        params = generate_record_list(**kwargs)
        return self.client.call_rrecordset("WorkPlan.PlansList", **params).result
