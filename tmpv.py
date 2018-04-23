import gettext
import locale
import sys
from os import path

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QEvent, QTranslator

from src.gui.main import Ui_MainWindow
from src.player.widgets import MpvWidget

# noinspection PyUnresolvedReferences,PyProtectedMember


DIRECTORY_PROGRAM = sys._MEIPASS if getattr(sys, "frozen", False) else path.dirname(path.realpath(__file__))
APPLICATION_VERSION = "0.0.1"
APPLICATION_NAME = "mpv-qc"


class ApplicationWindow(QtWidgets.QMainWindow):
    #  Will be set by *if __name__ == "__main__"*

    def __init__(self, appl: QtWidgets.QApplication):
        super(ApplicationWindow, self).__init__()

        self.__application = appl
        self.translator = QTranslator()
        self.reload_translator()
        self.__application.installTranslator(self.translator)

        from src.player.handlers import MenubarHandler
        mpv_widget = MpvWidget()
        mpv_ah = MenubarHandler(self, mpv_widget)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionNew_QC_Document.triggered.connect(lambda c, f=mpv_ah.on_pressed_new_qc_document: f())
        self.ui.action_Open_QC_Document.triggered.connect(lambda c, f=mpv_ah.on_pressed_open_qc_document: f())
        self.ui.action_Save_QC_Document.triggered.connect(lambda c, f=mpv_ah.on_pressed_save_qc_document: f())
        self.ui.actionS_ave_QC_Document_As.triggered.connect(lambda c, f=mpv_ah.on_pressed_save_qc_document_as: f())
        self.ui.action_Exit_mpvQC.triggered.connect(lambda c, f=mpv_ah.on_pressed_exit: f())

        self.ui.action_Open_Video_File.triggered.connect(lambda c, f=mpv_ah.on_pressed_open_video: f())
        self.ui.actionOpen_Network_Stream.triggered.connect(lambda c, f=mpv_ah.on_pressed_open_network_stream: f())
        self.ui.action_Resize_Video_To_Its_Original_Resolutio.triggered.connect(
            lambda c, f=mpv_ah.on_pressed_resize_video: f())

        self.ui.action_Settings.triggered.connect(lambda c, f=mpv_ah.on_pressed_settings: f())
        self.ui.action_Check_For_Updates.triggered.connect(lambda c, f=mpv_ah.on_pressed_check_for_update: f())
        self.ui.actionAbout_Qt.triggered.connect(lambda c, f=mpv_ah.on_pressed_about_qt: f())
        self.ui.actionAbout_mpvqc.triggered.connect(lambda c, f=mpv_ah.on_pressed_about_mpvqc: f())

        self.ui.splitter.insertWidget(0, mpv_widget)

        self.installEventFilter(self)

    def changeEvent(self, event: QtCore.QEvent):
        if event.type() == QEvent.LanguageChange:
            self.ui.retranslateUi(self)
        else:
            super().changeEvent(event)

    def reload_translator(self):
        from src.preferences.configuration import get_paths

        self.__application.removeTranslator(self.translator)
        _locale_structure = path.join(get_paths().dir_program, "locale", "{}", "LC_MESSAGES")

        l: str = settings.get_settings().language.value

        if l.startswith("German"):
            value = "de"
        else:
            value = "en"

        trans_dir = _locale_structure.format(value)
        trans_present = path.isdir(trans_dir)

        print("Trans present: ", trans_present)
        print("Trans in: ", trans_dir)
        if trans_present:
            join = path.join(get_paths().dir_program, "locale")
            print("Looking up in ", join)
            gettext.translation(domain="ui_transmo",
                                localedir=join,
                                languages=['de', 'en']).install()
            print("Installed")
            self.translator.load("ui_trans", trans_dir)
        else:
            self.translator.load("ui_trans", _locale_structure.format("en"))

        self.__application.installTranslator(self.translator)


if __name__ == "__main__":
    from src.preferences import settings

    app = QtWidgets.QApplication(sys.argv)

    locale.setlocale(locale.LC_NUMERIC, "C")

    application = ApplicationWindow(app)
    application.show()

    print(QtCore.QCoreApplication.translate("Misc", "Translation"))
    sys.exit(app.exec_())
