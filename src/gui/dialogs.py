import sys
from os import path

from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog

_translate = QtCore.QCoreApplication.translate


def get_open_file_name(directory, parent=None) -> path or None:
    """
    Will open a dialog to select a video to open.

    :param directory: The directory to open initially
    :param parent: The parent window
    :return: the selected file or None if abort
    """

    return QFileDialog.getOpenFileName(
        parent=parent,
        caption=_translate("MessageBox", "Open Video File"),
        directory=directory,
        filter=_translate("MessageBox", "Video files (*.mkv *.mp4);;All files (*.*)")
    )[0]


def get_open_file_names(directory, parent=None) -> path or None:
    """
    Will open a dialog to select multiple qc documents.

    :param directory: The directory to open initially
    :param parent: The parent window
    :return: The selected files or None if abort
    """

    return QFileDialog.getOpenFileNames(
        parent,
        _translate("MessageBox", "Open QC Document"),
        directory,
        _translate("MessageBox", "QC documents (*.txt);;All files (*.*)"),
    )[0]


def get_save_file_name(video_file: path, nick: str, qc_doc=None, parent=None) -> path or None:
    """
    Will display a **Save as** dialog to the user.

    :param qc_doc: Current qc document path (full)
    :param video_file: The video file to save
    :param nick: The nickname to append
    :param parent: The parent window
    :return: the path to save or None if no video file was given
    """

    if qc_doc is not None and path.isfile(qc_doc):
        txt_proposal = qc_doc
    elif not bool(video_file):
        txt_proposal = "[QC]_{}".format(nick)
    else:
        base = path.basename(video_file)

        txt_file = "[QC]_{}_{}.txt".format(path.splitext(base)[0], nick)

        if sys.platform.startswith("win32"):
            trtable = str.maketrans('\\/:*?"<>|', "_________")
            txt_file = txt_file.translate(trtable)

        txt_proposal = path.join(path.dirname(video_file), txt_file.replace(" ", "_"))

    return QFileDialog.getSaveFileName(
        parent,
        _translate("MessageBox", "Save QC document as"),
        txt_proposal,
        _translate("MessageBox", "QC documents (*.txt);;All files (*.*)"),
    )[0]
