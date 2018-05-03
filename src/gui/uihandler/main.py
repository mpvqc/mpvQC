# noinspection PyMethodMayBeStatic
import gettext
import inspect
from os import path
from typing import List

from PyQt5.QtCore import QTranslator, Qt, QCoreApplication, QByteArray
from PyQt5.QtGui import QShowEvent, QCursor, QCloseEvent, QDragEnterEvent, QDropEvent
from PyQt5.QtWidgets import QMainWindow, QApplication

from src.gui.messageboxes import OpenVideoFileDialog, QuitNotSavedQMessageBox, NewQCDocumentOldNotSavedQMessageBox, \
    LoadQCDocumentOldNotSavedQMessageBox, OpenQcFileDialog, ValidVideoFileFoundQMessageBox, \
    WhatToDoWithExistingCommentsInTableWhenOpeningNewQCDocument
from src.gui.uielements.main import Ui_MainWindow

_translate = QCoreApplication.translate
_DROPABLE_SUBS = ("ass", "ssa", "srt", "sup", "idx", "utf", "utf8", "utf-8", "smi", "rt", "aqt", "jss", "js",
                  "mks", "vtt", "sub", "scc")
_DROPABLE_VIDS = ("mp4", "mkv", "avi")


class MainHandler(QMainWindow):

    def __init__(self, application: QApplication):
        super(MainHandler, self).__init__()
        self.application = application
        self.setAcceptDrops(True)

        # User interface setup
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.__setup_menu_bar()

        # Translator
        self.translator = QTranslator()
        self.reload_ui_language()

        # Widgets
        from src.gui.widgets import CommentsTable, StatusBar, MpvWidget, ContextMenu

        self.widget_status_bar = StatusBar(self)
        self.widget_mpv = MpvWidget(self)
        self.widget_comments = CommentsTable(self)
        self.widget_context_menu = ContextMenu(self)
        self.player = self.widget_mpv.mpv_player

        self.setStatusBar(self.widget_status_bar)
        self.ui.splitter.insertWidget(0, self.widget_comments)
        self.ui.splitter.insertWidget(0, self.widget_mpv)

        # Settings for main window relevant observed properties
        self.main_window_title_setting: int = 2  # 0 -> Nothing, 1 -> File only , 2 -> Full path todo document

        # Class variables
        from src.qcutils import QualityCheckManager
        self.current_geometry: QByteArray = None
        self.menubar_height = None
        self.qc_manager = QualityCheckManager(self)

    def __setup_menu_bar(self) -> None:
        """
        Binds the menubar to the their actions.
        """

        self.ui.actionNew_QC_Document.triggered.connect(lambda c, f=self.action_new_qc_document: f())
        self.ui.action_Open_QC_Document.triggered.connect(lambda c, f=self.action_open_qc_document: f())
        self.ui.action_Save_QC_Document.triggered.connect(lambda c, f=self.action_save_qc_document: f())
        self.ui.actionS_ave_QC_Document_As.triggered.connect(lambda c, f=self.action_save_qc_document_as: f())
        self.ui.action_Exit_mpvQC.triggered.connect(lambda c, f=self.action_close: f())

        self.ui.action_Open_Video_File.triggered.connect(lambda c, f=self.action_open_video: f())
        self.ui.actionOpen_Network_Stream.triggered.connect(lambda c, f=self.action_open_network_stream: f())
        self.ui.action_Resize_Video_To_Its_Original_Resolutio.triggered.connect(
            lambda c, f=self.action_resize_video: f())

        self.ui.action_Settings.triggered.connect(lambda c, f=self.action_open_settings: f())
        self.ui.action_Check_For_Updates.triggered.connect(lambda c, f=self.action_check_for_update: f())
        self.ui.actionAbout_Qt.triggered.connect(lambda c, f=self.action_open_about_qt: f())
        self.ui.actionAbout_mpvqc.triggered.connect(lambda c, f=self.action_open_about_mpvqc: f())

    def toggle_fullscreen(self) -> None:
        """
        Will toggle the fullscreen mode.
        """

        if self.isFullScreen():
            self.display_normal()
        else:
            self.display_fullscreen()

    def display_fullscreen(self) -> None:
        """
        Will show the video in fullscreen. If already fullscreen no action will be triggered.
        """

        if self.isFullScreen():
            return

        self.current_geometry: QByteArray = self.saveGeometry()
        self.menubar_height = self.menuBar().height()
        self.widget_comments.on_before_fullscreen()

        self.widget_comments.hide()
        self.widget_status_bar.hide()
        # Needed because otherwise no shortcuts would work in fullscreen mode
        self.ui.menuBar.setMaximumHeight(0)
        self.display_mouse_cursor(display=True)

        self.showFullScreen()

    def display_normal(self) -> None:
        """
        Will restore the default view. If already normal view no action will be triggered.
        """

        if not self.isFullScreen():
            return

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

    def action_new_qc_document(self) -> None:

        def new_qc_document():
            self.widget_comments.reset_comments_table()
            self.qc_manager.reset_qc_document_path()

        if self.qc_manager.should_save():
            if NewQCDocumentOldNotSavedQMessageBox().exec_():
                new_qc_document()
        else:
            new_qc_document()

    def action_open_qc_document(self) -> None:

        if self.qc_manager.should_save():
            if LoadQCDocumentOldNotSavedQMessageBox().exec_():
                self.__open_qc_txt_files(OpenQcFileDialog.get_open_file_names("", parent=self))
        else:
            self.__open_qc_txt_files(OpenQcFileDialog.get_open_file_names("", parent=self))

    def __open_qc_txt_files(self, file_list: List, ask_to_open_found_vid=True) -> None:
        """
        Plain action. Will try to open the txt_files.

        :param file_list: The txt files to open
        """

        from src.qcutils import QualityCheckParser

        amount: int = len(file_list)
        wid_comments = self.widget_comments

        if wid_comments.get_all_comments():
            if not WhatToDoWithExistingCommentsInTableWhenOpeningNewQCDocument().exec_():
                wid_comments.reset_comments_table()

        for txt in file_list:
            is_valid = txt and path.isfile(txt)

            if is_valid:
                video_path, com_list = QualityCheckParser(txt).results()

                for com in com_list:
                    wid_comments.add_comment(com.coty, com.note, com.time, sort=False,
                                             will_change_qc=False, edit_mode_active=False)

                if amount == 1:
                    self.qc_manager.update_path_qc_document_to(txt)

                    if video_path and path.isfile(video_path) \
                            and ask_to_open_found_vid and ValidVideoFileFoundQMessageBox().exec_():
                        self.action_open_video(video_path)

        if amount >= 2:
            self.qc_manager.reset_qc_document_path()
            wid_comments.sort()

    def action_save_qc_document(self) -> None:
        self.qc_manager.save()

    def action_save_qc_document_as(self) -> None:
        self.qc_manager.save_as()

    def action_close(self) -> None:
        """
        Emits a close event.
        Continue to read with *closeEvent()*.
        """

        self.display_normal()
        self.close()

    def action_open_video(self, file: path = None) -> None:

        from src.settings import Settings
        setting = Settings

        if file is None:
            file = OpenVideoFileDialog.get_open_file_name(directory=setting.Holder.PLAYER_LAST_PLAYED_DIR.value,
                                                          parent=self)

        if path.isfile(file):
            setting.Holder.PLAYER_LAST_PLAYED_DIR.value = path.dirname(file)
            setting.save()
            self.player.open_video(file, play=True)

    def action_open_network_stream(self) -> None:
        pass

    def action_resize_video(self) -> None:
        pass

    def action_open_settings(self) -> None:
        """
        When user hits Options -> Settings.
        """

        from src.gui.uihandler.preferences import PreferenceHandler

        player = self.player
        was_paused_by_user = player.is_paused()
        player.pause()

        PreferenceHandler().exec_()

        # After dialog closed
        if not was_paused_by_user:
            player.play()

        self.reload_ui_language()
        self.widget_context_menu.update_entries()

    def action_check_for_update(self) -> None:
        print(inspect.stack()[0][3])

    def action_open_about_qt(self) -> None:
        print(inspect.stack()[0][3])

    def action_open_about_mpvqc(self) -> None:
        print(inspect.stack()[0][3])

    def observed_player_property_video_file_name(self, video_file_name):
        from src.settings import Settings

        if Settings.Holder.CUSTOMIZATION_WINDOW_TITLE.value == 1:
            self.setWindowTitle(video_file_name)

    def observed_player_property_full_path(self, full_path):
        from src.settings import Settings

        if Settings.Holder.CUSTOMIZATION_WINDOW_TITLE.value == 2:
            self.setWindowTitle(full_path)

    def closeEvent(self, cev: QCloseEvent):

        if self.qc_manager.should_save():
            self.player.pause()
            if QuitNotSavedQMessageBox().exec_():
                self.player.terminate()
                self.close()

        else:
            super().closeEvent(cev)

    def showEvent(self, sev: QShowEvent) -> None:
        print(inspect.stack()[0][3])

    def dragEnterEvent(self, e: QDragEnterEvent):
        e.acceptProposedAction()

    def dropEvent(self, e: QDropEvent):
        dropped_local_files = [x.toLocalFile() for x in e.mimeData().urls() if path.isfile(x.toLocalFile())]

        txts, subs, vids = [], [], []

        for file in dropped_local_files:
            ext = file.rsplit('.', 1)[-1]

            if ext == "txt":
                txts.append(file)
            if ext in _DROPABLE_SUBS:
                subs.append(file)
            if ext in _DROPABLE_VIDS:
                vids.append(file)

        for s in subs:
            self.player.add_sub_files(s)

        video_found = bool(vids)
        if video_found:
            self.player.open_video(vids[0], play=True)

        self.__open_qc_txt_files(txts, ask_to_open_found_vid=not video_found)
