import gettext
import inspect
import locale
import sys
from os import path

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QTranslator, Qt
from PyQt5.QtGui import QCursor, QShowEvent

from src.gui.dialogs import OpenVideoFileDialog
from src.gui.main import Ui_MainWindow
from src.player.widgets import CommentsWidget, CustomStatusBar, MpvWidget
from src.preferences import settings
from src.shared.references import References

DIRECTORY_PROGRAM = sys._MEIPASS if getattr(sys, "frozen", False) else path.dirname(path.realpath(__file__))
APPLICATION_VERSION = "0.0.1"
APPLICATION_NAME = "mpv-qc"

_translate = QtCore.QCoreApplication.translate


# todo logger


# noinspection PyMethodMayBeStatic
class ApplicationWindow(QtWidgets.QMainWindow):

    def __init__(self, application: QtWidgets.QApplication):
        super(ApplicationWindow, self).__init__()

        # References initialization
        self.references = References()
        self.references.widget_main = self
        self.references.application = application
        self.references.widget_mpv = MpvWidget(self.references)
        self.references.widget_comments = CommentsWidget(self.references)
        self.references.widget_status_bar = CustomStatusBar(self.references)
        self.references.player = self.references.widget_mpv.mpv_player

        # User interface setup
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.__setup_menu_bar()

        self.setStatusBar(self.references.widget_status_bar)
        self.ui.splitter.insertWidget(0, self.references.widget_comments)
        self.ui.splitter.insertWidget(0, self.references.widget_mpv)

        # Translator
        self.translator = QTranslator()
        self.reload_ui_language()

        # Initialize event filter
        self.__handle_application_events(handle=True)

    def toggle_fullscreen(self):
        """Will """
        if self.isFullScreen():
            self.hide_fullscreen()
        else:
            self.display_fullscreen()
        self.display_mouse_cursor(display=True)

    def display_fullscreen(self):
        self.references.widget_comments.hide()
        self.references.widget_status_bar.hide()
        self.ui.menuBar.hide()
        self.showFullScreen()

    def hide_fullscreen(self):
        self.showNormal()
        self.references.widget_comments.show()
        self.references.widget_status_bar.show()
        self.ui.menuBar.show()

    def display_mouse_cursor(self, display: bool):
        if display:
            this_app = self.references.application

            while this_app.overrideCursor():
                this_app.restoreOverrideCursor()

            self.references.widget_mpv.cursor_timer.start(1000)
        else:
            if self.isFullScreen():
                self.references.application.setOverrideCursor(QCursor(Qt.BlankCursor))

    def showEvent(self, sev: QShowEvent):
        print(inspect.stack()[0][3])

    def reload_ui_language(self):
        """
        Reloads the user interface language.
        It uses the language stored in the current settings.json.
        """
        from src.preferences.configuration import paths

        self.references.application.removeTranslator(self.translator)

        _locale_structure = path.join(paths.dir_program, "locale", "{}", "LC_MESSAGES")
        language: str = settings.settings.language.value

        if language.startswith("German"):
            value = "de"
        else:
            value = "en"

        trans_dir = _locale_structure.format(value)
        trans_present = path.isdir(trans_dir)

        if trans_present:
            directory = path.join(paths.dir_program, "locale")
            gettext.translation(domain="ui_transmo", localedir=directory, languages=['de', 'en']).install()
            self.translator.load("ui_trans", trans_dir)
        else:
            self.translator.load("ui_trans", _locale_structure.format("en"))

        self.references.application.installTranslator(self.translator)
        self.ui.retranslateUi(self)

    def __on_pressed_new_qc_document(self):
        print(inspect.stack()[0][3])

    def __on_pressed_open_qc_document(self):
        print(inspect.stack()[0][3])

    def __on_pressed_save_qc_document(self):
        print(inspect.stack()[0][3])

    def __on_pressed_save_qc_document_as(self):
        print(inspect.stack()[0][3])

    def __on_pressed_exit(self):
        print(inspect.stack()[0][3])

    def __on_pressed_open_video(self):
        """
        When user hits Video -> Open Video ...
        """

        setting = settings.settings
        file = OpenVideoFileDialog.get_open_file_name(parent=self, directory=setting.player_last_played_directory.value)

        if path.isfile(file):
            setting.player_last_played_directory.value = path.dirname(file)
            setting.save()
            self.references.player.open_video(file, play=True)

    def __on_pressed_open_network_stream(self):
        print(inspect.stack()[0][3])

    def __on_pressed_resize_video(self):
        print(inspect.stack()[0][3])

    def __on_pressed_settings(self):
        """When user hits Options -> Settings."""

        from src.preferences.widgets import PreferenceDialog

        player = self.references.player
        player.pause()

        self.__handle_application_events(handle=False)

        dialog = PreferenceDialog(self.references)
        dialog.exec()

        # Ugly way to execute code after preference dialog was closed
        if True or dialog.exec_():
            if player.is_paused():
                player.play()
            self.reload_ui_language()
            self.__handle_application_events(handle=True)

    def __on_pressed_check_for_update(self):
        print(inspect.stack()[0][3])

    def __on_pressed_about_qt(self):
        print(inspect.stack()[0][3])

    def __on_pressed_about_mpvqc(self):
        print(inspect.stack()[0][3])

    def __setup_menu_bar(self):
        """Binds the menubar to the """

        self.ui.actionNew_QC_Document.triggered.connect(lambda c, f=self.__on_pressed_new_qc_document: f())
        self.ui.action_Open_QC_Document.triggered.connect(lambda c, f=self.__on_pressed_open_qc_document: f())
        self.ui.action_Save_QC_Document.triggered.connect(lambda c, f=self.__on_pressed_save_qc_document: f())
        self.ui.actionS_ave_QC_Document_As.triggered.connect(
            lambda c, f=self.__on_pressed_save_qc_document_as: f())
        self.ui.action_Exit_mpvQC.triggered.connect(lambda c, f=self.__on_pressed_exit: f())

        self.ui.action_Open_Video_File.triggered.connect(lambda c, f=self.__on_pressed_open_video: f())
        self.ui.actionOpen_Network_Stream.triggered.connect(
            lambda c, f=self.__on_pressed_open_network_stream: f())
        self.ui.action_Resize_Video_To_Its_Original_Resolutio.triggered.connect(
            lambda c, f=self.__on_pressed_resize_video: f())

        self.ui.action_Settings.triggered.connect(lambda c, f=self.__on_pressed_settings: f())
        self.ui.action_Check_For_Updates.triggered.connect(
            lambda c, f=self.__on_pressed_check_for_update: f())
        self.ui.actionAbout_Qt.triggered.connect(lambda c, f=self.__on_pressed_about_qt: f())
        self.ui.actionAbout_mpvqc.triggered.connect(lambda c, f=self.__on_pressed_about_mpvqc: f())

    def __handle_application_events(self, handle: bool):
        """
        Will delegate all events from the
        :param handle: True if delegate to mpv widget
        """

        if handle:
            self.references.widget_comments.installEventFilter(self.references.widget_mpv)
            self.references.widget_mpv.installEventFilter(self.references.widget_mpv)

        else:
            self.references.widget_mpv.removeEventFilter(self.references.widget_mpv)
            self.references.widget_comments.removeEventFilter(self.references.widget_mpv)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    locale.setlocale(locale.LC_NUMERIC, "C")

    container = ApplicationWindow(app)
    container.show()

    sys.exit(app.exec_())
