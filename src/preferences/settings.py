import copy
import io
import json
import locale
import os
from abc import ABC, abstractmethod
from typing import Dict, List, Set

from PyKF5.KWidgetsAddons import KMessageWidget
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QListView, QAbstractItemView, QLineEdit, QDialogButtonBox, QMessageBox, QDialog, QComboBox
from appdirs import unicode

from src.gui.preferences import Ui_Dialog
from src.preferences import configuration

try:
    to_unicode = unicode
except NameError:
    to_unicode = str

_tr = _translate = QtCore.QCoreApplication.translate


# noinspection PyAttributeOutsideInit

# from PyKF5.KWidgetsAddons import KMessageWidget, KEditListWidget


class JsonLoader:
    JSON_SETTINGS = None
    instance = None

    def __init__(self):
        if JsonLoader.JSON_SETTINGS is None:
            settings_json = configuration.get_paths().settings_json
            if not os.path.isfile(settings_json):
                with io.open(settings_json, 'w', encoding='utf8') as outfile:
                    str_ = json.dumps({}, indent=4, separators=(',', ': '), ensure_ascii=False)
                    outfile.write(to_unicode(str_))
            with open(settings_json) as df:
                JsonLoader.JSON_SETTINGS = json.load(df)

    @staticmethod
    def get_value(key: str):
        if JsonLoader.instance is None:
            JsonLoader.instance = JsonLoader()

        dictionary: Dict = JsonLoader.JSON_SETTINGS

        return dictionary.get(key)


class AbstractSetting(ABC):

    def __init__(self):
        val = JsonLoader.get_value(self.name)
        self._value = self.read_string_value_from_json(val, bool(val))

    # def __str__(self):
    #     return "{}: {}".format(self.name, self.value)

    def read_string_value_from_json(self, string, is_not_none: bool):
        if is_not_none:
            return string
        else:
            return self.default_value

    @property
    def name(self):
        raise NotImplementedError

    @property
    def default_value(self):
        raise NotImplementedError

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value is None:
            self._value = self.default_value
        else:
            self._value = value


class AbstractSettingEditable(AbstractSetting):

    def __init__(self):
        super().__init__()
        self.ui = None
        self.mw = None

    def bind_preference(self, ui: Ui_Dialog, message_widget):
        self.ui = ui
        self.mw = message_widget

    def is_valid(self) -> bool:
        return True

    @abstractmethod
    def provide(self, update_function):
        raise NotImplementedError

    @abstractmethod
    def has_changed(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def push_to_config(self):
        raise NotImplementedError


class SettingVersion(AbstractSetting):

    @property
    def name(self):
        return "version"

    @property
    def default_value(self):
        return "0.0.1"


class SettingPlayerLastPlayed(AbstractSetting):

    @property
    def name(self):
        return "player_last_played_directory"

    @property
    def default_value(self):
        return ""


class SettingNickname(AbstractSettingEditable):

    def bind_preference(self, ui: Ui_Dialog, message_widget):
        super().bind_preference(ui, message_widget)
        self.nickname_LineEdit = self.ui.authorLineEdit

    @property
    def name(self):
        return "nickname"

    @property
    def default_value(self):
        return "nickname"

    def provide(self, update_function):
        self.nickname_LineEdit.setPlaceholderText(_tr("Misc", "Type here to change the nick name"))
        self.nickname_LineEdit.setText(self.value)
        self.nickname_LineEdit.textChanged.connect(update_function)

    def is_valid(self) -> bool:
        message = _tr("Misc", "Nick name must not be empty")

        if bool(self.nickname_LineEdit.text()):
            self.mw.remove_message(message)
            return True
        else:
            self.mw.add_message(message)
            return False

    def has_changed(self) -> bool:
        text_ = self.value == self.nickname_LineEdit.text()
        return not text_

    def push_to_config(self):
        self.value = self.nickname_LineEdit.text()


class SettingLanguage(AbstractSettingEditable):

    @property
    def name(self):
        return "language"

    @property
    def default_value(self):
        default_locale = locale.getdefaultlocale()[0]
        if default_locale.startswith("de"):
            return _tr("Dialog", "German")
        else:
            return _tr("Dialog", "English")

    def bind_preference(self, ui: Ui_Dialog, message_widget):
        super().bind_preference(ui, message_widget)
        self.language_box: QComboBox = ui.comboBox
        self.languages = {
            _tr("Dialog", "English"): "English",
            _tr("Dialog", "German"): "German"
        }

    def provide(self, update_function):
        self.language_box.setCurrentIndex(max(self.language_box.findText(_tr("Dialog", self.value)), 0))
        self.language_box.currentIndexChanged.connect(update_function)

    def has_changed(self) -> bool:
        return not self.value == self.languages.get(self.language_box.currentText())

    def push_to_config(self):
        self.value = self.languages.get(self.language_box.currentText())


class SettingCommentTypes(AbstractSettingEditable):

    @property
    def name(self):
        return "comment_types"

    @property
    def default_value(self):
        return ["Spelling", "Punctuation", "Translation", "Phrasing", "Timing", "Typeset", "Note"]

    def bind_preference(self, ui: Ui_Dialog, message_widget):
        super().bind_preference(ui, message_widget)
        self.comment_types_ui = self.ui.kCommentTypes
        self.comment_type_english = {}
        for ct in self.default_value:
            self.comment_type_english.update({_tr("Misc", ct): ct})

    def provide(self, update_function):
        cts = self.comment_types_ui
        cts.setStyleSheet(" QPushButton { text-align:left; padding: 8px; } ")

        cts_lv: QListView = cts.listView()
        cts_lv.setEditTriggers(QAbstractItemView.NoEditTriggers)

        cts_lv_le: QLineEdit = cts.lineEdit()
        cts_lv_le.setPlaceholderText(_tr("Misc", "Type here to add new comment types"))

        cts.addButton().setText(_tr("Misc", "Add"))
        cts.removeButton().setText(_tr("Misc", "Remove"))
        cts.upButton().setText(_tr("Misc", "Move Up"))
        cts.downButton().setText(_tr("Misc", "Move Down"))

        for ct in self.value:
            item = _tr("Misc", ct)
            self.comment_types_ui.insertItem(item)

        self.comment_types_ui.changed.connect(update_function)

    def is_valid(self) -> bool:
        ct_items: List[str] = self.comment_types_ui.items()

        items_are_not_empty = bool(ct_items)
        m = _tr("Misc", "At least one comment type is required")
        if not items_are_not_empty:
            self.mw.add_message(m)
        else:
            self.mw.remove_message(m)

        no_item_empty_str = True
        m = _tr("Misc", "Each comment type needs a valid name")
        for ct_item in ct_items:
            message = m
            if not ct_item:
                no_item_empty_str = False
                self.mw.add_message(message)
                break
            else:
                self.mw.remove_message(message)
        else:
            self.mw.remove_message(m)

        return items_are_not_empty and no_item_empty_str

    def has_changed(self) -> bool:
        return not self.value == [self.comment_type_english.get(x, x) for x in self.comment_types_ui.items()]

    def push_to_config(self):
        self.value = [self.comment_type_english.get(x, x).strip() for x in self.comment_types_ui.items()]

    def remove_focus(self):
        # Remove selection from comment type items
        ct_list_view: QListView = self.comment_types_ui.listView()

        if ct_list_view.selectionModel().selectedIndexes():
            ct_list_view.clearSelection()
            edit = self.comment_types_ui.lineEdit()
            edit.setReadOnly(False)
            edit.setPlaceholderText(_tr("Misc", "Type here to add new comment types"))


class SettingAutoSaveEnabled(AbstractSettingEditable):

    @property
    def name(self):
        return "autosave_enabled"

    @property
    def default_value(self):
        return True

    def read_string_value_from_json(self, string, is_not_none: bool):
        if is_not_none:
            return bool(string)
        else:
            return self.default_value

    def bind_preference(self, ui: Ui_Dialog, message_widget):
        super().bind_preference(ui, message_widget)
        self.chkBox = ui.autoSaveEnabledCheckBox_4

    def provide(self, update_function):
        self.chkBox.setChecked(self.value)
        self.chkBox.stateChanged.connect(update_function)

    def is_valid(self) -> bool:
        return True

    def has_changed(self) -> bool:
        return not self.value == self.chkBox.isChecked()

    def push_to_config(self):
        self.value = self.chkBox.isChecked()


class SettingAutoSaveInterval(AbstractSettingEditable):

    @property
    def name(self):
        return "autosave_interval_seconds"

    @property
    def default_value(self):
        return 90

    def read_string_value_from_json(self, string, is_not_none: bool):
        if is_not_none:
            return int(string)
        else:
            return self.default_value

    def bind_preference(self, ui: Ui_Dialog, message_widget):
        super().bind_preference(ui, message_widget)
        self.spinBox = ui.autosaveSpinBox_4

    def provide(self, update_function):
        self.spinBox.setValue(int(self.value))
        self.spinBox.valueChanged.connect(update_function)

    def is_valid(self) -> bool:
        return True

    def has_changed(self) -> bool:
        return not self.value == self.spinBox.value()

    def push_to_config(self):
        self.value = self.spinBox.value()


class SettingQcDocumentWriteVideoPathToFile(AbstractSettingEditable):

    @property
    def name(self):
        return "qc_doc_write_video_path_to_file"

    @property
    def default_value(self):
        return True

    def read_string_value_from_json(self, string, is_not_none: bool):
        if is_not_none:
            return bool(string)
        else:
            return self.default_value

    def bind_preference(self, ui: Ui_Dialog, message_widget):
        super().bind_preference(ui, message_widget)
        self.chkBox = ui.saveVideoPathCheckBox

    def provide(self, update_function):
        self.chkBox.setChecked(self.value)
        self.chkBox.stateChanged.connect(update_function)

    def is_valid(self) -> bool:
        return True

    def has_changed(self) -> bool:
        return not self.value == self.chkBox.isChecked()

    def push_to_config(self):
        self.value = self.chkBox.isChecked()


class SettingQcDocumentWriteNickNameToFile(AbstractSettingEditable):

    @property
    def name(self):
        return "qc_doc_write_nick_name_to_file"

    @property
    def default_value(self):
        return True

    def read_string_value_from_json(self, string, is_not_none: bool):
        if is_not_none:
            return bool(string)
        else:
            return self.default_value

    def bind_preference(self, ui: Ui_Dialog, message_widget):
        super().bind_preference(ui, message_widget)
        self.chkBox = ui.saveNickNameCheckBox

    def provide(self, update_function):
        self.chkBox.setChecked(self.value)
        self.chkBox.stateChanged.connect(update_function)

    def is_valid(self) -> bool:
        return True

    def has_changed(self) -> bool:
        return not self.value == self.chkBox.isChecked()

    def push_to_config(self):
        self.value = self.chkBox.isChecked()


class MessageWidget:
    """ A small wrapper for the KDE KMessage Widget."""

    def __init__(self, message_widget: KMessageWidget):
        self.message_widget = message_widget
        self.message_widget_messages: Set[str] = set()
        self.__update_widget()

    def add_message(self, message: str):
        """Adds a new message. Displays the message immediately."""

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

    def __init__(self):
        super().__init__()

        self.settings: MpvQcSettings = get_settings()
        self.ui: Ui_Dialog = Ui_Dialog()
        self.ui.setupUi(self)

        self.all_settings: List[AbstractSettingEditable] = self.settings.all_editable

        self.__setup()

    def __setup(self):
        """Set up all editable preference objects."""

        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        message_widget = MessageWidget(self.ui.kmessagewidget)

        for setting in self.all_settings:
            setting.bind_preference(self.ui, message_widget)
            setting.provide(update_function=self.__update_accept_button_state)

    def __is_data_valid(self) -> bool:
        """
        Checks whether the current data in all input widgets is valid.

        Must call each *is_valid* method in case a warning message is necessary for a specific widget.
        """

        valid: bool = True
        for setting in self.all_settings:
            if not setting.is_valid():
                valid = False
        return valid

    def __has_changed(self) -> bool:
        """Calls each setting's *has_changed* method."""

        has_changed = False
        for setting in self.all_settings:
            if setting.has_changed():
                has_changed = True
                print()

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
            setting.push_to_config()

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


class MpvQcSettings:

    def __init__(self):
        self.version: SettingVersion = SettingVersion()
        self.nickname: SettingNickname = SettingNickname()
        self.language: SettingLanguage = SettingLanguage()
        self.comment_types: SettingCommentTypes = SettingCommentTypes()
        self.autosave_enabled: SettingAutoSaveEnabled = SettingAutoSaveEnabled()
        self.autosave_interval: SettingAutoSaveInterval = SettingAutoSaveInterval()
        self.qc_doc_write_nick: SettingQcDocumentWriteNickNameToFile = SettingQcDocumentWriteNickNameToFile()
        self.qc_doc_write_video: SettingQcDocumentWriteVideoPathToFile = SettingQcDocumentWriteVideoPathToFile()
        self.player_last_played_dir: SettingPlayerLastPlayed = SettingPlayerLastPlayed()

        self.all_editable: List[AbstractSetting] = [
            self.nickname,
            self.language,
            self.comment_types,
            self.autosave_enabled,
            self.autosave_interval,
            self.qc_doc_write_nick,
            self.qc_doc_write_video,
        ]

        self.all_writable = copy.copy(self.all_editable)
        self.all_writable.extend([
            self.version,
            self.player_last_played_dir
        ])

    def save(self):
        wr_setting = {}
        for s in self.all_writable:
            wr_setting.update({s.name: s.value})

        with io.open(configuration.get_paths().settings_json, 'w', encoding='utf8') as outfile:
            str_ = json.dumps(wr_setting, indent=4, separators=(',', ': '), sort_keys=True, ensure_ascii=False)
            outfile.write(to_unicode(str_))

    def reset(self):
        pass


class __Holder:
    settings: MpvQcSettings = None


def get_settings():
    if __Holder.settings is None:
        __Holder.settings = MpvQcSettings()
    return __Holder.settings

# COMMENT_TABLE_ENTRY_FONT = ("comment_table_entry_font", "")
#     SOFTSUB_OVERWRITE_VIDEO_FONT_ENABLED = ("softsub_overwrite_video_font_enabled", False)
#     SOFTSUB_OVERWRITE_VIDEO_FONT_FONT = ("softsub_overwrite_video_font_font", "")
