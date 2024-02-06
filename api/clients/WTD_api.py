from atf.api.base_api_ui import BaseApiUI
from atf.api.helpers import *


class WTDApi(BaseApiUI):
    """
    WTD
    документы графика работ
    """

    def list(self, **kwargs):
        """
        WTD.List
        получить список документов
        :param kwargs: параметры
        :return: в ответе список описания документов
        """
        params = generate_record_list(**kwargs)
        return self.client.call_rrecordset("WTD.List", **params).result
