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


from PyQt5.QtCore import Qt, QTimer, QEvent, QObject
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QStatusBar, QLabel

from src import settings, events


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
        self.__label_information.setAlignment(Qt.AlignRight)
        self.__label_information.installEventFilter(self)

        self.__label_comment_selection_slash_amount = QLabel()

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
                "{current}/{total}".format(current=self.__comments_current_selection + 1, total=self.__comments_amount)
            )
        else:
            self.__label_comment_selection_slash_amount.setText("")

    def customEvent(self, ev: QEvent):

        ev_type = ev.type()

        if ev_type == events.PlayerVideoTimeChanged:
            ev: events.EventPlayerVideoTimeChanged
            self.__time_current = ev.time_current

        elif ev_type == events.PlayerRemainingVideoTimeChanged:
            ev: events.EventPlayerRemainingVideoTimeChanged
            self.__time_remaining = ev.time_remaining

        elif ev_type == events.PlayerPercentChanged:
            ev: events.EventPlayerPercentChanged
            self.__percent = ev.percent

        elif ev_type == events.CommentAmountChanged:
            ev: events.EventCommentAmountChanged
            self.__comments_amount = ev.new_amount
            self.__update_comment_amount_slash_selection()

        elif ev_type == events.CommentCurrentSelectionChanged:
            ev: events.EventCommentCurrentSelectionChanged
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
