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


from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QStatusBar, QLabel

from src import settings, events


class _TimeLabel(QLabel):

    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignRight)

        self.__time_format = settings.Setting_Internal_STATUS_BAR_TIME_MODE

        self._percent = 0
        self.current_time = "00:00"
        self.remaining_time = "00:00"
        self.__update()

    def __update(self) -> None:
        """
        Will update the current status bar information about video time and comments
        """

        time = self.current_time if self.__time_format.value else "-{}".format(self.remaining_time)
        percent = self._percent
        self.setText("{percent:3}%{time:>{padding}}".format(percent=percent, padding=15, time=time))

    def customEvent(self, event: QEvent) -> None:
        ev_type = event.type()

        if ev_type == events.PlayerVideoTimeChanged:
            event: events.EventPlayerVideoTimeChanged
            current_time = event.time_current
            if self.current_time != current_time:
                self.current_time = current_time
                self.__update()

        elif ev_type == events.PlayerRemainingVideoTimeChanged:
            event: events.EventPlayerRemainingVideoTimeChanged
            self.remaining_time = event.time_remaining

        elif ev_type == events.PlayerPercentChanged:
            event: events.EventPlayerPercentChanged
            percent = event.percent
            if self._percent != percent:
                self._percent = percent
                self.__update()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.__time_format.value = not self.__time_format.value
            self.__update()
            event.accept()


class StatusBar(QStatusBar):

    def __init__(self):
        super().__init__()
        self.__comments_amount: int = 0
        self.__comments_current_selection: int = -1

        self.__label_information = _TimeLabel()
        self.__label_comment_selection_slash_amount = QLabel()

        self.addPermanentWidget(self.__label_comment_selection_slash_amount, 0)
        self.addPermanentWidget(QLabel(), 1)
        self.addPermanentWidget(self.__label_information, 0)

    def __update_comment_amount_slash_selection(self):
        if self.__comments_current_selection >= 0:
            self.__label_comment_selection_slash_amount.setText(
                "{current}/{total}".format(current=self.__comments_current_selection + 1, total=self.__comments_amount)
            )
        else:
            self.__label_comment_selection_slash_amount.setText("")

    def customEvent(self, ev: QEvent):
        self.__label_information.customEvent(ev)

        ev_type = ev.type()

        if ev_type == events.CommentAmountChanged:
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

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        previous_widget = self.previousInFocusChain()
        self.setFocus()
        previous_widget.setFocus()
