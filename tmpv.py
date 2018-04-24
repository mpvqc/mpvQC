import gettext
import inspect
import locale
import sys
from os import path

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTranslator, Qt, QEvent, QObject
from PyQt5.QtGui import QCursor, QShowEvent, QResizeEvent, QKeyEvent

from src.gui.main import Ui_MainWindow
# noinspection PyUnresolvedReferences,PyProtectedMember
from src.player.players import ActionType

DIRECTORY_PROGRAM = sys._MEIPASS if getattr(sys, "frozen", False) else path.dirname(path.realpath(__file__))
APPLICATION_VERSION = "0.0.1"
APPLICATION_NAME = "mpv-qc"


# todo logger

class ApplicationWindow(QtWidgets.QMainWindow):

    def __init__(self, appl: QtWidgets.QApplication):
        super(ApplicationWindow, self).__init__()

        # Keep a reference to application
        self.__application = appl
        self.__application.installEventFilter(self)

        # Ui setup
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Translator
        self.translator = QTranslator()
        self.reload_ui_language()

        from src.player.handlers import MenubarHandler
        from src.player.widgets import MpvWidget

        # Create a mpv widget and add it on top, pass a reference to the menu bar handler and bind it
        self.mpv_widget = MpvWidget(self)
        self.ui.splitter.insertWidget(0, self.mpv_widget)

        self.menubar_handler = MenubarHandler(self, self.mpv_widget)
        self.menubar_handler.bind()

    def reload_ui_language(self):
        from src.preferences.configuration import get_paths

        self.__application.removeTranslator(self.translator)

        _locale_structure = path.join(get_paths().dir_program, "locale", "{}", "LC_MESSAGES")
        language: str = settings.get_settings().language.value

        if language.startswith("German"):
            value = "de"
        else:
            value = "en"

        trans_dir = _locale_structure.format(value)
        trans_present = path.isdir(trans_dir)

        if trans_present:
            directory = path.join(get_paths().dir_program, "locale")
            gettext.translation(domain="ui_transmo", localedir=directory, languages=['de', 'en']).install()
            self.translator.load("ui_trans", trans_dir)
        else:
            self.translator.load("ui_trans", _locale_structure.format("en"))

        self.__application.installTranslator(self.translator)
        self.ui.retranslateUi(self)

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.hide_fullscreen()
        else:
            self.display_fullscreen()
        self.display_mouse_cursor()

    def display_fullscreen(self):
        self.ui.tableView.hide()
        self.ui.statusbar.hide()
        self.ui.menuBar.hide()
        self.showFullScreen()

    def hide_fullscreen(self):
        self.showNormal()
        self.ui.tableView.show()
        self.ui.statusbar.show()
        self.ui.menuBar.show()

    def display_mouse_cursor(self):
        this_app = self.__application

        while this_app.overrideCursor():
            this_app.restoreOverrideCursor()

        self.mpv_widget.cursor_timer.start(1000)

    def hide_mouse_cursor(self):
        if self.isFullScreen():
            self.__application.setOverrideCursor(QCursor(Qt.BlankCursor))

    def showEvent(self, sev: QShowEvent):
        print(inspect.stack()[0][3])

    def __resize_event(self, rev: QResizeEvent) -> bool:
        # print(inspect.stack()[0][3])

        return False

    def __key_press_event(self, kev: QKeyEvent) -> bool:
        print(inspect.stack()[0][3])

        pressed_key = kev.key()
        modifiers = self.__application.keyboardModifiers()

        if pressed_key == Qt.Key_F and modifiers == Qt.NoModifier:
            self.toggle_fullscreen()
            return True

        return False

    # noinspection PyTypeChecker
    def eventFilter(self, target: QObject, event: QEvent):
        """We have *subscribed* to the *main application's event*. Here we're delegating them to our own methods."""

        ev_type = event.type()

        if ev_type == QEvent.Resize:
            return self.__resize_event(event)
        elif ev_type == QEvent.KeyPress:
            return self.__key_press_event(event)
        else:
            return super().eventFilter(target, event)


if __name__ == "__main__":
    from src.preferences import settings

    app = QtWidgets.QApplication(sys.argv)

    locale.setlocale(locale.LC_NUMERIC, "C")

    application = ApplicationWindow(app)
    application.show()

    sys.exit(app.exec_())
