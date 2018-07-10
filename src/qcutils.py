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

import re
from datetime import datetime
from os import path, linesep
from typing import List, Tuple
from zipfile import ZipFile, ZIP_DEFLATED

from PyQt5.QtCore import QObject, QEvent

from src import settings
from src.files import Files
from src.gui.dialogs import get_save_file_name
from src.gui.events import EventCommentsUpToDate, CommentsUpToDate, PlayerCurrentVideoPath, EventPlayerCurrentVideoPath, \
    PlayerCurrentVideoFile, EventPlayerCurrentVideoFile
from src.gui.uihandler.main import MainHandler
from start import APPLICATION_NAME, APPLICATION_VERSION

# If a file is a valid qc document is determined if line (stripped) 1 starts with '[FILE]'.
QC_DOCUMENT_START_VALIDATOR = "[FILE]"

_REGEX_PATH = re.compile("^path:*\s*")
_REGEX_LINE = re.compile("^\[\d{2}:\d{2}:\d{2}\]\s*\[[^\[\]]*\]\s*.*$")

# Used to find the first two columns
_REGEX_COLUMN = re.compile("\[[^\[\]]*\]")

# Uses platform dependent line separator
_LINE_BREAK = linesep

_QC_TEMPLATE = """[FILE]
date: {}
generator: {}
{}{}
[DATA]
{}
# total lines: {}
"""


class Comment:
    """
    A representation for a comment line. Not used widely.
    """

    def __init__(self, time: str, coty: str, note: str):
        self.time = time
        self.coty = coty
        self.note = note

    def __str__(self):
        return "[{}][{}] {}".format(self.time, self.coty, self.note)


class QualityCheckWriter:

    def __init__(self, video_path, comments: Tuple[Comment]):
        # [FILE]
        self.__date = str(datetime.now().replace(microsecond=0))
        self.__generator = "{} {}".format(APPLICATION_NAME, APPLICATION_VERSION)
        self.__nick_name = settings.Setting_Custom_General_NICKNAME.value \
            if bool(settings.Setting_Custom_QcDocument_WRITE_NICK_TO_FILE.value) else ""
        self.__video_path = video_path if bool(
            settings.Setting_Custom_QcDocument_WRITE_VIDEO_PATH_TO_FILE.value) else ""

        qc_author = "qc author: {}{}".format(self.__nick_name, _LINE_BREAK) if bool(self.__nick_name) else ""
        video_path = "path: {}{}".format(self.__video_path, _LINE_BREAK) if bool(self.__video_path) else ""

        # [DATA]
        self.__comments_joined = _LINE_BREAK.join(map(lambda c: str(c), comments))
        self.__comments_size = len(comments)

        self.__file_content = _QC_TEMPLATE.format(
            self.__date,
            self.__generator,
            qc_author,
            video_path,
            self.__comments_joined,
            self.__comments_size
        )

    def write_to_disc(self, path_document) -> None:
        """
        Writes the current QualityCheck to disc.

        :param path_document: the path to write
        """

        with open(path_document, "w", encoding="utf-8") as file:
            file.write(self.__file_content)

    def qc_file_content(self) -> str:
        """
        Returns the content of this QualityCheck which would be written into the file.

        :return: the content of this QualityCheck as a string
        """
        return self.__file_content


class QualityCheckManager(QObject):

    def __init__(self, main_handler: MainHandler):
        super().__init__()

        # Store references because they should never be changed
        self.__main_handler = main_handler
        self.__widget_comments = main_handler.widget_comments
        self.__mpv_player = main_handler.widget_mpv.mpv_player

        self.__current_path_document: path = None
        self.__current_video_path: path = None
        self.__current_video_file: path = None
        self.__comments_up_to_date: bool = True

    def autosave(self) -> None:
        """
        Will save a QC document into auto save zip file if a video was loaded.
        """

        if self.__mpv_player.is_video_loaded():
            today = str(datetime.today())

            as_zip_name = "{}.zip".format("-".join(today.split("-")[:2]))
            as_path = path.join(Files.DIRECTORY_AUTOSAVE, as_zip_name)

            as_zip = ZipFile(as_path, "a" if path.isfile(as_path) else "w", compression=ZIP_DEFLATED)

            try:
                file_name = "{}-{}.txt".format(today.replace(":", "-").replace(" ", "_"), self.__current_video_file)

                quality_check_writer = QualityCheckWriter(video_path=self.__current_video_path,
                                                          comments=self.__widget_comments.get_all_comments())

                as_zip.writestr(file_name, quality_check_writer.qc_file_content())
            finally:
                as_zip.close()

    def should_save(self) -> bool:
        """
        Returns whether the QC should be saved in order to prevent data loss. In particular:

            * Comment table changed

        :return: whether saving would be valuable
        """

        return not self.__comments_up_to_date

    def update_path_qc_document_to(self, new_path) -> None:
        """
        Will set the current document path to the *new_path*.

        :param new_path: The new path
        """

        self.__current_path_document = new_path

    def reset_qc_document_path(self) -> None:
        """
        Will set the current document path to None.
        """

        self.__current_path_document = None

    def save(self) -> None:
        """
        Will save the current qc with the current path.
        """

        document = self.__current_path_document

        if bool(document):
            self.__save_with_path(document)
        else:
            self.save_as()

    def save_as(self) -> None:
        """
        Will offer a new *Save as* file dialog.
        """

        document = get_save_file_name(
            self.__current_video_path, settings.Setting_Custom_General_NICKNAME.value,
            qc_doc=self.__current_path_document, parent=self.__main_handler)

        if document:
            self.__save_with_path(document)

    def __save_with_path(self, path_document: path) -> None:
        """
        Invokes the **Write to disc** action.

        :param path_document: The path to write into
        """

        self.__current_path_document = path_document

        QualityCheckWriter(self.__current_video_path, self.__widget_comments.get_all_comments()) \
            .write_to_disc(path_document)

        self.__comments_up_to_date = True

    def customEvent(self, ev: QEvent):

        ev_type = ev.type()

        if ev_type == CommentsUpToDate:
            ev: EventCommentsUpToDate
            self.__comments_up_to_date = ev.status

        elif ev_type == PlayerCurrentVideoPath:
            ev: EventPlayerCurrentVideoPath
            self.__current_video_path = ev.current_video_path

        elif ev_type == PlayerCurrentVideoFile:
            ev: EventPlayerCurrentVideoFile
            self.__current_video_file = ev.current_video_file


class QualityCheckReader:
    """
    Class for reading qc document files.
    """

    def __init__(self, qc_document_full_path):
        self.__file = qc_document_full_path

        with open(qc_document_full_path, "r", encoding="utf-8-sig") as file:
            self.__qc_lines = [x.strip() for x in file.readlines()]

        self.__video_path = ""
        self.__comments: List[Comment] = []

        path_found = False

        if len(self.__qc_lines) > 0 and self.__qc_lines[0].strip().startswith(QC_DOCUMENT_START_VALIDATOR):
            for line in self.__qc_lines:
                if bool(line):
                    if not path_found:
                        path_found, self.__video_path = QualityCheckReader.__find_path(line)

                    comment_found, comment = QualityCheckReader.__find_comment(line)
                    if comment_found:
                        self.__comments.append(comment)
        else:
            self.__video_path = None
            self.__comments = None

    @staticmethod
    def __find_path(line: str) -> (bool, str):
        match = _REGEX_PATH.match(line)
        if match is not None:
            qc_vid_path = line.replace(match.group(), "").strip()
            return True, qc_vid_path
        return False, ""

    @staticmethod
    def __find_comment(line: str) -> (bool, Comment):
        match = _REGEX_LINE.match(line)
        if match is not None:
            time_braces = _REGEX_COLUMN.search(line)[0]
            line = line.replace(time_braces, "", 1)
            time = time_braces[1:-1]

            coty_braces = _REGEX_COLUMN.search(line)[0]
            line = line.replace(coty_braces, "", 1)
            coty = coty_braces[1:-1]

            return True, Comment(time, coty, line.strip())
        return False, None

    def results(self) -> (str, Tuple[Comment]):
        """
        Returns the results found in the qc document.

        :returns: **if valid qc document** a Tuple with

            1. str: the path in the document or the empty string if not found
            2. comments: the comments found in the document

        :returns: a Tuple (None, None) if not a valid qc document
        """

        return self.__video_path, tuple(self.__comments) if self.__comments is not None else None
