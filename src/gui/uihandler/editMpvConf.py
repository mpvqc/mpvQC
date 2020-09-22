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


from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QMouseEvent, QFontDatabase
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QPushButton, QAbstractItemView

from src import settings
from src.gui.generated.editCommentTypes import Ui_editCommentTypeDialog
from src.gui.generated.editMpvConf import Ui_editMpvConf

_translate = QCoreApplication.translate


class EditMpvConfDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.__ui = Ui_editMpvConf()
        self.__ui.setupUi(self)

        self.restore_default_button = QPushButton(_translate("EditConfigurationCustomDialog", "Reset"))
        self.restore_default_button.clicked.connect(self.reset)

        self.__ui.buttonBox.addButton(self.restore_default_button, QDialogButtonBox.ResetRole)

        self.__ui.plainTextEdit.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))
        self.__ui.plainTextEdit.setPlainText(settings.Setting_Custom_Configuration_MPV.value)

    def accept(self):
        """
        Action when apply button is pressed.
        """

        settings.Setting_Custom_Configuration_MPV.value = self.__ui.plainTextEdit.toPlainText()
        super(EditMpvConfDialog, self).accept()

    def reset(self):
        settings.Setting_Custom_Configuration_MPV.reset()
        self.__ui.plainTextEdit.setPlainText(settings.Setting_Custom_Configuration_MPV.value)
