from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QMouseEvent, QWheelEvent
from PyQt5.QtWidgets import QFrame

from src.player import bindings
from src.player.players import MpvPlayer, ActionType
from src.preferences import configuration
from tmpv import ApplicationWindow


class MpvWidget(QFrame):

    def __init__(self, parent):
        super(MpvWidget, self).__init__(parent)
        self.main_window: ApplicationWindow = parent
        self.comment_list = self.main_window.ui.tableView

        self.setStyleSheet("background-color:black;")
        self.setMouseTracking(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        self.cursor_timer = QTimer(self)
        self.cursor_timer.setSingleShot(True)
        self.cursor_timer.timeout.connect(self.main_window.hide_mouse_cursor)

        mpv_mpv = bindings.MPV(
            wid=str(int(self.winId())),
            keep_open="yes",
            idle="yes",
            osc="yes",
            cursor_autohide="no",
            input_cursor="no",
            input_default_bindings="no",
            config="yes",
            config_dir=configuration.get_paths().dir_main_cfg,
            ytdl="yes",
            # log_handler=mpvLogHandler,
        )

        self.mpv_player = MpvPlayer(mpv_mpv)

    def mouseMoveEvent(self, mev: QMouseEvent):

        if mev.type() == QMouseEvent.MouseMove:
            try:
                self.mpv_player.mouse_move(mev.pos().x(), mev.pos().y())
            except OSError:
                # todo logger
                pass

        self.main_window.display_mouse_cursor()

    def mousePressEvent(self, mev: QMouseEvent):
        self.setFocus()
        self.comment_list.setFocus()

        button = mev.button()

        if button == Qt.LeftButton:
            self.mpv_player.mouse_action(0, ActionType.DOWN)
        elif button == Qt.MiddleButton:
            self.mpv_player.mouse_action(1, ActionType.PRESS)
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
            self.main_window.toggle_fullscreen()
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
