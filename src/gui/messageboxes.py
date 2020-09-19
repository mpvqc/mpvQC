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
from PyQt5.QtWidgets import QMessageBox

_translate = QCoreApplication.translate


class ConfigurationHasChangedMB(QMessageBox):
    """
    The message box when the user has changed the configuration but is about to discard the changes.
    """

    def __init__(self):
        super().__init__()
        self.setText(_translate("MessageBoxes", "Your configuration has changed.")
                     + " " + _translate("MessageBoxes", "Discard changes") + "?")
        self.setIcon(QMessageBox.Warning)
        self.setWindowTitle(_translate("MessageBoxes", "Discard changes"))
        self.addButton(_translate("MessageBoxes", "Yes"), QMessageBox.YesRole)
        self.addButton(_translate("MessageBoxes", "No"), QMessageBox.NoRole)


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


class LoadQCDocumentOldNotSavedMB(QMessageBox):
    """
    The message box when the user wants to open a new QC document but the old one is not saved.
    """

    def __init__(self):
        super().__init__()
        self.setText(
            _translate("MessageBoxes", "Do you really want to open a QC Document without saving your current one?"))
        self.setIcon(QMessageBox.Warning)
        self.setWindowTitle(_translate("MessageBoxes", "Open QC document"))
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

    def __init__(self, not_valid_file):
        super().__init__()
        self.setText(str(not_valid_file) +
                     _translate("MessageBoxes", " does not seem to be a QC document file."))
        self.setIcon(QMessageBox.Information)
        self.setWindowTitle(_translate("MessageBoxes", "Not a QC document"))
        self.addButton(_translate("MessageBoxes", "Ok"), QMessageBox.AcceptRole)


class SubtitlesCanNotBeAddedToNoVideo(QMessageBox):
    """
    The message box if user wants to drop subtitles if no video is loaded.
    """

    def __init__(self):
        super().__init__()
        self.setText(_translate("MessageBoxes",
                                "There is no video loaded currently. Load a video before you add a subtitle file."))
        self.setIcon(QMessageBox.Information)
        self.setWindowTitle(_translate("MessageBoxes", "No video loaded"))
        self.addButton(_translate("MessageBoxes", "Ok"), QMessageBox.AcceptRole)
