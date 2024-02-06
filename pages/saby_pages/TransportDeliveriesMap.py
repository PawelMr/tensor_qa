from atf.ui import *
from controls import *
from atf import *


class TransportDeliveriesMap(Region):
    """Бизнес/Транспорт/На карте"""
    map_container = Element(By.CSS_SELECTOR, '.SabyMaps', 'Карта')
    chauffeur_container = Element(By.CSS_SELECTOR, ".geo-extend-map-executors-panel-workload-small", "Меню водителей")
    object_maps_click = Element(By.CSS_SELECTOR, ".maplibregl-canvas", 'элемент принимающий клик по карте')
    point_of_creation = ExtControlsDropdownAddButton(SabyBy.DATA_QA, 'ruleChanger_menu', "Точка для создания документа")
    list_mark = CustomList(By.CSS_SELECTOR, '.SabyMaps-markerWrapper', "метки поставленные на карту")
    info_mark_button = Element(By.CSS_SELECTOR, ".transport-map-popup-box", 'всплывающая информация у марки')

    def refresh_page(self):
        """обновить страницу Бизнес/Транспорт/На карте"""
        self.browser.refresh()
        self.check_load_map()

    def open_page(self):
        """открыть страницу Бизнес/Транспорт/На карте"""
        site = self.config.get('SITE') + "/page/transport-deliveries-map"
        self.browser.open(site)

    def check_load_map(self):
        """Проверка загрузки карты"""
        self.map_container.should_be(Displayed, msg='Карта не отображается', wait_time=True)
        self.object_maps_click.should_be(Displayed, wait_time=True, msg="Карта не загружена")
        self.chauffeur_container.should_be(Displayed, wait_time=True, msg="Меню водителей не загружено")

    def get_card_size(self):
        """
        вернуть размер карты
        :return: словарь с размерами вида {"x":123, "y":123}
        """
        str_style = self.object_maps_click.get_attribute("style")
        str_style = str_style.replace("px;", "").replace("width: ", "").replace("height: ", "")
        list_size = str_style.split(" ")
        size_dict = dict({"x": int(list_size[0]),
                          "y": int(list_size[1])})
        return size_dict

    def create_point_on_map(self, x_offset_from_center, y_offset_from_center):
        """
        создать точку на карте со смещением от центра карты
        :param x_offset_from_center: смещение от центра по оси х
        :param y_offset_from_center: смещение от центра по оси y
        """
        chain = ActionChainsATF(self.driver)
        chain.move_to_element_with_offset(self.object_maps_click, x_offset_from_center, y_offset_from_center).\
            context_click().perform()

    def create_doc(self,  menu_item='Доставка'):
        """
        открываем карточку создания документа при наличие точки создания на карте
        :param menu_item: название пункта меню
        """
        self.point_of_creation.should_be(Visible,msg = "точки создания нет на карте")
        self.point_of_creation.select(menu_item)

    def get_mark_by_id_doc(self, id_doc):
        """
        найти в списке меток, метку по id документа
        :param id_doc: id документа в формате int
        :return: элемент метки
        """

        my_mark = self.list_mark.find_item(By.CSS_SELECTOR, f'[marker-document="{id_doc}"]')
        return my_mark

    def check_visible_mark_by_id_doc(self, id_doc, visible=True):
        """
        проверить наличие метки на карте по id документа
        :param id_doc: id документа в формате int
        :param visible: True - есть на карте, False - метки не существует вообще
        :return: элемент метки
        """
        my_mark = self.get_mark_by_id_doc(id_doc)
        if visible:
            my_mark.should_be(Visible, msg=f"Марка документа id={id_doc} не появилась на карте")
        else:
            my_mark.should_not_be(Present, msg=f"Марка  документа id={id_doc}  есть на странице")

    def check_number_mark(self, len_list_mar):
        """
        проверить количество марок на карте
        :param len_list_mar: ожидаемая длинна списка меток
        """
        assert_that(len_list_mar, equal_to(self.list_mark.size), "Количество марок на странице не совпало с ожидаемым")

    def open_doc_by_mark(self, id_doc):
        """
        открыть документ через метку по id документа
        :param id_doc: id документа в формате int
        """
        my_mark = self.list_mark.find_item(By.CSS_SELECTOR, f'[marker-document="{id_doc}"]')
        chain = ActionChainsATF(self.driver)
        chain.move_to_element(my_mark).pause(1).perform()
        chain.move_to_element(self.info_mark_button).pause(1).click(self.info_mark_button).perform()
