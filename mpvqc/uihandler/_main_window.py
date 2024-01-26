# Copyright (C) 2016-2017 Frechdachs <frechdachs@rekt.cc>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from os import path
from pathlib import Path

from PyQt5.QtCore import QTranslator, Qt, QCoreApplication, QByteArray, QTimer, QLocale, QLibraryInfo
from PyQt5.QtGui import QShowEvent, QCursor, QCloseEvent, QDragEnterEvent, QDropEvent, QPalette, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QStyle, QDesktopWidget, QVBoxLayout, QWidget, QStyleFactory

from mpvqc import get_settings, get_resources
from mpvqc.ui_loader import init_from_resources
from mpvqc.uihandler._search_form import SearchHandler
from mpvqc.uiutil import SUPPORTED_SUB_FILES, dialogs

_translate = QCoreApplication.translate


class MainHandler(QMainWindow):

    def __init__(self, application: QApplication):
        super(MainHandler, self).__init__()
        from mpvqc.widgets import UserSettings
        self.user_settings = UserSettings

        self.application = application
        self.setAcceptDrops(True)

        self.__ui = init_from_resources(self, "qrc:/data/ui/main_window.ui")

        # Widgets
        from mpvqc.widgets import CommentsTable, StatusBar, MpvWidget, ContextMenu

        """
        Layout:
            Splitter
                - MpvWidget
                - Wrapper
                    - CommentsTable
                    - SearchBar (hidden by default)
            StatusBar
        """

        self.widget_mpv = MpvWidget(self)
        self.widget_comments = CommentsTable(self)
        self.widget_context_menu = ContextMenu(self)
        self.search_bar = SearchHandler(self)
        self.__widget_status_bar = StatusBar()
        self.__player = self.widget_mpv.player

        from mpvqc.manager import QcManager
        self.__qc_manager = QcManager(self, self.widget_mpv, self.widget_comments)
        self.__qc_manager_has_changes = False

        def __state_changed(has_changes):
            self.__qc_manager_has_changes = has_changes
            self.__update_window_title()

        self.search_bar.sig_shown.connect(self.widget_comments.on_search_shown)
        self.search_bar.sig_hidden.connect(self.widget_comments.on_search_hidden)
        self.search_bar.sig_query_changed.connect(self.widget_comments.on_search_query_changed)
        self.search_bar.sig_result_previous.connect(self.widget_comments.on_search_previous_result)
        self.search_bar.sig_result_next.connect(self.widget_comments.on_search_next_result)
        self.search_bar.sig_edit_comment.connect(self.widget_comments.on_search_edit_comment)
        self.widget_comments.search_highlight_changed.connect(self.search_bar.on_search_highlight_changed)

        self.__qc_manager.state_changed.connect(__state_changed)
        self.__qc_manager.video_imported.connect(self.__on_new_video_imported)
        self.widget_mpv.player.sig_mpv_percent_pos.connect(self.__widget_status_bar.on_value_percent_pos_changed)
        self.widget_mpv.player.sig_mpv_time_pos.connect(self.__widget_status_bar.on_value_time_pos_changed)
        self.widget_mpv.player.sig_mpv_time_remaining.connect(self.__widget_status_bar.on_value_time_remaining_changed)
        self.widget_comments.comment_amount_changed.connect(self.__widget_status_bar.on_comment_amount_changed)
        self.widget_comments.comment_selection_changed.connect(self.__widget_status_bar.on_comment_selection_changed)

        self.__splitter_bottom_layout = QVBoxLayout()
        self.__splitter_bottom_layout.addWidget(self.widget_comments)
        self.__splitter_bottom_layout.addWidget(self.search_bar)
        self.__splitter_bottom_layout.setContentsMargins(2, 0, 2, 0)
        self.__splitter_bottom_layout.setSpacing(2)

        self.__splitter_bottom_content_wrapper = QWidget()
        self.__splitter_bottom_content_wrapper.setLayout(self.__splitter_bottom_layout)

        self.setStatusBar(self.__widget_status_bar)
        self.__ui.mainWindowContentSplitter.insertWidget(0, self.__splitter_bottom_content_wrapper)
        self.__ui.mainWindowContentSplitter.insertWidget(0, self.widget_mpv)
        self.__ui.mainWindowContentSplitter.setSizes([400, 20])
        self.search_bar.hide()

        # Class variables
        self.__current_geometry: QByteArray = None
        self.__current_video_file = ""
        self.__current_video_path = ""
        self.__comment_types_scroll_position = 0
        self.__menubar_height = None

        # Timer invoking autosave action
        self.__autosave_interval_timer: QTimer = None
        self.__qc_manager.reset_auto_save()

        # Translator
        self._mpvqc_translator = QTranslator()
        self._qt_translator = QTranslator()
        self.__update_ui_language()

        self.__setup_menu_bar()

        self.__color_palette = application.palette()
        self.__style_name = application.style().objectName()
        self.set_theme()

    def display_mouse_cursor(self, display: bool) -> None:
        """
        Will display the mouse cursor.

        :param display: True if display mouse cursor, False if hide mouse cursor.
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

        self.__splitter_bottom_content_wrapper.show()
        self.__widget_status_bar.show()
        self.__ui.mainWindowMenuBar.setMaximumHeight(self.__menubar_height)
        self.display_mouse_cursor(display=True)

        self.restoreGeometry(self.__current_geometry)
        self.widget_comments.verticalScrollBar().setValue(self.__comment_types_scroll_position)

    def __display_fullscreen(self) -> None:
        """
        Will show the video in fullscreen. If already fullscreen no action will be triggered.
        """

        if self.isFullScreen():
            return

        self.__current_geometry: QByteArray = self.saveGeometry()
        self.__menubar_height = self.menuBar().height()

        self.__comment_types_scroll_position = self.widget_comments.verticalScrollBar().value()
        self.__splitter_bottom_content_wrapper.hide()
        self.__widget_status_bar.hide()

        # Needed because otherwise no shortcuts would work in fullscreen mode
        self.__ui.mainWindowMenuBar.setMaximumHeight(0)
        self.display_mouse_cursor(display=True)

        self.showFullScreen()

    def __setup_menu_bar(self) -> None:

        self.__ui.actionNewQcDocument.triggered.connect(self.__qc_manager.request_new_document)
        self.__ui.actionOpenQcDocuments.triggered.connect(self.__qc_manager.request_open_qc_documents)
        self.__ui.actionSaveQcDocument.triggered.connect(self.__qc_manager.request_save_qc_document)
        self.__ui.actionSaveQcDocumentAs.triggered.connect(self.__qc_manager.request_save_qc_document_as)
        self.__ui.actionExitMpvQc.triggered.connect(self.close)

        self.__ui.actionOpenVideoFile.triggered.connect(self.__qc_manager.request_open_video)
        self.__ui.actionOpenSubtitleFile.triggered.connect(self.__qc_manager.request_open_subtitles)
        self.__ui.actionOpenNetworkStream.triggered.connect(self.__action_open_network_stream)
        self.__ui.actionResizeVideoToOriginalResolution.triggered.connect(self.__action_resize_video)

        self.__ui.actionEditNickname.triggered.connect(lambda a, b=self, f=self.user_settings.edit_nickname: f(b))
        self.__ui.actionEditCommentTypes.triggered.connect(
            lambda a, callback=self.__after_edited_comment_types, f=self.user_settings.edit_comment_types: f(callback))

        self.user_settings.setup_menu_window_title(self.__ui.menuWindowTitle, self.__update_window_title)
        self.user_settings.setup_dark_theme(self.__ui.actionDarkTheme, self.set_theme)

        self.user_settings.setup_languages(self.__ui.menuLanguage, self.__update_ui_language)

        self.__ui.actionEditMpvConf.triggered.connect(self.user_settings.edit_mpv_conf)
        self.__ui.actionEditInputConf.triggered.connect(self.user_settings.edit_input_conf)

        self.user_settings.setup_document(
            self.__ui.actionSaveVideoPathToDocument, self.__ui.actionSaveNickNameToDocument)

        self.__ui.actionOpenBackupPreferences.triggered.connect(
            lambda a, parent=self, qc_manager=self.__qc_manager,
                   f=self.user_settings.edit_backup_preferences: f(parent, qc_manager))

        self.__ui.actionCheckForUpdates_2.triggered.connect(self.__check_for_update)
        self.__ui.actionAboutQt.triggered.connect(QApplication.instance().aboutQt)
        self.__ui.actionAboutMpvQc.triggered.connect(self.user_settings.display_about_dialog)

    def __after_edited_comment_types(self):
        self.widget_context_menu.update_entries()
        self.widget_comments.resize_column_type_column()

    def __update_window_title(self) -> None:
        """
        Will set the current window title according to the user setting.
        """

        value = get_settings().window_title_info

        if value == 2 and self.__current_video_path:
            txt = self.__current_video_path
        elif value == 1 and self.__current_video_file:
            txt = self.__current_video_file
        else:
            txt = "mpvQC"

        self.setWindowTitle(
            txt + " " + (_translate("MainWindow", "(unsaved)") if self.__qc_manager_has_changes else ""))

    def __update_ui_language(self) -> None:
        r = get_resources()
        s = get_settings()

        language = s.language
        q_locale = QLocale(language)

        self.application.removeTranslator(self._qt_translator)
        self.application.removeTranslator(self._mpvqc_translator)

        self._qt_translator.load(q_locale, "qtbase", "_", QLibraryInfo.location(QLibraryInfo.TranslationsPath))
        self._mpvqc_translator.load(r.get_path_translation(language))

        self.application.installTranslator(self._qt_translator)
        self.application.installTranslator(self._mpvqc_translator)

        s.comment_types_update_current_language()
        self.widget_context_menu.update_entries()
        self.__ui.retranslateUi(self)
        self.user_settings.setup_languages(self.__ui.menuLanguage, self.__update_ui_language)
        self.widget_comments.resize_column_type_column()
        self.__update_window_title()

        self.application.setLayoutDirection(q_locale.textDirection())

    def __resize_video(self, check_desktop_size=False) -> None:

        if self.isFullScreen() or self.isMaximized() or not self.__player.has_video():
            return

        # Block until the first frame has been decoded
        # TODO: Find a better way to do this
        while self.__player.video_width() == 0:
            pass

        width = self.__player.video_width()
        height = self.__player.video_height()

        if check_desktop_size:
            desktop_widget = QDesktopWidget()
            screen_geometry = desktop_widget.screenGeometry(desktop_widget.screenNumber(QCursor.pos()))

            if self.height() - self.widget_mpv.height() + height > screen_geometry.height():
                height = int(screen_geometry.height() * 2 / 3)
                width = int(width * height / self.__player.video_height())

        # DA FUQ!
        # Have not found a better way .. :/
        for i in range(0, 8):
            if width and height:
                additional_height = self.height() - self.widget_mpv.height()
                self.resize(width, height + additional_height)

        self.__move_window_to_center()

    def __action_open_network_stream(self) -> None:

        url = dialogs.get_open_network_stream(self)

        if url:
            self.__player.open_url(url, play=True)

    def __action_resize_video(self) -> None:
        self.__resize_video()

    def __on_new_video_imported(self, new_video: str):
        self.__current_video_path = new_video
        self.__current_video_file = Path(new_video).stem

        QTimer.singleShot(0, self.__update_window_title)
        QTimer.singleShot(0, self.__resize_video)

    def __move_window_to_center(self) -> None:
        """
        Moves window to center of the screen.
        https://wiki.qt.io/How_to_Center_a_Window_on_the_Screen
        """

        desktop_widget = QDesktopWidget()
        screen_geometry = desktop_widget.screenGeometry(desktop_widget.screenNumber(QCursor.pos()))

        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter, self.window().size(), screen_geometry))

    def closeEvent(self, cev: QCloseEvent) -> None:
        self.display_normal()
        saved = self.__qc_manager.request_quit_application()
        if saved:
            self.__player.terminate()
            get_settings().write_to_disk()
            cev.accept()
        else:
            cev.ignore()

    def showEvent(self, sev: QShowEvent) -> None:
        self.__move_window_to_center()

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        e.acceptProposedAction()

    def dropEvent(self, e: QDropEvent) -> None:
        dropped_local_files = [x.toLocalFile() for x in e.mimeData().urls() if path.isfile(x.toLocalFile())]

        txts, subs, vids = [], [], []

        for file in dropped_local_files:
            ext = path.splitext(file)[-1]

            if ext == ".txt":
                txts.append(file)
            elif ext in SUPPORTED_SUB_FILES:
                subs.append(file)
            else:
                vids.append(file)

        self.__qc_manager.do_open_drag_and_drop_data(vids, txts, subs)

    def set_theme(self):
        dark_theme = get_settings().dark_theme

        if dark_theme:
            palette = QPalette()  # https://gist.github.com/QuantumCD/6245215
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Light,
                             Qt.transparent)  # text shadow color of the disabled options in context menu
            palette.setColor(QPalette.Disabled, QPalette.Text, Qt.gray)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            self.application.setStyle("Fusion")
            self.application.setPalette(palette)
            self.application.setStyleSheet(
                "QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
        else:
            self.application.setStyle(QStyleFactory.create(self.__style_name))
            self.application.setPalette(self.__color_palette)
            self.application.setStyleSheet("")

    def __check_for_update(self):
        from mpvqc.uiutil import messageboxes
        messageboxes.CheckForUpdates().exec_()
