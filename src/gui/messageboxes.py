from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox, QFileDialog

_translate = QtCore.QCoreApplication.translate


class OpenVideoFileDialog:
    """
    The dialog to open video files.
    """

    @staticmethod
    def get_open_file_name(directory, parent=None):
        return QFileDialog.getOpenFileName(
            parent=parent,
            caption=_translate("Misc", "Open Video File"),
            directory=directory,
            filter=_translate("Misc", "Video files (*.mkv *.mp4);;All files (*.*)")
        )[0]


class ConfigurationHasChangedQMessageBox(QMessageBox):
    """
    The message box when the user has changed the configuration but is about to discard the changes.
    """

    def __init__(self):
        super().__init__()
        self.setText(
            _translate("Misc", "Your configuration has changed.") + " " + _translate("Misc", "Discard changes") + "?")
        self.setIcon(QMessageBox.Warning)
        self.setWindowTitle(_translate("Misc", "Discard changes"))
        self.addButton(_translate("Misc", "Yes"), QMessageBox.YesRole)
        self.addButton(_translate("Misc", "No"), QMessageBox.NoRole)


class ConfigurationResetQMessageBox(QMessageBox):
    """
    The message box when the user wants to reset the configuration changes.
    """

    def __init__(self):
        super().__init__()
        self.setText(
            _translate("Misc", "Do you really want to restore the default configuration? This can not be undone."))
        self.setIcon(QMessageBox.Critical)
        self.setWindowTitle(_translate("Misc", "Reset configuration"))
        self.addButton(_translate("Misc", "Reset"), QMessageBox.ApplyRole)
        self.addButton(_translate("Misc", "Cancel"), QMessageBox.RejectRole)


class QuitNotSavedQMessageBox(QMessageBox):

    def __init__(self):
        super().__init__()
        self.setText(
            _translate("Dialog", "Do you really want to quit without saving your QC?"))
        self.setIcon(QMessageBox.Warning)
        self.setWindowTitle(_translate("Dialog", "Discard QC"))
        self.addButton(_translate("Dialog", "No"), QMessageBox.NoRole)
        self.addButton(_translate("Dialog", "Yes"), QMessageBox.YesRole)


class NewQCDocumentOldNotSavedQMessageBox(QMessageBox):

    def __init__(self):
        super().__init__()
        self.setText(
            _translate("Dialog", "Do you really want to open a new QC Document without saving your QC?"))
        self.setIcon(QMessageBox.Warning)
        self.setWindowTitle(_translate("Dialog", "Create new QC document"))
        self.addButton(_translate("Dialog", "No"), QMessageBox.NoRole)
        self.addButton(_translate("Dialog", "Yes"), QMessageBox.YesRole)
