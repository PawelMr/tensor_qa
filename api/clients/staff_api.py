from atf.api.base_api_ui import BaseApiUI
from atf.api.helpers import *


class StaffApi(BaseApiUI):
    """
    Staff
    Управление персоналом
    """

    def wasaby_list_api(self, **kwargs):
        """
        Staff.WasabyList
        получение списка сотрудников
        :param kwargs: Параметры поиска
        :return: в ответе метода список найденных сотрудников и подразделений
        """
        params = generate_record_list(**kwargs)
        return self.client.call_rrecordset("Staff.WasabyList", **params).result
