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


from mpvqc.enums import TimeFormat, TitleFormat


class SettingsService:
    """Access to all settings"""

    def __init__(self):
        import mpvqc.impl.settings as settings

        self._import_video_from_document_automatically = \
            settings.MpvqcBool(key='Import/Load-video-from-document-automatically', default_value=False)

        self._export_nickname = \
            settings.MpvqcNickname(key='Export/Nickname')
        self._export_append_nickname = \
            settings.MpvqcBool(key='Export/Append-nickname', default_value=True)
        self._export_write_header = \
            settings.MpvqcBool(key='Export/Write-header', default_value=True)
        self._export_write_header_date = \
            settings.MpvqcBool(key='Export/Write-header-date', default_value=True)
        self._export_write_header_generator = \
            settings.MpvqcBool(key='Export/Write-header-generator', default_value=True)
        self._export_write_header_nickname = \
            settings.MpvqcBool(key='Export/Write-header-nickname', default_value=False)
        self._export_write_header_video_path = \
            settings.MpvqcBool(key='Export/Write-header-video-path', default_value=True)

        self._title_bar_format = \
            settings.MpvqcTitleFormat(key='TitleBar/Title-format')
        self._status_bar_time_format = \
            settings.MpvqcTimeFormat(key='StatusBar/Time-format')
        self._status_bar_percentage = \
            settings.MpvqcBool(key='StatusBar/Percentage', default_value=True)

        self._backup_enabled = \
            settings.MpvqcBool(key='Backup/Enabled', default_value=True)
        self._backup_interval = \
            settings.MpvqcInt(key='Backup/Interval', default_value=90)

        self._config_input = \
            settings.MpvqcInputConf()
        self._config_mpv = \
            settings.MpvqcMpvConf()

    #
    # Title bar format
    #

    @property
    def title_bar_format(self) -> TitleFormat:
        return self._title_bar_format.get()

    @title_bar_format.setter
    def title_bar_format(self, value: TitleFormat) -> None:
        self._title_bar_format.set(value)

    #
    # Backup enabled
    #

    @property
    def backup_enabled(self) -> bool:
        return self._backup_enabled.get()

    @backup_enabled.setter
    def backup_enabled(self, value: bool) -> None:
        self._backup_enabled.set(value)

    #
    # Backup interval
    #

    @property
    def backup_interval(self) -> int:
        return self._backup_interval.get()

    @backup_interval.setter
    def backup_interval(self, value: int) -> None:
        self._backup_interval.set(value)

    #
    # Status bar time format
    #

    @property
    def status_bar_time_format(self) -> TimeFormat:
        return self._status_bar_time_format.get()

    @status_bar_time_format.setter
    def status_bar_time_format(self, value: TimeFormat) -> None:
        self._status_bar_time_format.set(value)

    #
    # Status bar percentage
    #

    @property
    def status_bar_percentage(self) -> bool:
        return self._status_bar_percentage.get()

    @status_bar_percentage.setter
    def status_bar_percentage(self, value: bool) -> None:
        self._status_bar_percentage.set(value)

    #
    # Import video from document automatically
    #

    @property
    def import_video_from_document_automatically(self) -> bool:
        return self._import_video_from_document_automatically.get()

    @import_video_from_document_automatically.setter
    def import_video_from_document_automatically(self, value: bool) -> None:
        self._import_video_from_document_automatically.set(value)

    #
    # Export: nickname
    #

    @property
    def export_nickname(self) -> str:
        return self._export_nickname.get()

    @export_nickname.setter
    def export_nickname(self, value: str) -> None:
        self._export_nickname.set(value)

    #
    # Export: append nickname
    #

    @property
    def export_append_nickname(self) -> bool:
        return self._export_append_nickname.get()

    @export_append_nickname.setter
    def export_append_nickname(self, value: bool) -> None:
        self._export_append_nickname.set(value)

    #
    # Export: write header
    #

    @property
    def export_write_header(self) -> bool:
        return self._export_write_header.get()

    @export_write_header.setter
    def export_write_header(self, value: bool) -> None:
        self._export_write_header.set(value)

    #
    # Export: write header date
    #

    @property
    def export_write_header_date(self) -> bool:
        return self._export_write_header_date.get()

    @export_write_header_date.setter
    def export_write_header_date(self, value: bool) -> None:
        self._export_write_header_date.set(value)

    #
    # Export: write header generator
    #

    @property
    def export_write_header_generator(self) -> bool:
        return self._export_write_header_generator.get()

    @export_write_header_generator.setter
    def export_write_header_generator(self, value: bool) -> None:
        self._export_write_header_generator.set(value)

    #
    # Export: write header nickname
    #

    @property
    def export_write_header_nickname(self) -> bool:
        return self._export_write_header_nickname.get()

    @export_write_header_nickname.setter
    def export_write_header_nickname(self, value: bool) -> None:
        self._export_write_header_nickname.set(value)

    #
    # Export: write header video path
    #

    @property
    def export_write_header_video_path(self) -> bool:
        return self._export_write_header_video_path.get()

    @export_write_header_video_path.setter
    def export_write_header_video_path(self, value: bool) -> None:
        self._export_write_header_video_path.set(value)

    #
    # Config input
    #

    @property
    def config_input(self) -> str:
        return self._config_input.get()

    @config_input.setter
    def config_input(self, value: str) -> None:
        self._config_input.set(value)

    #
    # Config mpv
    #

    @property
    def config_mpv(self) -> str:
        return self._config_mpv.get()

    @config_mpv.setter
    def config_mpv(self, value: str) -> None:
        self._config_mpv.set(value)
