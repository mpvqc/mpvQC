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


def test_get_theme_summaries_and_builtin_themes(service):
    summaries = service.get_theme_summaries()
    assert len(summaries) > 0

    summaries = service.get_theme_summaries()
    assert any("Material You" == summary["name"] for summary in summaries)
    assert any("Material You Dark" == summary["name"] for summary in summaries)


def test_get_summary(service):
    existing = service.get_theme_summary("Material You")
    assert existing["name"] == "Material You"

    fallback = "Material You Dark"
    assert service.get_theme_summary("")["name"] == fallback


def test_get_theme_colors(service):
    fallback_0_background = "#221919"
    colors = service.get_theme_colors("")
    assert len(colors) > 0
    assert colors[0]["background"].casefold() == fallback_0_background.casefold()

    selected_0_background = "#FFF0F0"
    colors = service.get_theme_colors("Material You")
    assert len(colors) > 0
    assert colors[0]["background"].casefold() == selected_0_background.casefold()


def test_get_theme_color(service):
    fallback_background = "#221919"
    color = service.get_theme_color(0, "")
    assert color["background"].casefold() == fallback_background.casefold()

    fallback_background = "#231917"
    color = service.get_theme_color(3, "")
    assert color["background"].casefold() == fallback_background.casefold()

    fallback_background = "#22191A"
    color = service.get_theme_color(4000, "")
    assert color["background"].casefold() == fallback_background.casefold()

    selected_background = "#FFF0F0"
    color = service.get_theme_color(0, "Material You")
    assert color["background"].casefold() == selected_background.casefold()

    selected_background = "#FFF1ED"
    color = service.get_theme_color(3, "Material You")
    assert color["background"].casefold() == selected_background.casefold()

    selected_background = "#FFF0F0"
    color = service.get_theme_color(4000, "Material You")
    assert color["background"].casefold() == selected_background.casefold()
