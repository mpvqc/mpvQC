from os import path

from PyQt5 import QtCore, QtGui

from src.player.bindings import MPV

_tr = QtCore.QCoreApplication.translate


class MpvPlayer:
    """A wrapper class for the MpvPlayer. """

    def __init__(self, mpv_player: MPV):
        self.mpv = mpv_player

    def is_playing(self) -> bool:
        """Returns whether the player is currently playing."""

        return self.mpv.pause

    def play(self) -> None:
        """Will start playing the current file."""

        self.mpv.pause = False

    def pause(self) -> None:
        """Will pause the current file."""

        self.mpv.pause = True

    def play_pause(self) -> None:
        """Will toggle play/pause the current file."""

        self.mpv.pause = not self.mpv.pause

    def open_video(self, video: path, play: bool) -> None:
        """Opens the given path and if selected starts playing."""

        self.mpv.command("loadfile", video, "replace")
        if play:
            self.play()

