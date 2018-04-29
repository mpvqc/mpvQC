# noinspection PyMethodMayBeStatic
import gettext
import inspect
from os import path

from PyQt5.QtCore import QTranslator, Qt, QCoreApplication, QByteArray
from PyQt5.QtGui import QShowEvent, QCursor
from PyQt5.QtWidgets import QMainWindow, QApplication

from src.gui.dialogs import OpenVideoFileDialog
from src.gui.uielements.main import Ui_MainWindow

_translate = QCoreApplication.translate


class MainHandler(QMainWindow):

    def __init__(self, application: QApplication):
        super(MainHandler, self).__init__()
        self.action = MenuBarActionHandler(self)
        self.application = application

        # User interface setup
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.__setup_menu_bar()

        # Translator
        self.translator = QTranslator()
        self.reload_ui_language()

        # Widgets
        from src.gui.widgets import CommentsWidget, CustomStatusBar, MpvWidget, CustomContextMenu

        self.widget_mpv = MpvWidget(self)
        self.widget_comments = CommentsWidget(self)
        self.widget_status_bar = CustomStatusBar(self)
        self.widget_context_menu = CustomContextMenu(self)
        self.player = self.widget_mpv.mpv_player

        self.setStatusBar(self.widget_status_bar)
        self.ui.splitter.insertWidget(0, self.widget_comments)
        self.ui.splitter.insertWidget(0, self.widget_mpv)

        # Class variables
        self.current_geometry: QByteArray = None

    def __setup_menu_bar(self):
        """Binds the menubar to the """

        self.ui.actionNew_QC_Document.triggered.connect(lambda c, f=self.action.on_pressed_new_qc_document: f())
        self.ui.action_Open_QC_Document.triggered.connect(lambda c, f=self.action.on_pressed_open_qc_document: f())
        self.ui.action_Save_QC_Document.triggered.connect(lambda c, f=self.action.on_pressed_save_qc_document: f())
        self.ui.actionS_ave_QC_Document_As.triggered.connect(
            lambda c, f=self.action.on_pressed_save_qc_document_as: f())
        self.ui.action_Exit_mpvQC.triggered.connect(lambda c, f=self.action.on_pressed_exit: f())

        self.ui.action_Open_Video_File.triggered.connect(lambda c, f=self.action.on_pressed_open_video: f())
        self.ui.actionOpen_Network_Stream.triggered.connect(
            lambda c, f=self.action.on_pressed_open_network_stream: f())
        self.ui.action_Resize_Video_To_Its_Original_Resolutio.triggered.connect(
            lambda c, f=self.action.on_pressed_resize_video: f())

        self.ui.action_Settings.triggered.connect(lambda c, f=self.action.on_pressed_settings: f())
        self.ui.action_Check_For_Updates.triggered.connect(
            lambda c, f=self.action.on_pressed_check_for_update: f())
        self.ui.actionAbout_Qt.triggered.connect(lambda c, f=self.action.on_pressed_about_qt: f())
        self.ui.actionAbout_mpvqc.triggered.connect(lambda c, f=self.action.on_pressed_about_mpvqc: f())

    def toggle_fullscreen(self):
        """
        Will toggle the fullscreen mode.
        """

        if self.isFullScreen():
            self.hide_fullscreen()
        else:
            self.display_fullscreen()

    def display_fullscreen(self) -> None:
        """
        Will show the video in fullscreen.
        """

        self.current_geometry: QByteArray = self.saveGeometry()

        self.widget_comments.hide()
        self.widget_status_bar.hide()
        self.ui.menuBar.hide()
        self.display_mouse_cursor(display=True)

        self.showFullScreen()

    def hide_fullscreen(self) -> None:
        """
        Will restore the default view.
        """

        self.showNormal()

        self.widget_comments.show()
        self.widget_status_bar.show()
        self.ui.menuBar.show()
        self.display_mouse_cursor(display=True)

        self.restoreGeometry(self.current_geometry)

    def display_mouse_cursor(self, display: bool) -> None:
        """
        Will display the mouse cursor.
        :param display: True if display mouse cursor, False if hide mouse cursor
        """

        if display:
            this_app = self.application

            while this_app.overrideCursor():
                this_app.restoreOverrideCursor()

            self.widget_mpv.cursor_timer.start(1000)
        else:
            if self.isFullScreen():
                self.application.setOverrideCursor(QCursor(Qt.BlankCursor))

    def showEvent(self, sev: QShowEvent) -> None:
        print(inspect.stack()[0][3])

    def reload_ui_language(self) -> None:
        """
        Reloads the user interface language.
        It uses the language stored in the current settings.json.
        """

        self.application.removeTranslator(self.translator)

        from src.files import Files
        from src.settings import Settings

        _locale_structure = path.join(Files.DIRECTORY_PROGRAM, "locale", "{}", "LC_MESSAGES")
        language: str = Settings.Holder.LANGUAGE.value

        if language.startswith("German"):
            value = "de"
        else:
            value = "en"

        trans_dir = _locale_structure.format(value)
        trans_present = path.isdir(trans_dir)

        if trans_present:
            directory = path.join(Files.DIRECTORY_PROGRAM, "locale")
            gettext.translation(domain="ui_transmo", localedir=directory, languages=['de', 'en']).install()
            self.translator.load("ui_trans", trans_dir)
        else:
            self.translator.load("ui_trans", _locale_structure.format("en"))

        self.application.installTranslator(self.translator)
        self.ui.retranslateUi(self)


class MenuBarActionHandler:

    def __init__(self, main_handler: MainHandler):
        self.widget = main_handler

    def on_pressed_new_qc_document(self) -> None:
        print(inspect.stack()[0][3])

    def on_pressed_open_qc_document(self) -> None:
        print(inspect.stack()[0][3])

    def on_pressed_save_qc_document(self) -> None:
        print(inspect.stack()[0][3])

    def on_pressed_save_qc_document_as(self) -> None:
        print(inspect.stack()[0][3])

    def on_pressed_exit(self) -> None:
        print(inspect.stack()[0][3])

    def on_pressed_open_video(self) -> None:
        """
        When user hits Video -> Open Video ...
        """

        from src import settings

        setting = settings.Settings
        file = OpenVideoFileDialog.get_open_file_name(directory=setting.Holder.PLAYER_LAST_PLAYED_DIR.value)

        if path.isfile(file):
            setting.Holder.PLAYER_LAST_PLAYED_DIR.value = path.dirname(file)
            setting.save()
            self.widget.widget_mpv.mpv_player.open_video(file, play=True)

    def on_pressed_open_network_stream(self) -> None:
        print(inspect.stack()[0][3])

    def on_pressed_resize_video(self) -> None:
        print(inspect.stack()[0][3])

    def on_pressed_settings(self) -> None:
        """
        When user hits Options -> Settings.
        """

        from src.gui.uihandler.preferences import PreferenceHandler

        player = self.widget.widget_mpv.mpv_player
        player.pause()

        dialog = PreferenceHandler()
        dialog.exec_()

        # After dialog closed
        if player.is_paused():
            player.play()
        self.widget.reload_ui_language()
        self.widget.widget_context_menu.update_entries()

    def on_pressed_check_for_update(self) -> None:
        print(inspect.stack()[0][3])

    def on_pressed_about_qt(self) -> None:
        print(inspect.stack()[0][3])

    def on_pressed_about_mpvqc(self) -> None:
        print(inspect.stack()[0][3])
