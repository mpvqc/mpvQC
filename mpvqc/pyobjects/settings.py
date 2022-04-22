#  mpvQC
#
#  Copyright (C) 2022 mpvQC developers
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


from pathlib import Path

import inject
from PySide6.QtCore import Signal, Property, QUrl, QObject
from PySide6.QtQml import QmlElement, QmlSingleton

from mpvqc.enums import TimeFormat, TitleFormat
from mpvqc.services import SettingsService, SettingsInitializerService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
@QmlSingleton
class SettingsPyObject(QObject):
    _settings = inject.attr(SettingsService)
    _settings_backend = inject.attr(SettingsInitializerService)

    def get_backing_object_file_name(self):
        return self._settings_backend.backing_object.fileName()

    backing_object_file_name_changed = Signal(str)
    backing_object_file_name = Property(str, get_backing_object_file_name, notify=backing_object_file_name_changed)

    @staticmethod
    def _fire_on_change(value_old: any, value_new: any, signal: Signal):
        if value_old != value_new:
            signal.emit(value_new)

    #
    # Title bar format
    #

    def get_title_bar_format(self) -> TitleFormat:
        return self._settings.title_bar_format

    def set_title_bar_format(self, value: TitleFormat) -> None:
        value_old = self.get_title_bar_format()
        self._settings.title_bar_format = value
        self._fire_on_change(value_old, value, signal=self.title_bar_format_changed)

    title_bar_format_changed = Signal(int)
    title_bar_format = Property(int, get_title_bar_format, set_title_bar_format,
                                notify=title_bar_format_changed)

    #
    # Comment types
    #

    def get_comment_types(self) -> list[str]:
        return self._settings.comment_types

    def set_comment_types(self, value: list[str]) -> None:
        value_old = self.get_comment_types()
        self._settings.comment_types = value
        self._fire_on_change(value_old, value, signal=self.comment_types_changed)

    comment_types_changed = Signal(list)
    comment_types = Property(list, get_comment_types, set_comment_types, notify=comment_types_changed)

    #
    # Backup enabled
    #

    def get_backup_enabled(self) -> bool:
        return self._settings.backup_enabled

    def set_backup_enabled(self, value: bool) -> None:
        value_old = self.get_backup_enabled()
        self._settings.backup_enabled = value
        self._fire_on_change(value_old, value, signal=self.backup_enabled_changed)

    backup_enabled_changed = Signal(bool)
    backup_enabled = Property(bool, get_backup_enabled, set_backup_enabled, notify=backup_enabled_changed)

    #
    # Backup interval
    #

    def get_backup_interval(self) -> int:
        return self._settings.backup_interval

    def set_backup_interval(self, value: int) -> None:
        value_old = self.get_backup_interval()
        self._settings.backup_interval = value
        self._fire_on_change(value_old, value, signal=self.backup_interval_changed)

    backup_interval_changed = Signal(int)
    backup_interval = Property(int, get_backup_interval, set_backup_interval, notify=backup_interval_changed)

    #
    # Status bar time format
    #

    def get_status_bar_time_format(self) -> TimeFormat:
        return self._settings.status_bar_time_format

    def set_status_bar_time_format(self, value: TimeFormat):
        value_old = self.get_status_bar_time_format()
        self._settings.status_bar_time_format = value
        self._fire_on_change(value_old, value, signal=self.status_bar_time_format_changed)

    status_bar_time_format_changed = Signal(int)
    status_bar_time_format = Property(int, get_status_bar_time_format, set_status_bar_time_format,
                                      notify=status_bar_time_format_changed)

    #
    # Status bar percentage
    #

    def get_status_bar_percentage(self) -> bool:
        return self._settings.status_bar_percentage

    def set_status_bar_percentage(self, value: bool):
        old_value = self.get_status_bar_percentage()
        self._settings.status_bar_percentage = value
        self._fire_on_change(old_value, value, signal=self.status_bar_percentage_changed)

    status_bar_percentage_changed = Signal(bool)
    status_bar_percentage = Property(bool, get_status_bar_percentage, set_status_bar_percentage,
                                     notify=status_bar_percentage_changed)

    #
    # Import video from document automatically
    #

    def get_import_video_from_document_automatically(self) -> bool:
        return self._settings.import_video_from_document_automatically

    def set_import_video_from_document_automatically(self, value: bool) -> None:
        old_value = self.get_import_video_from_document_automatically()
        self._settings.import_video_from_document_automatically = value
        self._fire_on_change(old_value, value, signal=self.import_video_from_document_automatically_changed)

    import_video_from_document_automatically_changed = Signal(bool)
    import_video_from_document_automatically = Property(bool,
                                                        get_import_video_from_document_automatically,
                                                        set_import_video_from_document_automatically,
                                                        notify=import_video_from_document_automatically_changed)

    #
    # Export: nickname
    #

    def get_export_nickname(self) -> str:
        return self._settings.export_nickname

    def set_export_nickname(self, value: str):
        old_value = self.get_export_nickname()
        self._settings.export_nickname = value
        self._fire_on_change(old_value, value, signal=self.export_nickname_changed)

    export_nickname_changed = Signal(str)
    export_nickname = Property(str, get_export_nickname, set_export_nickname, notify=export_nickname_changed)

    #
    # Export: append nickname
    #

    def get_export_append_nickname(self) -> bool:
        return self._settings.export_append_nickname

    def set_export_append_nickname(self, value: bool) -> None:
        old_value = self.get_export_append_nickname()
        self._settings.export_append_nickname = value
        self._fire_on_change(old_value, value, signal=self.export_append_nickname_changed)

    export_append_nickname_changed = Signal(bool)
    export_append_nickname = Property(bool, get_export_append_nickname, set_export_append_nickname,
                                      notify=export_append_nickname_changed)

    #
    # Export: write header
    #

    def get_export_write_header(self) -> bool:
        return self._settings.export_write_header

    def set_export_write_header(self, value: bool) -> None:
        old_value = self.get_export_write_header()
        self._settings.export_write_header = value
        self._fire_on_change(old_value, value, signal=self.export_write_header_changed)

    export_write_header_changed = Signal(bool)
    export_write_header = Property(bool, get_export_write_header, set_export_write_header,
                                   notify=export_write_header_changed)

    #
    # Export: write header date
    #

    def get_export_write_header_date(self) -> bool:
        return self._settings.export_write_header_date

    def set_export_write_header_date(self, value: bool) -> None:
        old_value = self.get_export_write_header_date()
        self._settings.export_write_header_date = value
        self._fire_on_change(old_value, value, signal=self.export_write_header_date_changed)

    export_write_header_date_changed = Signal(bool)
    export_write_header_date = Property(bool, get_export_write_header_date, set_export_write_header_date,
                                        notify=export_write_header_date_changed)

    #
    # Export: write header generator
    #

    def get_export_write_header_generator(self) -> bool:
        return self._settings.export_write_header_generator

    def set_export_write_header_generator(self, value: bool) -> None:
        old_value = self.get_export_write_header_generator()
        self._settings.export_write_header_generator = value
        self._fire_on_change(old_value, value, signal=self.export_write_header_generator_changed)

    export_write_header_generator_changed = Signal(bool)
    export_write_header_generator = Property(bool, get_export_write_header_generator, set_export_write_header_generator,
                                             notify=export_write_header_generator_changed)

    #
    # Export: write header nickname
    #

    def get_export_write_header_nickname(self) -> bool:
        return self._settings.export_write_header_nickname

    def set_export_write_header_nickname(self, value: bool) -> None:
        old_value = self.get_export_write_header_nickname()
        self._settings.export_write_header_nickname = value
        self._fire_on_change(old_value, value, signal=self.export_write_header_nickname_changed)

    export_write_header_nickname_changed = Signal(bool)
    export_write_header_nickname = Property(bool, get_export_write_header_nickname, set_export_write_header_nickname,
                                            notify=export_write_header_nickname_changed)

    #
    # Export: write header video path
    #

    def get_export_write_header_video_path(self) -> bool:
        return self._settings.export_write_header_video_path

    def set_export_write_header_video_path(self, value: bool) -> None:
        old_value = self.get_export_write_header_video_path()
        self._settings.export_write_header_video_path = value
        self._fire_on_change(old_value, value, signal=self.export_write_header_video_path_changed)

    export_write_header_video_path_changed = Signal(bool)
    export_write_header_video_path = Property(bool,
                                              get_export_write_header_video_path,
                                              set_export_write_header_video_path,
                                              notify=export_write_header_video_path_changed)

    #
    # Config input
    #

    def get_config_input(self) -> str:
        return self._settings.config_input

    def set_config_input(self, value: str) -> None:
        old_value = self.get_config_input()
        self._settings.config_input = value
        self._fire_on_change(old_value, value, signal=self.config_input_changed)

    config_input_changed = Signal(str)
    config_input = Property(str, get_config_input, set_config_input, notify=config_input_changed)

    #
    # Config mpv
    #

    def get_config_mpv(self) -> str:
        return self._settings.config_mpv

    def set_config_mpv(self, value: str) -> None:
        old_value = self.get_config_mpv()
        self._settings.config_mpv = value
        self._fire_on_change(old_value, value, signal=self.config_mpv_changed)

    config_mpv_changed = Signal(str)
    config_mpv = Property(str, get_config_mpv, set_config_mpv, notify=config_mpv_changed)
