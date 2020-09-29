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


from enum import Enum
from typing import Tuple

from PyQt5.QtCore import QEvent, QObject
from PyQt5.QtWidgets import QApplication


class EventReceiver(Enum):
    MAIN_HANDLER = 0
    WIDGET_MPV = 1
    WIDGET_COMMENTS = 2
    WIDGET_CONTEXT_MENU = 3
    WIDGET_STATUS_BAR = 4
    QC_MANAGER = 5


class EventDistributor:
    __CustomEventReceiver: dict = {}

    @staticmethod
    def add_receiver(*receivers: Tuple[QObject, EventReceiver]) -> None:
        """
        Will add a QWidget as custom event receiver. If the same receiver already exists it will be overwritten.

        :Example:

        >>> EventDistributor.add_receiver(
        >>>     (widget_main_handler, EventReceiver.MAIN_HANDLER),
        >>>     (widget_qc_manager, EventReceiver.QC_MANAGER)
        >>> )

        :param receivers: A tuple of QWidget and the enum entry EventReceiver.
        """

        for receiver_tuple in receivers:
            receiver = receiver_tuple[0]
            identifier = receiver_tuple[1]
            EventDistributor.__CustomEventReceiver[identifier] = receiver

    @staticmethod
    def send_event(event: QEvent, *receivers: EventReceiver) -> None:
        """
        Will send the given event to the given receivers.

        :Example:

        >>> EventDistributor.send_event(event, EventReceiver.MAIN_HANDLER, EventReceiver.QC_MANAGER)

        :param event: The event to distribute
        :param receivers: The receiver to receive the event. If no receiver is given, the event will be send to all existing receivers.
        """

        for receiver in receivers:
            target = EventDistributor.__CustomEventReceiver.get(receiver, None)
            if target is None:
                print(str(EventReceiver(receiver[1]).name), "is currently not added as receiver yet!")
            else:
                QApplication.sendEvent(target, event)
        else:
            for identifier, receiver in EventDistributor.__CustomEventReceiver.items():
                QApplication.sendEvent(receiver, event)


############################################################################ Player Event Types between 1001 - 1050 ###

PlayerVideoTimeChanged \
    = QEvent.Type(1001)

PlayerRemainingVideoTimeChanged \
    = QEvent.Type(1002)

PlayerPercentChanged \
    = QEvent.Type(1003)

##################################################################### Comment Table Event Types between 1051 - 1070 ###

CommentAmountChanged \
    = QEvent.Type(1051)

CommentCurrentSelectionChanged \
    = QEvent.Type(1052)

#######################################################################################################################


class EventPlayerVideoTimeChanged(QEvent):

    def __init__(self, current_time: str):
        super().__init__(PlayerVideoTimeChanged)
        self.__current_time: str = current_time

    @property
    def time_current(self) -> str:
        return self.__current_time


class EventPlayerRemainingVideoTimeChanged(QEvent):

    def __init__(self, remaining_time: str):
        super().__init__(PlayerRemainingVideoTimeChanged)
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


#######################################################################################################################

class EventCommentAmountChanged(QEvent):

    def __init__(self, new_amount: int):
        super().__init__(CommentAmountChanged)
        self.__new_amount: int = new_amount

    @property
    def new_amount(self) -> int:
        return self.__new_amount


class EventCommentCurrentSelectionChanged(QEvent):

    def __init__(self, current_selection: int):
        super().__init__(CommentCurrentSelectionChanged)
        self.__current_selection = current_selection

    @property
    def current_selection(self) -> int:
        return self.__current_selection

