# Copyright (C) 2016-2017 Frechdachs <frechdachs@rekt.cc>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import io
import json
import locale
import os
from os import path
from typing import Dict

from PyQt5.QtCore import QCoreApplication
from appdirs import unicode

from src import constants
from src.files import Files

try:
    to_unicode = unicode
except NameError:
    to_unicode = str

_translate = QCoreApplication.translate

# The following list exists only for easing the translation process
__for_translation_only = [
    _translate("CommentTypes", "Translation"),
    _translate("CommentTypes", "Punctuation"),
    _translate("CommentTypes", "Spelling"),
    _translate("CommentTypes", "Phrasing"),
    _translate("CommentTypes", "Timing"),
    _translate("CommentTypes", "Typeset"),
    _translate("CommentTypes", "Note"),
    _translate("CommentTypes", "Type here to add new comment types")
]


class Entry:
    """
    An entry represents a property which is saved to disc.
    """

    def __init__(self, identifier: str or path, default_value):
        """
        :param identifier:
            * *normal* setting: the json key to read and write
            * *CONF* setting: the full canonical file path to read and write
        :param default_value:
            the default value
        """

        self.identifier = identifier
        self.default_value = default_value

        self.temporary_value = None
        self._value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    def save(self) -> None:
        """
        Saves the current temporary value, but does **not** write to disc [use Setting.save()] to write to disc.
        """

        if self.temporary_value is not None:
            self.value = self.temporary_value

        self.temporary_value = None

    def reset(self) -> None:
        """
        Sets the value to the default value and the temporary value to *None*.
        """

        self.value = self.default_value
        self.temporary_value = None

    def changed(self) -> bool:
        """
        :return: whether the value and the temporary value are different.
        """
        return self.temporary_value is not None and self.value != self.temporary_value


class CommentTypesEntry(Entry):
    def __init__(self, identifier: str or path, default_value):
        super().__init__(identifier, default_value)
        self.current_lang_to_english = {}

    def update(self):
        """
        Will update the internal dictionary to map current language to English.
        :return:
        """
        self.current_lang_to_english.clear()
        for ct in self.default_value:
            self.current_lang_to_english.update({_translate("CommentTypes", ct): ct})

    @property
    def value(self):
        retu = []
        for ct in self._value if self._value is not None else self.default_value:
            retu.append(_translate("CommentTypes", ct))
        return retu

    @value.setter
    def value(self, val):
        eng = []
        for ct in val:
            eng.append(self.current_lang_to_english.get(ct, ct))

        self._value = eng

    def save(self) -> None:
        """
        Saves the current temporary value, but does **not** write to disc [use setting.save()] to write to disc.
        """

        if self.temporary_value is not None:
            self.value = self.temporary_value

        self.temporary_value = None

    def reset(self) -> None:
        """
        Sets the value to the default value and the temporary value to *None*.
        """

        self.value = self.default_value
        self.temporary_value = None

    def changed(self) -> bool:
        """
        :return: whether the value and the temporary value are different.
        """
        return self.temporary_value is not None and self.value != self.temporary_value


############################################################################################################## INTERNAL

Setting_Internal_PLAYER_LAST_PLAYED_DIR = \
    Entry("internal_player_last_played_dir", "")

Setting_Internal_STATUS_BAR_TIME_MODE = \
    Entry("internal_status_bar_current_time", True)
"""True: Current Time; False: Remaining Time"""

############################################################################## PREFERENCES -> GENERAL ### CUSTOMIZATION

Setting_Custom_General_NICKNAME = \
    Entry("custom_general_nickname", "nick")

Setting_Custom_General_COMMENT_TYPES = \
    CommentTypesEntry("custom_general_comment_types", ["Spelling", "Punctuation", "Translation", "Phrasing",
                                                       "Timing", "Typeset", "Note"])

############################################################################# PREFERENCES -> LANGUAGE ### CUSTOMIZATION

Setting_Custom_Language_LANGUAGE = \
    Entry("custom_language_language", "German" if locale.getdefaultlocale()[0].startswith("de") else "English")

########################################################################## PREFERENCES -> QC DOCUMENT ### CUSTOMIZATION

Setting_Custom_QcDocument_AUTOSAVE_ENABLED = \
    Entry("custom_qcdocument_autosave_enabled", True)

Setting_Custom_QcDocument_AUTOSAVE_INTERVAL = \
    Entry("custom_qcdocument_autosave_interval", 150)  # in seconds

Setting_Custom_QcDocument_WRITE_VIDEO_PATH_TO_FILE = \
    Entry("custom_qcdocument_write_video_path_to_file", True)

Setting_Custom_QcDocument_WRITE_NICK_TO_FILE = \
    Entry("custom_qcdocument_write_nick_to_file", True)

######################################################################## PREFERENCES -> CONFIGURATION ### CUSTOMIZATION

Setting_Custom_Configuration_INPUT = \
    Entry(Files.FILE_CONF_INPUT, constants.CFG_INPUT)

Setting_Custom_Configuration_MPV = \
    Entry(Files.FILE_CONF_MPV, constants.CFG_MPV)

########################################################################### PREFERENCES -> APPEARANCE ### CUSTOMIZATION

Setting_Custom_Appearance_General_WINDOW_TITLE = \
    Entry("custom_appearance_general_window_title_nothing_name_full", 0)
"""0: Default Window Title; 1: Current File name only; 2: Full path"""

#######################################################################################################################
SettingJson = (
    Setting_Internal_PLAYER_LAST_PLAYED_DIR,
    Setting_Internal_STATUS_BAR_TIME_MODE,

    Setting_Custom_General_NICKNAME,
    Setting_Custom_General_COMMENT_TYPES,
    Setting_Custom_Language_LANGUAGE,
    Setting_Custom_QcDocument_AUTOSAVE_ENABLED,
    Setting_Custom_QcDocument_AUTOSAVE_INTERVAL,
    Setting_Custom_QcDocument_WRITE_NICK_TO_FILE,
    Setting_Custom_QcDocument_WRITE_VIDEO_PATH_TO_FILE,
    Setting_Custom_Appearance_General_WINDOW_TITLE
)

SettingConfs = (
    Setting_Custom_Configuration_INPUT,
    Setting_Custom_Configuration_MPV
)

SettingJsonSettingConfs = SettingJson + SettingConfs


#######################################################################################################################

def __read_json():
    file = Files.FILE_SETTINGS
    if not os.path.isfile(file):
        __write_json()

    with open(Files.FILE_SETTINGS) as df:
        json_values: Dict = json.load(df)

    for json_setting in SettingJson:
        json_setting._value = json_values.get(json_setting.identifier, json_setting.default_value)
        # todo logger


def __write_json():
    dictionary = {}
    for s in SettingJson:
        # noinspection PyProtectedMember
        dictionary.update({
            s.identifier: s._value if s._value is not None else s.default_value
        })

    with io.open(Files.FILE_SETTINGS, 'w', encoding='utf8') as file:
        str_ = json.dumps(dictionary, indent=4, separators=(',', ': '), sort_keys=True, ensure_ascii=False)
        file.write(to_unicode(str_))
        #  todo logger


def __read_confs():
    for conf in SettingConfs:
        if not os.path.isfile(conf.identifier):
            __write_confs(True)
            # That may override the other config, but I think that this will never happen in "production"
        with open(conf.identifier, "r", encoding="utf-8") as file:
            conf._value = file.read()
            # todo logger


def __write_confs(default_value=False):
    for conf in SettingConfs:
        with open(conf.identifier, "w", encoding="utf-8") as file:
            file.write(conf._value if not default_value else conf.default_value)
        #  todo logger


def __read() -> None:
    """
    Reads all values from their files.
    Will assign a value to the corresponding entry if a value was found.
    """

    __read_json()
    __read_confs()


def save() -> None:
    """
    Saves **and writes** all entries to disc (their current value).
    """

    __write_json()
    __write_confs()


__read()
