# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
from collections.abc import Callable
from typing import override

import pytest

from mpvqc.appearance.services import AppearanceSettingsService, ColorScheme, SystemColorScheme
from mpvqc.services import ResourceService


@pytest.fixture
def appearance_settings_service(qsettings) -> AppearanceSettingsService:
    return AppearanceSettingsService(qsettings)


class FakeResourceService(ResourceService):
    def __init__(self, palette_catalog_json: str) -> None:
        self._palette_catalog_json = palette_catalog_json

    @property
    @override
    def palette_catalog_json(self) -> str:
        return self._palette_catalog_json


@pytest.fixture(scope="session")
def make_palette_family_data():
    def _make(
        *,
        default_accent_color: str,
        accents: list[str],
        color_scheme: str | None = None,
        preview_color: str | None = None,
    ) -> dict:
        palette_family = json.loads(ResourceService().palette_catalog_json)[0]
        palettes = palette_family["palettes"][: len(accents)]
        for palette, accent in zip(palettes, accents, strict=True):
            palette["identifier"] = accent
        if color_scheme is not None:
            palette_family["color_scheme"] = color_scheme
        if preview_color is not None:
            palette_family["preview_color"] = preview_color
        palette_family["palettes"] = palettes
        palette_family["default_accent_color"] = default_accent_color
        return palette_family

    return _make


@pytest.fixture(scope="session")
def make_resource_service():
    def _make(*palette_families: dict) -> ResourceService:
        return FakeResourceService(json.dumps(list(palette_families)))

    return _make


class FakeStyleHints:
    """Stands in for the application's style hints: what the system reports,
    the override the app pushes back, and the change notification."""

    def __init__(self, system_color_scheme: SystemColorScheme) -> None:
        self._system_color_scheme = system_color_scheme
        self._override: ColorScheme | None = None
        self._callbacks: list[Callable[[], None]] = []
        self.calls: list[str] = []

    @property
    def color_scheme(self) -> SystemColorScheme:
        return self._system_color_scheme if self._override is None else self._override

    def set_color_scheme(self, color_scheme: ColorScheme) -> None:
        self.calls.append(f"set {type(color_scheme).__name__}")
        self._apply(override=color_scheme, system_color_scheme=self._system_color_scheme)

    def unset_color_scheme(self) -> None:
        self.calls.append("unset")
        self._apply(override=None, system_color_scheme=self._system_color_scheme)

    def on_color_scheme_changed(self, callback: Callable[[], None]) -> None:
        self._callbacks.append(callback)

    def system_reports(self, color_scheme: SystemColorScheme) -> None:
        """The desktop flipped its color scheme."""
        self._apply(override=self._override, system_color_scheme=color_scheme)

    def _apply(self, *, override: ColorScheme | None, system_color_scheme: SystemColorScheme) -> None:
        before = self.color_scheme
        self._override = override
        self._system_color_scheme = system_color_scheme
        if self.color_scheme != before:
            for callback in self._callbacks:
                callback()


@pytest.fixture(scope="session")
def make_style_hints():
    def _make(system_color_scheme: SystemColorScheme) -> FakeStyleHints:
        return FakeStyleHints(system_color_scheme)

    return _make
