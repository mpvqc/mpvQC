from PyQt5 import QtCore

from src import settings
from src.player.bindings import MPV

_translate = QtCore.QCoreApplication.translate

TIME_TEMPLATE = "{}{:02d}:{:02d}"


class MpvPropertyObserver:
    VIDEO_PERCENT: float = 0
    VIDEO_TIME_CURRENT: str = "00:00"
    VIDEO_TIME_REMAINING: str = "42:42"

    VIDEO_FILE = ""
    VIDEO_PATH = ""

    def __init__(self, mpv: MPV):

        @mpv.property_observer('percent-pos')
        def observe_percent_pos(__, value):
            if value and settings.Setting_Custom_Appearance_StatusBar_Percentage.value:
                MpvPropertyObserver.VIDEO_PERCENT = round(value)

        @mpv.property_observer('time-pos')
        def observe_time_pos(__, value):
            if value and settings.Setting_Custom_Appearance_StatusBar_CurrentTime.value:
                MpvPropertyObserver.VIDEO_TIME_CURRENT \
                    = MpvPropertyObserver.__seconds_float_to_formatted_string_hours(value)

        @mpv.property_observer('time-remaining')
        def observe_time_remaining(__, value):
            if value and not settings.Setting_Custom_Appearance_StatusBar_CurrentTime.value:
                MpvPropertyObserver.VIDEO_TIME_REMAINING \
                    = MpvPropertyObserver.__seconds_float_to_formatted_string_hours(value)

        @mpv.property_observer('filename/no-ext')
        def observe_filename(__, value):
            if value:
                MpvPropertyObserver.VIDEO_FILE = value

        @mpv.property_observer('path')
        def observe_full_path(__, value):
            if value:
                MpvPropertyObserver.VIDEO_PATH = value

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

        return TIME_TEMPLATE.format(h, m, s)
