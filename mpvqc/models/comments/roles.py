# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import ClassVar

from PySide6.QtCore import QByteArray


class Role:
    TIME = 1010
    TYPE = 1020
    COMMENT = 1030

    MAPPING: ClassVar[dict[int, QByteArray]] = {
        TIME: QByteArray(b"time"),
        TYPE: QByteArray(b"commentType"),
        COMMENT: QByteArray(b"comment"),
    }
