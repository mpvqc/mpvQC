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
from unittest.mock import MagicMock

import inject
from PySide6.QtCore import QResource

from mpvqc.services import TranslationService, SettingsService


class TestTranslationService(unittest.TestCase):
    mocked_application: MagicMock
    mocked_engine: MagicMock
    mocked_settings: MagicMock
    translation_service: TranslationService

    @classmethod
    def setUpClass(cls):
        from test import import_resources
        import_resources()

    def setUp(self):
        self.mocked_settings = MagicMock()

        inject.clear_and_configure(lambda binder: binder
                                   .bind(SettingsService, self.mocked_settings))

        self.mocked_application = MagicMock()
        self.mocked_engine = MagicMock()

        self.translation_service = TranslationService()
        self.translation_service.initialize_with(application=self.mocked_application, engine=self.mocked_engine)

    def tearDown(self):
        inject.clear()

    def test_restore_language(self):
        # noinspection PyBroadException
        try:
            self.mocked_settings.language = 'en'

            service = self.translation_service
            service.restore_language()
        except Exception as e:
            self.fail(f"'service.restore_language()' raised {type(e)}")

    def test_set_language_load_translation(self):
        service = self.translation_service
        service.set_language('de')

        self.assertTrue(self.mocked_application.installTranslator.called)

    def test_set_language_layout_has_changed(self):
        service = self.translation_service
        service.set_language('he')

        self.assertTrue(service.rtl_enabled)

    def test_set_language_layout_has_not_changed(self):
        service = self.translation_service
        service.set_language('it')

        self.assertFalse(service.rtl_enabled)

    def test_set_language_update_language_settings(self):
        before, after = 'en', 'he'
        self.mocked_settings.language = before

        service = self.translation_service
        service.set_language(after)

        self.assertEqual(after, self.mocked_settings.language)

    def test_set_language_retranslate(self):
        service = self.translation_service
        service.set_language('it')

        self.assertTrue(self.mocked_engine.retranslate.called)

    def test_translation_language_doesnt_exists(self):
        service = self.translation_service
        locale = 'non-existent'

        path = service.translation_path_for(locale)
        self.assertFalse(QResource(path).isValid())

    def test_translation_language_de_exists(self):
        service = self.translation_service
        locale = 'de'

        path = service.translation_path_for(locale)
        self.assertTrue(QResource(path).isValid())
