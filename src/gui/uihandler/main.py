import gettext
import inspect
from os import path
from typing import List

from PyQt5.QtCore import QTranslator, Qt, QCoreApplication, QByteArray, QEvent, QTimer
from PyQt5.QtGui import QShowEvent, QCursor, QCloseEvent, QDragEnterEvent, QDropEvent
from PyQt5.QtWidgets import QMainWindow, QApplication, QStyle

from src import settings
from src.gui.dialogs import get_open_file_name, get_open_file_names, get_open_network_stream
from src.gui.events import EventPlayerCurrentFile, PlayerCurrentFile, PlayerCurrentPath, EventPlayerCurrentPath
from src.gui.messageboxes import QuitNotSavedQMessageBox, NewQCDocumentOldNotSavedQMessageBox, \
    LoadQCDocumentOldNotSavedQMessageBox, ValidVideoFileFoundQMessageBox, \
    WhatToDoWithExistingCommentsInTableWhenOpeningNewQCDocument
from src.gui.uielements.main import Ui_MainWindow

_translate = QCoreApplication.translate
_DROPABLE_SUBS = ("ass", "ssa", "srt", "sup", "idx", "utf", "utf8", "utf-8", "smi", "rt", "aqt", "jss", "js",
                  "mks", "vtt", "sub", "scc")
_DROPABLE_VIDS = ("mp4", "mkv", "avi")

CustomEventReceiver = []


# noinspection PyMethodMayBeStatic
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
        self.__translator = QTranslator()
        self.__update_ui_language()

        # Widgets
        from src.gui.widgets import CommentsTable, StatusBar, MpvWidget, ContextMenu
        from src.qcutils import QualityCheckManager

        self.widget_mpv = MpvWidget(self)
        self.widget_comments = CommentsTable(self)
        self.widget_context_menu = ContextMenu(self)
        self.__widget_status_bar = StatusBar()
        self.__player = self.widget_mpv.mpv_player
        self.__qc_manager = QualityCheckManager(self)

        CustomEventReceiver.extend([
            self,
            self.widget_mpv,
            self.widget_comments,
            self.widget_context_menu,
            self.__widget_status_bar,
            self.__qc_manager
        ])

        self.setStatusBar(self.__widget_status_bar)
        self.ui.splitter.insertWidget(0, self.widget_comments)
        self.ui.splitter.insertWidget(0, self.widget_mpv)

        # Class variables
        self.__current_geometry: QByteArray = None
        self.__menubar_height = None
        self.__current_file = ""
        self.__current_path = ""

        # Timer which binds 2 class variables
        self.__window_title_update_timer = QTimer()
        self.__window_title_update_timer.timeout.connect(self.__update_window_title)
        self.__window_title_update_timer.start(1000)

        # Timer for autosave
        self.__autosave_interval_timer: QTimer = None
        self.__reload_autosave_settings()

        self.ui.splitter.setSizes([400, 20])

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

    def toggle_fullscreen(self) -> None:
        """
        Will toggle the fullscreen mode.
        """

        if self.isFullScreen():
            self.display_normal()
        else:
            self.__display_fullscreen()

    def display_normal(self) -> None:
        """
        Will restore the default view. If already normal view no action will be triggered.
        """

        if not self.isFullScreen():
            return

        self.showNormal()

        self.widget_comments.show()
        self.__widget_status_bar.show()
        self.ui.menuBar.setMaximumHeight(self.__menubar_height)
        self.display_mouse_cursor(display=True)

        self.restoreGeometry(self.__current_geometry)
        self.widget_comments.on_after_fullscreen()

    def __reload_autosave_settings(self):

        if settings.Setting_Custom_QcDocument_AUTOSAVE_ENABLED.value:

            interval = settings.Setting_Custom_QcDocument_AUTOSAVE_INTERVAL.value

            if interval >= 15:
                self.__autosave_interval_timer = QTimer()
                self.__autosave_interval_timer.timeout.connect(self.__qc_manager.autosave)
                self.__autosave_interval_timer.start(interval * 1000)
        else:
            self.__autosave_interval_timer.stop()

    def __display_fullscreen(self) -> None:
        """
        Will show the video in fullscreen. If already fullscreen no action will be triggered.
        """

        if self.isFullScreen():
            return

        self.__current_geometry: QByteArray = self.saveGeometry()
        self.__menubar_height = self.menuBar().height()
        self.widget_comments.on_before_fullscreen()

        self.widget_comments.hide()
        self.__widget_status_bar.hide()
        # Needed because otherwise no shortcuts would work in fullscreen mode
        self.ui.menuBar.setMaximumHeight(0)
        self.display_mouse_cursor(display=True)

        self.showFullScreen()

    def __setup_menu_bar(self) -> None:
        """
        Binds the menubar to the their actions.
        """

        self.ui.actionNew_QC_Document.triggered.connect(lambda c, f=self.__action_new_qc_document: f())
        self.ui.action_Open_QC_Document.triggered.connect(lambda c, f=self.__action_open_qc_document: f())
        self.ui.action_Save_QC_Document.triggered.connect(lambda c, f=self.__action_save_qc_document: f())
        self.ui.actionS_ave_QC_Document_As.triggered.connect(lambda c, f=self.__action_save_qc_document_as: f())
        self.ui.action_Exit_mpvQC.triggered.connect(lambda c, f=self.__action_close: f())

        self.ui.action_Open_Video_File.triggered.connect(lambda c, f=self.__action_open_video: f())
        self.ui.actionOpen_Network_Stream.triggered.connect(lambda c, f=self.__action_open_network_stream: f())
        self.ui.action_Resize_Video_To_Its_Original_Resolutio.triggered.connect(
            lambda c, f=self.__action_resize_video: f())

        self.ui.action_Settings.triggered.connect(lambda c, f=self.__action_open_settings: f())
        self.ui.action_Check_For_Updates.triggered.connect(lambda c, f=self.__action_check_for_update: f())
        self.ui.actionAbout_Qt.triggered.connect(lambda c, f=self.__action_open_about_qt: f())
        self.ui.actionAbout_mpvqc.triggered.connect(lambda c, f=self.__action_open_about_mpvqc: f())

    def __update_window_title(self) -> None:
        """
        Will set the current window title according to the user setting.
        """

        value = settings.Setting_Custom_Appearance_General_WINDOW_TITLE.value

        if value == 2 and self.__current_path:
            txt = self.__current_path
        elif value == 1 and self.__current_file:
            txt = self.__current_file
        else:
            txt = _translate("MainWindow", "MainWindow")

        self.setWindowTitle(txt)

    def __update_ui_language(self) -> None:
        """
        Reloads the user interface language.
        It uses the language stored in the current settings.json.
        """

        self.application.removeTranslator(self.__translator)

        from src.files import Files

        _locale_structure = path.join(Files.DIRECTORY_PROGRAM, "locale", "{}", "LC_MESSAGES")
        language: str = settings.Setting_Custom_Language_LANGUAGE.value

        if language.startswith("German"):
            value = "de"
        else:
            value = "en"

        trans_dir = _locale_structure.format(value)
        trans_present = path.isdir(trans_dir)

        if trans_present:
            directory = path.join(Files.DIRECTORY_PROGRAM, "locale")
            gettext.translation(domain="ui_transmo", localedir=directory, languages=['de', 'en']).install()
            self.__translator.load("ui_trans", trans_dir)
        else:
            self.__translator.load("ui_trans", _locale_structure.format("en"))

        self.application.installTranslator(self.__translator)
        self.ui.retranslateUi(self)
        settings.Setting_Custom_General_COMMENT_TYPES.update()

    def __action_new_qc_document(self) -> None:

        def new_qc_document():
            self.widget_comments.reset_comments_table()
            self.__qc_manager.reset_qc_document_path()

        if self.__qc_manager.should_save():
            if NewQCDocumentOldNotSavedQMessageBox().exec_():
                new_qc_document()
        else:
            new_qc_document()

    def __action_open_qc_document(self) -> None:

        if self.__qc_manager.should_save():
            if LoadQCDocumentOldNotSavedQMessageBox().exec_():
                self.__open_qc_txt_files(get_open_file_names("", parent=self))
        else:
            self.__open_qc_txt_files(get_open_file_names("", parent=self))

    def __open_qc_txt_files(self, file_list: List, ask_to_open_found_vid=True) -> None:
        """
        Plain action. Will try to open the txt_files.

        :param file_list: The txt files to open
        """

        from src.qcutils import QualityCheckReader

        amount: int = len(file_list)
        wid_comments = self.widget_comments

        if wid_comments.get_all_comments():
            if not WhatToDoWithExistingCommentsInTableWhenOpeningNewQCDocument().exec_():
                wid_comments.reset_comments_table()

        for qc_doc in file_list:
            is_valid = qc_doc and path.isfile(qc_doc)

            if is_valid:
                video_path, com_list = QualityCheckReader(qc_doc).results()

                for com in com_list:
                    wid_comments.add_comment(com.coty, com.note, com.time, sort=False,
                                             will_change_qc=False, edit_mode_active=False)

                if amount == 1:
                    self.__qc_manager.update_path_qc_document_to(qc_doc)

                    if video_path and path.isfile(video_path) \
                            and ask_to_open_found_vid and ValidVideoFileFoundQMessageBox().exec_():
                        self.__action_open_video(video_path)

        if amount >= 2:
            self.__qc_manager.reset_qc_document_path()
            wid_comments.sort()

    def __action_save_qc_document(self) -> None:
        self.__qc_manager.save()

    def __action_save_qc_document_as(self) -> None:
        self.__qc_manager.save_as()

    def __action_close(self) -> None:
        """
        Emits a close event.
        Continue to read with *closeEvent()*.
        """

        self.display_normal()
        self.close()

    def __action_open_video(self, file: path = None) -> None:

        if file is None:
            file = get_open_file_name(
                directory=settings.Setting_Internal_PLAYER_LAST_PLAYED_DIR.value,
                parent=self)

        if path.isfile(file):
            settings.Setting_Internal_PLAYER_LAST_PLAYED_DIR.value = path.dirname(file)
            settings.save()
            self.__player.open_video(file, play=True)

    def __action_open_network_stream(self) -> None:

        url = get_open_network_stream(self)

        if url:
            self.__player.open_url(url, play=True)

    def __action_resize_video(self) -> None:

        if self.isFullScreen() or self.isMaximized() or not self.__player.is_video_loaded():
            return

        def __resize():
            # DA FUQ!
            for i in range(0, 5):
                try:
                    width = self.__player.video_width()
                    height = self.__player.video_height()

                    if width and height:
                        additional_mb = self.menuBar().height()
                        additional_ct = self.widget_comments.height()
                        additional_sb = self.statusBar().height()

                        self.resize(width, height + additional_mb + additional_sb + additional_ct + 2)
                except TypeError:
                    return

        __resize()
        self.__move_window_to_center()

    def __action_open_settings(self, display_about=False) -> None:

        from src.gui.uihandler.preferences import PreferenceHandler

        player = self.__player
        was_paused_manually = player.is_paused()
        player.pause()

        PreferenceHandler(display_about).exec_()

        # After dialog closed
        if not display_about and not was_paused_manually:
            player.play()

        self.__update_ui_language()
        self.widget_context_menu.update_entries()
        self.__update_window_title()
        self.__reload_autosave_settings()

    def __action_check_for_update(self) -> None:
        print(inspect.stack()[0][3])

    def __action_open_about_qt(self) -> None:
        QApplication.instance().aboutQt()

    def __action_open_about_mpvqc(self) -> None:
        self.__action_open_settings(display_about=True)

    def __move_window_to_center(self):
        """
        Moves window to screen center https://wiki.qt.io/How_to_Center_a_Window_on_the_Screen
        """

        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter, self.window().size(),
                                            self.application.desktop().availableGeometry()))

    def closeEvent(self, cev: QCloseEvent):

        if self.__qc_manager.should_save():
            self.__player.pause()
            if QuitNotSavedQMessageBox().exec_():
                self.close()
            else:
                cev.ignore()
        else:
            self.close()

    def showEvent(self, sev: QShowEvent) -> None:
        self.__move_window_to_center()

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        e.acceptProposedAction()

    def dropEvent(self, e: QDropEvent) -> None:
        dropped_local_files = [x.toLocalFile() for x in e.mimeData().urls() if path.isfile(x.toLocalFile())]

        txts, subs, vids = [], [], []

        for file in dropped_local_files:
            ext = file.rsplit('.', 1)[-1]

            if ext == "txt":
                txts.append(file)
            elif ext in _DROPABLE_SUBS:
                subs.append(file)
            elif ext in _DROPABLE_VIDS:
                vids.append(file)

        for s in subs:
            self.__player.add_sub_files(s)

        video_found = bool(vids)
        if video_found:
            self.__player.open_video(vids[0], play=True)

        self.__open_qc_txt_files(txts, ask_to_open_found_vid=not video_found)

    def close(self) -> None:
        """
        Will close the window and terminate the application.
        """

        self.__player.terminate()
        settings.save()
        super().close()

    def customEvent(self, ev: QEvent) -> None:

        ev_type = ev.type()

        if ev_type == PlayerCurrentFile:
            ev: EventPlayerCurrentFile
            self.__current_file = ev.current_file
        elif ev_type == PlayerCurrentPath:
            ev: EventPlayerCurrentPath
            self.__current_path = ev.current_path

    @staticmethod
    def send_event(event: QEvent) -> None:
        for rec in CustomEventReceiver:
            QApplication.sendEvent(rec, event)
