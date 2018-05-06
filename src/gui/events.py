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

from PyQt5.QtCore import QEvent

############################################################################ Player Event Types between 1001 - 1050 ###

PlayerTimeChanged \
    = QEvent.Type(1001)

PlayerRemainingChanged \
    = QEvent.Type(1002)

PlayerPercentChanged \
    = QEvent.Type(1003)

PlayerCurrentFile \
    = QEvent.Type(1004)

PlayerCurrentPath \
    = QEvent.Type(1005)

##################################################################### Comment Table Event Types between 1051 - 1070 ###

CommentsAmountChanged \
    = QEvent.Type(1051)

CommentsUpToDate \
    = QEvent.Type(1052)


#######################################################################################################################


class EventPlayerTimeChanged(QEvent):

    def __init__(self, current_time: str):
        super().__init__(PlayerTimeChanged)
        self.__current_time: str = current_time

    @property
    def time_current(self) -> str:
        return self.__current_time


class EventPlayerTimeRemainingChanged(QEvent):

    def __init__(self, remaining_time: str):
        super().__init__(PlayerRemainingChanged)
        self.__remaining_time: str = remaining_time

    @property
    def time_remaining(self) -> str:
        return self.__remaining_time


class EventPlayerPercentChanged(QEvent):

    def __init__(self, percent: int):
        super().__init__(PlayerPercentChanged)
        self.__percent: int = percent

    @property
    def percent(self) -> int:
        return self.__percent


class EventPlayerCurrentFile(QEvent):

    def __init__(self, current_file):
        super().__init__(PlayerCurrentFile)
        self.__current_file = current_file

    @property
    def current_file(self):
        return self.__current_file


class EventPlayerCurrentPath(QEvent):

    def __init__(self, current_path):
        super().__init__(PlayerCurrentPath)
        self.__current_path = current_path

    @property
    def current_path(self):
        return self.__current_path


#######################################################################################################################

class EventCommentsAmountChanged(QEvent):

    def __init__(self, new_amount: int):
        super().__init__(CommentsAmountChanged)
        self.__new_amount: int = new_amount

    @property
    def new_amount(self) -> int:
        return self.__new_amount


class EventCommentsUpToDate(QEvent):

    def __init__(self, status: bool):
        super().__init__(CommentsUpToDate)
        self.__status: bool = status

    @property
    def status(self) -> int:
        return self.__status
