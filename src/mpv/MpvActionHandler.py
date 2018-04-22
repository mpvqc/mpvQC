import inspect
from os import path

from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog

from src import configuration
# noinspection PyMethodMayBeStatic
from src.mpv.MpvWidget import MpvWidget
from src.preferences.PreferenceDialog import PreferenceDialog

_tr = QtCore.QCoreApplication.translate


# noinspection PyMethodMayBeStatic
class MpvActionHandler:

    def __init__(self, mpv_widget: MpvWidget):
        self.config = configuration.get_config()
        self.player = mpv_widget.mpv_player
        self.mpv_widget = mpv_widget

    def on_pressed_new_qc_document(self):
        print(inspect.stack()[0][3])

    def on_pressed_open_qc_document(self):
        print(inspect.stack()[0][3])

    def on_pressed_save_qc_document(self):
        print(inspect.stack()[0][3])

    def on_pressed_save_qc_document_as(self):
        print(inspect.stack()[0][3])

    def on_pressed_exit(self):
        print(inspect.stack()[0][3])

    def on_pressed_open_video(self):
        file = QFileDialog.getOpenFileName(
            parent=self.mpv_widget.parent(),
            caption=_tr("Misc", "Open Video File"),
            directory=self.config.player_last_played_directory,
            filter=_tr("Misc", "Video files (*.mkv *.mp4);;All files (*.*)")
        )[0]

        if path.isfile(file):
            self.config.player_last_played_directory = path.dirname(file)
            self.player.open_video(file, play=True)
            self.config.save()

    def on_pressed_open_network_stream(self):
        print(inspect.stack()[0][3])

    def on_pressed_resize_video(self):
        print(inspect.stack()[0][3])

    def on_pressed_settings(self):
        is_playing = self.player.is_playing()
        self.player.pause()
        dialog = PreferenceDialog()
        dialog.exec_()


        if is_playing:
            self.player.play()

    def on_pressed_check_for_update(self):
        print(inspect.stack()[0][3])

    def on_pressed_about_qt(self):
        print(inspect.stack()[0][3])

    def on_pressed_about_mpvqc(self):
        print(inspect.stack()[0][3])
