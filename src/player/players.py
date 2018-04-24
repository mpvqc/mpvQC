from enum import Enum
from os import path

from PyQt5 import QtCore

from src.player.bindings import MPV

_tr = QtCore.QCoreApplication.translate


class ActionType(Enum):
    PRESS = "keypress"
    DOWN = "keydown"
    UP = "keyup"


class MpvPlayer:
    """A wrapper class for the MpvPlayer. """

    def __init__(self, mpv_player: MPV):
        self.mpv = mpv_player

    def is_playing(self) -> bool:
        """Returns whether the player is currently playing."""

        print(self.mpv.pause)
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

    def mouse_move(self, x, y):
        """Command for the mouse move. """

        self.mpv.command("mouse", x, y)

    def mouse_action(self, btn_idx: int, action_type: ActionType):


        if action_type == ActionType.PRESS:
            ac_ty = "keypress"
        elif action_type == ActionType.DOWN:
            ac_ty = "keydown"
        else:
            ac_ty = "keyup"
        print(ac_ty, btn_idx)

        self.mpv.command(ac_ty, "MOUSE_BTN" + str(btn_idx))
