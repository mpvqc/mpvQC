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


from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMouseEvent, QWheelEvent, QKeyEvent
from PyQt5.QtWidgets import QFrame, QAbstractItemView

from mpvqc import logging
from mpvqc.player import MPV, MpvPlayer
from mpvqc.uihandler import MainHandler
from mpvqc.uiutil import KEY_MAPPINGS, command_generator, ActionType


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
        self.setMouseTracking(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setFocusPolicy(Qt.ClickFocus)

        from mpvqc import get_files
        files = get_files()

        __mpv = MPV(
            wid=str(int(self.winId())),
            keep_open="yes",
            idle="yes",
            osc="yes",
            cursor_autohide="no",
            input_cursor="no",
            input_default_bindings="no",
            config="yes",
            config_dir=files.dir_config,
            screenshot_directory=files.dir_screenshots,
            ytdl="yes",
            log_handler=logging.mpv_log_handler,
        )

        self.player = MpvPlayer(__mpv)

        from mpvqc.uihandler import AboutDialog
        AboutDialog.VERSION_MPV = self.player.version_mpv()
        AboutDialog.VERSION_FFMPEG = self.player.version_ffmpeg()

    def mouseMoveEvent(self, e: QMouseEvent):
        if e.type() == QMouseEvent.MouseMove:
            try:
                self.player.mouse_move(e.pos().x(), e.pos().y())
            except OSError:
                # todo logger
                pass

        self.__main_handler.display_mouse_cursor(display=True)

    def mousePressEvent(self, e: QMouseEvent):
        button = e.button()

        if button == Qt.LeftButton:
            self.player.mouse_action(0, ActionType.DOWN)
        elif button == Qt.MiddleButton:
            self.player.mouse_action(1, ActionType.PRESS)
        elif button == Qt.RightButton and self.player.has_video():
            self.__main_handler.widget_context_menu.exec_()
        elif button == Qt.BackButton:
            self.player.mouse_action(5, ActionType.PRESS)
        elif button == Qt.ForwardButton:
            self.player.mouse_action(6, ActionType.PRESS)

    def mouseReleaseEvent(self, e: QMouseEvent):
        button = e.button()

        if button == Qt.LeftButton:
            self.player.mouse_action(0, ActionType.UP)

    def mouseDoubleClickEvent(self, mev: QMouseEvent):
        button = mev.button()

        if button == Qt.LeftButton and self.player.has_video():
            self.__main_handler.toggle_fullscreen()
            self.player.mouse_action(0, ActionType.PRESS)
        elif button == Qt.MiddleButton:
            self.player.mouse_action(1, ActionType.PRESS)
        elif button == Qt.BackButton:
            self.player.mouse_action(5, ActionType.PRESS)
        elif button == Qt.ForwardButton:
            self.player.mouse_action(6, ActionType.PRESS)
        else:
            return super().mouseDoubleClickEvent(mev)

    def wheelEvent(self, e: QWheelEvent):
        delta = e.angleDelta()

        x_d = delta.x()
        y_d = delta.y()

        if x_d == 0 and y_d != 0:
            if y_d > 0:
                self.player.mouse_action(3, ActionType.PRESS)
            else:
                self.player.mouse_action(4, ActionType.PRESS)
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

        # Mpv Video widgets bindings
        elif key == Qt.Key_F and mod == Qt.NoModifier and self.player.has_video():
            self.__main_handler.toggle_fullscreen()
        elif key == Qt.Key_E and mod == Qt.NoModifier and self.player.has_video():
            self.__main_handler.widget_context_menu.exec_()
        elif key == Qt.Key_Escape and mod == Qt.NoModifier:
            if self.__main_handler.isFullScreen():
                self.__main_handler.display_normal()
            else:
                self.__main_handler.search_bar.keyPressEvent(e)
        elif key in KEY_MAPPINGS:
            cmd = command_generator(mod, *KEY_MAPPINGS[key])
        elif key != 0:
            try:
                ks = chr(key)
            except ValueError:
                pass
            else:
                cmd = command_generator(mod, ks, is_char=True)
        else:
            super(MpvWidget, self).keyPressEvent(e)

        if cmd:
            self.player.button_action(cmd, ActionType.PRESS)
