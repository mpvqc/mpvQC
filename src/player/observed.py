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

from src.gui.events import EventPlayerVideoTimeChanged, EventPlayerRemainingVideoTimeChanged, EventPlayerPercentChanged, \
    EventPlayerCurrentVideoFile, EventPlayerCurrentVideoPath, EventDistributor
from src.player.bindings import MPV

_TIME_TEMPLATE = "{}{:02d}:{:02d}"


class MpvPropertyObserver:

    def __init__(self, mpv: MPV):

        @mpv.property_observer('percent-pos')
        def observe_percent_pos(__, value):
            if value:
                EventDistributor.send_event(EventPlayerPercentChanged(round(value)))

        @mpv.property_observer('time-pos')
        def observe_time_pos(__, value):
            if value:
                EventDistributor.send_event(
                    EventPlayerVideoTimeChanged(MpvPropertyObserver.__seconds_float_to_formatted_string_hours(value)))

        @mpv.property_observer('time-remaining')
        def observe_time_remaining(__, value):
            if value:
                EventDistributor.send_event(
                    EventPlayerRemainingVideoTimeChanged(
                        MpvPropertyObserver.__seconds_float_to_formatted_string_hours(value)))

        @mpv.property_observer('filename/no-ext')
        def observe_filename(__, value):
            if value:
                EventDistributor.send_event(EventPlayerCurrentVideoFile(value))

        @mpv.property_observer('path')
        def observe_full_path(__, value):
            if value:
                EventDistributor.send_event(EventPlayerCurrentVideoPath(value))

    @staticmethod
    def __seconds_float_to_formatted_string_hours(seconds: float) -> str:
        """
        Transforms the seconds into a string of the following format **hh:mm:ss**.

        :param seconds: The seconds to transform
        :return: string representing the time
        """

        int_val = int(seconds)
        m, s = divmod(int_val, 60)
        h, m = divmod(m, 60)
        h = "{:02d}:".format(h) if h else ""

        return _TIME_TEMPLATE.format(h, m, s)
