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


from typing import Dict

from ._bindings import MPV
from ._observed import MpvPropertyObserver


def _seconds_float_to_formatted_string_hours(seconds: float, short=True) -> str:
    """
    Transforms the seconds into a string of the following format **hh:mm:ss**.
    :param short: If True "mm:ss" will be returned, else "HH:mm:ss"
    :param seconds: The seconds to transform
    :return: string representing the time
    """

    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    h = "{:02d}:".format(h) if h else ("" if short else "00:")

    return "{}{:02d}:{:02d}".format(h, m, s)


class _Observer:
    """
    Class which allows to subscribe to mpv properties.

    Usage::

        mpv = MpvPlayer()
        mpv.connect('time-pos', print)
        mpv.connect('time-remaining', self.some_func)
        mpv.disconnect('time-pos', print)
        mpv.disconnect('time-remaining', self.some_func)
    """

    class MpvPropertyObserver:
        def __init__(self, mpv_property_id):
            self.__id = mpv_property_id
            self.__callbacks = []
            self.__registered = False

        def add_callback(self, callback):
            self.__callbacks.append(callback)

        def remove_callback(self, callback):
            self.__callbacks.remove(callback)

        def mpv_register(self, mpv: MPV):
            if not self.__registered and self.__callbacks:
                self.__registered = True
                mpv.observe_property(self.__id, self.on_property_changed)

        def mpv_unregister(self, mpv: MPV):
            if self.__registered and not self.__callbacks:
                self.__registered = False
                mpv.unobserve_property(self.__id, self.on_property_changed)

        def on_property_changed(self, _, value):
            if value and self.__callbacks:
                for cb in self.__callbacks:
                    cb(self.__id, value)

    def __init__(self, **properties):
        super().__init__(**properties)

        # noinspection PyTypeChecker
        self._mpv: MPV = None

        self._observers: Dict[str, _Observer.MpvPropertyObserver] = {}

    def connect(self, mpv_property: str, handler):
        """
        Connects a handler to a mpv property.
        Run 'man mpv > manual.txt' for a complete guide of all available properties.
        **Save to call this function before initialize(...).**
        :param mpv_property: e.g. 'time-pos'
        :param handler: a function which then will be called every time mpv_property changes
        """

        observer = self._observers.get(mpv_property, None)
        if observer is None:
            observer = _Observer.MpvPropertyObserver(mpv_property)
            self._observers[mpv_property] = observer
        observer.add_callback(handler)

        if self._mpv:
            observer.mpv_register(self._mpv)

    def disconnect(self, mpv_property: str, handler):
        """
        Connects a handler from a mpv property.
        **Save to call this function before initialize(...).**
        :param mpv_property: the property (e.g. 'time-pos') the handler has subscribed
        :param handler: the previous registered handler
        """

        observer = self._observers[mpv_property]
        observer.remove_callback(handler)
        observer.mpv_unregister(self._mpv)

    def initialize(self, mpv_bindings: MPV):
        """
        Initializes the player and registers all unregistered observers.
        """

        self._mpv = mpv_bindings

        for observer in self._observers.values():
            observer.mpv_register(self._mpv)


class MpvPlayer(_Observer):
    """
    A wrapper class for the MpvPlayer.
    Unless otherwise stated all function require 'initialize(...)' to be called at
    the initialization of the low level mpv bindings.
    """

    def __init__(self, **properties):
        super().__init__(**properties)

        self.__subtitle_cache = []

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

        return seconds, _seconds_float_to_formatted_string_hours(seconds)

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

        return position, _seconds_float_to_formatted_string_hours(position, short=False)

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
