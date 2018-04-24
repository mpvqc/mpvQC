# noinspection PyMethodMayBeStatic
import inspect
from os import path

from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog

from src.player.widgets import MpvWidget
from src.preferences import settings
from src.preferences.widgets import PreferenceDialog
from tmpv import ApplicationWindow

_tr = QtCore.QCoreApplication.translate


# noinspection PyMethodMayBeStatic
class MenubarHandler:
    """Class for handling the menu bar actions."""

    def __init__(self, application: ApplicationWindow, mpv_widget: MpvWidget):
        self.application = application

        self.settings = settings.get_settings()
        self.player = mpv_widget.mpv_player

    def bind(self):
        """Binds the menubar to the """

        self.application.ui.actionNew_QC_Document.triggered.connect(lambda c, f=self.on_pressed_new_qc_document: f())
        self.application.ui.action_Open_QC_Document.triggered.connect(lambda c, f=self.on_pressed_open_qc_document: f())
        self.application.ui.action_Save_QC_Document.triggered.connect(lambda c, f=self.on_pressed_save_qc_document: f())
        self.application.ui.actionS_ave_QC_Document_As.triggered.connect(
            lambda c, f=self.on_pressed_save_qc_document_as: f())
        self.application.ui.action_Exit_mpvQC.triggered.connect(lambda c, f=self.on_pressed_exit: f())

        self.application.ui.action_Open_Video_File.triggered.connect(lambda c, f=self.on_pressed_open_video: f())
        self.application.ui.actionOpen_Network_Stream.triggered.connect(
            lambda c, f=self.on_pressed_open_network_stream: f())
        self.application.ui.action_Resize_Video_To_Its_Original_Resolutio.triggered.connect(
            lambda c, f=self.on_pressed_resize_video: f())

        self.application.ui.action_Settings.triggered.connect(lambda c, f=self.on_pressed_settings: f())
        self.application.ui.action_Check_For_Updates.triggered.connect(
            lambda c, f=self.on_pressed_check_for_update: f())
        self.application.ui.actionAbout_Qt.triggered.connect(lambda c, f=self.on_pressed_about_qt: f())
        self.application.ui.actionAbout_mpvqc.triggered.connect(lambda c, f=self.on_pressed_about_mpvqc: f())

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
            parent=self.application,
            caption=_tr("Misc", "Open Video File"),
            directory=self.settings.player_last_played.value,
            filter=_tr("Misc", "Video files (*.mkv *.mp4);;All files (*.*)")
        )[0]

        if path.isfile(file):
            self.settings.player_last_played.value = path.dirname(file)
            self.player.open_video(file, play=True)
            self.settings.save()

    def on_pressed_open_network_stream(self):
        print(inspect.stack()[0][3])

    def on_pressed_resize_video(self):
        print(inspect.stack()[0][3])

    def on_pressed_settings(self):
        """When user hits Options -> Settings."""

        self.player.pause()
        dialog = PreferenceDialog(parent=self.application)
        dialog.exec()

        # Ugly way to execute code after preference dialog was changed
        if True or dialog.exec_():
            if self.player.is_playing():
                self.player.play()
            self.application.reload_ui_language()

    def on_pressed_check_for_update(self):
        print(inspect.stack()[0][3])

    def on_pressed_about_qt(self):
        print(inspect.stack()[0][3])

    def on_pressed_about_mpvqc(self):
        print(inspect.stack()[0][3])
