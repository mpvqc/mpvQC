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
