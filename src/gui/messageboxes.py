from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox

_translate = QtCore.QCoreApplication.translate


class ConfigurationHasChangedQMessageBox(QMessageBox):
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


class ConfigurationResetQMessageBox(QMessageBox):
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


class QuitNotSavedQMessageBox(QMessageBox):
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


class NewQCDocumentOldNotSavedQMessageBox(QMessageBox):
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


class LoadQCDocumentOldNotSavedQMessageBox(QMessageBox):
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


class ValidVideoFileFoundQMessageBox(QMessageBox):
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


class WhatToDoWithExistingCommentsInTableWhenOpeningNewQCDocument(QMessageBox):
    """
    he message box when the user imports QC documents to ask what to do with the existing comments.
    """

    def __init__(self):
        super().__init__()
        self.setText(
            _translate("MessageBoxes", "What would you want to do with all existing comments?"))
        self.setIcon(QMessageBox.Information)
        self.setWindowTitle(_translate("MessageBoxes", "How to proceed"))
        self.addButton(_translate("MessageBoxes", "Delete"), QMessageBox.YesRole)
        self.addButton(_translate("MessageBoxes", "Nothing"), QMessageBox.NoRole)
