# mpvQC
#
# Copyright (C) 2025 mpvQC developers
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

import pytest
from PySide6.QtCore import QLocale

from mpvqc.services.i18n import create_locale_from


@pytest.mark.parametrize(
    ("language_code", "expected_locale"),
    [
        ("de-DE", QLocale("de-DE")),
        ("en-US", QLocale("en-US")),
        ("pt-PT", QLocale("pt-BR")),
        ("pt-BR", QLocale("pt-BR")),
    ],
    ids=[
        "de-DE -> de-DE",
        "en-US -> en-US",
        "pt-PT -> pt-BR",
        "pt-BR -> pt-BR",
    ],
)
def test_locale_mapping(language_code: str, expected_locale: QLocale) -> None:
    result = create_locale_from(language_code)
    assert result == expected_locale
