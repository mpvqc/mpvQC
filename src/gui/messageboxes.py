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


from typing import List

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMessageBox

_translate = QCoreApplication.translate


class ConfigurationResetMB(QMessageBox):
    """
    The message box when the user wants to reset the configuration changes.
    """

    def __init__(self):
        super().__init__()
        self.setText(
            _translate("MessageBoxes",
                       "Do you really want to restore the default configuration? This can not be undone."))
        self.setIcon(QMessageBox.Critical)
        self.setWindowTitle(_translate("MessageBoxes", "Reset configuration"))
        self.addButton(_translate("MessageBoxes", "Reset"), QMessageBox.ApplyRole)
        self.addButton(_translate("MessageBoxes", "Cancel"), QMessageBox.RejectRole)


class QuitNotSavedMB(QMessageBox):
    """
    The message box when the user wants to leave but not all changes were saved.
    """

    def __init__(self):
        super().__init__()
        self.setText(
            _translate("MessageBoxes", "Do you really want to quit without saving your QC?"))
        self.setIcon(QMessageBox.Warning)
        self.setWindowTitle(_translate("MessageBoxes", "Discard QC"))
        self.addButton(_translate("MessageBoxes", "No"), QMessageBox.NoRole)
        self.addButton(_translate("MessageBoxes", "Yes"), QMessageBox.YesRole)


class NewQCDocumentOldNotSavedMB(QMessageBox):
    """
    The message box when the user wants to create a new QC document but the old one is not saved.
    """

    def __init__(self):
        super().__init__()
        self.setText(
            _translate("MessageBoxes", "Do you really want to create a new QC Document without saving your QC?"))
        self.setIcon(QMessageBox.Warning)
        self.setWindowTitle(_translate("MessageBoxes", "Create new QC document"))
        self.addButton(_translate("MessageBoxes", "No"), QMessageBox.NoRole)
        self.addButton(_translate("MessageBoxes", "Yes"), QMessageBox.YesRole)


class ValidVideoFileFoundMB(QMessageBox):
    """
    The message box when the user imports a QC document and a valid path was found.
    """

    def __init__(self):
        super().__init__()
        self.setText(
            _translate("MessageBoxes", "A valid video file was found. Do you want to open it?"))
        self.setIcon(QMessageBox.Information)
        self.setWindowTitle(_translate("MessageBoxes", "Open corresponding video file"))
        self.addButton(_translate("MessageBoxes", "No"), QMessageBox.NoRole)
        self.addButton(_translate("MessageBoxes", "Yes"), QMessageBox.YesRole)


class WhatToDoWithExistingCommentsWhenOpeningNewQCDocumentMB(QMessageBox):
    """
    The message box when the user imports QC documents to ask what to do with the existing comments.
    """

    def __init__(self):
        super().__init__()
        self.setText(
            _translate("MessageBoxes", "What would you want to do with all existing comments?"))
        self.setIcon(QMessageBox.Information)
        self.setWindowTitle(_translate("MessageBoxes", "How to proceed"))
        self.addButton(_translate("MessageBoxes", "Abort import"), QMessageBox.RejectRole)
        self.addButton(_translate("MessageBoxes", "Delete"), QMessageBox.YesRole)
        self.addButton(_translate("MessageBoxes", "Keep"), QMessageBox.NoRole)


class QCDocumentToImportNotValidQCDocumentMB(QMessageBox):
    """
    The message box if the user wants to import a txt file which does not seem to be a valid qc document.
    """

    def __init__(self, not_valid_files: List[str]):
        super().__init__()
        self.setText("\n".join(not_valid_files) +
                     _translate("MessageBoxes", " does not seem to be valid."))
        self.setIcon(QMessageBox.Information)
        self.setWindowTitle(_translate("MessageBoxes", "Not valid"))
        self.addButton(_translate("MessageBoxes", "Ok"), QMessageBox.AcceptRole)


class CheckForUpdates(QMessageBox):

    _UPDATER_URL = "https://mpvqc.rekt.cc/download/latest.txt"

    def __init__(self):
        super().__init__()
        from start import APPLICATION_VERSION
        import requests

        try:
            r = requests.get(self._UPDATER_URL, timeout=5)
            version_new = r.text.strip()
            if APPLICATION_VERSION != version_new:
                self.setWindowTitle(_translate("VersionCheck", "New version available"))
                self.setText(
                    _translate("VersionCheck", "There is a new version of mpvQC available ({}).<br>"
                                               "Visit <a href='https://mpvqc.rekt.cc/'>"
                                               "https://mpvqc.rekt.cc/</a> to download it.").format(version_new))
            else:
                self.setWindowTitle("👌")
                self.setText(_translate("VersionCheck", "You are already using the most recent version of mpvQC!"))
        except requests.exceptions.ConnectionError:
            self.setText(_translate("VersionCheck", "A connection to the server could not be established."))
        except requests.exceptions.Timeout:
            self.setText(_translate("VersionCheck", "The server did not respond quickly enough."))