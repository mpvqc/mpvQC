# mpvQC
#
# Copyright (C) 2022 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest

import pytest
from PySide6.QtCore import QCoreApplication, QTranslator, QLocale

from mpvqc.services import ReverseTranslatorService


def set_up_service() -> ReverseTranslatorService:
    service = ReverseTranslatorService()
    service._combined_lookup_table = {
        'Spelling': 'Spelling',
        'Rechtschreibung': 'Spelling',
        'איות': 'Spelling',
        'Typo': 'Spelling',
        'Ortografía': 'Spelling',
    }
    service._language_lookup_table = {
        'en-US': {'Spelling': 'Spelling', },
        'de-DE': {'Rechtschreibung': 'Spelling', },
        'he-IL': {'איות': 'Spelling', },
        'it-IT': {'Typo': 'Spelling', },
        'es-ES': {'Ortografía': 'Spelling', }
    }
    return service


SERVICE = set_up_service()


class TestReverseTranslatorService(unittest.TestCase):
    app = QCoreApplication()
    translator = QTranslator()

    def _change_language(self, to_language: str) -> None:
        locale = QLocale(to_language)
        self.app.removeTranslator(self.translator)
        self.translator.load(f':/i18n/{locale.name()}.qm')
        self.app.installTranslator(self.translator)

    def test_set_up(self):
        service = ReverseTranslatorService()
        service.set_up(self._change_language)

        self.assertTrue(len(service._combined_lookup_table) > 14)
        self.assertEqual('Typeset', service._combined_lookup_table['Cartelli'])

        self.assertEqual(5, len(service._language_lookup_table))
        self.assertEqual('Typeset', service._language_lookup_table['it-IT']['Cartelli'])


@pytest.mark.parametrize('expected, translated', [
    ('Spelling', 'Spelling'),
    ('Spelling', 'Rechtschreibung'),
    ('Spelling', 'איות'),
    ('Spelling', 'Typo'),
    ('Spelling', 'Ortografía'),
    ('not-found', 'not-found'),
])
def test_lookup(expected: str, translated: str) -> None:
    assert expected == SERVICE.lookup(translated)


@pytest.mark.parametrize('language, expected, translated', [
    ('en-US', 'Spelling', 'Spelling'),
    ('en-US', 'Rechtschreibung', 'Rechtschreibung'),
    ('de-DE', 'Spelling', 'Rechtschreibung'),
    ('de-DE', 'not-found', 'not-found'),
    ('he-IL', 'Spelling', 'איות'),
    ('es-ES', 'איות', 'איות'),
])
def test_lookup_specific_language(language: str, expected: str, translated: str) -> None:
    assert expected == SERVICE.lookup_specific_language(language, translated)
