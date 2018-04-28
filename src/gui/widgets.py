from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, Qt, QPoint
from PyQt5.QtGui import QMouseEvent, QWheelEvent, QKeyEvent, QCursor
from PyQt5.QtWidgets import QFrame, QTableView, QStatusBar, QMenu

from src.files import Files
from src.gui.uihandler.main import MainHandler
from src.player import bindings
from src.player.players import MpvPlayer, ActionType
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
        elif button == Qt.RightButton:
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


class CustomStatusBar(QStatusBar):
    def __init__(self, main_handler: MainHandler):
        super().__init__()
        self.showMessage("ada", 4000)


class CommentsWidget(QTableView):

    def __init__(self, main_handler: MainHandler):
        super().__init__()
        self.widget_mpv = main_handler.widget_mpv

    def add_comment(self, comment_type, comment_text="", time=None):
        print("Got new comment to add: {}".format(comment_type))

    def keyPressEvent(self, e: QKeyEvent):
        print("key press event from table")
        self.widget_mpv.keyPressEvent(e)

    def mousePressEvent(self, e: QMouseEvent):
        print("mouse press event from table")
        self.widget_mpv.mousePressEvent(e)


class CustomContextMenu(QMenu):
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
            cts_eng = {}
            for ct in Settings.Holder.COMMENT_TYPES.default_value:
                cts_eng.update({_translate("Misc", ct): ct})

            for ct in ct_list:
                act = self.addAction(_translate("CommentTypes", ct))
                act.triggered.connect(lambda x, t=cts_eng.get(ct, ct), f=self.widget_comments.add_comment: f(t))

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
