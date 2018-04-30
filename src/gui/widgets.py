from typing import List

from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, Qt, QPoint, QModelIndex
from PyQt5.QtGui import QMouseEvent, QWheelEvent, QKeyEvent, QCursor, QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QFrame, QTableView, QStatusBar, QMenu, QAbstractItemView

from src.files import Files
from src.gui import delegates
from src.gui.delegates import CommentTypeDelegate, CommentTimeDelegate
from src.gui.uihandler.main import MainHandler
from src.player import bindings
from src.player.players import MpvPlayer, ActionType
from src.qcutils import Comment
from src.settings import Settings

_translate = QtCore.QCoreApplication.translate


class MpvWidget(QFrame):

    def __init__(self, widget_main: MainHandler):
        super(MpvWidget, self).__init__(widget_main)
        self.widget_main = widget_main

        self.setStyleSheet("background-color:black;")
        self.setMouseTracking(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        self.cursor_timer = QTimer(self)
        self.cursor_timer.setSingleShot(True)
        # noinspection PyUnresolvedReferences
        self.cursor_timer.timeout.connect(
            lambda arg=False, f=self.widget_main.display_mouse_cursor: f(arg))

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
        # @mpv.property_observer('time-pos')
        # def time_observer(_name, value):
        #     print("Time: ", value)

        self.mpv_player = MpvPlayer(mpv)

    def mouseMoveEvent(self, mev: QMouseEvent):

        if mev.type() == QMouseEvent.MouseMove:
            try:
                self.mpv_player.mouse_move(mev.pos().x(), mev.pos().y())
            except OSError:
                # todo logger
                pass

        self.widget_main.display_mouse_cursor(display=True)

    def mousePressEvent(self, mev: QMouseEvent):
        self.setFocus()
        # self.comment_list.setFocus()

        button = mev.button()

        if button == Qt.LeftButton:
            self.mpv_player.mouse_action(0, ActionType.DOWN)
        elif button == Qt.MiddleButton:
            self.mpv_player.mouse_action(1, ActionType.PRESS)
        elif button == Qt.RightButton and self.mpv_player.is_video_loaded():
            self.widget_main.widget_context_menu.exec_()
        elif button == Qt.BackButton:
            self.mpv_player.mouse_action(5, ActionType.PRESS)
        elif button == Qt.ForwardButton:
            self.mpv_player.mouse_action(6, ActionType.PRESS)

    def mouseReleaseEvent(self, mev: QMouseEvent):
        button = mev.button()

        if button == Qt.LeftButton:
            self.mpv_player.mouse_action(0, ActionType.UP)

    def mouseDoubleClickEvent(self, mev: QMouseEvent):
        button = mev.button()

        if button == Qt.LeftButton:
            self.widget_main.toggle_fullscreen()
            self.mpv_player.mouse_action(0, ActionType.PRESS)
        elif button == Qt.MiddleButton:
            self.mpv_player.mouse_action(1, ActionType.PRESS)
        elif button == Qt.BackButton:
            self.mpv_player.mouse_action(5, ActionType.PRESS)
        elif button == Qt.ForwardButton:
            self.mpv_player.mouse_action(6, ActionType.PRESS)
        else:
            return super().mouseDoubleClickEvent(mev)

    def wheelEvent(self, whe: QWheelEvent):
        delta = whe.angleDelta()

        x_d = delta.x()
        y_d = delta.y()

        if x_d == 0 and y_d != 0:
            if y_d > 0:
                self.mpv_player.mouse_action(3, ActionType.PRESS)
            else:
                self.mpv_player.mouse_action(4, ActionType.PRESS)
        else:
            super().wheelEvent(whe)

    def keyPressEvent(self, kev: QKeyEvent):
        print(kev.text())


class ContextMenu(QMenu):
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

        if self.main_handler.isFullScreen():
            self.main_handler.hide_fullscreen()

        m_pos = QCursor.pos()
        # Fixes following: Qt puts the context menu in a place
        # where double clicking would trigger the fist menu option
        # instead of just calling the menu a second time
        # or ignoring the second press
        super().exec_(QPoint(m_pos.x() + 1, m_pos.y()))


class StatusBar(QStatusBar):
    def __init__(self, main_handler: MainHandler):
        super().__init__()
        self.showMessage("ada", 4000)


class CommentsWidget(QTableView):
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
        self.comment_type_delegate = CommentTypeDelegate(self, self.on_after_user_changed_comment_type)
        self.comment_time_delegate = CommentTimeDelegate(self, self.on_after_user_changed_time)
        self.setItemDelegateForColumn(0, self.comment_time_delegate)
        self.setItemDelegateForColumn(1, self.comment_type_delegate)

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

        *It will call the function with the given argument if the selection is not empty.*
        :param consume_selected_function: The function to apply if selection is not empty
        :return:
        """

        is_empty: bool = self.model.rowCount() == 0

        if not is_empty:
            selected = self.selectionModel().selectedRows()

            if selected:
                consume_selected_function(selected)

    def add_comment(self, comment_type: str, comment_text: str = "", time: str = None,
                    sort: bool = True, will_change_qc=True) -> None:
        """
        Will add a new comment type to the list view.

        :param will_change_qc: True if qc is changed with the addition.
        :param comment_type: The comment type to add
        :param comment_text: The text to add
        :param time: The time to add. If None the current video time will be used.
        :param sort: If True, the complete table will be sorted after the insertion.
        """

        if time is None:
            time: str = self.widget_mpv.mpv_player.position_current()

        ti = QStandardItem(time)
        ti.setFont(delegates.typewriter_font())

        ct = QStandardItem(_translate("CommentTypes", comment_type))
        ct.setFont(delegates.typewriter_font())

        note = QStandardItem(comment_text)

        new_entry = [ti, ct, note]
        self.model.appendRow([ti, ct, note])

        if sort:
            self.sortByColumn(0, Qt.AscendingOrder)
        self.resizeColumnToContents(1)

        new_index = self.model.indexFromItem(new_entry[2])
        self.scrollTo(new_index)
        self.setCurrentIndex(new_index)
        self.edit(new_index)

        if will_change_qc:
            self.comments_up_to_date = False

    def get_all_comments(self) -> List[Comment]:
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
        return ret_list

    def delete_all_comments(self) -> None:
        """
        Will clear all comments.
        """

        self.model.clear()
        self.comments_up_to_date = True

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

        self.sortByColumn(0, Qt.AscendingOrder)
        self.comments_up_to_date = False

    def on_after_user_changed_comment_type(self) -> None:
        """
        Action to invoke after comment type was changed manually by the user.
        """

        self.resizeColumnToContents(1)
        self.comments_up_to_date = False

    def keyPressEvent(self, e: QKeyEvent):

        mod = int(self.application.keyboardModifiers())
        key = e.key()

        if (key == Qt.Key_Up or key == Qt.Key_Down) and mod == Qt.NoModifier:
            super().keyPressEvent(e)
        elif key == Qt.Key_Delete:
            self.delete_current_selected_comment()
        elif key == Qt.Key_Return or key == Qt.Key_Backspace:  # Backspace or Enter
            self.edit_current_selected_comment()
        elif key == Qt.Key_C and mod == Qt.CTRL:
            self.copy_current_selected_comment()
        else:
            e.ignore()
        e.accept()

        self.widget_mpv.keyPressEvent(e)

    def mousePressEvent(self, e: QMouseEvent):

        if e.button() == Qt.LeftButton:
            mdi: QModelIndex = self.indexAt(e.pos())
            if mdi.column() == 0 and self.mpv_player.is_video_loaded():
                position = self.model.item(mdi.row(), 0).text()
                self.widget_mpv.mpv_player.position_jump(position=position)
            elif mdi.column() == 1:
                self.edit(mdi)
            else:
                pass
            e.accept()
        super().mousePressEvent(e)
