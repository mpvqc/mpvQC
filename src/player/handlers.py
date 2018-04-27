# noinspection PyMethodMayBeStatic

"""This file will be deleted soon! :)"""


class MenubarHandler:
    pass
    # """Class for handling the menu bar actions."""
    #
    # def __resize_event(self, rev: QResizeEvent) -> bool:
    #     # print(inspect.stack()[0][3])
    #
    #     return False
    #
    # def __key_press_event(self, kev: QKeyEvent) -> bool:
    #     print(inspect.stack()[0][3])
    #
    #     pressed_key = kev.key()
    #     modifiers = self.application.keyboardModifiers()
    #
    #     if pressed_key == Qt.Key_F and modifiers == Qt.NoModifier:
    #         self.toggle_fullscreen()
    #         return True
    #
    #     return False
    #
    # # noinspection PyTypeChecker
    # def eventFilter(self, target: QObject, event: QEvent):
    #     """We have *subscribed* to the *main application's event*. Here we're delegating them to our own methods."""
    #
    #     ev_type = event.type()
    #
    #     if ev_type == QEvent.Resize:
    #         return self.__resize_event(event)
    #     elif ev_type == QEvent.KeyPress:
    #         return self.__key_press_event(event)
    #     else:
    #         return super().eventFilter(target, event)
