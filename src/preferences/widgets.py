from typing import Set, List

from PyKF5.KWidgetsAddons import KMessageWidget
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QDialogButtonBox, QDialog

from src.gui.preferences import Ui_Dialog
from src.preferences.preferencesabstract import AbstractUserEditableSetting
from src.preferences.settings import get_settings, MpvQcSettings

_tr = _translate = QtCore.QCoreApplication.translate


class MessageWidget:
    """A small wrapper for the KDE KMessage Widget."""

    def __init__(self, message_widget: KMessageWidget):
        self.message_widget = message_widget
        self.message_widget_messages: Set[str] = set()
        self.__update_widget()

    def add_messages(self, messages: List[str]):
        """Adds a new message. Displays the message immediately."""

        for message in messages:
            if message:
                self.message_widget_messages.add(message)
        self.__update_widget()

    def remove_message(self, message: str):
        """Removes the passed message immediately."""

        if message in self.message_widget_messages:
            self.message_widget_messages.remove(message)
            self.__update_widget()

    def clear(self):
        """Clears all messages immediately."""

        self.message_widget_messages.clear()
        self.__update_widget()

    def __update_widget(self):
        """Changes the text of the KMessageWidget."""

        self.message_widget.setText("\n".join(set(self.message_widget_messages)))
        if self.message_widget_messages:
            self.message_widget.show()
        else:
            self.message_widget.hide()


class PreferenceDialog(QDialog):
    """The dialog for the preferences."""

    def __init__(self, parent):
        super().__init__(parent=parent)

        self.settings: MpvQcSettings = get_settings()
        self.ui: Ui_Dialog = Ui_Dialog()
        self.ui.setupUi(self)

        self.all_settings: List[AbstractUserEditableSetting] = self.settings.all_editable

        self.__setup()
        # self.installEventFilter(self)

    def __setup(self):
        """Set up all editable preference objects."""

        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        self.message_widget = MessageWidget(self.ui.kmessagewidget)

        for setting in self.all_settings:
            setting.bind_preference(self.ui)
            setting.setup(update_function=self.__update_accept_button_state)

    def __is_data_valid(self) -> bool:
        """
        Checks whether the current data in all input widgets is valid.

        Must call each *is_valid* method in case a warning message is necessary for a specific widget.
        """
        self.message_widget.clear()

        valid: bool = True
        for setting in self.all_settings:
            if not setting.is_valid():
                valid = False
                self.message_widget.add_messages(setting.error_messages())
        return valid

    def __has_changed(self) -> bool:
        """Calls each setting's *has_changed* method."""

        has_changed = False
        for setting in self.all_settings:
            if setting.has_changed():
                has_changed = True

        return has_changed

    def __update_accept_button_state(self):
        """
        Updates the accept button.

        Button should be enabled if changed and valid, disable else.
        """

        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(self.__has_changed() and self.__is_data_valid())

    def mousePressEvent(self, mouse_ev: QtGui.QMouseEvent):
        """
        On mouse pressed event (pressed anywhere except the comment type widget)
        the focus needs to be removed from the comment type widget.
        """

        self.settings.comment_types.remove_focus()
        super().mousePressEvent(mouse_ev)

    def accept(self):
        """Action when accept button is pressed."""

        for setting in self.all_settings:
            setting.take_over()

        self.settings.save()

        super().accept()

    def reject(self):
        """Action when reject button is pressed."""

        if self.__has_changed():
            q = QMessageBox()
            q.setText(_tr("Misc", "Your configuration has changed.") + " " + _tr("Misc", "Discard changes?"))
            q.setIcon(QMessageBox.Warning)
            q.setWindowTitle(_tr("Misc", "Discard changes?"))
            q.addButton(_tr("Misc", "Yes"), QMessageBox.YesRole)
            q.addButton(_tr("Misc", "No"), QMessageBox.NoRole)

            if not q.exec_():
                super().reject()
        else:
            super().reject()

    def keyPressEvent(self, a0: QtGui.QKeyEvent):
        print("a")
