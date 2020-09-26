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
        # todo needs work if we use it again
        # self.setText(
        #     _translate("MessageBoxes",
        #                "Do you really want to restore the default configuration? This can not be undone."))
        # self.setIcon(QMessageBox.Critical)
        # self.setWindowTitle(_translate("MessageBoxes", "Reset configuration"))
        # self.addButton(_translate("MessageBoxes", "Reset"), QMessageBox.ApplyRole)
        # self.addButton(_translate("MessageBoxes", "Cancel"), QMessageBox.RejectRole)


class QuitNotSavedMB(QMessageBox):
    """
    The message box when the user wants to leave but not all changes were saved.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle(_translate("MessageBoxes", "Unsaved Changes"))
        self.setText(_translate("MessageBoxes", "Do you really want to quit without saving your QC?"))
        self.setIcon(QMessageBox.Critical)
        self.addButton(QMessageBox.Yes)
        self.addButton(QMessageBox.No)


class NewQCDocumentOldNotSavedMB(QMessageBox):
    """
    The message box when the user wants to create a new QC document but the old one is not saved.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle(_translate("MessageBoxes", "Unsaved Changes"))
        self.setText(_translate("MessageBoxes",
                                "Do you really want to create a new QC document without saving your QC?"))
        self.setIcon(QMessageBox.Critical)
        self.addButton(QMessageBox.Yes)
        self.addButton(QMessageBox.No)


class ValidVideoFileFoundMB(QMessageBox):
    """
    The message box when the user imports a QC document and a valid path was found.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle(_translate("MessageBoxes", "Video Found"))
        self.setText(_translate("MessageBoxes", "A video was found. Do you want to open it?"))
        self.setIcon(QMessageBox.Question)
        self.addButton(QMessageBox.Yes)
        self.addButton(QMessageBox.No)


class WhatToDoWithExistingCommentsWhenOpeningNewQCDocumentMB(QMessageBox):
    """
    The message box when the user imports QC documents to ask what to do with the existing comments.
    """

    def __init__(self):
        super().__init__()
        self.setIcon(QMessageBox.Question)
        self.setWindowTitle(_translate("MessageBoxes", "Existing Comments"))
        self.setText(_translate("MessageBoxes", "What do you want to do with the existing comments?"))
        self.setIcon(QMessageBox.Question)
        self.addButton(QMessageBox.Abort)
        self.addButton(_translate("MessageBoxes", "Delete"), QMessageBox.YesRole)
        self.addButton(_translate("MessageBoxes", "Keep"), QMessageBox.NoRole)


class QCDocumentToImportNotValidQCDocumentMB(QMessageBox):
    """
    The message box if the user wants to import a txt file which does not seem to be a valid qc document.
    """

    def __init__(self, not_valid_files: List[str]):
        super().__init__()

        self.setWindowTitle(_translate("MessageBoxes", "Imported Document Not Compatible"))
        self.setText(_translate(
            "MessageBoxes", "The following file(s) are not compatible:", "", len(not_valid_files)))
        self.setInformativeText("- " + "\n\n".join(not_valid_files))
        self.setIcon(QMessageBox.Information)
        self.addButton(QMessageBox.Ok)


class CouldNotSaveQCDocumentError(QMessageBox):
    """
    The message box if saving the document failed.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle(_translate("MessageBoxes", "Saving the QC Document Failed"))
        self.setText(_translate(
            "MessageBoxes", "Are you sure you have permission to write in the selected directory?"))
        self.setIcon(QMessageBox.Critical)
        self.addButton(QMessageBox.Ok)


class CheckForUpdates(QMessageBox):
    _UPDATER_URL = "https://mpvqc.rekt.cc/download/latest.txt"

    def __init__(self):
        super().__init__()

        import requests

        from src import get_metadata
        md = get_metadata()

        try:
            r = requests.get(self._UPDATER_URL, timeout=5)
            version_new = r.text.strip()
            if md.app_version != version_new:
                self.setWindowTitle(_translate("VersionCheckDialog", "New Version Available"))
                self.setText(
                    _translate("VersionCheckDialog", "There is a new version of mpvQC available ({}).<br>"
                                                     "Visit <a href='https://mpvqc.rekt.cc/'>"
                                                     "https://mpvqc.rekt.cc/</a> to download it.").format(version_new))
                self.setIcon(QMessageBox.Information)
            else:
                self.setWindowTitle("👌")
                self.setText(
                    _translate("VersionCheckDialog", "You are already using the most recent version of mpvQC!"))
                self.setIcon(QMessageBox.Information)
        except requests.exceptions.ConnectionError:
            self.setWindowTitle(_translate("VersionCheckDialog", "Server Not Reachable"))
            self.setText(_translate("VersionCheckDialog", "A connection to the server could not be established."))
            self.setIcon(QMessageBox.Warning)
        except requests.exceptions.Timeout:
            self.setWindowTitle(_translate("VersionCheckDialog", "Server Not Reachable"))
            self.setText(_translate("VersionCheckDialog", "The server did not respond quickly enough."))
            self.setIcon(QMessageBox.Warning)
