# mpvQC
#
# Copyright (C) 2024 mpvQC developers
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

from mpvqc.services import ThemeService


@pytest.fixture(scope="session")
def service():
    return ThemeService()


def test_parse_builtin_themes(service):
    summaries = service.get_theme_summaries()
    assert len(summaries) > 0

    for summary in summaries:
        color_options = service.get_options_for_theme(summary["name"])
        assert len(color_options) > 3
