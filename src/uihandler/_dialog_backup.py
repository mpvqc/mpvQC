# mpvQC
#
# Copyright (C) 2020 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QDialog

from src import settings, get_files
from src.manager import QcManager
from src.ui import Ui_BackupDialog


class DialogBackup(QDialog):

    def __init__(self, parent, qc_manager: QcManager):
        super().__init__(parent)

        self.__qc_manager = qc_manager
        self.__backup_directory = str(get_files().dir_backup)

        self.__ui = Ui_BackupDialog()
        self.__ui.setupUi(self)

        self.__ui.checkBox.setEnabled(settings.Setting_Custom_QcDocument_AUTOSAVE_ENABLED.value)
        self.__ui.spinBox.setValue(settings.Setting_Custom_QcDocument_AUTOSAVE_INTERVAL.value)

        self.__ui.backupPathLabel.setText(self.__backup_directory)
        self.__ui.openButton.pressed.connect(self.__open_backup_directory)

    def __open_backup_directory(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.__backup_directory))

    def accept(self) -> None:
        settings.Setting_Custom_QcDocument_AUTOSAVE_ENABLED.value = self.__ui.checkBox.isEnabled()
        settings.Setting_Custom_QcDocument_AUTOSAVE_INTERVAL.value = self.__ui.spinBox.value()
        self.__qc_manager.reset_auto_save()
        super(DialogBackup, self).accept()
