from atf.api.base_api_ui import BaseApiUI
from atf.api.helpers import *
from api.clients.event_aggregator_api import EventAggregatorApi


class EventAggregatorApiWrappers(BaseApiUI):
    """
    EventAggregator
    календарь событий
    """

    def __init__(self, client):
        super().__init__(client=client)
        self.event_api = EventAggregatorApi(client)

    def get_event_list_day_api(self, comment, user_private_person, date):
        """
        получить uuid событий за день
        :param comment: комментарий события (можно передать пустую строку что бы не фильтровать)
        :param user_private_person: PrivatePerson сотрудника чей календарь
        :param date: дата формата "2023-06-28"
        :return: список uuid ExtId
        """
        params = dict(ShiftMinutes=180,
                      calendars_uuid=(None, 'Строка'),
                      date_begin=(date, 'Строка'),
                      date_end=(date, 'Строка'),
                      excludeHolidays=False,
                      person=user_private_person)
        list_event = self.event_api.event_list_day_api(**params)[0]["hourEvents"]
        list_event_uuid = [i["ExtId"] for i in list_event if comment in i["Примечание"]]
        return list_event_uuid

    def get_and_del_event(self, comment, user_private_person, date, event_source="Работа"):
        """
        найти и удалить события
        :param comment: комментарий события (можно передать пустую строку что бы не фильтровать)
        :param user_private_person: PrivatePerson сотрудника чей календарь
        :param date: дата формата "2023-06-28"
        :param event_source: источник события
        :return: список uuid ExtId
        """
        list_event_uuid = self.get_event_list_day_api(comment, user_private_person, date)
        for i in list_event_uuid:
            self.event_api.delete_event(i, event_source)
