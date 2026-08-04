# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
from typing import override

import pytest

from mpvqc.services import ResourceService


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
