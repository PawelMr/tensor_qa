from atf.api.base_api_ui import BaseApiUI
from atf.api.helpers import *


class EventAggregatorApi(BaseApiUI):
    """
    EventAggregator
    календарь событий
    """

    def event_list_day_api(self, **kwargs):
        """
        EventAggregator.EventListDay
        получение списка событий календаря формата день
        :param kwargs: Параметры поиска
        :return: в ответе метода список найденных сотрудников и подразделений
        """
        params = generate_record_list(**kwargs)
        return self.client.call_rrecordset("EventAggregator.EventListDay", **params).result

    def delete_event(self, event_uuid, event_source="Работа"):
        """
        EventAggregator.DeleteEvent
        удалить событие
        :param event_source: источник события
        :param event_uuid: UUID события
        :return: логическое значение
        """
        params = {"event_source": event_source,
                  "event_uuid": event_uuid}
        return self.client.call_rvalue("EventAggregator.DeleteEvent", **params).result
