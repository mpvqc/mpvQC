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


from os import path
from pathlib import Path
from typing import List

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QInputDialog

from src import settings

_translate = QtCore.QCoreApplication.translate
_flags = (Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)

# Supported subtitle file extensions for drag and drop and for opening via dialog
_SUPPORTED_SUB_FILES = (".ass", ".ssa", ".srt", ".sup", ".idx", ".utf", ".utf8", ".utf-8", ".smi",
                        ".rt", ".aqt", ".jss", ".js", ".mks", ".vtt", ".sub", ".scc")

_FILTER_SUBS = " ".join(["*" + x for x in _SUPPORTED_SUB_FILES])


def generate_file_name_proposal(video_file: str):
    nick = ("_" + settings.Setting_Custom_General_NICKNAME.value) or ""

    # For translator: The file name proposal if video file is unknown
    untitled = _translate("FileInteractionDialogs", "untitled")

    video = path.splitext(path.basename(video_file))[0] if video_file else untitled
    return "[QC]_{0}{1}.txt".format(video, nick)


def get_open_video(parent=None) -> path or None:
    """
    Will open a dialog to select a video to open.

    :param parent: The parent window
    :return: the selected file or None if abort
    """

    caption = _translate("FileInteractionDialogs", "Open Video File")
    directory = settings.Setting_Internal_PLAYER_LAST_VIDEO_DIR.value
    file_filter = _translate("FileInteractionDialogs", "Video files") + " (*.mp4 *.mkv *.avi);;" + \
                  _translate("FileInteractionDialogs", "All files") + " (*.*)"

    new_video_path = QFileDialog.getOpenFileName(parent=parent, caption=caption,
                                                 directory=directory, filter=file_filter)[0]

    if new_video_path:
        settings.Setting_Internal_PLAYER_LAST_VIDEO_DIR.value = str(Path(new_video_path).parent)

    return new_video_path


def get_open_subs(parent=None) -> List[str] or None:
    """
    Will open a dialog to select subtitles to open.

    :param parent: The parent window
    :return: the selected file or None if abort
    """

    caption = _translate("FileInteractionDialogs", "Open Subtitle File")
    directory = settings.Setting_Internal_PLAYER_LAST_SUB_DIR.value
    file_filter = _translate("FileInteractionDialogs", "Subtitle files") + " ({});;".format(_FILTER_SUBS) + \
                  _translate("FileInteractionDialogs", "All files") + " (*.*)"

    new_subtitle_paths = QFileDialog.getOpenFileNames(parent=parent, caption=caption,
                                                      directory=directory, filter=file_filter)[0]

    if new_subtitle_paths:
        settings.Setting_Internal_PLAYER_LAST_SUB_DIR.value = str(Path(new_subtitle_paths[0]).parent)

    return new_subtitle_paths


def get_open_file_names(parent=None) -> List[str] or None:
    """
    Will open a dialog to select multiple qc documents.

    :param parent: The parent window
    :return: The selected files or None if abort
    """

    caption = _translate("FileInteractionDialogs", "Open QC Document")
    directory = settings.Setting_Internal_PLAYER_LAST_DOCUMENT_DIR.value
    file_filter = _translate("FileInteractionDialogs", "QC documents") + " (*.txt);;" + \
                  _translate("FileInteractionDialogs", "All files") + " (*.*)"

    new_document_paths = QFileDialog.getOpenFileNames(parent=parent, caption=caption,
                                                      directory=directory, filter=file_filter)[0]

    if new_document_paths:
        settings.Setting_Internal_PLAYER_LAST_DOCUMENT_DIR.value = str(Path(new_document_paths[0]).parent)

    return new_document_paths


def get_save_file_name(video_file: str, parent=None) -> path or None:
    """
    Will display a **Save as** dialog to the user.

    :param video_file: The video file to save
    :param parent: The parent window
    :return: the path to save or None if no video file was given
    """

    txt_proposal = generate_file_name_proposal(video_file)

    caption = _translate("FileInteractionDialogs", "Save QC Document As")
    directory = "{0}/{1}".format(settings.Setting_Internal_PLAYER_LAST_DOCUMENT_DIR_EXPORT.value, txt_proposal)
    file_filter = _translate("FileInteractionDialogs", "QC documents") + " (*.txt);;" + \
                  _translate("FileInteractionDialogs", "All files") + " (*.*)"

    new_file_name = QFileDialog.getSaveFileName(parent=parent, caption=caption,
                                                directory=directory, filter=file_filter)[0]

    if new_file_name:
        settings.Setting_Internal_PLAYER_LAST_DOCUMENT_DIR_EXPORT.value = str(Path(new_file_name).parent)

    return new_file_name


def get_open_network_stream(parent) -> path or None:
    """
    Will display a dialog with a single QLineEdit input field.

    :param parent: The parent widget of this dialog
    :return: The URL or None if nothing was given
    """

    dialog = QInputDialog(parent)
    dialog.setInputMode(QInputDialog.TextInput)
    dialog.setWindowTitle(_translate("FileInteractionDialogs", "Open Network Stream"))
    dialog.setLabelText(_translate("FileInteractionDialogs", "Enter URL:"))
    dialog.resize(700, 0)
    dialog.exec_()
    return dialog.textValue()
