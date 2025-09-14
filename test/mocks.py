# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from PySide6.QtCore import QObject, QUrl, Signal


class MockedMessageBox(QObject):
    accepted = Signal()
    rejected = Signal()
    closed = Signal()

    def open(self):
        pass


class MockedDialog(QObject):
    accepted = Signal()
    rejected = Signal()
    savePressed = Signal(QUrl)

    def __init__(self):
        super().__init__()
        self.openCalled = False

    def open(self):
        self.openCalled = True
