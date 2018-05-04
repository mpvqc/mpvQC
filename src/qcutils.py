import re
from datetime import datetime
from os import path, linesep
from typing import List, Tuple

from src.gui.messageboxes import SaveAsFileDialog
from src.gui.uihandler.main import MainHandler
from src import settings
from start import APPLICATION_NAME, APPLICATION_VERSION

_REGEX_PATH = re.compile("^path:*\s*")
_REGEX_LINE = re.compile("^\[\d{2}:\d{2}:\d{2}\]\s*\[\w+.*\]\s*.*$")
_REGEX_COLUMN = re.compile("\[([A-Za-z0-9\:_\s]+)\]")

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


class WritableQualityCheckFile:

    def __init__(self, video_path, comments: Tuple[Comment]):
        # [FILE]
        self.date = str(datetime.now().replace(microsecond=0))
        self.generator = "{} {}".format(APPLICATION_NAME, APPLICATION_VERSION)
        self.nick_name = settings.Setting_Custom_General_NICKNAME.value \
            if bool(settings.Setting_Custom_QcDocument_WRITE_NICK_TO_FILE.value) else ""
        self.video_path = video_path if bool(settings.Setting_Custom_QcDocument_WRITE_VIDEO_PATH_TO_FILE.value) else ""

        # [DATA]
        self.comments_joined = _LINE_BREAK.join(map(lambda c: str(c), comments))
        self.comments_size = len(comments)

        qc_author = "qc author: {}{}".format(self.nick_name, _LINE_BREAK) if bool(self.nick_name) else ""
        video_path = "path: {}{}".format(self.video_path, _LINE_BREAK) if bool(self.video_path) else ""

        self.file_content = _QC_TEMPLATE.format(
            self.date,
            self.generator,
            qc_author,
            video_path,
            self.comments_joined,
            self.comments_size
        )

    def write_to_disc(self, path_document):
        with open(path_document, "w", encoding="utf-8") as file:
            file.write(self.file_content)


class QualityCheckManager:

    def __init__(self, main_handler: MainHandler):

        # Store references because they should never be changed
        self.main_handler = main_handler
        self.widget_comments = main_handler.widget_comments
        self.widget_mpv = main_handler.widget_mpv
        self.mpv_player = self.widget_mpv.mpv_player
        self.path_document: path = None

    @property
    def comments(self) -> Tuple[Comment]:
        """
        A reference to the comments widget content cells.

        :return: all comments currently
        """
        return self.widget_comments.get_all_comments()

    @property
    def video_path(self) -> path or str:
        """
        A reference to the player's current video file.

        :return: the current video file of the player
        """

        return self.mpv_player.video_file_current()

    @property
    def is_up_to_date(self) -> bool:
        """
        Fetches the current status of the comments table.

        :return: True if up to date, False else.
        """

        return self.widget_comments.comments_up_to_date

    def should_save(self) -> bool:
        """
        Returns whether the QC should be saved in order to prevent data loss. In particular:

            1. Comments are available (not 0)
            2. Comment table changed

        :return: whether saving would be valuable
        """

        return not self.is_up_to_date

    def update_path_qc_document_to(self, new_path) -> None:
        """
        Will set the current document path to the *new_path*.

        :param new_path: The new path
        """

        self.path_document = new_path

    def reset_qc_document_path(self) -> None:
        """
        Will set the current document path to None.
        """

        self.path_document = None

    def save(self) -> None:
        """
        Will save the current qc with the current path.
        """

        document = self.path_document

        if bool(document):
            self.__save_with_path(document)
        else:
            self.save_as()

    def save_as(self) -> None:
        """
        Will offer a new *Save as* file dialog.
        """

        document = SaveAsFileDialog.get_save_file_name(
            self.video_path, settings.Setting_Custom_General_NICKNAME.value,
            qc_doc=self.path_document, parent=self.main_handler)

        if document:
            self.__save_with_path(document)

    def __save_with_path(self, path_document: path) -> None:
        """
        Invokes the **Write to disc** action.

        :param path_document: The path to write into
        """
        self.update_path_qc_document_to(path_document)

        WritableQualityCheckFile(self.video_path, self.comments).write_to_disc(path_document)

        self.main_handler.widget_comments.comments_up_to_date = True


class QualityCheckParser:

    def __init__(self, qc_document_full_path):
        self.file = qc_document_full_path
        self.__qc_lines = []
        self.qc_comments: List[Comment] = []

        with open(qc_document_full_path, "r", encoding="utf-8") as file:
            self.__qc_lines = [x.strip() for x in file.readlines()]

        self.video_path = ""
        self.comments: List[Comment] = []

        path_found = False

        for line in self.__qc_lines:
            if bool(line):
                if not path_found:
                    path_found, self.video_path = QualityCheckParser.__find_path(line)

                comment_found, comment = QualityCheckParser.__find_comment(line)
                if comment_found:
                    self.comments.append(comment)

    def results(self) -> (str, Tuple[Comment]):
        """
        Returns the results found in the qc document.

        :returns: a Tuple with

            1. str: the path in the document or the empty string if not found
            2. comments: the comments found in the document
        """

        return self.video_path, tuple(self.comments)

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
