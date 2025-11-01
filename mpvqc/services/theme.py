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
        self._id_to_theme = {theme["identifier"]: theme for theme in self._themes}
        self._id_to_index = {theme["identifier"]: idx for idx, theme in enumerate(self._themes)}

    @property
    def previews(self) -> list[dict]:
        return self._themes

    def palette(self, identifier: str) -> list[dict]:
        theme = self._id_to_theme.get(identifier, self._id_to_theme.get("material-you-dark"))
        return theme["palettes"]

    def index(self, identifier: str) -> int:
        return self._id_to_index.get(identifier, self._id_to_index.get("material-you-dark", 4))
