# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os

from PySide6.QtQml import QmlSingleton

IS_TESTING = os.getenv("MPVQC_QML_TESTS", "false").lower() == "true"


def QmlSingletonInProductionOnly(cls):
    if IS_TESTING:
        return cls  # Do not add decorator
    return QmlSingleton(cls)
