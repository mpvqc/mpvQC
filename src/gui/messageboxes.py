from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox

_translate = QtCore.QCoreApplication.translate


class ConfigurationHasChangedQMessageBox(QMessageBox):
    """
    The message box when the user has changed the configuration but is about to discard the changes.
    """

    def __init__(self):
        super().__init__()
        self.setText(_translate("MessageBox", "Your configuration has changed.")
                     + " " + _translate("MessageBox", "Discard changes") + "?")
        self.setIcon(QMessageBox.Warning)
        self.setWindowTitle(_translate("MessageBox", "Discard changes"))
        self.addButton(_translate("MessageBox", "Yes"), QMessageBox.YesRole)
        self.addButton(_translate("MessageBox", "No"), QMessageBox.NoRole)


class ConfigurationResetQMessageBox(QMessageBox):
    """
    The message box when the user wants to reset the configuration changes.
    """

    def __init__(self):
        super().__init__()
        self.setText(
            _translate("MessageBox",
                       "Do you really want to restore the default configuration? This can not be undone."))
        self.setIcon(QMessageBox.Critical)
        self.setWindowTitle(_translate("MessageBox", "Reset configuration"))
        self.addButton(_translate("MessageBox", "Reset"), QMessageBox.ApplyRole)
        self.addButton(_translate("MessageBox", "Cancel"), QMessageBox.RejectRole)


class QuitNotSavedQMessageBox(QMessageBox):
    """
    The message box when the user wants to leave but not all changes were saved.
    """

    def __init__(self):
        super().__init__()
        self.setText(
            _translate("MessageBox", "Do you really want to quit without saving your QC?"))
        self.setIcon(QMessageBox.Warning)
        self.setWindowTitle(_translate("MessageBox", "Discard QC"))
        self.addButton(_translate("MessageBox", "No"), QMessageBox.NoRole)
        self.addButton(_translate("MessageBox", "Yes"), QMessageBox.YesRole)


class NewQCDocumentOldNotSavedQMessageBox(QMessageBox):
    """
    The message box when the user wants to open a new QC document but the old one is not saved.
    """

    def __init__(self):
        super().__init__()
        self.setText(
            _translate("MessageBox", "Do you really want to open a new QC Document without saving your QC?"))
        self.setIcon(QMessageBox.Warning)
        self.setWindowTitle(_translate("MessageBox", "Create new QC document"))
        self.addButton(_translate("MessageBox", "No"), QMessageBox.NoRole)
        self.addButton(_translate("MessageBox", "Yes"), QMessageBox.YesRole)


class LoadQCDocumentOldNotSavedQMessageBox(QMessageBox):

    def __init__(self):
        super().__init__()
        self.setText(
            _translate("MessageBox", "Do you really want to open a new QC Document without saving your QC?"))
        self.setIcon(QMessageBox.Warning)
        self.setWindowTitle(_translate("MessageBox", "Open QC document"))
        self.addButton(_translate("MessageBox", "No"), QMessageBox.NoRole)
        self.addButton(_translate("MessageBox", "Yes"), QMessageBox.YesRole)


class ValidVideoFileFoundQMessageBox(QMessageBox):

    def __init__(self):
        super().__init__()
        self.setText(
            _translate("MessageBox", "A valid video file was found. Do you want to open it?"))
        self.setIcon(QMessageBox.Information)
        self.setWindowTitle(_translate("MessageBox", "Open corresponding video file"))
        self.addButton(_translate("MessageBox", "No"), QMessageBox.NoRole)
        self.addButton(_translate("MessageBox", "Yes"), QMessageBox.YesRole)


class WhatToDoWithExistingCommentsInTableWhenOpeningNewQCDocument(QMessageBox):

    def __init__(self):
        super().__init__()
        self.setText(
            _translate("MessageBox", "What would you want to do with all existing comments?"))
        self.setIcon(QMessageBox.Information)
        self.setWindowTitle(_translate("MessageBox", "How to proceed"))
        self.addButton(_translate("MessageBox", "Delete"), QMessageBox.YesRole)
        self.addButton(_translate("MessageBox", "Nothing"), QMessageBox.NoRole)
