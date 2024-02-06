from controls import *
from atf.ui import *
from pages.Staff.selection import Stack


@templatename("EDO3/passage:Panel")
class Panel(DialogTemplate):
    """окно на выполнение"""
    executor_cl = ControlsLookupInput(By.CSS_SELECTOR, '.staffCommon-Lookup__wrapper', 'исполнитель', catalog=Stack)
    button_coordinate_day_off = Button(By.CSS_SELECTOR, '[title="Согласовать отгул"] .controls-BaseButton__text',
                                       'Кнопка отправки отгула на согласование')
