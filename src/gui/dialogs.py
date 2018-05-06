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

import sys
from os import path

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QInputDialog

_translate = QtCore.QCoreApplication.translate

_flags = (Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)


def get_open_file_name(directory, parent=None) -> path or None:
    """
    Will open a dialog to select a video to open.

    :param directory: The directory to open initially
    :param parent: The parent window
    :return: the selected file or None if abort
    """

    return QFileDialog.getOpenFileName(
        parent=parent,
        caption=_translate("Dialogs", "Open Video File"),
        directory=directory,
        filter=_translate("Dialogs", "Video files (*.mkv *.mp4);;All files (*.*)")
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
        _translate("Dialogs", "Open QC Document"),
        directory,
        _translate("Dialogs", "QC documents (*.txt);;All files (*.*)"),
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
        _translate("Dialogs", "Save QC document as"),
        txt_proposal,
        _translate("Dialogs", "QC documents (*.txt);;All files (*.*)"),
    )[0]


def get_open_network_stream(parent) -> path or None:
    """
    Will display a dialog with a single QLineEdit input field.

    :param parent: The parent widget of this dialog
    :return: The URL or None if nothing was given
    """

    return QInputDialog.getText(
        parent,
        _translate("Dialogs", "Open network stream"),
        _translate("Dialogs", "Enter URL"),
        flags=Qt.WindowFlags(_flags),
    )[0]
