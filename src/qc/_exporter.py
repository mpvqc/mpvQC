# mpvQC
#
# Copyright (C) 2020 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from datetime import datetime
from os import path
from typing import Optional, Tuple
from zipfile import ZipFile, ZIP_DEFLATED

from src import settings
from src.files import Files
from src.qc import Comment
from start import APPLICATION_NAME, APPLICATION_VERSION


def __prepare_file_content(b_header: bool,
                           b_date: bool, v_date: str,
                           b_generator: bool, v_generator: str,
                           b_nick: bool, v_nick: str,
                           b_path: bool, v_path: str,
                           comments: Tuple[Comment]):
    """
    Builds the qc file content using the given arguments.

    :param b_header: True, if write header, False else.
    :param b_date: True, if write date, False else.
    :param v_date: the date as string
    :param b_generator: True, if write generator, False else.
    :param v_generator: the generator as string
    :param b_nick: True, if write nick, False else.
    :param v_nick: the nickname as string
    :param b_path: True, if write path, False else.
    :param v_path: the video path as string
    :param comments: a list of comments objects
    :return: the file content of the qc document as a string
    """

    if b_header:
        d_date = "date      : {0}\n".format(v_date) if b_date else ""
        d_gnrt = "generator : {0}\n".format(v_generator) if b_generator else ""
        d_nick = "nickname  : {0}\n".format(v_nick) if b_nick else ""
        d_path = "path      : {0}\n".format(v_path) if b_path else ""
        d_header = "{0}{1}{2}{3}".format(d_date, d_gnrt, d_nick, d_path)
    else:
        d_header = ""

    comments_joined = "\n".join(map(lambda c: str(c), comments))
    comments_size = len(comments)

    return ("[FILE]\n"
            "{0}\n"
            "[DATA]\n"
            "{1}\n"
            "# total lines: {2}").format(d_header, comments_joined, comments_size)


def get_file_content(video_path: Optional[str], comments: Tuple[Comment]):
    """
    Will take into account all user settings provided as arguments to build and return the qc file content.

    :param video_path: the path of the video
    :param comments: a list of comments objects
    :return: the file content of the qc document as a string
    """

    b_header = True

    b_date = True
    v_date = str(datetime.now().replace(microsecond=0))

    b_generator = True
    v_generator = "{} {}".format(APPLICATION_NAME, APPLICATION_VERSION)

    b_nick = settings.Setting_Custom_QcDocument_WRITE_NICK_TO_FILE.value
    v_nick = settings.Setting_Custom_General_NICKNAME.value

    b_path = settings.Setting_Custom_QcDocument_WRITE_VIDEO_PATH_TO_FILE.value
    v_path = video_path if video_path else ""

    return __prepare_file_content(b_header,
                                  b_date, v_date,
                                  b_generator, v_generator,
                                  b_nick, v_nick,
                                  b_path, v_path,
                                  comments)


def write_qc_document(file_path, file_content):
    """
    Writes a qc file to disk.

    :param file_path: the file path to write
    :param file_content: the content to write
    """

    with open(file_path, "w") as f:
        f.write(file_content)


def write_auto_save(video_path, file_content):
    """
    Writes a qc file into the auto save zip.

    :param video_path: the name of the current video file
    :param file_content: the content to write
    """

    today = str(datetime.today())

    zip_name = "{}.zip".format("-".join(today.split("-")[:2]))
    zip_path = path.join(Files.DIRECTORY_AUTOSAVE, zip_name)
    zip_file = ZipFile(zip_path, "a" if path.isfile(zip_path) else "w", compression=ZIP_DEFLATED)

    file_name = "{}-{}.txt".format(today.replace(":", "-").replace(" ", "_"),
                                   path.splitext(path.basename(video_path))[0])

    try:
        zip_file.writestr(file_name, file_content)
    finally:
        zip_file.close()
