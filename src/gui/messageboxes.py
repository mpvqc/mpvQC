import sys
from os import path

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox, QFileDialog

_translate = QtCore.QCoreApplication.translate


class OpenVideoFileDialog:
    """
    The dialog to open video files.
    """

    @staticmethod
    def get_open_file_name(directory, parent=None):
        """
        Will open a dialog to select a video to open.

        :param directory:
        :param parent:
        :return:
        """

        return QFileDialog.getOpenFileName(
            parent=parent,
            caption=_translate("MessageBox", "Open Video File"),
            directory=directory,
            filter=_translate("MessageBox", "Video files (*.mkv *.mp4);;All files (*.*)")
        )[0]


class SaveAsFileDialog:
    """
    The message box when the user not saved before or selects explicitly to save with a new file name.
    """

    @staticmethod
    def get_save_file_name(video_file: path, nick: str, parent=None) -> path or None:
        """
        Will display a **Save as** dialog to the user.

        :param video_file: The video file to save
        :param nick: The nickname to append
        :param parent: The parent window
        :return: the path to save or None if no video file was given
        """

        if not bool(video_file):
            return None

        base = path.basename(video_file)
        txt_file = "[QC]_{}_{}.txt".format(path.splitext(base)[0], nick)
        if sys.platform.startswith("win32"):
            trtable = str.maketrans('\\/:*?"<>|', "_________")
            txt_file = txt_file.translate(trtable)

        txt_proposal = path.join(path.dirname(video_file), txt_file)

        return QFileDialog.getSaveFileName(
            parent=parent,
            caption=_translate("MessageBox", "Save QC document as"),
            directory=txt_proposal,
            filter=_translate("MessageBox", "QC documents (*.txt);;All files (*.*)"),
        )[0]


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
