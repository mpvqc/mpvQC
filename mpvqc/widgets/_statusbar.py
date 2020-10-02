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

from mpvqc import get_settings
from mpvqc.player import seconds_float_to_formatted_string_hours


class _TimeLabel(QLabel):

    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignRight)

        self.__time_format = get_settings().statusbar_time_mode

        self.__percent = 0
        self.__current_time = "00:00"
        self.__remaining_time = "00:00"
        self.__update()

    def __update(self) -> None:
        """
        Will update the current status bar information about video time and comments
        """

        time = self.__current_time if self.__time_format else "-{}".format(self.__remaining_time)
        percent = self.__percent
        self.setText("{percent:3}%{time:>{padding}}".format(percent=percent, padding=15, time=time))

    def on_value_percent_pos_changed(self, _, value: float):
        percent = int(value)
        if self.__percent != percent:
            self.__percent = percent
            self.__update()

    def on_value_time_pos_changed(self, _, value: float):
        current_time = seconds_float_to_formatted_string_hours(value)
        if self.__current_time != current_time:
            self.__current_time = current_time
            self.__update()

    def on_value_time_remaining_changed(self, _, value: float):
        self.__remaining_time = seconds_float_to_formatted_string_hours(value)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.__time_format = (self.__time_format + 1) % 2
            get_settings().statusbar_time_mode = self.__time_format
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

    def on_value_percent_pos_changed(self, _, value: float):
        self.__label_information.on_value_percent_pos_changed(_, value)

    def on_value_time_pos_changed(self, _, value: float):
        self.__label_information.on_value_time_pos_changed(_, value)

    def on_value_time_remaining_changed(self, _, value: float):
        self.__label_information.on_value_time_remaining_changed(_, value)

    def on_comment_selection_changed(self, new_selection: int):
        self.__comments_current_selection = new_selection
        self.__update_comment_amount_slash_selection()

    def on_comment_amount_changed(self, total_amount):
        self.__comments_amount = total_amount
        self.__update_comment_amount_slash_selection()

    def changeEvent(self, ev: QEvent):
        ev_type = ev.type()

        if ev_type == QEvent.LanguageChange:
            self.__update_comment_amount_slash_selection()

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        previous_widget = self.previousInFocusChain()
        self.setFocus()
        previous_widget.setFocus()
