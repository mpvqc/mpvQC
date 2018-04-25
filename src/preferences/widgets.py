from typing import Set, List

from PyKF5.KWidgetsAddons import KMessageWidget
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QDialogButtonBox, QDialog

from src.gui.dialogs import ConfigurationHasChangedQMessageBox, ConfigurationResetQMessageBox
from src.gui.preferences import Ui_Dialog
from src.preferences.preferencesabstract import AbstractUserEditableSetting
from src.preferences.settings import get_settings, MpvQcSettings
from src.shared.references import References

_translate = QtCore.QCoreApplication.translate


class MessageWidget:
    """
    A small wrapper for the KDE KMessage Widget.
    """

    def __init__(self, message_widget: KMessageWidget):
        self.message_widget = message_widget
        self.message_widget_messages: Set[str] = set()
        self.__update_widget()

    def add_messages(self, messages: List[str]):
        """
        Adds a new message. Displays the message immediately.
        """

        for message in messages:
            if message:
                self.message_widget_messages.add(message)
        self.__update_widget()

    def remove_message(self, message: str):
        """
        Removes the passed message immediately.
        """

        if message in self.message_widget_messages:
            self.message_widget_messages.remove(message)
            self.__update_widget()

    def clear(self):
        """
        Clears all messages immediately.
        """

        self.message_widget_messages.clear()
        self.__update_widget()

    def __update_widget(self):
        """
        Changes the text of the KMessageWidget.
        """

        self.message_widget.setText("\n".join(set(self.message_widget_messages)))
        if self.message_widget_messages:
            self.message_widget.show()
        else:
            self.message_widget.hide()


class PreferenceDialog(QDialog):
    """
    The dialog for the preferences.
    """

    def __init__(self, references: References):
        super().__init__(parent=references.widget_main)

        self.references: References = references

        self.ui: Ui_Dialog = Ui_Dialog()
        self.ui.setupUi(self)

        self.settings: MpvQcSettings = get_settings()
        self.all_settings: List[AbstractUserEditableSetting] = self.settings.all_editable

        self.message_widget = MessageWidget(self.ui.kmessagewidget)

        self.__is_any_setting_changed = False

        self.__setup()

    def __setup(self):
        """
        Set up all editable preference objects.
        """

        # Buttons box
        button_box = self.ui.buttonBox

        btn_apply = button_box.button(QDialogButtonBox.Apply)
        btn_apply.setEnabled(False)
        btn_apply.clicked.connect(self.accept)
        btn_apply.setText(_translate("Misc", "Apply"))

        btn_discard = button_box.button(QDialogButtonBox.Discard)
        btn_discard.clicked.connect(self.reject)
        btn_discard.setText(_translate("Misc", "Discard"))

        btn_restore_defaults = button_box.button(QDialogButtonBox.RestoreDefaults)
        btn_restore_defaults.clicked.connect(self.__on_restore_default)
        btn_restore_defaults.setText(_translate("Misc", "Defaults"))

        # Settings
        for setting in self.all_settings:
            setting.bind_preference(self.ui)
            setting.setup(update_function=self.__update_apply_button_state)

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
        """
        Calls each setting's *has_changed* method.
        """

        has_changed = False
        for setting in self.all_settings:
            if setting.has_changed():
                has_changed = True
        return has_changed

    def __update_apply_button_state(self):
        """
        Updates the accept button.

        Button should be enabled if changed and valid, disable else.
        """

        changed = self.__has_changed()
        valid = self.__is_data_valid()

        btn_apply = self.ui.buttonBox.button(QDialogButtonBox.Apply)
        btn_apply.setEnabled(changed and valid)

    def mousePressEvent(self, mouse_ev: QtGui.QMouseEvent):
        """
        On mouse pressed event (pressed anywhere except the comment type widget)
        the focus needs to be removed from the comment type widget.
        """

        self.settings.comment_types.remove_focus()
        super().mousePressEvent(mouse_ev)

    def reject(self):
        """
        Action when reject button is pressed.
        """

        if self.__has_changed():
            if ConfigurationHasChangedQMessageBox().exec_():
                return

        super().reject()

    def accept(self):
        """
        Action when apply button is pressed.
        """

        for setting in self.all_settings:
            setting.take_over()

        self.settings.save()

        super().accept()

    def __on_restore_default(self):
        """
        Action when restore default button is pressed.
        """

        if not ConfigurationResetQMessageBox().exec_():

            for setting in self.all_settings:
                setting.reset_value()

            self.settings.save()
            super().accept()
