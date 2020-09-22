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
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QPushButton

from src.gui.generated.editConf import Ui_editConf

_translate = QCoreApplication.translate


class EditConfDialog(QDialog):

    def __init__(self, settings_object, title: str):
        super().__init__()

        self.__ui = Ui_editConf()
        self.__ui.setupUi(self)
        self.__ui.title.setText(title)

        self.__settings_object = settings_object

        self.restore_default_button = QPushButton(_translate("EditConfigurationCustomDialog", "Reset"))
        self.restore_default_button.clicked.connect(self.reset)

        self.__ui.buttonBox.addButton(self.restore_default_button, QDialogButtonBox.ResetRole)

        self.__ui.plainTextEdit.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))
        self.__ui.plainTextEdit.setPlainText(self.__settings_object.value)

    def accept(self):
        """
        Action when apply button is pressed.
        """

        self.__settings_object.value = self.__ui.plainTextEdit.toPlainText()
        super(EditConfDialog, self).accept()

    def reset(self):
        self.__settings_object.reset()
        self.__ui.plainTextEdit.setPlainText(self.__settings_object.value)
