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


import re
from os import path
from typing import Optional, List, Tuple

from src.uiutil.utils import replace_special_characters
from src.manager import Comment

_REGEX_PATH = re.compile("^path\s*:*\s*")
_REGEX_LINE = re.compile("^\[\d{2}:\d{2}:\d{2}\]\s*\[[^\[\]]*\]\s*.*$")

# Used to find the first two columns
_REGEX_COLUMN = re.compile("\[[^\[\]]*\]")

# If a file is a valid qc document is determined if line (stripped) 1 starts with '[FILE]'.
QC_DOCUMENT_HEADER = "[FILE]"


def __find_path(line):
    """
    Checks whether line is a line.

    :param line: the line to check
    :return: the video path if found, None else.
    """

    match = _REGEX_PATH.match(line)
    if match is not None:
        qc_vid_path = line.replace(match.group(), "").strip()
        return qc_vid_path
    return None


def __find_comment(line):
    """
    Checks whether line is a comment.

    :param line: the line to check
    :return: a comment object if line is comment, None else
    """

    match = _REGEX_LINE.match(line)
    if match is not None:
        time_braces = _REGEX_COLUMN.search(line).group(0)
        line = line.replace(time_braces, "", 1)
        time = time_braces[1:-1]

        coty_braces = _REGEX_COLUMN.search(line).group(0)
        line = line.replace(coty_braces, "", 1)
        coty = coty_braces[1:-1]

        return Comment(time, coty, replace_special_characters(line.strip()))
    return None


def get_qc_content(document_paths: Optional[List[str]]) -> Tuple[List[str], Tuple[Comment], List[str], List[str]]:
    """
    Reads qc information from the given paths.

    :param document_paths: a list with file paths pointing to existing qc document files.
    :return: four lists:<br>
        - video_paths: all found video paths<br>
        - combined_comments: all combined comments from all provided files<br>
        - valid_files: all files considered valid<br>
        - non_valid_files: all files considered not valid
    """

    video_paths, combined_comments, valid_files, non_valid_files = [], [], [], []

    for document_path in document_paths:
        with open(document_path, "r", encoding="utf-8-sig") as file:
            lines = [x.strip() for x in file.readlines() if x]

        video_path_found = False

        if len(lines) > 0 and lines[0].startswith(QC_DOCUMENT_HEADER):
            valid_files.append(document_path)
            for line in lines:
                if not video_path_found:
                    video_path = __find_path(line)
                    if video_path:
                        video_paths.append(video_path)
                        video_path_found = True

                comment = __find_comment(line)
                if comment:
                    combined_comments.append(comment)
        else:
            non_valid_files.append(document_path)

    # Return only existing paths
    video_paths = [p for p in video_paths if p and path.exists(p)]

    # Sort comments by time
    combined_comments = tuple(sorted(combined_comments, key=lambda x: x.comment_time))

    return video_paths, combined_comments, valid_files, non_valid_files
