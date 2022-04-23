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


import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import inject
from PySide6.QtCore import QSettings

from mpvqc.enums import TimeFormat, TitleFormat
from mpvqc.impl import FileReader
from mpvqc.services import SettingsInitializerService, SettingsService, FileService, ResourceService


class TestSettingsService(unittest.TestCase):
    q_settings = QSettings('', QSettings.IniFormat)

    def execute_get(self, setting: str, expect: any):
        actual = getattr(SettingsService(), setting)
        self.assertEqual(expect, actual)

    def execute_set_get(self, setting: str, then_set: any, then_expect: any):
        settings = SettingsService()
        setattr(settings, setting, then_set)
        self.execute_get(setting, expect=then_expect)

    def setUp(self):
        settings_init = MagicMock()
        settings_init.backing_object = self.q_settings
        inject.clear_and_configure(lambda binder: binder
                                   .bind(SettingsInitializerService, settings_init)
                                   .bind(ResourceService, MagicMock()))

    def tearDown(self):
        self.q_settings.clear()
        inject.clear()

    #
    # Title bar format
    #

    def test_title_bar_format_get(self):
        self.execute_get('title_bar_format', expect=TitleFormat.FILE_NAME)

    def test_title_bar_format_set_get(self):
        different = TitleFormat.EMPTY
        self.execute_set_get('title_bar_format', then_set=different, then_expect=different)

    #
    # Backup enabled
    #

    def test_backup_enabled_get(self):
        self.execute_get('backup_enabled', expect=True)

    def test_backup_enabled_set_get(self):
        different = False
        self.execute_set_get('backup_enabled', then_set=different, then_expect=different)

    #
    # Backup interval
    #

    def test_backup_interval_get(self):
        self.execute_get('backup_interval', expect=90)

    def test_backup_interval_set_get(self):
        different = 42
        self.execute_set_get('backup_interval', then_set=different, then_expect=different)

    #
    # Status bar time format
    #

    def test_status_bar_time_format_get(self):
        self.execute_get('status_bar_time_format', expect=TimeFormat.CURRENT_TOTAL_TIME)

    def test_status_bar_time_format_set_get(self):
        different = TimeFormat.EMPTY
        self.execute_set_get('status_bar_time_format', then_set=different, then_expect=different)

    #
    # Status bar percentage
    #

    def test_status_bar_percentage_get(self):
        self.execute_get('status_bar_percentage', expect=True)

    def test_status_bar_percentage_set_get(self):
        different = False
        self.execute_set_get('status_bar_percentage', then_set=different, then_expect=different)

    #
    # Import video from document automatically
    #

    def test_import_video_from_document_automatically_get(self):
        self.execute_get('import_video_from_document_automatically', expect=False)

    def test_import_video_from_document_automatically_set_get(self):
        different = True
        self.execute_set_get('import_video_from_document_automatically', then_set=different, then_expect=different)

    #
    # Export: nickname
    #

    MODULE_NICKNAME = 'mpvqc.impl.settings.defaults'
    username = 'mpvqc-username'
    user = 'mpvqc-user'

    @patch(f'{MODULE_NICKNAME}.environ', {'USERNAME': username, 'USER': user})
    def test_export_nickname_get(self):
        self.execute_get('export_nickname', expect=self.username)

    def test_export_nickname_set_get(self):
        different = 'kotlin'
        self.execute_set_get('export_nickname', then_set=different, then_expect=different)

    #
    # Export: append nickname
    #

    def test_export_append_nickname_get(self):
        self.execute_get('export_append_nickname', expect=True)

    def test_export_append_nickname_set_get(self):
        different = False
        self.execute_set_get('export_append_nickname', then_set=different, then_expect=different)

    #
    # Export: write header
    #

    def test_export_write_header_get(self):
        self.execute_get('export_write_header', expect=True)

    def test_export_write_header_set_get(self):
        different = False
        self.execute_set_get('export_write_header', then_set=different, then_expect=different)

    #
    # Export: write header date
    #

    def test_export_write_header_date_get(self):
        self.execute_get('export_write_header_date', expect=True)

    def test_export_write_header_date_set_get(self):
        different = False
        self.execute_set_get('export_write_header_date', then_set=different, then_expect=different)

    #
    # Export: write header generator
    #

    def test_export_write_header_generator_get(self):
        self.execute_get('export_write_header_generator', expect=True)

    def test_export_write_header_generator_set_get(self):
        different = False
        self.execute_set_get('export_write_header_generator', then_set=different, then_expect=different)

    #
    # Export: write header nickname
    #

    def test_export_write_header_nickname_get(self):
        self.execute_get('export_write_header_nickname', expect=False)

    def test_export_write_header_nickname_set_get(self):
        different = True
        self.execute_set_get('export_write_header_nickname', then_set=different, then_expect=different)

    #
    # Export: write header video path
    #

    def test_export_write_header_video_path_get(self):
        self.execute_get('export_write_header_video_path', expect=True)

    def test_export_write_header_video_path_set_get(self):
        different = False
        self.execute_set_get('export_write_header_video_path', then_set=different, then_expect=different)

    #
    # Config input
    #

    MODULE_INPUT_CONF = 'mpvqc.impl.settings.special_input_conf'
    MODULE_CONF = 'mpvqc.impl.settings.templates'

    # noinspection DuplicatedCode
    def test_config_input_get(self, *_):
        content = 'Hello'

        def additional(binder: inject.Binder):
            mocked_file_reader = MagicMock()
            mocked_file_reader.read.return_value = content

            settings_init = MagicMock()
            settings_init.backing_object = self.q_settings

            file_service = MagicMock()
            file_service.file_input_conf = Path.home()

            binder.bind_to_constructor(ResourceService, lambda: MagicMock())
            binder.bind_to_constructor(FileReader, lambda: mocked_file_reader)
            binder.bind_to_constructor(FileService, lambda: file_service)
            binder.bind_to_constructor(SettingsInitializerService, lambda: settings_init)

        inject.clear_and_configure(additional, bind_in_runtime=False)
        self.execute_get('config_input', expect=content)

    # noinspection DuplicatedCode
    @patch(f'{MODULE_CONF}.FileWriter.write')
    def test_config_input_set_get(self, *_):
        content = 'Hello'
        different = 'World'

        def additional(binder: inject.Binder):
            mocked_file_reader = MagicMock()
            mocked_file_reader.read.side_effect = [content, different]

            settings_init = MagicMock()
            settings_init.backing_object = self.q_settings

            file_service = MagicMock()
            file_service.file_input_conf = Path.home()

            binder.bind_to_constructor(ResourceService, lambda: MagicMock())
            binder.bind_to_constructor(FileReader, lambda: mocked_file_reader)
            binder.bind_to_constructor(FileService, lambda: file_service)
            binder.bind_to_constructor(SettingsInitializerService, lambda: settings_init)

        inject.clear_and_configure(additional, bind_in_runtime=False)

        self.execute_get('config_input', expect=content)
        self.execute_set_get('config_input', then_set=different, then_expect=different)

    #
    # Config mpv
    #

    # noinspection DuplicatedCode
    def test_config_mpv_get(self, *_):
        content = 'Hello'

        def additional(binder: inject.Binder):
            mocked_file_reader = MagicMock()
            mocked_file_reader.read.return_value = content

            settings_init = MagicMock()
            settings_init.backing_object = self.q_settings

            file_service = MagicMock()
            file_service.file_input_conf = Path.home()

            binder.bind_to_constructor(ResourceService, lambda: MagicMock())
            binder.bind_to_constructor(FileReader, lambda: mocked_file_reader)
            binder.bind_to_constructor(FileService, lambda: file_service)
            binder.bind_to_constructor(SettingsInitializerService, lambda: settings_init)

        inject.clear_and_configure(additional, bind_in_runtime=False)
        self.execute_get('config_mpv', expect=content)

    # noinspection DuplicatedCode
    @patch(f'{MODULE_CONF}.FileWriter.write')
    def test_config_mpv_set_get(self, *_):
        content = 'Hello'
        different = 'World'

        def additional(binder: inject.Binder):
            mocked_file_reader = MagicMock()
            mocked_file_reader.read.side_effect = [content, different]

            settings_init = MagicMock()
            settings_init.backing_object = self.q_settings

            file_service = MagicMock()
            file_service.file_input_conf = Path.home()

            binder.bind_to_constructor(ResourceService, lambda: MagicMock())
            binder.bind_to_constructor(FileReader, lambda: mocked_file_reader)
            binder.bind_to_constructor(FileService, lambda: file_service)
            binder.bind_to_constructor(SettingsInitializerService, lambda: settings_init)

        inject.clear_and_configure(additional, bind_in_runtime=False)

        self.execute_get('config_mpv', expect=content)
        self.execute_set_get('config_mpv', then_set=different, then_expect=different)
