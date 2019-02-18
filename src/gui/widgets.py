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
from enum import Enum
from typing import List, Tuple

from PyQt5.QtCore import QTimer, Qt, QPoint, QModelIndex, QEvent, QItemSelection, QObject, pyqtSignal, QCoreApplication, \
    QRegExp, QItemSelectionModel
from PyQt5.QtGui import QMouseEvent, QWheelEvent, QKeyEvent, QCursor, QStandardItem, QStandardItemModel, \
    QRegExpValidator
from PyQt5.QtWidgets import QFrame, QTableView, QStatusBar, QMenu, QAbstractItemView, QLabel, QLineEdit, QListWidget, \
    QPushButton, QListWidgetItem, QApplication

from src import settings, logging
from src.files import Files
from src.gui import utils, TYPEWRITER_FONT
from src.gui.delegates import CommentTypeDelegate, CommentTimeDelegate, CommentNoteDelegate
from src.gui.events import PlayerVideoTimeChanged, EventPlayerVideoTimeChanged, PlayerRemainingVideoTimeChanged, \
    EventPlayerRemainingVideoTimeChanged, EventPlayerPercentChanged, PlayerPercentChanged, EventCommentAmountChanged, \
    CommentAmountChanged, EventCommentsUpToDate, EventDistributor, CommentCurrentSelectionChanged, \
    EventCommentCurrentSelectionChanged, EventReceiver
from src.gui.searchutils import SearchResult
from src.gui.uihandler.main import MainHandler
from src.gui.uihandler.preferences import PreferenceHandler
from src.gui.utils import KEY_MAPPINGS
from src.player import bindings
from src.player.observed import MpvPropertyObserver
from src.player.players import MpvPlayer, ActionType
from src.qcutils import Comment

_translate = QCoreApplication.translate


class MpvWidget(QFrame):

    def __init__(self, main_handler: MainHandler):
        super(MpvWidget, self).__init__(main_handler)
        self.__main_handler = main_handler

        self.cursor_timer = QTimer(self)
        self.cursor_timer.setSingleShot(True)
        # noinspection PyUnresolvedReferences
        self.cursor_timer.timeout.connect(
            lambda arg=False, f=self.__main_handler.display_mouse_cursor: f(arg))

        self.setStyleSheet("background-color:black;")
        # todo/discussion Add a little welcome text/tutorial instead of displaying a plain dark widget
        # It should hint the user to learn about mpv and its keyboard shortcuts and the basic workflow
        # This requires a user setting to disable the text on the widget too

        self.setMouseTracking(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        __mpv = bindings.MPV(
            wid=str(int(self.winId())),
            keep_open="yes",
            idle="yes",
            osc="yes",
            cursor_autohide="no",
            input_cursor="no",
            input_default_bindings="no",
            config="yes",
            config_dir=Files.DIRECTORY_CONFIGURATION,
            ytdl="yes",
            log_handler=logging.mpv_log_handler,
        )

        self.mpv_player = MpvPlayer(__mpv)
        MpvPropertyObserver(__mpv)

        PreferenceHandler.VERSION_MPV = self.mpv_player.version_mpv()
        PreferenceHandler.VERSION_FFMPEG = self.mpv_player.ffmpeg_version()

    def mouseMoveEvent(self, e: QMouseEvent):
        if e.type() == QMouseEvent.MouseMove:
            try:
                self.mpv_player.mouse_move(e.pos().x(), e.pos().y())
            except OSError:
                # todo logger
                pass

        self.__main_handler.display_mouse_cursor(display=True)

    def mousePressEvent(self, e: QMouseEvent):
        button = e.button()
        self.setFocus()

        if button == Qt.LeftButton:
            self.mpv_player.mouse_action(0, ActionType.DOWN)
        elif button == Qt.MiddleButton:
            self.mpv_player.mouse_action(1, ActionType.PRESS)
        elif button == Qt.RightButton and self.mpv_player.is_video_loaded():
            self.__main_handler.widget_context_menu.exec_()
        elif button == Qt.BackButton:
            self.mpv_player.mouse_action(5, ActionType.PRESS)
        elif button == Qt.ForwardButton:
            self.mpv_player.mouse_action(6, ActionType.PRESS)

    def mouseReleaseEvent(self, e: QMouseEvent):
        button = e.button()

        if button == Qt.LeftButton:
            self.mpv_player.mouse_action(0, ActionType.UP)

    def mouseDoubleClickEvent(self, mev: QMouseEvent):
        button = mev.button()

        if button == Qt.LeftButton and self.mpv_player.video_file_current():
            self.__main_handler.toggle_fullscreen()
            self.mpv_player.mouse_action(0, ActionType.PRESS)
        elif button == Qt.MiddleButton:
            self.mpv_player.mouse_action(1, ActionType.PRESS)
        elif button == Qt.BackButton:
            self.mpv_player.mouse_action(5, ActionType.PRESS)
        elif button == Qt.ForwardButton:
            self.mpv_player.mouse_action(6, ActionType.PRESS)
        else:
            return super().mouseDoubleClickEvent(mev)

    def wheelEvent(self, e: QWheelEvent):
        delta = e.angleDelta()

        x_d = delta.x()
        y_d = delta.y()

        if x_d == 0 and y_d != 0:
            if y_d > 0:
                self.mpv_player.mouse_action(3, ActionType.PRESS)
            else:
                self.mpv_player.mouse_action(4, ActionType.PRESS)
        else:
            super().wheelEvent(e)

    def keyPressEvent(self, e: QKeyEvent):
        mod = e.modifiers()
        key = e.key()
        cmd = ""

        # Comment table bindings
        if (key == Qt.Key_Up or key == Qt.Key_Down) and mod == Qt.NoModifier:
            self.__main_handler.widget_comments.keyPressEvent(e)
        elif key == Qt.Key_Delete:
            self.__main_handler.widget_comments.delete_current_selected_comment()
        elif key == Qt.Key_Return or key == Qt.Key_Backspace:  # Backspace or Enter
            if self.__main_handler.widget_comments.state() == QAbstractItemView.NoState:
                self.__main_handler.widget_comments.edit_current_selected_comment()
        elif key == Qt.Key_C and mod == Qt.ControlModifier:
            self.__main_handler.widget_comments.copy_current_selected_comment()
        elif key == Qt.Key_F and mod == Qt.ControlModifier:
            self.__main_handler.search_bar.keyPressEvent(e)

        # Mpv Video widget bindings
        elif key == Qt.Key_F and mod == Qt.NoModifier and self.mpv_player.is_video_loaded():
            self.__main_handler.toggle_fullscreen()
        elif key == Qt.Key_E and mod == Qt.NoModifier and self.mpv_player.is_video_loaded():
            self.__main_handler.widget_context_menu.exec_()
        elif key == Qt.Key_Escape and mod == Qt.NoModifier:
            self.__main_handler.display_normal()
        elif key in KEY_MAPPINGS:
            cmd = utils.command_generator(mod, *KEY_MAPPINGS[key])
        elif key != 0:
            try:
                ks = chr(key)
            except ValueError:
                pass
            else:
                cmd = utils.command_generator(mod, ks, is_char=True)
        else:
            super(MpvWidget, self).keyPressEvent(e)

        if cmd:
            self.mpv_player.button_action(cmd, ActionType.PRESS)


class ContextMenu(QMenu):
    """
    Pseudo context menu when user right clicks into the video or presses the 'e' button and if video is loaded.
    """

    def __init__(self, main_handler: MainHandler):
        super().__init__()
        self.__main_handler = main_handler
        self.__widget_comments = main_handler.widget_comments
        self.__mpv_player = main_handler.widget_mpv.mpv_player
        self.update_entries()

    def update_entries(self):
        """
        Will update the entries of this context menu to match the comment types from the settings.
        """

        self.clear()

        ct_list = settings.Setting_Custom_General_COMMENT_TYPES.value
        if not ct_list:
            no_ct_action = _translate("CommentTypes",
                                      "No comment types defined." + " " + "Define new comment types in the settings.")
            ac = self.addAction(no_ct_action)
            ac.setEnabled(False)
        else:
            for ct in ct_list:
                act = self.addAction(ct)
                act.triggered.connect(lambda x, t=ct, f=self.__widget_comments.add_comment: f(t))

    def exec_(self):
        """
        Will display the menu with comment types.
        """

        self.__mpv_player.pause()
        self.__main_handler.display_normal()

        m_pos = QCursor.pos()

        # Fixes following: Qt puts the context menu in a place
        # where double clicking would trigger the fist menu option
        # instead of just calling the menu a second time
        # or ignoring the second press
        super().exec_(QPoint(m_pos.x() + 1, m_pos.y()))


class CommentsTable(QTableView):
    """
    The comment table below the video.
    """

    def __init__(self, main_handler: MainHandler):
        super().__init__()
        self.__widget_mpv = main_handler.widget_mpv
        self.__mpv_player = self.__widget_mpv.mpv_player

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
        self.setWordWrap(True)
        self.setShowGrid(False)

    def delete_current_selected_comment(self) -> None:
        """
        Will delete the current selected comment row.
        If selection is empty, no action will be invoked.
        """

        def delete(selected: List[QModelIndex]):
            self.__model.removeRows(selected[0].row(), 1)
            EventDistributor.send_event(EventCommentsUpToDate(False))
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
            EventDistributor.send_event(EventCommentsUpToDate(False))

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
            QApplication.clipboard().setText("[{}][{}] {}".format(time, coty, note))

        self.__do_with_selected_comment_row(copy)

    def add_comment(self, comment_type: str, comment_text: str = "", time: str = None,
                    sort: bool = True, will_change_qc=True, edit_mode_active=True, resize_columns=True) -> None:
        """
        Will add a new comment to the list view.

        :param resize_columns: If True comment type column will be resized
        :param comment_type: The comment type to add
        :param comment_text: The text to add
        :param time: The time to add. If None the current video time will be used.
        :param sort: If True, the complete table will be sorted after the insertion.
        :param edit_mode_active: If True, edit mode will be started.
        :param will_change_qc: True if qc is changed with the addition.
        """

        if time is None:
            time: str = self.__widget_mpv.mpv_player.position_current()

        ti = QStandardItem(time)
        ti.setFont(TYPEWRITER_FONT)

        ct = QStandardItem(_translate("CommentTypes", comment_type))

        note = QStandardItem(comment_text)

        new_entry = [ti, ct, note]
        self.__model.appendRow(new_entry)

        self.__after_comment_added(new_entry, sort, edit_mode_active, will_change_qc, resize_columns)

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
            ret_list.append(Comment(time=time, coty=coty, note=note))
        return tuple(ret_list)

    def reset_comments_table(self) -> None:
        """
        Will clear all comments.
        """

        self.__model.clear()
        EventDistributor.send_event(EventCommentsUpToDate(True))
        EventDistributor.send_event(EventCommentAmountChanged(self.__model.rowCount()))
        EventDistributor.send_event(EventCommentCurrentSelectionChanged(-1))

    def sort(self) -> None:
        """
        Will sort the comments table by time column.
        """

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

    def __after_comment_added(self, new_entry: List[QStandardItem], sort: bool,
                              edit_mode: bool, will_change_qc: bool, resize_columns: bool) -> None:
        """
        This function must be called after a comment was added.

        :param new_entry: The newly added entry
        :param sort: If True, the complete table will be sorted after the insertion.
        :param edit_mode: If True edit mode will be started.
        :param will_change_qc: True if qc is changed with the addition.
        :param resize_columns: If True, comment type column will be resized
        """

        EventDistributor.send_event(EventCommentAmountChanged(self.__model.rowCount()))
        self.__on_row_selection_changed()

        if resize_columns:
            self.resizeColumnToContents(1)

        if sort:
            self.sort()

        if edit_mode:
            new_index = self.__model.indexFromItem(new_entry[2])
            self.scrollTo(new_index)
            self.setCurrentIndex(new_index)
            self.edit(new_index)

        if will_change_qc:
            EventDistributor.send_event(EventCommentsUpToDate(False))

    def __on_after_user_changed_time(self) -> None:
        """
        Action to invoke after time was changed manually by the user.
        """

        self.sort()
        EventDistributor.send_event(EventCommentsUpToDate(False))

    def __on_after_user_changed_comment_type(self) -> None:
        """
        Action to invoke after comment type was changed manually by the user.
        """

        self.resizeColumnToContents(1)
        EventDistributor.send_event(EventCommentsUpToDate(False))

    # noinspection PyMethodMayBeStatic
    def __on_after_user_changed_comment_note(self) -> None:
        """
        Action to invoke after comment note was changed manually by the user.
        """

        EventDistributor.send_event(EventCommentsUpToDate(False))

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
            if mdi.column() == 0 and self.__mpv_player.is_video_loaded():
                position = self.__model.item(mdi.row(), 0).text()
                self.__widget_mpv.mpv_player.position_jump(position=position)
                e.accept()
            elif mdi.column() == 1 and mdi == self.selectionModel().currentIndex():
                self.edit(mdi)
                e.accept()
        super().mousePressEvent(e)

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


class StatusBar(QStatusBar):

    def __init__(self):
        super().__init__()
        self.__time_current: str = "00:00"
        self.__time_remaining: str = "23:59:59"
        self.__percent: int = 0

        self.__comments_amount: int = 0
        self.__comments_current_selection: int = -1

        self.__time_format = settings.Setting_Internal_STATUS_BAR_TIME_MODE

        self.__label_information = QLabel()
        self.__label_information.setFont(TYPEWRITER_FONT)
        self.__label_information.setAlignment(Qt.AlignRight)
        self.__label_information.installEventFilter(self)

        self.__label_comment_selection_slash_amount = QLabel()
        self.__label_comment_selection_slash_amount.setFont(TYPEWRITER_FONT)

        # Timer updates status bar every 100 ms
        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__update_status_bar_text)
        self.__timer.start(100)

        self.addPermanentWidget(self.__label_comment_selection_slash_amount, 0)
        self.addPermanentWidget(QLabel(), 1)
        self.addPermanentWidget(self.__label_information, 0)

    def __update_status_bar_text(self) -> None:
        """
        Will update the current status bar information about video time and comments
        """

        time = self.__time_current if self.__time_format.value else "-{}".format(self.__time_remaining)
        percent = self.__percent if self.__time_format.value else 100 - self.__percent

        self.__label_information.setText("{:>9}{:2}{:3}%".format(time, "", percent))

    def __update_comment_amount_slash_selection(self):
        if self.__comments_current_selection >= 0:
            self.__label_comment_selection_slash_amount.setText(
                _translate("StatusBar", "Line") + ": {}/{}".format(self.__comments_current_selection + 1,
                                                                   self.__comments_amount))
        else:
            self.__label_comment_selection_slash_amount.setText("")

    def customEvent(self, ev: QEvent):

        ev_type = ev.type()

        if ev_type == PlayerVideoTimeChanged:
            ev: EventPlayerVideoTimeChanged
            self.__time_current = ev.time_current

        elif ev_type == PlayerRemainingVideoTimeChanged:
            ev: EventPlayerRemainingVideoTimeChanged
            self.__time_remaining = ev.time_remaining

        elif ev_type == PlayerPercentChanged:
            ev: EventPlayerPercentChanged
            self.__percent = ev.percent

        elif ev_type == CommentAmountChanged:
            ev: EventCommentAmountChanged
            self.__comments_amount = ev.new_amount
            self.__update_comment_amount_slash_selection()

        elif ev_type == CommentCurrentSelectionChanged:
            ev: EventCommentCurrentSelectionChanged
            self.__comments_current_selection = ev.current_selection
            self.__update_comment_amount_slash_selection()

    def changeEvent(self, ev: QEvent):
        ev_type = ev.type()

        if ev_type == QEvent.LanguageChange:
            self.__update_comment_amount_slash_selection()

    def eventFilter(self, source: QObject, event: QEvent):

        if source == self.__label_information and event.type() == QEvent.MouseButtonPress:
            event: QMouseEvent

            if event.button() == Qt.LeftButton:
                self.__time_format.value = not self.__time_format.value
                return True
        return super(StatusBar, self).eventFilter(source, event)


class PreferenceCommentTypesWidget(QObject):
    """
    This class is used in the preference window to create the comment type list widget
    which is controllable with four buttons and a line edit.

    It combines a QLineEdit, a QListWidget and four QPushButtons to a list widget.

    It is imitating the basic functionality of a KEditListWidget.
    """

    class __Mode(Enum):
        ADD = 0
        EDIT = 1

    # Signal is called after the items of the list view have changed
    changed = pyqtSignal()

    def __init__(self, line_edit: QLineEdit, list_widget: QListWidget, button_add: QPushButton,
                 button_remove: QPushButton, button_up: QPushButton, button_down: QPushButton):

        """
        All of the given widgets will define the Comment Types Widget.

        :param line_edit: The line edit to enter new comment types
        :param list_widget: The list widget to move items up and down or delete items.
        :param button_add: The button which allows to add an item
        :param button_remove: The button which allows to remove an item
        :param button_up: The button which allows to move up an item
        :param button_down: The button which allows to move down an item
        """

        super().__init__()

        self.__mode: PreferenceCommentTypesWidget.__Mode = PreferenceCommentTypesWidget.__Mode.ADD

        self.__line_edit = line_edit
        self.__line_edit.textChanged.connect(lambda txt, fun=self.__on_text_changed_line_edit: fun(txt))
        self.__line_edit.setValidator(QRegExpValidator(QRegExp("[^\[\]]*")))

        self.__list_widget = list_widget
        self.__list_widget.selectionModel().selectionChanged.connect(
            lambda selected, deselected, fun=self.__on_row_selection_changed: fun(selected, deselected))

        self.__button_add = button_add
        self.__button_add.clicked.connect(lambda _, fun=self.__on_pressed_button_add: fun())

        self.__button_remove = button_remove
        self.__button_remove.clicked.connect(lambda _, fun=self.__on_pressed_button_remove: fun())

        self.__button_up = button_up
        self.__button_up.clicked.connect(lambda _, fun=self.__on_pressed_button_up: fun())

        self.__button_down = button_down
        self.__button_down.clicked.connect(lambda _, fun=self.__on_pressed_button_down: fun())

    def __on_text_changed_line_edit(self, text) -> None:
        if self.__mode == PreferenceCommentTypesWidget.__Mode.ADD:
            self.__button_add.setEnabled(bool(text))
        else:
            self.__list_widget.item(self.__get_selected_row()).setText(self.__line_edit.text())
            self.changed.emit()

    def __on_pressed_button_add(self) -> None:
        self.__add_item(self.__line_edit.text())
        self.__line_edit.clear()
        self.__list_widget.selectionModel().clearSelection()
        self.__line_edit.setFocus()
        self.changed.emit()

    def __on_pressed_button_remove(self) -> None:
        self.__list_widget.model().removeRows(self.__get_selected_row(), 1)
        self.__list_widget.selectionModel().clearSelection()
        self.__line_edit.clear()
        self.changed.emit()

    def __on_pressed_button_up(self) -> None:
        idx: int = self.__get_selected_row()
        itm = self.__list_widget.takeItem(idx)
        self.__list_widget.insertItem(idx - 1, itm)
        self.__list_widget.setCurrentRow(idx - 1)

        self.changed.emit()

    def __on_pressed_button_down(self) -> None:
        idx: int = self.__get_selected_row()
        itm = self.__list_widget.takeItem(idx)
        self.__list_widget.insertItem(idx + 1, itm)
        self.__list_widget.setCurrentRow(idx + 1)

        self.changed.emit()

    def __add_item(self, text) -> None:
        item = QListWidgetItem(text)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.__list_widget.insertItem(0, item)

    def __get_selected_row(self) -> int:
        return self.__list_widget.selectionModel().selectedRows()[0].row()

    def __get_selected_item(self) -> QListWidgetItem:
        return self.__list_widget.item(self.__get_selected_row())

    def __on_row_selection_changed(self, selected: QItemSelection, deselected: QItemSelection) -> None:
        is_valid_selected = bool(selected)

        if is_valid_selected:
            self.__mode = PreferenceCommentTypesWidget.__Mode.EDIT
            self.__line_edit.setText(self.__get_selected_item().text())
            self.__line_edit.setFocus()
        else:
            self.__mode = PreferenceCommentTypesWidget.__Mode.ADD

        self.__button_remove.setEnabled(is_valid_selected)
        self.__button_up.setEnabled(is_valid_selected and selected.indexes()[0].row() != 0)
        self.__button_down.setEnabled(
            is_valid_selected and selected.indexes()[0].row() != self.__list_widget.model().rowCount() - 1)

    def remove_focus(self) -> None:
        """
        Will remove the focus from the line edit.
        """

        if self.__list_widget.selectionModel().selectedIndexes():
            self.__list_widget.clearSelection()
            self.__line_edit.clear()

            for btn in [self.__button_add, self.__button_remove, self.__button_up, self.__button_down]:
                btn.setEnabled(False)

    def items(self) -> List[str]:
        """
        Returns the items of the list widget.
        """

        ret_list = []
        for row in range(0, self.__list_widget.count()):
            content = self.__list_widget.item(row).text()
            ret_list.append(str(content))

        return ret_list
