# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/elias/PycharmProjects/mpvQC/gui/main.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.tableView = QtWidgets.QTableView(self.splitter)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 30))
        self.menuBar.setObjectName("menuBar")
        self.menu_File = QtWidgets.QMenu(self.menuBar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Video = QtWidgets.QMenu(self.menuBar)
        self.menu_Video.setObjectName("menu_Video")
        self.menu_Settings = QtWidgets.QMenu(self.menuBar)
        self.menu_Settings.setObjectName("menu_Settings")
        self.menuAbout = QtWidgets.QMenu(self.menuBar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menuBar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew_QC_Document = QtWidgets.QAction(MainWindow)
        self.actionNew_QC_Document.setObjectName("actionNew_QC_Document")
        self.action_Open_QC_Document = QtWidgets.QAction(MainWindow)
        self.action_Open_QC_Document.setObjectName("action_Open_QC_Document")
        self.action_Save_QC_Document = QtWidgets.QAction(MainWindow)
        self.action_Save_QC_Document.setObjectName("action_Save_QC_Document")
        self.actionS_ave_QC_Document_As = QtWidgets.QAction(MainWindow)
        self.actionS_ave_QC_Document_As.setObjectName("actionS_ave_QC_Document_As")
        self.action_Exit_mpvQC = QtWidgets.QAction(MainWindow)
        self.action_Exit_mpvQC.setObjectName("action_Exit_mpvQC")
        self.action_Open_Video_File = QtWidgets.QAction(MainWindow)
        self.action_Open_Video_File.setObjectName("action_Open_Video_File")
        self.actionOpen_Network_Stream = QtWidgets.QAction(MainWindow)
        self.actionOpen_Network_Stream.setObjectName("actionOpen_Network_Stream")
        self.action_Resize_Video_To_Its_Original_Resolutio = QtWidgets.QAction(MainWindow)
        self.action_Resize_Video_To_Its_Original_Resolutio.setObjectName("action_Resize_Video_To_Its_Original_Resolutio")
        self.action_Check_For_Updates = QtWidgets.QAction(MainWindow)
        self.action_Check_For_Updates.setObjectName("action_Check_For_Updates")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionAbout_mpvqc = QtWidgets.QAction(MainWindow)
        self.actionAbout_mpvqc.setObjectName("actionAbout_mpvqc")
        self.action_Settings = QtWidgets.QAction(MainWindow)
        self.action_Settings.setObjectName("action_Settings")
        self.menu_File.addAction(self.actionNew_QC_Document)
        self.menu_File.addAction(self.action_Open_QC_Document)
        self.menu_File.addAction(self.action_Save_QC_Document)
        self.menu_File.addAction(self.actionS_ave_QC_Document_As)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Exit_mpvQC)
        self.menu_Video.addAction(self.action_Open_Video_File)
        self.menu_Video.addAction(self.actionOpen_Network_Stream)
        self.menu_Video.addSeparator()
        self.menu_Video.addAction(self.action_Resize_Video_To_Its_Original_Resolutio)
        self.menu_Settings.addAction(self.action_Settings)
        self.menuAbout.addAction(self.action_Check_For_Updates)
        self.menuAbout.addSeparator()
        self.menuAbout.addAction(self.actionAbout_Qt)
        self.menuAbout.addAction(self.actionAbout_mpvqc)
        self.menuBar.addAction(self.menu_File.menuAction())
        self.menuBar.addAction(self.menu_Video.menuAction())
        self.menuBar.addAction(self.menu_Settings.menuAction())
        self.menuBar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Video.setTitle(_translate("MainWindow", "Vi&deo"))
        self.menu_Settings.setTitle(_translate("MainWindow", "Optio&ns"))
        self.menuAbout.setTitle(_translate("MainWindow", "Abo&ut"))
        self.actionNew_QC_Document.setText(_translate("MainWindow", "&New QC document"))
        self.actionNew_QC_Document.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.action_Open_QC_Document.setText(_translate("MainWindow", "&Open QC document ..."))
        self.action_Open_QC_Document.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.action_Save_QC_Document.setText(_translate("MainWindow", "&Save QC document"))
        self.action_Save_QC_Document.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionS_ave_QC_Document_As.setText(_translate("MainWindow", "S&ave QC document as ..."))
        self.actionS_ave_QC_Document_As.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.action_Exit_mpvQC.setText(_translate("MainWindow", "&Exit mpvQC"))
        self.action_Exit_mpvQC.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.action_Open_Video_File.setText(_translate("MainWindow", "Open &video ..."))
        self.action_Open_Video_File.setShortcut(_translate("MainWindow", "Ctrl+Shift+O"))
        self.actionOpen_Network_Stream.setText(_translate("MainWindow", "Open &network stream ..."))
        self.actionOpen_Network_Stream.setShortcut(_translate("MainWindow", "Ctrl+Alt+Shift+O"))
        self.action_Resize_Video_To_Its_Original_Resolutio.setText(_translate("MainWindow", "&Resize video to original resolution"))
        self.action_Resize_Video_To_Its_Original_Resolutio.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.action_Check_For_Updates.setText(_translate("MainWindow", "&Check For Updates ..."))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About &Qt"))
        self.actionAbout_mpvqc.setText(_translate("MainWindow", "About &mpvQC"))
        self.action_Settings.setText(_translate("MainWindow", "&Settings"))
        self.action_Settings.setShortcut(_translate("MainWindow", "Ctrl+Alt+S"))

