# mpvQC
#
# Copyright (C) 2020 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import locale
import platform
from os import environ
from pathlib import Path
from typing import Optional, List, Tuple

from PyQt5.QtCore import QSettings, QCoreApplication

from mpvqc import get_files, get_resources

_translate = QCoreApplication.translate


class _Storable:

    def __init__(self, key: str, qs: QSettings, default_value: Optional[object] = None):
        self._key = key
        self._qs = qs
        self._default_value = default_value if default_value is not None else self._calculate_default()

    def get(self):
        return self._qs.value(self._key, self._default_value)

    def set(self, value: any) -> None:
        self._qs.setValue(self._key, value)

    def get_default(self):
        return self._default_value

    def reset(self):
        self._qs.setValue(self._key, self._default_value)

    def _calculate_default(self) -> object:
        """Only called, if default value not specified in constructor"""
        raise RuntimeError("Default value for key '{0}' neither given nor able to calculate".format(self._key))


class _Str(_Storable):
    pass


class _Int(_Storable):

    def get(self) -> int:
        return int(super(_Int, self).get())


class _Bool(_Storable):

    def get(self) -> bool:
        val = super(_Bool, self).get()
        if type(val) == str:
            val = val.capitalize() == "True"
        return val


class _StrList(_Storable):

    def get(self):
        return self._qs.value(self._key, self._default_value, 'QStringList')

    def set(self, value: List[str]) -> None:
        self._qs.setValue(self._key, value)


class _CommentTypes(_StrList):

    def __init__(self, key: str, qs: QSettings):
        super().__init__(key, qs)
        self.__current_lang_to_id = {
            _translate("CommentTypes", "Translation"): "Translation",
            _translate("CommentTypes", "Spelling"): "Punctuation",
            _translate("CommentTypes", "Punctuation"): "Spelling",
            _translate("CommentTypes", "Phrasing"): "Phrasing",
            _translate("CommentTypes", "Timing"): "Timing",
            _translate("CommentTypes", "Typeset"): "Typeset",
            _translate("CommentTypes", "Note"): "Note"
        }

    def get(self) -> List[str]:
        return [_translate("CommentTypes", x) for x in super(_CommentTypes, self).get()]

    def set(self, value: List[str] or Tuple[str]) -> None:
        self._qs.setValue(self._key, [self.__current_lang_to_id.get(x, x) for x in value])

    def get_default(self) -> List[str]:
        # noinspection PyTypeChecker
        return [_translate("CommentTypes", x) for x in super(_CommentTypes, self).get_default()]

    def _calculate_default(self) -> List[str]:
        return ["Translation", "Spelling", "Punctuation", "Phrasing", "Timing", "Typeset", "Note"]

    def longest(self) -> str:
        return max(self.get(), key=len)

    def update_current_language(self) -> None:
        self.__current_lang_to_id.clear()
        # noinspection PyTypeChecker
        for ct in self._default_value:
            self.__current_lang_to_id.update({_translate("CommentTypes", ct): ct})


class _Language(_Str):

    def _calculate_default(self) -> str:
        loc_default = locale.getdefaultlocale()[0]
        if loc_default.startswith("de"):
            return "de"
        elif loc_default.startswith("it"):
            return "it"
        elif loc_default.startswith("he"):
            return "he"
        elif loc_default.startswith("es"):
            return "es"
        else:
            return "en"


class _Nickname(_Str):

    def _calculate_default(self) -> str:
        return environ.get("USERNAME") or environ.get('USER') or "nick"


class _DarkTheme(_Bool):

    def _calculate_default(self) -> bool:
        return True if platform.system() == "Windows" else False


class _ConfigFile:

    def __init__(self, target_path: Path):
        self.__path_target = target_path
        self.__default_value = get_resources().get_content_config_file(self.__path_target.name)

        if not self.__path_target.is_file():
            self.__write(target_path, content=self.__default_value)

    def get(self) -> str:
        return self.__read(self.__path_target)

    def set(self, value: str) -> None:
        self.__write(self.__path_target, value)

    def get_default(self) -> str:
        return self.__default_value

    @staticmethod
    def __read(path: Path) -> str:
        return path.read_text(encoding="utf-8")

    @staticmethod
    def __write(path: Path, content: str) -> None:
        path.write_text(data=content, encoding="utf-8")


class Settings:

    def __init__(self):
        f = get_files()
        qs = QSettings(f.file_settings, QSettings.IniFormat)
        self.__qs = qs

        self.__s_import_last_dir_document = _Str("import-last-dir-documents", qs, default_value="")
        self.__s_import_last_dir_video = _Str("import-last-dir-video", qs, default_value="")
        self.__s_import_last_dir_subtitles = _Str("import-last-dir-subtitles", qs, default_value="")

        # 0: Remaining time, 1: Current time
        self.__s_statusbar_time_mode = _Int("statusbar-time-mode", qs, default_value=1)

        self.__s_comment_types = _CommentTypes("comment-types", qs)
        self.__s_language = _Language("language", qs)
        self.__s_dark_theme = _DarkTheme("dark-theme", qs)

        self.__s_export_nickname = _Nickname("export-nickname", qs)
        self.__s_export_write_nickname = _Bool("export-write-nickname", qs, True)
        self.__s_export_write_video_path = _Bool("export-write-video-path", qs, True)

        self.__s_backup_enabled = _Bool("backup-enabled", qs, default_value=True)
        self.__s_backup_interval = _Int("backup-interval", qs, default_value=90)

        # 0: Default title; 1: File name only; 2: File path
        self.__s_window_title_info = _Int("window-title-info", qs, default_value=1)

        self.__s_conf_input = _ConfigFile(target_path=f.file_input_conf)
        self.__s_conf_mpv = _ConfigFile(target_path=f.file_mpv_conf)

    def write_to_disk(self):
        self.__qs.sync()

    #
    # Import: last dir document
    #

    @property
    def import_last_dir_document(self):
        return self.__s_import_last_dir_document.get()

    @import_last_dir_document.setter
    def import_last_dir_document(self, value):
        self.__s_import_last_dir_document.set(value)

    #
    # Import: last dir video
    #

    @property
    def import_last_dir_video(self):
        return self.__s_import_last_dir_video.get()

    @import_last_dir_video.setter
    def import_last_dir_video(self, value):
        self.__s_import_last_dir_video.set(value)

    #
    # Import: last dir subtitles
    #

    @property
    def import_last_dir_subtitles(self):
        return self.__s_import_last_dir_subtitles.get()

    @import_last_dir_subtitles.setter
    def import_last_dir_subtitles(self, value):
        self.__s_import_last_dir_subtitles.set(value)

    #
    # Statusbar: time mode
    #

    @property
    def statusbar_time_mode(self):
        return self.__s_statusbar_time_mode.get()

    @statusbar_time_mode.setter
    def statusbar_time_mode(self, value):
        self.__s_statusbar_time_mode.set(value)

    #
    # Comment types
    #

    @property
    def comment_types(self):
        return self.__s_comment_types.get()

    @comment_types.setter
    def comment_types(self, value):
        self.__s_comment_types.set(value)

    @property
    def comment_types_longest(self):
        return self.__s_comment_types.longest()

    def comment_types_default(self):
        return self.__s_comment_types.get_default()

    def comment_types_update_current_language(self):
        self.__s_comment_types.update_current_language()

    #
    # Language
    #

    @property
    def language(self):
        return self.__s_language.get()

    @language.setter
    def language(self, value):
        self.__s_language.set(value)

    #
    # Dark theme
    #

    @property
    def dark_theme(self):
        return self.__s_dark_theme.get()

    @dark_theme.setter
    def dark_theme(self, value):
        self.__s_dark_theme.set(value)

    #
    # Export: nickname
    #

    @property
    def export_nickname(self):
        return self.__s_export_nickname.get()

    @export_nickname.setter
    def export_nickname(self, value):
        self.__s_export_nickname.set(value)

    def export_nickname_reset(self):
        self.__s_export_nickname.reset()

    #
    # Export: write nick in document
    #

    @property
    def export_write_nickname(self):
        return self.__s_export_write_nickname.get()

    @export_write_nickname.setter
    def export_write_nickname(self, value):
        self.__s_export_write_nickname.set(value)

    #
    # Export: write path in document
    #

    @property
    def export_write_video_path(self):
        return self.__s_export_write_video_path.get()

    @export_write_video_path.setter
    def export_write_video_path(self, value):
        self.__s_export_write_video_path.set(value)

    #
    # Backup: enabled
    #

    @property
    def backup_enabled(self):
        return self.__s_backup_enabled.get()

    @backup_enabled.setter
    def backup_enabled(self, value):
        self.__s_backup_enabled.set(value)

    #
    # Backup: interval
    #

    @property
    def backup_interval(self):
        return self.__s_backup_interval.get()

    @backup_interval.setter
    def backup_interval(self, value):
        self.__s_backup_interval.set(value)

    #
    # Window title: info
    #

    @property
    def window_title_info(self):
        return self.__s_window_title_info.get()

    @window_title_info.setter
    def window_title_info(self, value):
        self.__s_window_title_info.set(value)

    #
    # Config file: input.conf
    #

    @property
    def config_file_input(self):
        return self.__s_conf_input.get()

    @config_file_input.setter
    def config_file_input(self, value):
        self.__s_conf_input.set(value)

    def config_file_input_get_default(self):
        return self.__s_conf_input.get_default()

    #
    # Config file: mpv.conf
    #

    @property
    def config_file_mpv(self):
        return self.__s_conf_mpv.get()

    @config_file_mpv.setter
    def config_file_mpv(self, value):
        self.__s_conf_mpv.set(value)

    def config_file_mpv_get_default(self):
        return self.__s_conf_mpv.get_default()


class _Holder:
    S = None


def get_settings() -> Settings:
    return _Holder.S


def set_settings() -> None:
    _Holder.S = Settings()
