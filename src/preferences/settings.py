import io
import json
import locale
import os
from abc import ABC, abstractmethod
from os import path
from typing import List, Any, Dict

from PyQt5.QtCore import QCoreApplication
from appdirs import unicode

from src.gui.preferences import Ui_Dialog
from src.preferences import configuration

try:
    to_unicode = unicode
except NameError:
    to_unicode = str

_translate = QCoreApplication.translate

# The following list exists only for easing the translation process
__for_translation_only = [
    _translate("Misc", "Translation"),
    _translate("Misc", "Punctuation"),
    _translate("Misc", "Spelling"),
    _translate("Misc", "Phrasing"),
    _translate("Misc", "Timing"),
    _translate("Misc", "Typeset"),
    _translate("Misc", "Note"),
    _translate("Misc", "Type here to add new comment types")
]


class SettingsEntry:

    def __init__(self, name: str, default_value):
        """
        Holder for a settings entry's data.

        :param name: The name of this attribute. The name is only used to store this entry in the JSON file.
        :param default_value: The default value to assign if no attribute with **name** was found.
            Used to assign the correct type to the variable when parsing the JSON string.
        """

        self._name = name
        self._default_value = default_value
        self._value = None

    def reset(self):
        self._value = self._default_value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value) -> None:
        self._name = value

    @property
    def default_value(self) -> Any:
        return self._default_value

    @default_value.setter
    def default_value(self, value) -> None:
        self._default_value = value

    @property
    def value(self) -> Any:
        return self._value if self._value is not None else self.default_value

    @value.setter
    def value(self, value):
        self._value = value


class PreferenceChangeWrapper(ABC):

    def __init__(self, setting: SettingsEntry):
        self.setting = setting
        self._changed = False
        self._valid = True, []

        self._new_value = None  # Used to cache the current value in the ui component
        self._update_fun = None  # Used to unbind the update function

    @abstractmethod
    def bind_to(self, ui: Ui_Dialog, call_me_after_change) -> None:
        """
        Will insert the setting into the given ui.
        :param call_me_after_change: Function to call after update
        :param ui: The UI component to insert the setting value.
        """

    @abstractmethod
    def unbind_from(self, ui: Ui_Dialog) -> None:
        """
        Will unbind the ui from this preference wrapper.
        :param ui: The UI component to unbind
        """

    @property
    def changed(self) -> bool:
        """
        :return: True if the value has changed (regarding the setting: SettingsEntry object), False else.
        """

        return self._changed

    @property
    def valid(self) -> (bool, List[str]):
        """
        :return: True if the ui component holds a valid setting, False else.
        :return: A list with error messages hinting the user whats wrong. *May be empty.*
        """
        return self._valid

    def save(self) -> None:
        if self._new_value is not None:
            self.setting.value = self._new_value
        self._changed = False
        self._valid = True, []

        self._new_value = None
        self._update_fun = None

    def reset(self) -> None:
        """
        Resets the value of the wrapped setting to default.
        """

        self.setting.reset()
        self._changed = False
        self._valid = True, []

        self._new_value = None
        self._update_fun = None


class NicknamePrefWrapper(PreferenceChangeWrapper):

    def unbind_from(self, ui: Ui_Dialog) -> None:
        ui.authorLineEdit.textChanged.disconnect(self._update_fun)

    def bind_to(self, ui: Ui_Dialog, call_me_after_update) -> None:
        line_edit = ui.authorLineEdit
        line_edit.setPlaceholderText(_translate("Misc", "Type here to change the nick name"))
        line_edit.setText(self.setting.value)

        def on_update():
            self._new_value = line_edit.text().strip().replace(" ", "_")
            self._changed = self.setting.value != self._new_value
            self._valid = bool(line_edit.text()), [_translate("Misc", "Nick name must not be empty")]
            call_me_after_update()

        self._update_fun = on_update
        line_edit.textChanged.connect(self._update_fun)


class LanguagePrefWrapper(PreferenceChangeWrapper):

    def __init__(self, setting: SettingsEntry):
        super().__init__(setting)
        self.languages = {
            _translate("Dialog", "English"): "English",
            _translate("Dialog", "German"): "German"
        }

    def bind_to(self, ui: Ui_Dialog, call_me_after_change) -> None:
        language_box = ui.comboBox
        language_box.setCurrentIndex(max(language_box.findText(_translate("Dialog", self.setting.value)), 0))

        self._valid = True, []

        def on_update():
            self._new_value = self.languages.get(language_box.currentText())
            self._changed = self.setting.value != self._new_value
            call_me_after_change()

        self._update_fun = on_update
        language_box.currentIndexChanged.connect(self._update_fun)

    def unbind_from(self, ui: Ui_Dialog) -> None:
        ui.comboBox.currentIndexChanged.disconnect(self._update_fun)


class CommentTypesWrapper(PreferenceChangeWrapper):

    def bind_to(self, ui: Ui_Dialog, call_me_after_value_update) -> None:

        # Keep the English comment types
        cts = ui.kCommentTypes
        cts.clear()
        cts_english = {}
        for ct in self.setting.default_value:
            cts_english.update({_translate("Misc", ct): ct})

        # Insert

        for ct in self.setting.value:
            cts.insertItem(_translate("Misc", ct))

        def on_update():
            self._new_value = [cts_english.get(x, x).strip() for x in cts.items()]
            self._changed = self.setting.value != self._new_value
            self._valid = CommentTypesWrapper.__validate(cts)
            call_me_after_value_update()

        self._update_fun = on_update
        cts.changed.connect(on_update)

    def unbind_from(self, ui: Ui_Dialog) -> None:
        ui.kCommentTypes.changed.disconnect(self._update_fun)

    @staticmethod
    def __validate(cts):
        errors = []
        ct_items: List[str] = cts.items()

        # Part I
        empty_comment_types = not bool(ct_items)
        if empty_comment_types:
            errors.append(_translate("Misc", "At least one comment type is required"))

        # Part II
        item_empty = False
        for ct_item in ct_items:
            if not ct_item.replace(" ", ""):
                item_empty = True

        if item_empty:
            errors.append(_translate("Misc", "Each comment type needs a valid name"))

        return not empty_comment_types and not item_empty, errors


class AutosaveEnabledWrapper(PreferenceChangeWrapper):

    def bind_to(self, ui: Ui_Dialog, call_me_after_change) -> Any:
        chk_box = ui.autoSaveEnabledCheckBox_4
        chk_box.setChecked(self.setting.value)

        self._valid = True, []

        def on_update():
            self._new_value = chk_box.isChecked()
            self._changed = self.setting.value != self._new_value
            call_me_after_change()

        self._update_fun = on_update

        chk_box.stateChanged.connect(on_update)

    def unbind_from(self, ui: Ui_Dialog) -> None:
        ui.autoSaveEnabledCheckBox_4.stateChanged.disconnect(self._update_fun)


class AutosaveIntervalWrapper(PreferenceChangeWrapper):

    def bind_to(self, ui: Ui_Dialog, call_me_after_change) -> None:
        spin_box = ui.autosaveSpinBox_4
        spin_box.setValue(self.setting.value)

        self._valid = True, []

        def on_update():
            self._new_value = spin_box.value()
            self._changed = self.setting.value != self._new_value
            call_me_after_change()

        self._update_fun = on_update

        spin_box.valueChanged.connect(on_update)

    def unbind_from(self, ui: Ui_Dialog) -> None:
        ui.autosaveSpinBox_4.valueChanged.disconnect(self._update_fun)


class QcDocumentWriteVideoPathToFileWrapper(PreferenceChangeWrapper):

    def bind_to(self, ui: Ui_Dialog, call_me_after_change) -> None:
        chk_box = ui.saveVideoPathCheckBox
        chk_box.setChecked(self.setting.value)

        self._valid = True, []

        def on_update():
            self._new_value = chk_box.isChecked()
            self._changed = self.setting.value != self._new_value
            call_me_after_change()

        self._update_fun = on_update
        chk_box.stateChanged.connect(on_update)

    def unbind_from(self, ui: Ui_Dialog) -> None:
        ui.saveVideoPathCheckBox.stateChanged.disconnect(self._update_fun)


class QcDocumentWriteNickNameToFileWrapper(PreferenceChangeWrapper):

    def bind_to(self, ui: Ui_Dialog, call_me_after_change) -> None:
        chk_box = ui.saveNickNameCheckBox
        chk_box.setChecked(self.setting.value)

        self._valid = True, []

        def on_update():
            self._new_value = chk_box.isChecked()
            self._changed = self.setting.value != self._new_value
            call_me_after_change()

        self._update_fun = on_update
        chk_box.stateChanged.connect(on_update)

    def unbind_from(self, ui: Ui_Dialog) -> None:
        ui.saveNickNameCheckBox.stateChanged.disconnect(self._update_fun)


class SettingsManager:

    def __init__(self):
        self.file: path = configuration.paths.settings_json

        self.settings_version = SettingsEntry("version", "0.0.1")
        self.player_last_played_directory = SettingsEntry("player_last_played_directory", "")
        self.nickname = SettingsEntry("nickname", "nick")
        self.language = SettingsManager.__find_language()
        self.comment_types = SettingsEntry("comment_types", ["Spelling", "Punctuation", "Translation", "Phrasing",
                                                             "Timing", "Typeset", "Note"])
        self.auto_save_enabled = SettingsEntry("autosave_enabled", True)
        self.auto_save_interval = SettingsEntry("autosave_interval_seconds", 90)
        self.qc_doc_write_video_path_to_file = SettingsEntry("qc_doc_write_video_path_to_file", True)
        self.qc_doc_write_nick_to_file = SettingsEntry("qc_doc_write_nick_to_file", True)

        self.comment_types_wrapper = CommentTypesWrapper(self.comment_types)

        self.writable_settings: List[SettingsEntry] = [
            self.settings_version,
            self.player_last_played_directory,
            self.nickname,
            self.language,
            self.auto_save_enabled,
            self.auto_save_interval,
            self.qc_doc_write_video_path_to_file,
            self.qc_doc_write_nick_to_file
        ]

        self.__read_values_from_config(self.writable_settings)

    @property
    def changeable_settings(self) -> List[PreferenceChangeWrapper]:
        return [
            NicknamePrefWrapper(self.nickname),
            LanguagePrefWrapper(self.language),
            self.comment_types_wrapper,
            AutosaveEnabledWrapper(self.auto_save_enabled),
            AutosaveIntervalWrapper(self.auto_save_interval),
            QcDocumentWriteVideoPathToFileWrapper(self.qc_doc_write_video_path_to_file),
            QcDocumentWriteNickNameToFileWrapper(self.qc_doc_write_nick_to_file)
        ]

    def __read(self):
        if not os.path.isfile(self.file):
            self.save()
        with open(self.file) as df:
            return json.load(df)

    def __read_values_from_config(self, writeable_settings):
        found_in_json: Dict = self.__read()
        for setting in writeable_settings:
            setting.value = found_in_json.get(setting.name, None)

    def save(self):
        wr_setting = {}
        for s in self.writable_settings:
            wr_setting.update({s.name: s.value})

        with io.open(self.file, 'w', encoding='utf8') as outfile:
            str_ = json.dumps(wr_setting, indent=4, separators=(',', ': '), sort_keys=True, ensure_ascii=False)
            outfile.write(to_unicode(str_))

    @staticmethod
    def __find_language():
        default_locale = locale.getdefaultlocale()[0]

        if default_locale.startswith("de"):
            def_value = _translate("Dialog", "German")
        else:
            def_value = _translate("Dialog", "English")

        return SettingsEntry(name="language",
                             default_value=def_value)


settings = SettingsManager()
