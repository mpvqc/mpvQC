# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import IntEnum
from typing import Final

from PySide6.QtCore import QByteArray, Qt


class Role(IntEnum):
    TIME = Qt.ItemDataRole.UserRole + 1
    TYPE = Qt.ItemDataRole.UserRole + 2
    COMMENT = Qt.ItemDataRole.UserRole + 3


ROLE_NAMES: Final[dict[int, QByteArray]] = {
    Role.TIME: QByteArray(b"time"),
    Role.TYPE: QByteArray(b"commentType"),
    Role.COMMENT: QByteArray(b"comment"),
}
