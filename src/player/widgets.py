from PyQt5.QtCore import QTimer, Qt, QObject, QEvent
from PyQt5.QtGui import QMouseEvent, QWheelEvent
from PyQt5.QtWidgets import QFrame, QTableView, QStatusBar

from src.player import bindings
from src.player.players import MpvPlayer, ActionType
from src.shared.references import References


class CustomStatusBar(QStatusBar):
    def __init__(self, references: References):
        super().__init__()
        self.references = references


class CommentsWidget(QTableView):

    def __init__(self, references: References):
        super().__init__()
        self.references = references


class MpvWidget(QFrame):

    def __init__(self, references: References):
        from src.preferences import configuration

        super(MpvWidget, self).__init__(references.widget_main)
        self.references = references

        self.setStyleSheet("background-color:black;")
        self.setMouseTracking(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        self.cursor_timer = QTimer(self)
        self.cursor_timer.setSingleShot(True)
        self.cursor_timer.timeout.connect(
            lambda arg=False, f=self.references.widget_main.display_mouse_cursor: f(arg))

        mpv = bindings.MPV(
            wid=str(int(self.winId())),
            keep_open="yes",
            idle="yes",
            osc="yes",
            cursor_autohide="no",
            input_cursor="no",
            input_default_bindings="no",
            config="yes",
            config_dir=configuration.paths.dir_main_cfg,
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

        self.references.widget_main.display_mouse_cursor(display=True)

    def mousePressEvent(self, mev: QMouseEvent):
        self.setFocus()
        # self.comment_list.setFocus()

        button = mev.button()

        if button == Qt.LeftButton:
            self.mpv_player.mouse_action(0, ActionType.DOWN)
        elif button == Qt.MiddleButton:
            self.mpv_player.mouse_action(1, ActionType.PRESS)
        elif button == Qt.RightButton:
            print("Right button pressed!")
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
            self.references.widget_main.toggle_fullscreen()
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

    def eventFilter(self, source: QObject, event: QEvent) -> bool:

        if event.type() == QEvent.KeyPress:
            print("Key-Press")

        return super().eventFilter(source, event)
