from controls import *
from atf.ui import *


@templatename("Controls/popupTemplate:ConfirmationDialog")
class ConfirmationDialog(ContainerPopup):
    """окно подтверждения удаления"""
    yes_button = Button(SabyBy.DATA_QA, "controls-ConfirmationDialog__button-true", "Кнопка подтверждения действия")

    def confirm(self):
        """
        подтвердить действие
        """
        self.yes_button.click()
