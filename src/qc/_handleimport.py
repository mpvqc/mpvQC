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


from typing import NamedTuple, Optional, List, Tuple

from src.qc import Comment, _importer


class HandleImportResult(NamedTuple):
    """Object for internal use only helping to differentiate the import"""

    # The new document path only if only 1 document was imported and it was valid
    doc_new: Optional[str] = None

    # The new video to open, either from a document or imported separately ones (prefers the later)
    vid_new: Optional[str] = None

    # The combined comments from all imported documents that were valid
    comments: Optional[Tuple[Comment]] = None

    # The valid documents
    docs_valid: Optional[List[str]] = None

    # The invalid documents
    docs_invalid: Optional[List[str]] = None


class HandleImportResultData:

    def __init__(
            self,
            doc_new: Optional[str] = None,
            vid_cur: Optional[str] = None,
            vid_new: Optional[str] = None,
            vid_new_from_docs: Optional[str] = None,
            vid_new_from_user: Optional[str] = None,
            comments: Optional[Tuple[Comment]] = None
    ):
        self.comments = comments

        self.__doc_new = doc_new
        self.__vid_cur = vid_cur
        self.__vid_new = vid_new
        self.__vid_new_docs = vid_new_from_docs
        self.__vid_new_user = vid_new_from_user

    @property
    def doc_new(self) -> Optional[str]:
        """
        Returns the new recommended document path. Only not None if exactly one valid document was imported
        """

        return self.__doc_new

    @property
    def vid_new(self) -> Optional[str]:
        """
        Returns the new video to open
        """

        return self.__vid_new

    @vid_new.setter
    def vid_new(self, value) -> None:
        """
        Sets the new video to open
        """

        self.__vid_new = value

    @property
    def is_cur_vid_is_imported_vid(self) -> bool:
        """
        Returns True if the current video equals the currently imported and actually opened video
        """

        return self.__vid_new and self.__vid_cur and self.__vid_new == self.__vid_cur

    @property
    def is_new_vid_from_doc(self) -> bool:
        """
        Returns True if user imports a document (with video path) and that video is the recommended video to open
        """

        return self.__vid_new_docs and not self.__vid_new_user and self.__vid_new_docs == self.__vid_new

    @property
    def is_vid_from_docs_equals_vid_from_user(self) -> bool:
        """
        Returns True if user imports 1 document (with video) and 1 video (by d&d) and both videos are equal
        """

        return self.__vid_new_docs and self.__vid_new_user and self.__vid_new_user == self.__vid_new_docs


def do_import(
        cur_vid: Optional[str],
        imp_docs: Optional[List[str]],
        imp_vids: Optional[List[str]],
) -> Tuple[HandleImportResult, HandleImportResultData]:
    doc_new: Optional[str] = None
    vid_new_from_docs: Optional[str] = None
    vid_new_from_user: Optional[str] = None
    comments: Optional[Tuple[Comment]] = None
    docs_valid: Optional[List[str]] = None
    docs_invalid: Optional[List[str]] = None

    if imp_docs:
        videos, comments, docs_valid, docs_invalid = _importer.get_qc_content(imp_docs)

        if videos:
            vid_new_from_docs = videos[0]

        if len(imp_docs) == len(docs_valid) == 1:
            doc_new = docs_valid[0]

    if imp_vids:
        vid_new_from_user = imp_vids[0]

    vid_new = vid_new_from_user or vid_new_from_docs

    hir = HandleImportResult(
        doc_new=doc_new,
        vid_new=vid_new,
        comments=comments,
        docs_valid=docs_valid,
        docs_invalid=docs_invalid
    )

    data = HandleImportResultData(
        doc_new=doc_new,
        vid_cur=cur_vid,
        vid_new=vid_new,
        vid_new_from_docs=vid_new_from_docs,
        vid_new_from_user=vid_new_from_user,
        comments=comments,
    )

    return hir, data
