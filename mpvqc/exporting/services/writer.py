# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from PySide6.QtCore import QCoreApplication

from .errors import ExportError

if TYPE_CHECKING:
    from pathlib import Path

logger = logging.getLogger(__name__)


def write(file: Path, content: str) -> None:
    try:
        file.write_text(content, encoding="utf-8", newline="\n")
    except OSError as e:
        logger.exception("Failed to save document to %s", file)
        #: Shown when writing the QC document fails (permission denied, disk full,
        #: target directory missing). The technical detail is logged, not surfaced.
        msg = QCoreApplication.translate("MessageBoxes", "The document could not be saved.")
        raise ExportError(msg) from e
