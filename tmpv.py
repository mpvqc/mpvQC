import locale
import sys
from os import path

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QFrame

from src import configuration
from src.gui.main import Ui_MainWindow
from src.mpvqc import MpvActionHandler

# noinspection PyUnresolvedReferences,PyProtectedMember
DIRECTORY_PROGRAM = sys._MEIPASS if getattr(sys, "frozen", False) else path.dirname(path.realpath(__file__))
APPLICATION_VERSION = "0.0.1"
APPLICATION_NAME = "mpvQC"
SYSTEM_LOCALE = locale.getdefaultlocale()[0]

_ = lambda s: s


class MpvWidget(QFrame):

    def __init__(self, parent=None):
        super(MpvWidget, self).__init__(parent)

        self.setStyleSheet("background-color:black;")
        self.setMouseTracking(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        self.cursor_timer = QTimer(self)
        self.cursor_timer.setSingleShot(True)
        # self.cursortimer.timeout.connect(hideCursor)


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.splitter.insertWidget(0, MpvWidget())

        mah = MpvActionHandler()
        self.ui.actionNew_QC_Document.triggered.connect(lambda c, f=mah.on_pressed_new_qc_document: f())
        self.ui.action_Open_QC_Document.triggered.connect(lambda c, f=mah.on_pressed_open_qc_document: f())
        self.ui.action_Save_QC_Document.triggered.connect(lambda c, f=mah.on_pressed_save_qc_document: f())
        self.ui.actionS_ave_QC_Document_As.triggered.connect(lambda c, f=mah.on_pressed_save_qc_document_as: f())
        self.ui.action_Exit_mpvQC.triggered.connect(lambda c, f=mah.on_pressed_exit: f())

        self.ui.action_Open_Video_File.triggered.connect(lambda c, f=mah.on_pressed_open_video: f())
        self.ui.actionOpen_Network_Stream.triggered.connect(lambda c, f=mah.on_pressed_open_network_stream: f())
        self.ui.action_Resize_Video_To_Its_Original_Resolutio.triggered.connect(
            lambda c, f=mah.on_pressed_resize_video: f())

        self.ui.action_Settings.triggered.connect(lambda c, f=mah.on_pressed_settings: f())
        self.ui.action_Check_For_Updates.triggered.connect(lambda c, f=mah.on_pressed_check_for_update: f())
        self.ui.actionAbout_Qt.triggered.connect(lambda c, f=mah.on_pressed_about_qt: f())
        self.ui.actionAbout_mpvqc.triggered.connect(lambda c, f=mah.on_pressed_about_mpvqc: f())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    qtranslator = configuration.provide_translator()
    app.installTranslator(qtranslator)
    application = ApplicationWindow()
    application.show()
    print(QtCore.QCoreApplication.translate("Misc", "Translation"))
    sys.exit(app.exec_())
