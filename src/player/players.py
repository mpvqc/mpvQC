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
from os import path

from PyQt5.QtCore import QTime

from src.gui import TIME_FORMAT
from src.player.bindings import MPV


class ActionType(Enum):
    """
    Action types for the MpvPlayer.
    """

    PRESS = "keypress"
    DOWN = "keydown"
    UP = "keyup"


class MpvPlayer:
    """
    A wrapper class for the MpvPlayer.
    """

    def __init__(self, mpv_player: MPV):
        self.__mpv = mpv_player
        self.pause()

        self.__time_format_string = TIME_FORMAT

    def add_sub_files(self, sub_file: path) -> None:
        """
        Add sub file to current video.

        :param sub_file: The sub file to add
        """

        self.__mpv.command("sub-add", sub_file, "select")

    def button_action(self, key_string, action_type: ActionType) -> None:
        """
        Will invoke the button action for the given arguments.

        :param key_string: The command to pass to the player
        :param action_type: The action type to invoke.
        """

        self.__mpv.command(action_type.value, key_string)

    def is_paused(self) -> bool:
        """
        Returns whether the player is currently paused.
        """

        return self.__mpv.pause

    def has_video(self) -> bool:
        """
        Returns whether the player has a video to play.
        """

        return bool(self.video_file_current())

    def mouse_action(self, btn_idx: int, action_type: ActionType) -> None:
        """
        Will invoke a the mouse action for the given arguments.

        :param btn_idx: The button index (e.g. 0 for *MOUSE_BTN0*)
        :param action_type: The type of press
        """

        self.__mpv.command(action_type.value, "MOUSE_BTN" + str(btn_idx))

    def mouse_move(self, x, y) -> None:
        """
        Command for the mouse move.

        :param x: Amount to move -> x
        :param y: Amount to move -> y
        """

        self.__mpv.command("mouse", x, y)

    def open_url(self, url, play: bool) -> None:
        """
        Opens the given url and if selected starts playing.

        :param url: The url to open
        :param play: True if start playing immediately, False else.
        """

        self.__mpv.command("loadfile", url, "replace")

        if play:
            self.play()

    def open_video(self, video: path, play: bool) -> None:
        """
        Opens the given path and if selected starts playing.

        :param video: The video to open
        :param play: If True, will start playing immediately
        """

        self.__mpv.command("loadfile", video, "replace")
        if play:
            self.play()

    def pause(self) -> None:
        """
        Will pause the current file.
        """

        self.__mpv.pause = True

    def play(self) -> None:
        """
        Will start playing the current file.
        """

        self.__mpv.pause = False

    def play_pause(self) -> None:
        """
        Will toggle play/pause the current file.
        """

        self.__mpv.pause = not self.__mpv.pause

    def position_current(self) -> str or None:
        """
        Will return the current time as string representation or None if no video is currently loaded.

        **TIME_FORMAT = "hh:mm:ss"**
        :return: the current time as string representation or None
        """

        position = self.__mpv.time_pos

        if position is None:
            return None

        return QTime(0, 0, 0, 0).addSecs(int(position)).toString(self.__time_format_string)

    def position_jump(self, position: str) -> None:
        """
        Will jump to the given time position.

        :param position: The time in the following format: **"hh:mm:ss"**
        """

        if self.has_video():
            self.__mpv.command("seek", QTime.fromString(position, self.__time_format_string).toPyTime(),
                               "absolute+exact")

    def terminate(self) -> None:
        """
        Will close the player.
        """

        self.__mpv.terminate()

    def video_file_current(self) -> path or None:
        """
        Access to the current file.

        :return: The current file of the player.
        """

        return self.__mpv.path

    def video_height(self) -> int:
        """
        Access the video size height.

        :return: The height of the video or 0 if no video is currently loaded.
        """

        try:
            return int(self.__mpv.height)
        except TypeError:
            return 0

    def video_width(self) -> int:
        """
        Access the video size width.

        :return: The width of the video or 0 if no video is currently loaded.
        """

        try:
            return int(self.__mpv.width)
        except TypeError:
            return 0

    def version_mpv(self) -> str:
        """
        Returns the underlying version

        :return: The mpv version
        """

        return self.__mpv.mpv_version

    def ffmpeg_version(self) -> str:
        """
        Returns the used ffmpeg version.

        :return: The ffmpeg version
        """

        return self.__mpv.ffmpeg_version
