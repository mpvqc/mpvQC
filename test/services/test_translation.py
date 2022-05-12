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

from mpvqc.services import TranslationService


class TestTranslationService(unittest.TestCase):
    mocked_application: MagicMock
    mocked_engine: MagicMock
    translation_service: TranslationService

    def setUp(self):
        self.mocked_application = MagicMock()
        self.mocked_engine = MagicMock()

        self.translation_service = TranslationService()
        self.translation_service.initialize_with(application=self.mocked_application, engine=self.mocked_engine)

    def tearDown(self):
        inject.clear()

    def test_set_language_load_translation(self):
        service = self.translation_service
        service.load('de')

        self.assertTrue(self.mocked_application.installTranslator.called)

    def test_set_language_retranslate(self):
        service = self.translation_service
        service.load('it')

        self.assertTrue(self.mocked_engine.retranslate.called)

    def test_translation_language_doesnt_exists(self):
        service = self.translation_service
        locale = 'non-existent'

        path = service._translation_path_for(locale)
        self.assertFalse(QResource(path).isValid())

    def test_translation_language_de_exists(self):
        service = self.translation_service
        locale = 'de'

        path = service._translation_path_for(locale)
        self.assertTrue(QResource(path).isValid())
