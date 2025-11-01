# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json

import inject

from mpvqc.services import ResourceReaderService


class ThemeService:
    _resource_reader: ResourceReaderService = inject.attr(ResourceReaderService)

    def __init__(self):
        resource = self._resource_reader.read_from(":/data/themes.json")
        self._themes = json.loads(resource)
        self._id_to_theme: dict[str, dict] = {theme["identifier"]: theme for theme in self._themes}
        self._id_to_index: dict[str, int] = {theme["identifier"]: idx for idx, theme in enumerate(self._themes)}

    @property
    def previews(self) -> list[dict]:
        return self._themes

    def palette(self, theme_identifier: str) -> list[dict]:
        theme = self._id_to_theme.get(theme_identifier) or self._id_to_theme.get("material-you-dark")
        if theme is None:
            msg = f"Theme identifier {theme_identifier} not found in themes.json"
            raise ValueError(msg)
        return theme["palettes"]

    def theme_index(self, theme_identifier: str) -> int:
        if (idx := self._id_to_index.get(theme_identifier)) is not None:
            return idx
        if (idx := self._id_to_index.get("material-you-dark")) is not None:
            return idx
        return 1
