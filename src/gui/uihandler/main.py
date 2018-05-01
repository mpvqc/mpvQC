# noinspection PyMethodMayBeStatic
import gettext
import inspect
from os import path

from PyQt5.QtCore import QTranslator, Qt, QCoreApplication, QByteArray
from PyQt5.QtGui import QShowEvent, QCursor, QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QApplication

from src.gui.messageboxes import OpenVideoFileDialog, QuitNotSavedQMessageBox, NewQCDocumentOldNotSavedQMessageBox, \
    SaveAsFileDialog
from src.gui.uielements.main import Ui_MainWindow

_translate = QCoreApplication.translate


class MainHandler(QMainWindow):

    def __init__(self, application: QApplication):
        super(MainHandler, self).__init__()
        self.action = MenuBarActionDelegate(self)
        self.application = application

        # User interface setup
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.__setup_menu_bar()

        # Translator
        self.translator = QTranslator()
        self.reload_ui_language()

        # Widgets
        from src.gui.widgets import CommentsTable, StatusBar, MpvWidget, ContextMenu

        self.widget_mpv = MpvWidget(self)
        self.widget_comments = CommentsTable(self)
        self.widget_status_bar = StatusBar(self)
        self.widget_context_menu = ContextMenu(self)
        self.player = self.widget_mpv.mpv_player

        self.setStatusBar(self.widget_status_bar)
        self.ui.splitter.insertWidget(0, self.widget_comments)
        self.ui.splitter.insertWidget(0, self.widget_mpv)

        # Class variables
        from src.qcutils import QualityCheck
        self.current_geometry: QByteArray = None
        self.qualityCheck = QualityCheck(self)
        self.menubar_height = None

    def __setup_menu_bar(self):
        """
        Binds the menubar to the MenuBarActionHandler.
        """

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
        self.menubar_height = self.menuBar().height()
        self.widget_comments.on_before_fullscreen()

        self.widget_comments.hide()
        self.widget_status_bar.hide()
        # Needed because otherwise no shortcuts would work in fullscreen mode
        self.ui.menuBar.setMaximumHeight(0)
        self.display_mouse_cursor(display=True)

        self.showFullScreen()

    def hide_fullscreen(self) -> None:
        """
        Will restore the default view.
        """

        self.showNormal()

        self.widget_comments.show()
        self.widget_status_bar.show()
        self.ui.menuBar.setMaximumHeight(self.menubar_height)
        self.display_mouse_cursor(display=True)

        self.restoreGeometry(self.current_geometry)
        self.widget_comments.on_after_fullscreen()

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
        Settings.Holder.COMMENT_TYPES.update()

    def action_new_qc_document(self):

        def open_new_one():
            from src.qcutils import QualityCheck
            self.widget_comments.reset_comments_table()
            self.qualityCheck = QualityCheck(self)

        if self.qualityCheck.should_save():
            if NewQCDocumentOldNotSavedQMessageBox().exec_():
                open_new_one()
        else:
            open_new_one()

    def action_open_qc_document(self):
        pass

    def action_save_qc_document(self):
        if bool(self.qualityCheck.path_document):
            self.qualityCheck.save()
        else:
            self.action_save_qc_document_as()

    def action_save_qc_document_as(self):
        from src.settings import Settings
        qc = self.qualityCheck
        current_path = qc.path_document

        def save_with(file: path):
            qc.path_document = file
            qc.save()

        if bool(current_path) and path.isfile(current_path):
            save_with(current_path)
        else:
            new_path = SaveAsFileDialog.get_save_file_name(self.widget_mpv.mpv_player.video_file_current(),
                                                           Settings.Holder.NICKNAME.value, self)
            if new_path:
                save_with(new_path)

    def action_open_video(self, file: path):
        if path.isfile(file):
            from src.settings import Settings
            setting = Settings
            setting.Holder.PLAYER_LAST_PLAYED_DIR.value = path.dirname(file)
            setting.save()
            self.widget_mpv.mpv_player.open_video(file, play=True)

    def action_close(self) -> None:
        """
        Emits a close event.
        Continue to read with *closeEvent()*.
        """

        self.close()

    def closeEvent(self, cev: QCloseEvent):

        if self.qualityCheck.should_save():
            self.widget_mpv.mpv_player.pause()
            if QuitNotSavedQMessageBox().exec_():
                self.close()
            else:
                cev.ignore()
        else:
            super().closeEvent(cev)


class MenuBarActionDelegate:

    def __init__(self, main_handler: MainHandler):
        self.widget = main_handler

    def on_pressed_new_qc_document(self) -> None:
        self.widget.action_new_qc_document()

    def on_pressed_open_qc_document(self) -> None:
        self.widget.action_open_qc_document()

    def on_pressed_save_qc_document(self) -> None:
        self.widget.action_save_qc_document()

    def on_pressed_save_qc_document_as(self) -> None:
        self.widget.action_save_qc_document_as()

    def on_pressed_exit(self) -> None:
        self.widget.action_close()

    def on_pressed_open_video(self) -> None:
        """
        When user hits Video -> Open Video ...
        """

        from src.settings import Settings
        file = OpenVideoFileDialog.get_open_file_name(directory=Settings.Holder.PLAYER_LAST_PLAYED_DIR.value)
        self.widget.action_open_video(file)

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
        was_paused_by_user = player.is_paused()
        player.pause()

        dialog = PreferenceHandler()
        dialog.exec_()

        # After dialog closed
        if not was_paused_by_user:
            player.play()

        self.widget.reload_ui_language()
        self.widget.widget_context_menu.update_entries()

    def on_pressed_check_for_update(self) -> None:
        print(inspect.stack()[0][3])

    def on_pressed_about_qt(self) -> None:
        print(inspect.stack()[0][3])

    def on_pressed_about_mpvqc(self) -> None:
        print(inspect.stack()[0][3])
