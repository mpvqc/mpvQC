# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import errno
import logging
import os
import secrets
import shutil
from contextlib import contextmanager
from typing import TYPE_CHECKING

from PySide6.QtCore import QCoreApplication

from .errors import ExportError

if TYPE_CHECKING:
    from collections.abc import Generator
    from pathlib import Path

logger = logging.getLogger(__name__)


def write(file: Path, content: str) -> None:
    try:
        with replacing(file) as temporary:
            temporary.write_text(content, encoding="utf-8", newline="\n")
    except OSError as e:
        logger.exception("Failed to save document to %s", file)
        #: Shown when writing the QC document fails (permission denied, disk full,
        #: target directory missing). The technical detail is logged, not surfaced.
        msg = QCoreApplication.translate("MessageBoxes", "The document could not be saved.")
        raise ExportError(msg) from e


@contextmanager
def replacing(target: Path) -> Generator[Path]:
    target = target.resolve()
    if target.exists() and not os.access(target, os.W_OK):
        raise PermissionError(errno.EACCES, os.strerror(errno.EACCES), str(target))

    temporary = target.with_name(f".{target.name}.{secrets.token_hex(4)}.tmp")
    try:
        yield temporary
        _move(temporary, onto=target)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def _move(temporary: Path, *, onto: Path) -> None:
    with temporary.open("rb+") as file:
        os.fsync(file.fileno())
    if onto.exists():
        shutil.copymode(onto, temporary)
    temporary.replace(onto)
