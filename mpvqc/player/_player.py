# mpvQC
#
# Copyright (C) 2020 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from PyQt5.QtCore import pyqtSignal, QObject

from ._bindings import MPV
from ._formatting import seconds_float_to_formatted_string_hours


class MpvPlayer(QObject):
    """A wrapper class for the MpvPlayer."""

    # 'percent-pos'
    sig_mpv_percent_pos = pyqtSignal(int)

    # 'time-pos' -> transformed into '00:20' or '00:20:20'
    sig_mpv_time_pos = pyqtSignal(str)

    # 'time-remaining' transformed into '00:20' or '00:20:20'
    sig_mpv_time_remaining = pyqtSignal(str)

    def __init__(self, mpv_bindings: MPV, **properties):
        super().__init__(**properties)
        self._mpv = mpv_bindings
        self.__subtitle_cache = []
        self.__observe_properties()

    def __observe_properties(self):
        self.__observe_prop_percent_pos = None
        self.__observe_prop_time_pos = None
        self.__observe_prop_time_remaining = None

        @self._mpv.property_observer('percent-pos')
        def percent_observer(_, value: float):
            if value:
                percent = int(value)
                if self.__observe_prop_percent_pos != percent:
                    self.sig_mpv_percent_pos.emit(percent)

        @self._mpv.property_observer('time-pos')
        def time_pos_observer(_, value: float):
            if value:
                time_pos: str = seconds_float_to_formatted_string_hours(value)
                if self.__observe_prop_time_pos != time_pos:
                    self.sig_mpv_time_pos.emit(time_pos)

        @self._mpv.property_observer('time-remaining')
        def time_remaining_observer(_, value: float):
            if value:
                time_remaining: str = seconds_float_to_formatted_string_hours(value)
                if self.__observe_prop_time_remaining != time_remaining:
                    self.sig_mpv_time_remaining.emit(time_remaining)

    def add_sub_files(self, sub_file):
        """
        Add sub file to current video or cache it until initialization.
        **Save to call this function before initialize(...).**
        :param sub_file: {path} The sub file to add
        """

        if self.is_video_loaded():
            self._mpv.command("sub-add", sub_file, "select")
        else:
            self.__subtitle_cache.append(sub_file)

    def button_action(self, key_string, action_type):
        """
        Will invoke the button action for the given arguments.
        :param key_string: The command to pass to the player
        :param action_type: The action type to invoke.
        """

        self._mpv.command(action_type.value, key_string)

    def duration(self):
        """
        Returns the duration of the current video.
        :return: a tuple (seconds [float], formatted string [string])
        """

        seconds = self._mpv.duration

        return seconds, seconds_float_to_formatted_string_hours(seconds)

    def is_paused(self):
        """
        Returns whether the player is currently paused.
        """

        return self._mpv.pause

    def is_video_loaded(self):
        """
        Returns whether the player has a video to play.
        **Save to call this function before initialize(...).**
        """

        # noinspection PyBroadException
        try:
            return bool(self.video_file_current())
        except Exception:
            return False

    def has_video(self) -> bool:
        """
        Returns whether the player has a video to play.
        """

        return bool(self.video_file_current())

    def mouse_action(self, btn_idx, action_type):
        """
        Will invoke a the mouse action for the given arguments.
        :param btn_idx: The button index (e.g. 0 for *MOUSE_BTN0*)
        :param action_type: The type of press
        """

        self._mpv.command(action_type.value, "MOUSE_BTN" + str(btn_idx))

    def mouse_move(self, x, y):
        """
        Command for the mouse move.
        :param x: Amount to move -> x
        :param y: Amount to move -> y
        """

        self._mpv.command("mouse", x, y)

    def open_url(self, url, play):
        """
        Opens the given url and if selected starts playing.
        :param url: The url to open
        :param play: True if start playing immediately, False else.
        """

        self._mpv.command("loadfile", url, "replace")
        self.__load_subtitle_files()

        if play:
            self.play()

    def open_video(self, video, play=True):
        """
        Opens the given path and if selected starts playing.
        :param video: The video to open
        :param play: If True, will start playing immediately
        """

        self._mpv.command("loadfile", video, "replace")
        self.__load_subtitle_files()

        if play:
            self.play()

    def pause(self):
        """
        Will pause the current file.
        """

        self._mpv.pause = True

    def play(self):
        """
        Will start playing the current file.
        """

        self._mpv.pause = False

    def play_pause(self):
        """
        Will toggle play/pause the current file.
        """

        self._mpv.pause = not self._mpv.pause

    def position_current(self):
        """
        Will return the current time as tuple (seconds, string representation)
        or (None, None) if no video is currently loaded.
        **TIME_FORMAT = "hh:mm:ss"**
        :return: the current time as tuple (seconds, string representation) or (None, None)
        """

        position = self._mpv.time_pos

        if position is None:
            return None, None

        return position, seconds_float_to_formatted_string_hours(position, short=False)

    def position_jump(self, position):
        """
        Will jump to the given time position.
        :param position: The time in the following format: **"hh:mm:ss"**
        """

        if self.is_video_loaded():
            self._mpv.command("seek", position, "absolute+exact")

    def terminate(self):
        """
        Will close the player.
        """

        self._mpv.terminate()

    def video_file_current(self):
        """
        Access to the current file.
        :return: The current file of the player.
        """

        return self._mpv.path

    def video_height(self):
        """
        Access the video size height.
        :return: The height of the video or 0 if no video is currently loaded.
        """

        if self.is_video_loaded() and self._mpv.height is not None:
            return int(self._mpv.height)
        return 0

    def video_width(self):
        """
        Access the video size width.
        :return: The width of the video or 0 if no video is currently loaded.
        """

        if self.is_video_loaded() and self._mpv.width is not None:
            return int(self._mpv.width)
        return 0

    def version_mpv(self):
        """
        Returns the underlying version
        :return: The mpv version
        """

        return self._mpv.mpv_version

    def version_ffmpeg(self):
        """
        Returns the used ffmpeg version.
        :return: The ffmpeg version
        """

        return self._mpv.ffmpeg_version

    def __load_subtitle_files(self):
        for subtitle in self.__subtitle_cache:
            self.add_sub_files(subtitle)
        self.__subtitle_cache.clear()
