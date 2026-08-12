# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import operator
from dataclasses import dataclass

import inject
from PySide6.QtCore import QUrl

from mpvqc.services import ApplicationPathsService, TypeMapperService


@dataclass(frozen=True)
class ExportTemplate:
    name: str
    url: QUrl


class ExportTemplateCatalogService:
    _app_paths = inject.attr(ApplicationPathsService)
    _type_mapper = inject.attr(TypeMapperService)

    def list_templates(self) -> list[ExportTemplate]:
        templates = [
            ExportTemplate(name=path.stem, url=self._type_mapper.map_path_to_url(path))
            for path in self._app_paths.files_export_templates
        ]
        templates.sort(key=operator.attrgetter("name"))
        return templates
