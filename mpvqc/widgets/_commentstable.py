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


from typing import List, Tuple, Optional

from PyQt5.QtCore import pyqtSignal, QItemSelectionModel, QModelIndex, QCoreApplication, QTimer, Qt, pyqtSlot
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QKeyEvent, QMouseEvent, QWheelEvent, QPalette
from PyQt5.QtWidgets import QTableView, QAbstractItemView, QApplication

from mpvqc.manager import Comment
from mpvqc.uihandler import MainHandler
from mpvqc.uiutil import CommentTimeDelegate, CommentTypeDelegate, CommentNoteDelegate, CommentsTableSearcher


class CommentsTable(QTableView):
    """
    The comment table below the video.
    """

    # Invoked, whenever the comments change
    comments_changed = pyqtSignal(bool)

    # Invoked, whenever the current selected comment has changed, p1='new selected comment'
    comment_selection_changed = pyqtSignal(int)

    # Invoked, whenever the comment amount changed, p1='new total amount'
    comment_amount_changed = pyqtSignal(int)

    # Invoked, whenever the search highlight should be changed,  p1='current hit' p2='total hits'
    search_highlight_changed = pyqtSignal(int, int)

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

        self.__search_helper = CommentsTableSearcher(parent=self, model=self.__model, model_sel=self.selectionModel())
        self.__search_helper.highlight.connect(self.__on_search_highlight_change)

        self.comments_changed.connect(self.__search_helper.on_comments_changed)
        self.comment_amount_changed.connect(self.__search_helper.on_comments_changed)

    def delete_current_selected_comment(self) -> None:
        """
        Will delete the current selected comment row.
        If selection is empty, no action will be invoked.
        """

        def delete(selected: List[QModelIndex]):
            self.__model.removeRows(selected[0].row(), 1)
            self.comments_changed.emit(False)
            self.comment_amount_changed.emit(self.__model.rowCount())

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
            self.comments_changed.emit(False)

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

    def add_comments(self, comments: Tuple[Comment], changes_qc=False, edit=False, resize_ct_column=True):
        if not comments:
            return

        model = self.__model
        last_entry = None

        # Always resize on the first comment imported
        resize_ct_column = resize_ct_column or not model.hasChildren()

        for comment in comments:
            time = QStandardItem(comment.comment_time)
            time.setTextAlignment(Qt.AlignCenter)
            ct = QStandardItem(QCoreApplication.translate("CommentTypes", comment.comment_type))
            note = QStandardItem(comment.comment_note)
            last_entry = [time, ct, note]
            model.appendRow(last_entry)

        if resize_ct_column:
            self.resize_column_type_column()

        self.sort()

        self.comment_amount_changed.emit(model.rowCount())
        self.__on_row_selection_changed()

        if changes_qc:
            self.comments_changed.emit(False)

        if edit:
            new_index = model.indexFromItem(last_entry[2])
            self.scrollTo(new_index)
            self.setCurrentIndex(new_index)
            self.edit(new_index)
        else:
            self.ensure_selection()

    def add_comment(self, comment_type: str) -> None:
        _, position_str = self.__widget_mpv.player.position_current()
        comment = Comment(
            comment_time=position_str,
            comment_type=comment_type,
            comment_note=""
        )
        self.add_comments((comment,), changes_qc=True, edit=True, resize_ct_column=False)

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
        self.comments_changed.emit(True)
        self.comment_amount_changed.emit(self.__model.rowCount())
        self.comment_selection_changed.emit(-1)

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
        self.comments_changed.emit(False)

    def __on_after_user_changed_comment_type(self) -> None:
        """
        Action to invoke after comment type was changed manually by the user.
        """

        self.comments_changed.emit(False)

    # noinspection PyMethodMayBeStatic
    def __on_after_user_changed_comment_note(self) -> None:
        """
        Action to invoke after comment note was changed manually by the user.
        """

        self.comments_changed.emit(False)

    # noinspection PyMethodMayBeStatic
    def __on_row_selection_changed(self) -> None:

        def after_model_updated():
            current_index = self.selectionModel().currentIndex()
            if current_index.isValid():
                new_row = current_index.row()
            else:
                new_row = -1
            self.comment_selection_changed.emit(new_row)

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
            if not self.selectionModel().hasSelection():
                self.__highlight_row(self.model().index(0, 2))

    def __highlight_row(self, m_idx: QModelIndex):
        if m_idx:
            self.selectionModel().setCurrentIndex(m_idx, self.__selection_flags)
            self.selectionModel().select(m_idx, self.__selection_flags)
            self.scrollTo(m_idx, QAbstractItemView.EnsureVisible)

    def resize_column_type_column(self):
        self.resizeColumnToContents(1)

    @pyqtSlot()
    def on_search_shown(self):
        self.__search_helper.on_search_shown()

    @pyqtSlot()
    def on_search_hidden(self):
        self.setFocus()
        self.__search_helper.on_search_hidden()

    @pyqtSlot(str)
    def on_search_query_changed(self, query: str):
        self.__search_helper.on_search_query_changed(query=query)

    @pyqtSlot()
    def on_search_next_result(self):
        self.__search_helper.on_search_next_result()

    @pyqtSlot()
    def on_search_previous_result(self):
        self.__search_helper.on_search_previous_result()

    @pyqtSlot()
    def on_search_edit_comment(self):
        self.edit_current_selected_comment()

    @pyqtSlot(object, int, int)
    def __on_search_highlight_change(self, m_idx: Optional[QModelIndex], current: int, total: int):
        self.search_highlight_changed.emit(current, total)
        self.__highlight_row(m_idx)
