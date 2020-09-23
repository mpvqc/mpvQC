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


from abc import abstractmethod, ABC
from typing import Optional, Tuple, List

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QMessageBox

from src.uiutil import dialogs as d
from src.uiutil import messageboxes as md
from src.uihandler.main_window import MainHandler as AppWindow
from src.widgets import CommentsTable as Table
from src.widgets import MpvWidget
from src.manager import Comment, _exporter
from src.manager import _handleimport as hi
from src.manager import _handlesave as hs
from src.manager._handleimport import HandleImportResultData as Data


class _StaticSignals(QObject):

    # Signal fired, when a video was imported
    video_imported = pyqtSignal(str)


# Connecting to the state class directly would not make sense
# We need something that remains untouched
Signals = _StaticSignals()


class State(ABC):

    def __init__(
            self,
            has_changes: bool,
            doc: Optional[str] = None,
            vid: Optional[str] = None,
            comments: Optional[Tuple[Comment]] = None,
    ):
        super().__init__()
        self.__has_changes = has_changes
        self._doc: Optional[str] = doc
        self._vid: Optional[str] = vid
        self._comments: Optional[Tuple[Comment]] = tuple(comments) if comments else ()

    def has_same_content_as(self, other: 'State') -> bool:
        changes = self._doc == other._doc and self._vid == other._vid and self._comments == other._comments
        return changes

    @property
    def has_changes(self) -> bool:
        return self.__has_changes

    def copy(self) -> 'State':
        """
        Returns a copy with document, video and comments copied
        """

        doc = self._doc
        vid = self._vid
        comments = self._comments

        if isinstance(self, _StateInitial):
            return self._state_initial(vid=vid, comments=comments)
        if isinstance(self, _StateSaved):
            return self._state_saved(doc, vid, comments)
        if isinstance(self, _StateUnsaved):
            return self._state_unsaved(doc, vid, comments)

        raise RuntimeError("State not allowed", self.__class__)

    @staticmethod
    def _state_initial(
            vid: Optional[str],
            comments: Optional[Tuple[Comment]]
    ) -> 'State':
        """
        Returns an initial state based on the current state.
        """

        return _StateInitial(
            vid=None if vid is None else vid,
            comments=None if comments is None else comments
        )

    @staticmethod
    def _state_saved(
            doc: Optional[str],
            vid: Optional[str],
            comments: Optional[Tuple[Comment]]
    ) -> 'State':
        """
        Returns a saved state based on the current state.
        """

        return _StateSaved(
            doc=None if doc is None else doc,
            vid=None if vid is None else vid,
            comments=None if comments is None else comments
        )

    @staticmethod
    def _state_unsaved(
            doc: Optional[str],
            vid: Optional[str],
            comments: Optional[Tuple[Comment]]
    ) -> 'State':
        """
        Returns an unsaved state based on the current state.
        """

        return _StateUnsaved(
            doc=None if doc is None else doc,
            vid=None if vid is None else vid,
            comments=None if comments is None else comments
        )

    def on_comments_modified(self, t: Table) -> 'State':
        """
        Called when the comments table was modified: added row, modified row or deleted row
        """

        comments = t.get_all_comments()
        return self._state_unsaved(doc=self._doc, vid=self._vid, comments=comments)

    def on_create_new_document(self, _: AppWindow, t: Table, __: MpvWidget) -> 'State':
        """
        Called when the user presses the 'New' button
        """

        if self.__has_changes:
            do_create_new = md.NewQCDocumentOldNotSavedMB().exec_()
            if do_create_new == QMessageBox.Yes:  # Clear comments
                pass
            else:  # Abort
                return self.copy()

        t.reset_comments_table()

        return self._state_initial(vid=self._vid, comments=self._comments)

    def on_save_pressed(self, a: AppWindow, t: Table, m: MpvWidget) -> 'State':
        """
        Called when the user presses the 'Save' button
        """

        if self._doc is None:
            return self.on_save_as_pressed(a, t, m)

        comments = t.get_all_comments()
        r = hs.do_save(self._doc, self._vid, comments)
        return self._state_saved(doc=r.doc_new,
                                 vid=r.vid_new,
                                 comments=comments)

    def on_save_as_pressed(self, a: AppWindow, t: Table, m: MpvWidget) -> 'State':
        """
        Called when the user presses the 'Save As...' button
        """

        m.player.pause()

        doc = d.get_save_file_name(self._vid, a)
        comments = t.get_all_comments()
        r = hs.do_save(doc, self._vid, comments)

        if r.abort:
            return self.copy()

        return self._state_saved(doc=r.doc_new,
                                 vid=r.vid_new,
                                 comments=comments)

    def on_write_auto_save(self, _: AppWindow, __: Table, m: MpvWidget) -> None:
        """
        Auto saves the current state
        """

        if m.player.has_video():
            content = _exporter.get_file_content(self._vid, self._comments or [])
            _exporter.write_auto_save(video_path=self._vid, file_content=content)

    def on_import(
            self,
            docs: Optional[List[str]],
            vids: Optional[List[str]],
            subs: Optional[List[str]],
            a: AppWindow,
            t: Table,
            m: MpvWidget
    ) -> 'State':
        """
        Called when the user imports something
        (no matter if it's by d&d or just by selecting something in the file manager).
        """

        if not docs and not vids and not subs:
            return self.copy()

        def _handle_docs_invalid(invalid_docs: List[str]) -> None:
            if invalid_docs:
                md.QCDocumentToImportNotValidQCDocumentMB(invalid_docs).exec_()

        def _handle_comments(comments: Tuple[Comment]) -> bool:
            """
            Returns True if abort import, False else
            """

            if t.get_all_comments():
                result = md.WhatToDoWithExistingCommentsWhenOpeningNewQCDocumentMB().exec_()
                if result == QMessageBox.Abort:  # Abort import
                    return True
                elif result == 0:  # Delete existing
                    t.reset_comments_table()
                elif result == 1:  # Keep comments and add new
                    pass

            t.add_comments(comments)
            return False

        def _handle_vids(vid: str) -> bool:
            """
            Returns True, if video actually was opened
            """

            do_open = md.ValidVideoFileFoundMB().exec_()
            if do_open == QMessageBox.Yes:
                __open_video(vid)
                return True
            return False

        def __open_video(vid: str) -> None:
            m.player.open_video(vid)
            Signals.video_imported.emit(vid)

        hir, data = hi.do_import(self._vid, docs, vids)
        vid_new = hir.vid_new

        if docs:
            abort_import = _handle_comments(hir.comments)
            if abort_import:
                return self.copy()

            _handle_docs_invalid(hir.docs_invalid)

            if not vids and hir.vid_new:
                opened = _handle_vids(vid_new)
                if not opened:
                    vid_new = None
                    data.vid_new = None

            if not vids and not subs and not hir.docs_valid:
                return self.copy()

        if vids:
            __open_video(vid_new)

        if subs:
            for sub in subs:
                m.player.add_sub_files(sub)

        return self.__on_import_handle_state(data=data, imp_docs=hir.docs_valid, imp_vid=vid_new, imp_subs=subs)

    def __on_import_handle_state(
            self,
            data: Data,
            imp_docs: Optional[List[str]],
            imp_vid: Optional[str],
            imp_subs: Optional[List[str]]
    ) -> 'State':
        """
        Delegates the import to the specific methods based on what was imported
        """

        docs, vid, subs = bool(imp_docs), bool(imp_vid), bool(imp_subs)

        # One of: doc, vid or subs
        if docs and not vid and not subs:
            return self.on_import_docs(imp_docs, data)
        elif not docs and vid and not subs:
            return self.on_import_vid(imp_vid, data)
        elif not docs and not vid and subs:
            return self.on_import_subs(imp_subs, data)

        # Two of: doc, vid or subs
        elif docs and vid and not subs:
            return self.on_import_docs_vid(imp_docs, imp_vid, data)
        elif docs and not vid and subs:
            return self.on_import_docs_subs(imp_docs, imp_subs, data)
        elif not docs and vid and subs:
            return self.on_import_vid_subs(imp_vid, imp_subs, data)

        # All three: doc, vid, subs
        return self.on_import_docs_vids_subs(imp_docs, imp_vid, imp_subs, data)

    @abstractmethod
    def on_import_docs(self, docs: List[str], data: Data) -> 'State':
        """Called when only documents were imported and possibly linked videos were not imported"""
        pass

    @abstractmethod
    def on_import_vid(self, video: str, data: Data) -> 'State':
        """Called when only a video was imported"""
        pass

    @abstractmethod
    def on_import_subs(self, subtitles: List[str], data: Data) -> 'State':
        """Called when only subtitles were imported"""
        pass

    @abstractmethod
    def on_import_docs_vid(self, docs: List[str], video: str, data: Data) -> 'State':
        """
        Called when either only documents were imported and the linked video was imported
        or when documents and a video was opened via drag and drop.
        """
        pass

    @abstractmethod
    def on_import_docs_subs(self, docs: List[str], subs: List[str], data: Data) -> 'State':
        """
        Called when only documents were imported and possibly linked videos were not imported
        and when subtitles were imported, too.
        """
        pass

    @abstractmethod
    def on_import_vid_subs(self, video: str, subtitles: List[str], data: Data) -> 'State':
        """Called when videos and subtitles were imported by drag and drop"""
        pass

    @abstractmethod
    def on_import_docs_vids_subs(self, docs: List[str], vid: str, subs: List[str], data: Data) -> 'State':
        """
        Called when all three were imported via drag and drop
        or when documents were imported as well as their linked video and subtitles as well.
        """
        pass


class __StateSubtitleImportDelegate(State, ABC):
    """
    Currently importing subtitles does not change the state.
    So we delegate these methods to the ones without subtitles.
    """

    def on_import_subs(self, __: List[str], ___: hi.HandleImportResultData) -> 'State':
        return self.copy()

    def on_import_docs_subs(self, docs: List[str], _: List[str], data: Data) -> 'State':
        return self.on_import_docs(docs, data)

    def on_import_vid_subs(self, video: str, _: List[str], data: Data) -> 'State':
        return self.on_import_vid(video, data)

    def on_import_docs_vids_subs(self, docs: List[str], vid: str, _: List[str], data: Data) -> 'State':
        return self.on_import_docs_vid(docs, vid, data)


class _StateInitial(__StateSubtitleImportDelegate):

    def __init__(
            self,
            doc: Optional[str] = None,
            vid: Optional[str] = None,
            comments: Optional[Tuple[Comment]] = None
    ):
        super().__init__(False, doc, vid, comments)

    def on_import_docs(self, docs: List[str], data: Data) -> 'State':
        if len(docs) == 1:
            return self._state_saved(doc=data.doc_new, vid=self._vid, comments=data.comments)
        return self._state_unsaved(doc=None, vid=self._vid, comments=data.comments)

    def on_import_vid(self, video: str, data: Data) -> 'State':
        if data.is_cur_vid_is_imported_vid:
            return self.copy()
        return self._state_initial(vid=video, comments=data.comments)

    def on_import_docs_vid(self, docs: List[str], video: str, data: Data) -> 'State':
        if len(docs) == 1:
            # If video was linked in the document
            vid_linked_in_doc = data.is_new_vid_from_doc
            # If video was linked in the document and imported separately and both match
            vid_linked_in_doc_equals_vid_separately = data.is_vid_from_docs_equals_vid_from_user

            if vid_linked_in_doc or vid_linked_in_doc_equals_vid_separately:
                return self._state_saved(doc=data.doc_new, vid=video, comments=data.comments)
        return self._state_unsaved(doc=None, vid=video, comments=data.comments)


# noinspection DuplicatedCode
class _StateSaved(__StateSubtitleImportDelegate):

    def __init__(
            self,
            doc: Optional[str] = None,
            vid: Optional[str] = None,
            comments: Optional[Tuple[Comment]] = None
    ):
        super().__init__(False, doc, vid, comments)

    def on_import_docs(self, docs: List[str], data: Data) -> 'State':
        return self._state_unsaved(doc=None, vid=self._vid, comments=data.comments)

    def on_import_vid(self, video: str, data: Data) -> 'State':
        if data.is_cur_vid_is_imported_vid:
            return self.copy()
        return self._state_unsaved(doc=None, vid=video, comments=data.comments)

    def on_import_docs_vid(self, docs: List[str], video: str, data: Data) -> 'State':
        return self._state_unsaved(doc=None, vid=video, comments=data.comments)


# noinspection DuplicatedCode
class _StateUnsaved(__StateSubtitleImportDelegate):

    def __init__(
            self,
            doc: Optional[str] = None,
            vid: Optional[str] = None,
            comments: Optional[Tuple[Comment]] = None
    ):
        super().__init__(True, doc, vid, comments)

    def on_import_docs(self, docs: List[str], data: Data) -> 'State':
        return self._state_unsaved(doc=None, vid=self._vid, comments=data.comments)

    def on_import_vid(self, video: str, data: Data) -> 'State':
        if data.is_cur_vid_is_imported_vid:
            return self.copy()
        return self._state_unsaved(doc=None, vid=video, comments=data.comments)

    def on_import_docs_vid(self, docs: List[str], video: str, data: Data) -> 'State':
        return self._state_unsaved(doc=None, vid=video, comments=data.comments)


def get_initial_state() -> State:
    return _StateInitial()
