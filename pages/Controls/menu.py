from controls import *
from atf.ui import *


@templatename("Controls/menu:Popup")
class Popup(DialogTemplate):
    """окно контекстного меню"""
    menu = ControlsMenuControl(rus_name="Контекстное меню")
