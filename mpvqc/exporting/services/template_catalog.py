# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import operator
from dataclasses import dataclass
from typing import TYPE_CHECKING

import inject

from mpvqc.services import ApplicationPathsService

if TYPE_CHECKING:
    from pathlib import Path


@dataclass(frozen=True)
class ExportTemplate:
    name: str
    path: Path


class ExportTemplateCatalogService:
    _app_paths = inject.attr(ApplicationPathsService)

    def list_templates(self) -> list[ExportTemplate]:
        templates = [ExportTemplate(name=path.stem, path=path) for path in self._app_paths.files_export_templates]
        templates.sort(key=operator.attrgetter("name"))
        return templates
