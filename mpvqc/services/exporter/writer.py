# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from PySide6.QtCore import QCoreApplication

from .documents import render_classic, render_v1

if TYPE_CHECKING:
    from pathlib import Path

    from mpvqc.services.resource import ResourceService

    from .context import RenderContext

logger = logging.getLogger(__name__)


class ExportError(Exception):
    def __init__(self, message: str, lineno: int = -1) -> None:
        super().__init__(message)
        self.message = message
        self.lineno = lineno


def export_document(file: Path, template: Path, context: RenderContext) -> None:
    from jinja2 import TemplateError, TemplateSyntaxError

    try:
        user_template = template.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        logger.exception("Failed to read export template %s", template)
        #: Shown when a user-supplied export template cannot be read (file gone,
        #: permission denied, or not valid UTF-8). The technical detail is logged,
        #: not surfaced to the user.
        message = QCoreApplication.translate("MessageBoxes", "The export template could not be read.")
        raise ExportError(message) from e

    try:
        content = render_classic(user_template, context)
    except TemplateSyntaxError as e:
        raise ExportError(e.message or "", e.lineno) from e
    except TemplateError as e:
        raise ExportError(e.message or "") from e

    _write(file, content)


def save_v1(file: Path, context: RenderContext) -> None:
    _write(file, render_v1(context))


def save_classic(file: Path, resources: ResourceService, context: RenderContext) -> None:
    _write(file, render_classic(resources.default_export_template, context))


def _write(file: Path, content: str) -> None:
    try:
        file.write_text(content, encoding="utf-8", newline="\n")
    except OSError as e:
        logger.exception("Failed to save document to %s", file)
        #: Shown when writing the QC document fails (permission denied, disk full,
        #: target directory missing). The technical detail is logged, not surfaced.
        message = QCoreApplication.translate("MessageBoxes", "The document could not be saved.")
        raise ExportError(message) from e
