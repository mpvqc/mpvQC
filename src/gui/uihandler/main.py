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

from PyQt5.QtCore import QTranslator, Qt, QCoreApplication, QByteArray, QEvent, QTimer
from PyQt5.QtGui import QShowEvent, QCursor, QCloseEvent, QDragEnterEvent, QDropEvent, QPalette, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QStyle, QDesktopWidget, QVBoxLayout, QWidget, QStyleFactory

from src import settings
from src.gui import SUPPORTED_SUB_FILES
from src.gui.dialogs import get_open_network_stream
from src.gui.events import EventPlayerCurrentVideoFile, PlayerCurrentVideoFile, PlayerCurrentVideoPath, \
    EventPlayerCurrentVideoPath, EventDistributor, EventReceiver
from src.gui.generated.main import Ui_MainPlayerView
from src.gui.uihandler.search import SearchHandler

_translate = QCoreApplication.translate


# noinspection PyMethodMayBeStatic
class MainHandler(QMainWindow):

    def __init__(self, application: QApplication):
        super(MainHandler, self).__init__()
        self.application = application
        self.setAcceptDrops(True)

        # User interface setup
        self.__ui = Ui_MainPlayerView()
        self.__ui.setupUi(self)

        # Translator
        self.__translator = QTranslator()
        self.__update_ui_language()

        self.__color_palette = application.palette()
        self.__style_name = application.style().objectName()
        self.set_theme()

        # Widgets
        from src.gui.widgets import CommentsTable, StatusBar, MpvWidget, ContextMenu

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

        from src.qc.manager import QcManager
        self.__qc_manager = QcManager(self, self.widget_mpv, self.widget_comments)
        self.__qc_manager_has_changes = False

        def __state_changed(has_changes):
            self.__qc_manager_has_changes = has_changes
            self.__update_window_title()

        self.__qc_manager.state_changed.connect(__state_changed)

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

        self.__setup_menu_bar()

        EventDistributor.add_receiver((self, EventReceiver.MAIN_HANDLER),
                                      (self.widget_mpv, EventReceiver.WIDGET_MPV),
                                      (self.widget_comments, EventReceiver.WIDGET_COMMENTS),
                                      (self.widget_context_menu, EventReceiver.WIDGET_CONTEXT_MENU),
                                      (self.__widget_status_bar, EventReceiver.WIDGET_STATUS_BAR))

        # Class variables
        self.__current_geometry: QByteArray = None
        self.__current_video_file = ""
        self.__current_video_path = ""
        self.__comment_types_scroll_position = 0
        self.__menubar_height = None

        # Timer invoking autosave action
        self.__autosave_interval_timer: QTimer = None
        self.__qc_manager.reset_auto_save()

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
        """
        Binds the menubar to the corresponding actions.
        """

        self.__ui.actionNewQcDocument.triggered.connect(lambda c, f=self.__qc_manager.request_new_document: f())
        self.__ui.actionOpenQcDocuments.triggered.connect(lambda c, f=self.__qc_manager.request_open_qc_documents: f())
        self.__ui.actionSaveQcDocument.triggered.connect(lambda c, f=self.__qc_manager.request_save_qc_document: f())
        self.__ui.actionSaveQcDocumentAs.triggered.connect(
            lambda c, f=self.__qc_manager.request_save_qc_document_as: f())
        self.__ui.actionExitMpvQc.triggered.connect(lambda c, f=self.__action_close: f())

        self.__ui.actionOpenVideoFile.triggered.connect(lambda c, f=self.__qc_manager.request_open_video: f())
        self.__ui.actionOpenSubtitleFile.triggered.connect(lambda c, f=self.__qc_manager.request_open_subtitles: f())
        self.__ui.actionOpenNetworkStream.triggered.connect(lambda c, f=self.__action_open_network_stream: f())
        self.__ui.actionResizeVideoToOriginalResolution.triggered.connect(lambda c, f=self.__action_resize_video: f())

        self.__ui.actionSettings.triggered.connect(lambda c, f=self.__action_open_settings: f())
        self.__ui.actionAboutQt.triggered.connect(lambda c, f=self.__action_open_about_qt: f())
        self.__ui.actionAboutMpvQc.triggered.connect(lambda c, f=self.__action_open_about_mpvqc: f())

    def __update_window_title(self) -> None:
        """
        Will set the current window title according to the user setting.
        """

        value = settings.Setting_Custom_Appearance_General_WINDOW_TITLE.value

        if value == 2 and self.__current_video_path:
            txt = self.__current_video_path
        elif value == 1 and self.__current_video_file:
            txt = self.__current_video_file
        else:
            txt = _translate("MainPlayerView", "MainWindow")

        self.setWindowTitle(
            txt + " " + (_translate("MainPlayerView", "(unsaved)") if self.__qc_manager_has_changes else ""))

    def __update_ui_language(self) -> None:
        """
        Reloads the user interface language.
        It uses the language stored in the current settings.json.
        """

        self.application.removeTranslator(self.__translator)

        from src.files import Files

        _locale_structure = path.join(Files.DIRECTORY_PROGRAM, "i18n")
        language: str = settings.Setting_Custom_Language_LANGUAGE.value

        if language.startswith("German"):
            value = "de"
        elif language.startswith("Italian"):
            value = "it"
        else:
            value = "en"

        trans_present = path.isdir(_locale_structure)

        if trans_present:
            self.__translator.load(value, _locale_structure)

        self.application.installTranslator(self.__translator)
        self.__ui.retranslateUi(self)
        settings.Setting_Custom_General_COMMENT_TYPES.update()

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

    def __action_close(self) -> None:
        self.display_normal()
        self.closeEvent(QCloseEvent())

    def __action_open_network_stream(self) -> None:

        url = get_open_network_stream(self)

        if url:
            self.__player.open_url(url, play=True)

    def __action_resize_video(self) -> None:
        self.__resize_video()

    def __action_open_settings(self, display_about=False) -> None:

        from src.gui.uihandler.preferences import PreferenceHandler

        player = self.__player
        was_paused_manually = player.is_paused()
        player.pause()

        PreferenceHandler(display_about).exec_()

        # After dialog closed
        if not was_paused_manually:
            player.play()

        self.__update_ui_language()
        self.set_theme()
        self.widget_context_menu.update_entries()
        self.__update_window_title()
        self.__qc_manager.reset_auto_save()

    def __action_open_about_qt(self) -> None:
        QApplication.instance().aboutQt()

    def __action_open_about_mpvqc(self) -> None:
        self.__action_open_settings(display_about=True)

    def __move_window_to_center(self) -> None:
        """
        Moves window to center of the screen.
        https://wiki.qt.io/How_to_Center_a_Window_on_the_Screen
        """

        desktop_widget = QDesktopWidget()
        screen_geometry = desktop_widget.screenGeometry(desktop_widget.screenNumber(QCursor.pos()))

        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter, self.window().size(), screen_geometry))

    def closeEvent(self, cev: QCloseEvent) -> None:
        saved = self.__qc_manager.request_quit_application()
        if saved:
            self.close()
            return
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

    def close(self) -> None:
        """
        Will close the window and terminate the application.
        """

        self.__player.terminate()
        settings.save()
        super().close()

    def customEvent(self, ev: QEvent) -> None:

        ev_type = ev.type()

        if ev_type == PlayerCurrentVideoFile:
            ev: EventPlayerCurrentVideoFile
            self.__current_video_file = ev.current_video_file
            self.__ui.actionOpenSubtitleFile.setEnabled(True)
            QTimer.singleShot(0, self.__update_window_title)

        elif ev_type == PlayerCurrentVideoPath:
            ev: EventPlayerCurrentVideoPath
            self.__ui.actionOpenSubtitleFile.setEnabled(True)
            self.__current_video_path = str(Path(ev.current_video_path))

    def set_theme(self):
        dark_theme = settings.Setting_Custom_Appearance_General_DARK_THEME.value

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
