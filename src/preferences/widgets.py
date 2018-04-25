from typing import Set, List

from PyKF5.KWidgetsAddons import KMessageWidget
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QDialogButtonBox, QDialog, QLineEdit, QAbstractItemView, QListView

from src.gui.dialogs import ConfigurationHasChangedQMessageBox, ConfigurationResetQMessageBox
from src.gui.preferences import Ui_Dialog
from src.preferences import settings
from src.preferences.settings import SettingsManager
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

        self.settings: SettingsManager = settings.settings
        self.all_writable = tuple(self.settings.changeable_settings) + tuple(self.settings.changeable_files)

        self.message_widget = MessageWidget(self.ui.kmessagewidget)

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

        # Comment Types
        cts = self.ui.kCommentTypes
        cts.setStyleSheet(" QPushButton { text-align:left; padding: 8px; } ")

        cts.addButton().setText(_translate("Misc", "Add"))
        cts.removeButton().setText(_translate("Misc", "Remove"))
        cts.upButton().setText(_translate("Misc", "Move Up"))
        cts.downButton().setText(_translate("Misc", "Move Down"))

        cts_lv: QListView = cts.listView()
        cts_lv.setEditTriggers(QAbstractItemView.NoEditTriggers)

        cts_lv_le: QLineEdit = cts.lineEdit()
        cts_lv_le.setPlaceholderText(_translate("Misc", "Type here to add new comment types"))

        # Settings
        for setting in self.all_writable:
            setting.bind_to(self.ui, self.__update_apply_button_state)

    def __is_data_valid(self) -> bool:
        """
        Checks whether the current data in all input widgets is is_valid.

        Must call each *is_valid* method in case a warning message is necessary for a specific widget.
        """

        self.message_widget.clear()

        is_valid: bool = True
        for setting in self.all_writable:
            valid, errors = setting.valid
            if not valid:
                is_valid = False
                self.message_widget.add_messages(errors)
        return is_valid

    def __has_changed(self) -> bool:
        """
        Calls each setting's *has_changed* method.
        """

        has_changed = False
        for setting in self.all_writable:
            if setting.changed:
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

        cts = self.ui.kCommentTypes
        ct_list_view: QListView = cts.listView()

        if ct_list_view.selectionModel().selectedIndexes():
            ct_list_view.clearSelection()
            edit = cts.lineEdit()
            edit.setReadOnly(False)
            edit.setPlaceholderText(_translate("Misc", "Type here to add new comment types"))

            for btn in [cts.addButton(), cts.removeButton(), cts.upButton(), cts.downButton()]:
                btn.setEnabled(False)

        super().mousePressEvent(mouse_ev)

    def reject(self):
        """
        Action when discard button is pressed.
        """

        if self.__has_changed():
            if ConfigurationHasChangedQMessageBox().exec_():
                return

        super().reject()

    def accept(self):
        """
        Action when apply button is pressed.
        """

        for setting in self.all_writable:
            setting.save()

        self.settings.save_settings()
        self.settings.save_conf_files()

        super().accept()

    def __on_restore_default(self):
        """
        Action when restore default button is pressed.
        """

        if not ConfigurationResetQMessageBox().exec_():

            for setting in self.all_writable:
                setting.unbind_from(self.ui)
                setting.reset()
                setting.bind_to(self.ui, self.__update_apply_button_state)
                self.__update_apply_button_state()

            self.settings.save_settings()
            self.settings.save_conf_files()
