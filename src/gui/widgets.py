from typing import List, Tuple

from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, Qt, QPoint, QModelIndex
from PyQt5.QtGui import QMouseEvent, QWheelEvent, QKeyEvent, QCursor, QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QFrame, QTableView, QStatusBar, QMenu, QAbstractItemView, QLabel

from src.files import Files
from src.gui import delegates, utils
from src.gui.delegates import CommentTypeDelegate, CommentTimeDelegate, CommentNoteDelegate
from src.gui.uihandler.main import MainHandler
from src.gui.utils import KEY_MAPPINGS
from src.player import bindings
from src.player.players import MpvPlayer, ActionType
from src.qcutils import Comment
from src.settings import Settings

_translate = QtCore.QCoreApplication.translate


class MpvWidget(QFrame):

    def __init__(self, widget_main: MainHandler):
        super(MpvWidget, self).__init__(widget_main)
        self.main_handler = widget_main
        self.application = widget_main.application

        self.setStyleSheet("background-color:black;")
        self.setMouseTracking(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        self.cursor_timer = QTimer(self)
        self.cursor_timer.setSingleShot(True)
        # noinspection PyUnresolvedReferences
        self.cursor_timer.timeout.connect(
            lambda arg=False, f=self.main_handler.display_mouse_cursor: f(arg))

        mpv = bindings.MPV(
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
            # log_handler=mpvLogHandler,
        )

        status_bar = widget_main.widget_status_bar

        @mpv.property_observer('percent-pos')
        def observe_percent_pos(_name, value):
            if value:
                status_bar.set_progress_percentage(value)

        @mpv.property_observer('time-pos')
        def observe_time_pos(_name, value):
            if value:
                status_bar.set_time_current(value)

        @mpv.property_observer('time-remaining')
        def observe_time_remaining(_name, value):
            if value:
                status_bar.set_time_remaining(value)

        @mpv.property_observer('path')
        def observe_full_path(_name, value):
            if value:
                widget_main.observed_player_property_full_path(value)

        @mpv.property_observer('filename/no-ext')
        def observe_filename(_name, value):
            if value:
                widget_main.observed_player_property_video_file_name(value)

        self.mpv_player = MpvPlayer(mpv)

    def mouseMoveEvent(self, e: QMouseEvent):

        if e.type() == QMouseEvent.MouseMove:
            try:
                self.mpv_player.mouse_move(e.pos().x(), e.pos().y())
            except OSError:
                # todo logger
                pass

        self.main_handler.display_mouse_cursor(display=True)

    def mousePressEvent(self, e: QMouseEvent):
        button = e.button()
        self.setFocus()

        if button == Qt.LeftButton:
            self.mpv_player.mouse_action(0, ActionType.DOWN)
        elif button == Qt.MiddleButton:
            self.mpv_player.mouse_action(1, ActionType.PRESS)
        elif button == Qt.RightButton and self.mpv_player.is_video_loaded():
            self.main_handler.widget_context_menu.exec_()
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
            self.main_handler.toggle_fullscreen()
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
        mod = int(self.application.keyboardModifiers())
        key = e.key()
        cmd = ""

        # List view bindings
        if (key == Qt.Key_Up or key == Qt.Key_Down) and mod == Qt.NoModifier:
            self.main_handler.widget_comments.keyPressEvent(e)
        elif key == Qt.Key_Delete:
            self.main_handler.widget_comments.delete_current_selected_comment()
        elif key == Qt.Key_Return or key == Qt.Key_Backspace:  # Backspace or Enter
            self.main_handler.widget_comments.edit_current_selected_comment()
        elif key == Qt.Key_C and mod == Qt.CTRL:
            self.main_handler.widget_comments.copy_current_selected_comment()

        #
        elif key == Qt.Key_F and mod == Qt.NoModifier and self.mpv_player.is_video_loaded():
            self.main_handler.toggle_fullscreen()
        elif key == Qt.Key_E and mod == Qt.NoModifier and self.mpv_player.is_video_loaded():
            self.main_handler.widget_context_menu.exec_()
        elif key == Qt.Key_Escape and mod == Qt.NoModifier:
            self.main_handler.display_normal()
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
    Pseudo context menu when user right clicks into the video or presses the 'e' button.
    """

    def __init__(self, main_handler: MainHandler):
        super().__init__()
        self.main_handler = main_handler
        self.widget_comments = main_handler.widget_comments
        self.mpv_player = main_handler.widget_mpv.mpv_player
        self.update_entries()

    def update_entries(self):
        """
        Will update the entries of this context menu to match the comment types from the settings.
        """

        self.clear()

        ct_list = Settings.Holder.COMMENT_TYPES.value
        if not ct_list:
            no_ct_action = _translate("CommentTypes",
                                      "No comment types defined." + " " + "Define new comment types in the settings.")
            ac = self.addAction(no_ct_action)
            ac.setEnabled(False)
        else:
            for ct in ct_list:
                act = self.addAction(ct)
                act.triggered.connect(lambda x, t=ct, f=self.widget_comments.add_comment: f(t))

    def exec_(self):
        """
        Will display the menu.
        """

        self.mpv_player.pause()
        self.main_handler.display_normal()

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
        self.main_handler = main_handler
        self.application = main_handler.application
        self.widget_mpv = main_handler.widget_mpv
        self.mpv_player = self.widget_mpv.mpv_player

        # Headers
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()

        # Model
        self.model = QStandardItemModel(self)
        self.setModel(self.model)

        # Delegates
        self.comment_time_delegate = CommentTimeDelegate(self, self.on_after_user_changed_time)
        self.comment_type_delegate = CommentTypeDelegate(self, self.on_after_user_changed_comment_type)
        self.comment_note_delegate = CommentNoteDelegate(self, self.on_after_user_changed_comment_note)
        self.setItemDelegateForColumn(0, self.comment_time_delegate)
        self.setItemDelegateForColumn(1, self.comment_type_delegate)
        self.setItemDelegateForColumn(2, self.comment_note_delegate)

        # Misc
        self.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setWordWrap(True)
        self.setShowGrid(False)

        self.scroll_position = 0
        self.comments_up_to_date = True

    def delete_current_selected_comment(self) -> None:
        """
        Will delete the current selected comment row.
        If selection is empty, no action will be invoked.
        """

        def delete(selected: List[QModelIndex]):
            self.model.removeRows(selected[0].row(), 1)
            self.comments_up_to_date = False

        self.__do_with_selected_comment_row(delete)

    def edit_current_selected_comment(self) -> None:
        """
        Will start edit mode on selected comment row.
        If selection is empty, no action will be invoked.
        """

        def edit(selected: List[QModelIndex]):
            row = selected[0].row()
            idx = self.model.item(row, 2).index()
            self.edit(idx)
            self.comments_up_to_date = False

        self.__do_with_selected_comment_row(edit)

    def copy_current_selected_comment(self) -> None:
        """
        Will copy the complete row to clipboard.
        If selection is empty, no action will be invoked.
        """

        def copy(selected: List[QModelIndex]):
            row = selected[0].row()
            time = self.model.item(row, 0).text()
            coty = self.model.item(row, 1).text()
            note = self.model.item(row, 2).text()
            self.application.clipboard().setText("[{}][{}] {}".format(time, coty, note))

        self.__do_with_selected_comment_row(copy)

    def __do_with_selected_comment_row(self, consume_selected_function) -> None:
        """
        This function takes a **function** as argument.

        *It will call the function with the current selection as argument if selection is not empty.*

        :param consume_selected_function: The function to apply if selection is not empty
        """

        is_empty: bool = self.model.rowCount() == 0

        if not is_empty:
            selected = self.selectionModel().selectedRows()

            if selected:
                consume_selected_function(selected)

    def add_comment(self, comment_type: str, comment_text: str = "", time: str = None,
                    sort: bool = True, will_change_qc=True, edit_mode_active=True) -> None:
        """
        Will add a new comment type to the list view.

        :param comment_type: The comment type to add
        :param comment_text: The text to add
        :param time: The time to add. If None the current video time will be used.
        :param sort: If True, the complete table will be sorted after the insertion.
        :param edit_mode_active: True then edit mode will be started.
        :param will_change_qc: True if qc is changed with the addition.
        """

        if time is None:
            time: str = self.widget_mpv.mpv_player.position_current()

        ti = QStandardItem(time)
        ti.setFont(delegates.TYPEWRITER_FONT)

        ct = QStandardItem(_translate("CommentTypes", comment_type))
        ct.setFont(delegates.TYPEWRITER_FONT)

        note = QStandardItem(comment_text)

        new_entry = [ti, ct, note]
        self.model.appendRow([ti, ct, note])

        self.__after_comment_added(new_entry, sort, edit_mode_active, will_change_qc)

    def __after_comment_added(self, new_entry: List[QStandardItem], sort: bool,
                              edit_mode: bool, will_change_qc: bool) -> None:
        """

        :param new_entry: The newly added entry
        :param sort: If True, the complete table will be sorted after the insertion.
        :param edit_mode: True then edit mode will be started.
        :param will_change_qc: True if qc is changed with the addition.
        """

        if sort:
            self.sort()
        self.resizeColumnToContents(1)

        new_index = self.model.indexFromItem(new_entry[2])
        self.scrollTo(new_index)
        self.setCurrentIndex(new_index)

        if edit_mode:
            self.edit(new_index)

        if will_change_qc:
            self.comments_up_to_date = False

    def get_all_comments(self) -> Tuple[Comment]:
        """
        Returns all comments.
        :return: all comments.
        """

        ret_list = []
        model = self.model

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

        self.model.clear()
        self.comments_up_to_date = True
        self.__delegate_row_count_to_status_bar()

    def on_before_fullscreen(self) -> None:
        """
        Action to invoke before switching to fullscreen.
        """

        self.scroll_position = self.verticalScrollBar().value()

    def on_after_fullscreen(self) -> None:
        """
        Action to invoke after switching back from fullscreen.
        """

        self.verticalScrollBar().setValue(self.scroll_position)

    def on_after_user_changed_time(self) -> None:
        """
        Action to invoke after time was changed manually by the user.
        """

        self.sort()
        self.comments_up_to_date = False

    def on_after_user_changed_comment_type(self) -> None:
        """
        Action to invoke after comment type was changed manually by the user.
        """

        self.resizeColumnToContents(1)
        self.comments_up_to_date = False

    def on_after_user_changed_comment_note(self) -> None:
        """
        Action to invoke after comment note was changed manually by the user.
        """

        self.comments_up_to_date = False

    def sort(self) -> None:
        """
        Will sort the comments table by time column.
        """

        self.sortByColumn(0, Qt.AscendingOrder)

    def keyPressEvent(self, e: QKeyEvent):

        mod = int(self.application.keyboardModifiers())
        key = e.key()

        if (key == Qt.Key_Up or key == Qt.Key_Down) and mod == Qt.NoModifier:
            super().keyPressEvent(e)
        else:
            self.widget_mpv.keyPressEvent(e)

    def mousePressEvent(self, e: QMouseEvent):

        if e.button() == Qt.LeftButton:
            mdi: QModelIndex = self.indexAt(e.pos())
            if mdi.column() == 0 and self.mpv_player.is_video_loaded():
                position = self.model.item(mdi.row(), 0).text()
                self.widget_mpv.mpv_player.position_jump(position=position)
            elif mdi.column() == 1:
                self.edit(mdi)
            e.accept()
        super().mousePressEvent(e)

    def rowsInserted(self, parent: QtCore.QModelIndex, start: int, end: int):
        super(CommentsTable, self).rowsInserted(parent, start, end)
        self.__delegate_row_count_to_status_bar()

    def rowsAboutToBeRemoved(self, parent: QtCore.QModelIndex, start: int, end: int):
        super(CommentsTable, self).rowsAboutToBeRemoved(parent, start, end)
        self.__delegate_row_count_to_status_bar()

    def __delegate_row_count_to_status_bar(self):
        self.main_handler.widget_status_bar.set_comments_amount(self.model.rowCount())


class StatusBar(QStatusBar):
    class ClickableQLabel(QLabel):
        def __init__(self):
            super().__init__()
            self.on_right_mouse_click = None
            self.on_left_mouse_click = None

        def mousePressEvent(self, e: QMouseEvent):
            button = e.button()

            if button == Qt.LeftButton and self.on_left_mouse_click:
                self.on_left_mouse_click()
            elif button == Qt.RightButton and self.on_right_mouse_click:
                self.on_right_mouse_click()

    def __init__(self, main_handler: MainHandler):
        super().__init__()

        # Time and remaining time
        self.__time_video = StatusBar.ClickableQLabel()
        self.__time_video_toggle: bool = True  # If True -> current Time, If False -> Remaining Time

        def toggle_show_current_video_time():
            self.__time_video_toggle = not self.__time_video_toggle

        self.__time_video.on_left_mouse_click = toggle_show_current_video_time

        # Percentage
        self.__label_percentage = QLabel()
        self.__label_comments_count = QLabel()

        # Widgets
        self.addWidget(self.__time_video)
        self.addWidget(self.__label_percentage)
        self.addWidget(self.__label_comments_count)

    @staticmethod
    def __seconds_float_to_formatted_string_hours(seconds: float):
        int_val = int(seconds)
        m, s = divmod(int_val, 60)
        h, m = divmod(m, 60)
        h = "{:02d}:".format(h) if h != 0 else ""

        return "{}{:02d}:{:02d}".format(h, m, s)

    def set_progress_percentage(self, value: float):
        prefix = _translate("StatusBar", "Progress")
        self.__label_percentage.setText("{}: {} %".format(prefix, int(value)))

    def set_time_current(self, value: float):
        if not self.__time_video_toggle:
            return

        self.__time_video.setText("{}: {}".format(_translate("StatusBar", "Time"),
                                                  StatusBar.__seconds_float_to_formatted_string_hours(value)))

    def set_time_remaining(self, value: float):
        if self.__time_video_toggle:
            return

        self.__time_video.setText("{}: {}".format(_translate("StatusBar", "Remaining"),
                                                  StatusBar.__seconds_float_to_formatted_string_hours(value)))

    def set_comments_amount(self, amount: int):
        self.__label_comments_count.setText("{}: {}".format(_translate("StatusBar", "Comments"), amount))
