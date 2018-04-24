import copy
import io
import json
import locale
from typing import Dict, List

from PyQt5 import QtCore
from PyQt5.QtWidgets import QComboBox, QLineEdit, QListView, QAbstractItemView, QCheckBox, QSpinBox
from appdirs import unicode

from src.preferences import configuration
from src.preferences.preferencesabstract import AbstractNonUserEditableSetting, SettingsEntry, SettingsType, \
    AbstractUserEditableSetting

try:
    to_unicode = unicode
except NameError:
    to_unicode = str

_tr = _translate = QtCore.QCoreApplication.translate


# from PyKF5.KWidgetsAddons import KMessageWidget, KEditListWidget


class SettingsVersion(AbstractNonUserEditableSetting):

    def provide_settings_declaration(self) -> SettingsEntry:
        return SettingsEntry(name="version",
                             default_value="0.0.1",
                             var_type=SettingsType.STRING)


class SettingsPlayerLastPlayedVideo(AbstractNonUserEditableSetting):

    def provide_settings_declaration(self) -> SettingsEntry:
        return SettingsEntry(name="player_last_played_directory",
                             default_value="",
                             var_type=SettingsType.STRING)


class SettingsNickname(AbstractUserEditableSetting):

    def __init__(self):
        super().__init__()
        self.nickname_LineEdit: QLineEdit
        self._is_valid: bool = True

    def provide_settings_declaration(self) -> SettingsEntry:
        return SettingsEntry(name="nickname",
                             default_value="nickname",
                             var_type=SettingsType.STRING)

    def setup(self, update_function) -> None:
        self.nickname_LineEdit = self.ui.authorLineEdit
        self.nickname_LineEdit.setPlaceholderText(_tr("Misc", "Type here to change the nick name"))
        self.nickname_LineEdit.setText(self.value)
        self.nickname_LineEdit.textChanged.connect(update_function)

    def is_valid(self) -> bool:
        self._is_valid = bool(self.nickname_LineEdit.text())
        return self._is_valid

    def error_messages(self) -> List[str]:
        return [_tr("Misc", "Nick name must not be empty")]

    def has_changed(self) -> bool:
        return not self.value == self.nickname_LineEdit.text().strip().replace(" ", "_")

    def take_over(self):
        self.value = self.nickname_LineEdit.text().strip().replace(" ", "_")


class SettingsLanguage(AbstractUserEditableSetting):

    def __init__(self):
        super().__init__()
        self.language_box: QComboBox = None
        self.languages: Dict = None

    def provide_settings_declaration(self) -> SettingsEntry:

        default_locale = locale.getdefaultlocale()[0]

        if default_locale.startswith("de"):
            def_value = _tr("Dialog", "German")
        else:
            def_value = _tr("Dialog", "English")

        return SettingsEntry(name="language",
                             default_value=def_value,
                             var_type=SettingsType.STRING)

    def setup(self, update_function) -> None:
        self.language_box = self.ui.comboBox
        self.languages = {
            _tr("Dialog", "English"): "English",
            _tr("Dialog", "German"): "German"
        }
        self.language_box.setCurrentIndex(max(self.language_box.findText(_tr("Dialog", self.value)), 0))
        self.language_box.currentIndexChanged.connect(update_function)

    def is_valid(self) -> bool:
        return True

    def has_changed(self) -> bool:
        return not self.value == self.languages.get(self.language_box.currentText())

    def take_over(self):
        self.value = self.languages.get(self.language_box.currentText())


class SettingsCommentTypes(AbstractUserEditableSetting):

    def __init__(self):
        super().__init__()
        self.comment_types_ui = None
        self.comment_types_english: Dict = {}

        self.not_empty_comment_types: bool = False
        self.no_item_empty_str: bool = True

    def provide_settings_declaration(self) -> SettingsEntry:
        return SettingsEntry(name="comment_types",
                             default_value=["Spelling", "Punctuation", "Translation", "Phrasing",
                                            "Timing", "Typeset", "Note"],
                             var_type=SettingsType.LIST_STRING)

    def setup(self, update_function) -> None:
        self.comment_types_ui = self.ui.kCommentTypes
        for ct in self.settings_entry.default_value:
            self.comment_types_english.update({_tr("Misc", ct): ct})

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
        self.not_empty_comment_types = bool(ct_items)

        self.no_item_empty_str = True
        for ct_item in ct_items:
            if not ct_item.replace(" ", ""):
                self.no_item_empty_str = False

        return self.not_empty_comment_types and self.no_item_empty_str

    def error_messages(self) -> List[str]:
        ret_list = []

        if not self.not_empty_comment_types:
            ret_list.append(_tr("Misc", "At least one comment type is required"))

        if not self.no_item_empty_str:
            ret_list.append(_tr("Misc", "Each comment type needs a valid name"))

        return ret_list

    def has_changed(self) -> bool:
        return not self.value == [self.comment_types_english.get(x, x) for x in self.comment_types_ui.items()]

    def take_over(self):
        self.value = [self.comment_types_english.get(x, x).strip() for x in self.comment_types_ui.items()]

    def remove_focus(self):
        # Remove selection from comment type items
        ct_list_view: QListView = self.comment_types_ui.listView()

        if ct_list_view.selectionModel().selectedIndexes():
            ct_list_view.clearSelection()
            edit = self.comment_types_ui.lineEdit()
            edit.setReadOnly(False)
            edit.setPlaceholderText(_tr("Misc", "Type here to add new comment types"))


class SettingsAutoSaveEnabled(AbstractUserEditableSetting):

    def __init__(self):
        super().__init__()
        self.chkBox: QCheckBox = None

    def provide_settings_declaration(self) -> SettingsEntry:
        return SettingsEntry(name="autosave_enabled",
                             default_value=True,
                             var_type=SettingsType.BOOL)

    def setup(self, update_function) -> None:
        self.chkBox = self.ui.autoSaveEnabledCheckBox_4
        self.chkBox.setChecked(self.value)
        self.chkBox.stateChanged.connect(update_function)

    def is_valid(self) -> bool:
        return True

    def has_changed(self) -> bool:
        return not self.value == self.chkBox.isChecked()

    def take_over(self):
        self.value = self.chkBox.isChecked()


class SettingsAutoSaveInterval(AbstractUserEditableSetting):

    def __init__(self):
        super().__init__()
        self.spinBox: QSpinBox = None

    def provide_settings_declaration(self) -> SettingsEntry:
        return SettingsEntry(name="autosave_interval_seconds",
                             default_value=90,
                             var_type=SettingsType.INT)

    def setup(self, update_function) -> None:
        self.spinBox = self.ui.autosaveSpinBox_4
        self.spinBox.setValue(int(self.value))
        self.spinBox.valueChanged.connect(update_function)

    def is_valid(self) -> bool:
        return True

    def has_changed(self) -> bool:
        return not self.value == self.spinBox.value()

    def take_over(self):
        self.value = self.spinBox.value()


class SettingsQcDocumentWriteVideoPathToFile(AbstractUserEditableSetting):

    def __init__(self):
        super().__init__()
        self.chkBox: QCheckBox = None

    def provide_settings_declaration(self) -> SettingsEntry:
        return SettingsEntry(name="qc_doc_write_video_path_to_file",
                             default_value=True,
                             var_type=SettingsType.BOOL)

    def setup(self, update_function) -> None:
        self.chkBox = self.ui.saveVideoPathCheckBox
        self.chkBox.setChecked(self.value)
        self.chkBox.stateChanged.connect(update_function)

    def is_valid(self) -> bool:
        return True

    def has_changed(self) -> bool:
        return not self.value == self.chkBox.isChecked()

    def take_over(self):
        self.value = self.chkBox.isChecked()


class SettingsQcDocumentWriteNickNameToFile(AbstractUserEditableSetting):
    def __init__(self):
        super().__init__()
        self.chkBox: QCheckBox = None

    def provide_settings_declaration(self) -> SettingsEntry:
        return SettingsEntry(name="qc_doc_write_nick_name_to_file",
                             default_value=True,
                             var_type=SettingsType.BOOL)

    def setup(self, update_function) -> None:
        self.chkBox = self.ui.saveNickNameCheckBox
        self.chkBox.setChecked(self.value)
        self.chkBox.stateChanged.connect(update_function)

    def is_valid(self) -> bool:
        return True

    def has_changed(self) -> bool:
        return not self.value == self.chkBox.isChecked()

    def take_over(self):
        self.value = self.chkBox.isChecked()


class MpvQcSettings:
    """A holder for all application relevant settings."""

    def __init__(self):
        self.version = SettingsVersion()
        self.player_last_played = SettingsPlayerLastPlayedVideo()

        self.language = SettingsLanguage()
        self.nickname = SettingsNickname()
        self.comment_types = SettingsCommentTypes()
        self.auto_save_enabled = SettingsAutoSaveEnabled()
        self.auto_save_interval = SettingsAutoSaveInterval()
        self.qc_doc_write_nick_name_to_file = SettingsQcDocumentWriteNickNameToFile()
        self.qc_doc_write_video_path_to_file = SettingsQcDocumentWriteVideoPathToFile()

        self.all_editable: List[AbstractUserEditableSetting] = [
            self.language,
            self.nickname,
            self.comment_types,
            self.auto_save_enabled,
            self.auto_save_interval,
            self.qc_doc_write_nick_name_to_file,
            self.qc_doc_write_video_path_to_file
        ]

        self.all_writable: List[AbstractNonUserEditableSetting] = copy.copy(self.all_editable)
        self.all_writable.extend([
            self.version,
            self.player_last_played
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
