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


from typing import Optional, NamedTuple, Tuple

from src.manager import Comment, _exporter


class HandleSaveResult(NamedTuple):
    # True if abort save
    abort: bool = False

    # True if exporting failed
    save_error: bool = False

    # The new document path
    doc_new: Optional[str] = None

    # The new video path used in the save
    vid_new: Optional[str] = None


def do_save(
        doc: Optional[str],
        vid: Optional[str],
        comments: Tuple[Comment]
) -> HandleSaveResult:
    if not doc:
        return HandleSaveResult(abort=True)

    content = _exporter.get_file_content(vid, comments)

    # noinspection PyBroadException
    try:
        _exporter.write_qc_document(doc, content)
    except Exception:
        return HandleSaveResult(save_error=True)

    return HandleSaveResult(doc_new=doc, vid_new=vid)
