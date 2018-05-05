from PyQt5 import QtCore

from src.gui.events import EventPlayerTimeChanged, EventPlayerTimeRemainingChanged, EventPlayerPercentChanged, \
    EventPlayerCurrentFile, EventPlayerCurrentPath
from src.player.bindings import MPV

_TIME_TEMPLATE = "{}{:02d}:{:02d}"

_translate = QtCore.QCoreApplication.translate


class MpvPropertyObserver:

    def __init__(self, mpv: MPV):

        from src.gui.uihandler.main import MainHandler

        @mpv.property_observer('percent-pos')
        def observe_percent_pos(__, value):
            if value:
                MainHandler.send_event(EventPlayerPercentChanged(round(value)))

        @mpv.property_observer('time-pos')
        def observe_time_pos(__, value):
            if value:
                MainHandler.send_event(
                    EventPlayerTimeChanged(MpvPropertyObserver.__seconds_float_to_formatted_string_hours(value)))

        @mpv.property_observer('time-remaining')
        def observe_time_remaining(__, value):
            if value:
                MainHandler.send_event(
                    EventPlayerTimeRemainingChanged(
                        MpvPropertyObserver.__seconds_float_to_formatted_string_hours(value)))

        @mpv.property_observer('filename/no-ext')
        def observe_filename(__, value):
            if value:
                MainHandler.send_event(EventPlayerCurrentFile(value))

        @mpv.property_observer('path')
        def observe_full_path(__, value):
            if value:
                MainHandler.send_event(EventPlayerCurrentPath(value))

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
        h = "{:02d}:".format(h) if h != 0 else ""

        return _TIME_TEMPLATE.format(h, m, s)
