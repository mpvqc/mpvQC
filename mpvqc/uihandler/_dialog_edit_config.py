# Copyright (C) 2016-2017 Frechdachs <frechdachs@rekt.cc>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from abc import abstractmethod

from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from mpvqc import get_settings
from mpvqc.ui_loader import init_from_resources


class _EditConfDialog(QDialog):

    def __init__(self, title: str):
        super().__init__()

        self._ui = init_from_resources(self, "qrc:/data/ui/dialog_edit_config.ui")
        self._ui.title.setText(title)

        self._reset_button = self._ui.buttonBox.addButton(QDialogButtonBox.Reset)
        self._reset_button.clicked.connect(self.on_reset)

        self._ui.plainTextEdit.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))

    def accept(self):
        self.on_accept()
        super(_EditConfDialog, self).accept()

    @abstractmethod
    def on_accept(self):
        pass

    @abstractmethod
    def on_reset(self):
        pass


class EditConfDialogInputConf(_EditConfDialog):

    def __init__(self, title: str):
        super().__init__(title)

        s = get_settings()
        self._ui.plainTextEdit.setPlainText(s.config_file_input)

    def on_accept(self):
        get_settings().config_file_input = self._ui.plainTextEdit.toPlainText()

    def on_reset(self):
        self._ui.plainTextEdit.setPlainText(get_settings().config_file_input_get_default())


class EditConfDialogMpvConf(_EditConfDialog):

    def __init__(self, title: str):
        super().__init__(title)

        s = get_settings()
        self._ui.plainTextEdit.setPlainText(s.config_file_mpv)

    def on_accept(self):
        get_settings().config_file_mpv = self._ui.plainTextEdit.toPlainText()

    def on_reset(self):
        self._ui.plainTextEdit.setPlainText(get_settings().config_file_mpv_get_default())
