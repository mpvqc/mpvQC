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


from typing import List, Tuple

from PyQt5.QtCore import pyqtSignal, QItemSelectionModel, QModelIndex, QCoreApplication, QTimer, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QKeyEvent, QMouseEvent, QWheelEvent, QPalette
from PyQt5.QtWidgets import QTableView, QAbstractItemView, QApplication

from src.uiutil.delegates import CommentTimeDelegate, CommentTypeDelegate, CommentNoteDelegate
from src.uiutil.events import EventDistributor, EventCommentAmountChanged, EventCommentCurrentSelectionChanged, \
    EventReceiver
from src.uiutil.searchutils import SearchResult
from src.uihandler.main_window import MainHandler
from src.manager import Comment

_translate = QCoreApplication.translate


class CommentsTable(QTableView):
    """
    The comment table below the video.
    """

    state_changed = pyqtSignal(bool)

    def __init__(self, main_handler: MainHandler):
        super().__init__()
        self.__widget_mpv = main_handler.widget_mpv
        self.__mpv_player = self.__widget_mpv.player

        palette = self.palette()
        palette.setColor(QPalette.Inactive, QPalette.Highlight,
                         palette.color(QPalette.Active, QPalette.Highlight))
        palette.setColor(QPalette.Inactive, QPalette.HighlightedText,
                         palette.color(QPalette.Active, QPalette.HighlightedText))
        self.setPalette(palette)

        # Model
        self.__model = QStandardItemModel(self)
        self.setModel(self.__model)
        self.selectionModel().selectionChanged.connect(lambda sel, __: self.__on_row_selection_changed())

        # Headers
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()

        # Delegates
        delegate_time = CommentTimeDelegate(self)
        delegate_coty = CommentTypeDelegate(self)
        delegate_note = CommentNoteDelegate(self)

        delegate_time.editing_done.connect(self.__on_after_user_changed_time)
        delegate_coty.editing_done.connect(self.__on_after_user_changed_comment_type)
        delegate_note.editing_done.connect(self.__on_after_user_changed_comment_note)

        self.setItemDelegateForColumn(0, delegate_time)
        self.setItemDelegateForColumn(1, delegate_coty)
        self.setItemDelegateForColumn(2, delegate_note)

        # Misc
        self.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.__selection_flags = QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows

        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setWordWrap(False)
        self.setShowGrid(False)

    def delete_current_selected_comment(self) -> None:
        """
        Will delete the current selected comment row.
        If selection is empty, no action will be invoked.
        """

        def delete(selected: List[QModelIndex]):
            self.__model.removeRows(selected[0].row(), 1)
            self.state_changed.emit(False)
            EventDistributor.send_event(EventCommentAmountChanged(self.__model.rowCount()))

        self.__do_with_selected_comment_row(delete)

    def edit_current_selected_comment(self) -> None:
        """
        Will start edit mode on selected comment row.
        If selection is empty, no action will be invoked.
        """

        def edit(selected: List[QModelIndex]):
            row = selected[0].row()
            idx = self.__model.item(row, 2).index()
            self.edit(idx)
            self.state_changed.emit(False)

        self.__do_with_selected_comment_row(edit)

    def copy_current_selected_comment(self) -> None:
        """
        Will copy the complete row to clipboard.
        If selection is empty, no action will be invoked.
        """

        def copy(selected: List[QModelIndex]):
            row = selected[0].row()
            time = self.__model.item(row, 0).text()
            coty = self.__model.item(row, 1).text()
            note = self.__model.item(row, 2).text()
            QApplication.clipboard().setText("[{}] [{}] {}".format(time, coty, note))

        self.__do_with_selected_comment_row(copy)

    def add_comments(self, comments: Tuple[Comment], changes_qc=False, edit=False):
        if not comments:
            return

        model = self.__model
        last_entry = None

        for comment in comments:
            time = QStandardItem(comment.comment_time)
            time.setTextAlignment(Qt.AlignCenter)
            ct = QStandardItem(_translate("CommentTypes", comment.comment_type))
            note = QStandardItem(comment.comment_note)
            last_entry = [time, ct, note]
            model.appendRow(last_entry)

        self.resizeColumnToContents(1)
        self.sort()

        EventDistributor.send_event(EventCommentAmountChanged(model.rowCount()))
        self.__on_row_selection_changed()

        if changes_qc:
            self.state_changed.emit(False)

        if edit:
            new_index = model.indexFromItem(last_entry[2])
            self.scrollTo(new_index)
            self.setCurrentIndex(new_index)
            self.edit(new_index)
        else:
            self.ensure_selection()

    def add_comment(self, comment_type: str) -> None:
        comment = Comment(
            comment_time=self.__widget_mpv.player.position_current(),
            comment_type=comment_type,
            comment_note=""
        )
        self.add_comments((comment,), changes_qc=True, edit=True)

    def get_all_comments(self) -> Tuple[Comment]:
        """
        Returns all comments.

        :return: all comments.
        """

        ret_list = []
        model = self.__model

        for r in range(0, model.rowCount()):
            time = model.item(r, 0).text()
            coty = model.item(r, 1).text()
            note = model.item(r, 2).text()
            ret_list.append(Comment(comment_time=time, comment_type=coty, comment_note=note))
        return tuple(ret_list)

    def reset_comments_table(self) -> None:
        """
        Will clear all comments.
        """

        self.__model.clear()
        self.state_changed.emit(True)
        EventDistributor.send_event(EventCommentAmountChanged(self.__model.rowCount()))
        EventDistributor.send_event(EventCommentCurrentSelectionChanged(-1))

    def sort(self) -> None:
        """
        Will sort the comments table by time column.
        """

        # Sorting is only triggered if the sorting policy changes
        self.setSortingEnabled(False)
        self.setSortingEnabled(True)
        self.sortByColumn(0, Qt.AscendingOrder)

    def __do_with_selected_comment_row(self, consume_selected_function) -> None:
        """
        This function takes a **function** as argument.

        *It will call the function with the current selection as argument if selection is not empty.*

        :param consume_selected_function: The function to apply if selection is not empty
        """

        is_empty: bool = self.__model.rowCount() == 0

        if not is_empty:
            selected = self.selectionModel().selectedRows()

            if selected:
                consume_selected_function(selected)

    def __on_after_user_changed_time(self) -> None:
        """
        Action to invoke after time was changed manually by the user.
        """

        self.sort()
        self.state_changed.emit(False)

    def __on_after_user_changed_comment_type(self) -> None:
        """
        Action to invoke after comment type was changed manually by the user.
        """

        self.resizeColumnToContents(1)
        self.state_changed.emit(False)

    # noinspection PyMethodMayBeStatic
    def __on_after_user_changed_comment_note(self) -> None:
        """
        Action to invoke after comment note was changed manually by the user.
        """

        self.state_changed.emit(False)

    # noinspection PyMethodMayBeStatic
    def __on_row_selection_changed(self) -> None:

        def after_model_updated():
            current_index = self.selectionModel().currentIndex()
            if current_index.isValid():
                new_row = current_index.row()
            else:
                new_row = -1
            EventDistributor.send_event(EventCommentCurrentSelectionChanged(new_row), EventReceiver.WIDGET_STATUS_BAR)

        QTimer.singleShot(0, after_model_updated)

    def keyPressEvent(self, e: QKeyEvent):
        mod = e.modifiers()
        key = e.key()

        # Only key up and key down are handled here because they require to call super
        if (key == Qt.Key_Up or key == Qt.Key_Down) and mod == Qt.NoModifier:
            super().keyPressEvent(e)
        else:
            self.__widget_mpv.keyPressEvent(e)

    def mousePressEvent(self, e: QMouseEvent):

        if e.button() == Qt.LeftButton:
            mdi: QModelIndex = self.indexAt(e.pos())
            if mdi.column() == 0 and self.__mpv_player.has_video():
                position = self.__model.item(mdi.row(), 0).text()
                self.__widget_mpv.player.position_jump(position=position)
                e.accept()
            elif mdi.column() == 1 and mdi == self.selectionModel().currentIndex():
                self.edit(mdi)
                e.accept()
        super().mousePressEvent(e)

    def wheelEvent(self, e: QWheelEvent):
        delta = e.angleDelta()

        x_d = delta.x()
        y_d = delta.y()

        if x_d == 0 and y_d != 0:
            position = self.verticalScrollBar().value()
            if y_d > 0:
                self.verticalScrollBar().setValue(position - 1)
            else:
                self.verticalScrollBar().setValue(position + 1)
        else:
            super().wheelEvent(e)

    def ensure_selection(self) -> None:
        """
        If no row is highlighted the first row will be highlighted.
        """

        self.setFocus()
        if self.__model.rowCount() != 0:
            if not self.selectionModel().currentIndex().isValid():
                self.__highlight_row(self.model().index(0, 2))

    def perform_search(self, query: str, top_down: bool, new_query: bool, last_index: QModelIndex) -> SearchResult:
        """
        Will perform the search for the given query and return a SearchResult.

        :param last_index: The index of the latest search result or any invalid index.
        :param query: search string ignore case (Qt.MatchContains)
        :param top_down: If True the next, if False the previous occurrence will be returned
        :param new_query: If True the search will be handled as a new one.
        :return:
        """

        current_index = self.selectionModel().currentIndex()

        if new_query:
            start_row = 0
        elif last_index and last_index.isValid():
            start_row = last_index.row()
        elif current_index and current_index.isValid():
            start_row = current_index.row()
        else:
            start_row = 0

        if query == "":
            return self.__generate_search_result(query)

        start = self.__model.index(start_row, 2)
        match: List[QModelIndex] = self.__model.match(start, Qt.DisplayRole, query, -1, Qt.MatchContains | Qt.MatchWrap)

        if not match:
            return self.__generate_search_result(query)

        return self.__provide_search_result(query, match, top_down, new_query)

    def __provide_search_result(self, query: str, match: List[QModelIndex], top_down: bool,
                                new_query: bool) -> SearchResult:

        if top_down and len(match) > 1:
            if new_query or self.selectionModel().currentIndex() not in match:
                model_index = match[0]
            else:
                model_index = match[1]
        else:
            model_index = match[-1]
        current_hit = sorted(match, key=lambda k: k.row()).index(model_index)
        return self.__generate_search_result(query, model_index, current_hit + 1, len(match))

    def __generate_search_result(self, query, model_index=None, current_hit=0, total_hits=0) -> SearchResult:
        result = SearchResult(query, model_index, current_hit, total_hits)
        result.highlight.connect(lambda index: self.__highlight_row(index))
        return result

    def __highlight_row(self, model_index: QModelIndex):
        if model_index:
            self.selectionModel().setCurrentIndex(model_index, self.__selection_flags)
            self.selectionModel().select(model_index, self.__selection_flags)
            self.scrollTo(model_index, QAbstractItemView.PositionAtCenter)
