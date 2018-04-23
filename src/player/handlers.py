# noinspection PyMethodMayBeStatic
import inspect
from os import path

from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog

from src.player.widgets import MpvWidget
from src.preferences import settings
from src.preferences.settings import PreferenceDialog
from tmpv import ApplicationWindow

_tr = QtCore.QCoreApplication.translate


# noinspection PyMethodMayBeStatic
class MenubarHandler:
    """Class for handling the menu bar actions."""

    def __init__(self, application: ApplicationWindow, mpv_widget: MpvWidget):
        self.application = application
        self.mpv_widget = mpv_widget

        self.config = settings.get_settings()
        self.player = mpv_widget.mpv_player

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
        """When user hits Video -> Open Video ..."""
        file = QFileDialog.getOpenFileName(
            parent=self.mpv_widget.parent(),
            caption=_tr("Misc", "Open Video File"),
            directory=self.config.player_last_played_dir.value,
            filter=_tr("Misc", "Video files (*.mkv *.mp4);;All files (*.*)")
        )[0]

        if path.isfile(file):
            self.config.player_last_played_dir.value = path.dirname(file)
            self.player.open_video(file, play=True)
            self.config.save()

    def on_pressed_open_network_stream(self):
        print(inspect.stack()[0][3])

    def on_pressed_resize_video(self):
        print(inspect.stack()[0][3])

    def on_pressed_settings(self):
        """When user hits Options -> Settings."""

        self.player.pause()
        dialog = PreferenceDialog()
        dialog.exec()

        if True or dialog.exec_():
            self.on_settings_closed()

    def on_settings_closed(self):
        if self.player.is_playing():
            self.player.play()
        self.application.reload_translator()

    def on_pressed_check_for_update(self):
        print(inspect.stack()[0][3])

    def on_pressed_about_qt(self):
        print(inspect.stack()[0][3])

    def on_pressed_about_mpvqc(self):
        print(inspect.stack()[0][3])
