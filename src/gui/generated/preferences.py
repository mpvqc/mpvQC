# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/elias/PycharmProjects/mpvQC/gui/preferences.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyKF5.KWidgetsAddons import KEditListWidget


class Ui_PreferencesView(object):
    def setupUi(self, PreferencesView):
        PreferencesView.setObjectName("PreferencesView")
        PreferencesView.resize(700, 551)
        PreferencesView.setMinimumSize(QtCore.QSize(700, 500))
        self.verticalLayout = QtWidgets.QVBoxLayout(PreferencesView)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(PreferencesView)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_13 = QtWidgets.QWidget(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_13.sizePolicy().hasHeightForWidth())
        self.widget_13.setSizePolicy(sizePolicy)
        self.widget_13.setObjectName("widget_13")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget_13)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.navigationList = QtWidgets.QListWidget(self.widget_13)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.navigationList.sizePolicy().hasHeightForWidth())
        self.navigationList.setSizePolicy(sizePolicy)
        self.navigationList.setMinimumSize(QtCore.QSize(130, 0))
        self.navigationList.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.navigationList.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.navigationList.setFrameShadow(QtWidgets.QFrame.Plain)
        self.navigationList.setLineWidth(0)
        self.navigationList.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.navigationList.setProperty("showDropIndicator", False)
        self.navigationList.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.navigationList.setAlternatingRowColors(False)
        self.navigationList.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.navigationList.setTextElideMode(QtCore.Qt.ElideRight)
        self.navigationList.setMovement(QtWidgets.QListView.Static)
        self.navigationList.setResizeMode(QtWidgets.QListView.Fixed)
        self.navigationList.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.navigationList.setViewMode(QtWidgets.QListView.ListMode)
        self.navigationList.setUniformItemSizes(True)
        self.navigationList.setSelectionRectVisible(False)
        self.navigationList.setObjectName("navigationList")
        item = QtWidgets.QListWidgetItem()
        icon = QtGui.QIcon.fromTheme("systemsettings")
        item.setIcon(icon)
        self.navigationList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        icon = QtGui.QIcon.fromTheme("photocollage")
        item.setIcon(icon)
        self.navigationList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        icon = QtGui.QIcon.fromTheme("mpv")
        item.setIcon(icon)
        self.navigationList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        icon = QtGui.QIcon.fromTheme("text-editor")
        item.setIcon(icon)
        self.navigationList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        icon = QtGui.QIcon.fromTheme("internet-archive")
        item.setIcon(icon)
        self.navigationList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        icon = QtGui.QIcon.fromTheme("help")
        item.setIcon(icon)
        self.navigationList.addItem(item)
        self.horizontalLayout_6.addWidget(self.navigationList)
        self.horizontalLayout.addWidget(self.widget_13)
        self.stackedWidget = QtWidgets.QStackedWidget(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setObjectName("stackedWidget")
        self.pageGeneral = QtWidgets.QWidget()
        self.pageGeneral.setObjectName("pageGeneral")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.pageGeneral)
        self.verticalLayout_4.setContentsMargins(6, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.widget_4 = QtWidgets.QWidget(self.pageGeneral)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy)
        self.widget_4.setObjectName("widget_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_4)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 18)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_2 = QtWidgets.QLabel(self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_5.addWidget(self.label_2)
        self.verticalLayout_4.addWidget(self.widget_4)
        self.widget_5 = QtWidgets.QWidget(self.pageGeneral)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_5.sizePolicy().hasHeightForWidth())
        self.widget_5.setSizePolicy(sizePolicy)
        self.widget_5.setObjectName("widget_5")
        self.formLayout_2 = QtWidgets.QFormLayout(self.widget_5)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.authorLabel = QtWidgets.QLabel(self.widget_5)
        self.authorLabel.setObjectName("authorLabel")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.authorLabel)
        self.authorLineEdit = QtWidgets.QLineEdit(self.widget_5)
        self.authorLineEdit.setPlaceholderText("")
        self.authorLineEdit.setObjectName("authorLineEdit")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.authorLineEdit)
        self.label_3 = QtWidgets.QLabel(self.widget_5)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.kCommentTypes = KEditListWidget(self.widget_5)
        self.kCommentTypes.setToolTip("")
        self.kCommentTypes.setStyleSheet("QPushButton { text-align:left; padding: 8px; }")
        self.kCommentTypes.setCheckAtEntering(True)
        self.kCommentTypes.setObjectName("kCommentTypes")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.kCommentTypes)
        self.verticalLayout_4.addWidget(self.widget_5)
        self.stackedWidget.addWidget(self.pageGeneral)
        self.pageAppearance = QtWidgets.QWidget()
        self.pageAppearance.setObjectName("pageAppearance")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.pageAppearance)
        self.verticalLayout_11.setContentsMargins(-1, 0, 0, 0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.widget_11 = QtWidgets.QWidget(self.pageAppearance)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_11.sizePolicy().hasHeightForWidth())
        self.widget_11.setSizePolicy(sizePolicy)
        self.widget_11.setObjectName("widget_11")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.widget_11)
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 18)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.label_9 = QtWidgets.QLabel(self.widget_11)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_12.addWidget(self.label_9)
        self.verticalLayout_11.addWidget(self.widget_11)
        self.widget_12 = QtWidgets.QWidget(self.pageAppearance)
        self.widget_12.setObjectName("widget_12")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_12)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.tabWidget_2 = QtWidgets.QTabWidget(self.widget_12)
        self.tabWidget_2.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget_2.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget_2.setDocumentMode(True)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tabGeneral = QtWidgets.QWidget()
        self.tabGeneral.setObjectName("tabGeneral")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.tabGeneral)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.widget_14 = QtWidgets.QWidget(self.tabGeneral)
        self.widget_14.setObjectName("widget_14")
        self.formLayout_4 = QtWidgets.QFormLayout(self.widget_14)
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_10 = QtWidgets.QLabel(self.widget_14)
        self.label_10.setObjectName("label_10")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.window_title_combo_box = QtWidgets.QComboBox(self.widget_14)
        self.window_title_combo_box.setObjectName("window_title_combo_box")
        self.window_title_combo_box.addItem("")
        self.window_title_combo_box.addItem("")
        self.window_title_combo_box.addItem("")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.window_title_combo_box)
        self.horizontalLayout_7.addWidget(self.widget_14)
        self.tabWidget_2.addTab(self.tabGeneral, "")
        self.horizontalLayout_4.addWidget(self.tabWidget_2)
        self.verticalLayout_11.addWidget(self.widget_12)
        self.stackedWidget.addWidget(self.pageAppearance)
        self.pageConfiguration = QtWidgets.QWidget()
        self.pageConfiguration.setObjectName("pageConfiguration")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.pageConfiguration)
        self.verticalLayout_8.setContentsMargins(-1, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.widget_9 = QtWidgets.QWidget(self.pageConfiguration)
        self.widget_9.setObjectName("widget_9")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.widget_9)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 18)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_5 = QtWidgets.QLabel(self.widget_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_9.addWidget(self.label_5)
        self.verticalLayout_8.addWidget(self.widget_9)
        self.label_8 = QtWidgets.QLabel(self.pageConfiguration)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_8.addWidget(self.label_8)
        self.widget_10 = QtWidgets.QWidget(self.pageConfiguration)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_10.sizePolicy().hasHeightForWidth())
        self.widget_10.setSizePolicy(sizePolicy)
        self.widget_10.setObjectName("widget_10")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.widget_10)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.tabWidget = QtWidgets.QTabWidget(self.widget_10)
        self.tabWidget.setTabletTracking(False)
        self.tabWidget.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.tabWidget.setAcceptDrops(False)
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab_4)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.mpv_conf_plain_text_edit = QtWidgets.QPlainTextEdit(self.tab_4)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.mpv_conf_plain_text_edit.setFont(font)
        self.mpv_conf_plain_text_edit.setFrameShadow(QtWidgets.QFrame.Plain)
        self.mpv_conf_plain_text_edit.setObjectName("mpv_conf_plain_text_edit")
        self.horizontalLayout_2.addWidget(self.mpv_conf_plain_text_edit)
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tab_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.input_conf_plain_text_edit = QtWidgets.QPlainTextEdit(self.tab_2)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.input_conf_plain_text_edit.setFont(font)
        self.input_conf_plain_text_edit.setFrameShadow(QtWidgets.QFrame.Plain)
        self.input_conf_plain_text_edit.setObjectName("input_conf_plain_text_edit")
        self.horizontalLayout_3.addWidget(self.input_conf_plain_text_edit)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout_10.addWidget(self.tabWidget)
        self.verticalLayout_8.addWidget(self.widget_10)
        self.stackedWidget.addWidget(self.pageConfiguration)
        self.pageQcDocument = QtWidgets.QWidget()
        self.pageQcDocument.setObjectName("pageQcDocument")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.pageQcDocument)
        self.verticalLayout_6.setContentsMargins(6, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.widget_6 = QtWidgets.QWidget(self.pageQcDocument)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_6.sizePolicy().hasHeightForWidth())
        self.widget_6.setSizePolicy(sizePolicy)
        self.widget_6.setObjectName("widget_6")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.widget_6)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 18)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_4 = QtWidgets.QLabel(self.widget_6)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_7.addWidget(self.label_4)
        self.verticalLayout_6.addWidget(self.widget_6)
        self.widget_7 = QtWidgets.QWidget(self.pageQcDocument)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_7.sizePolicy().hasHeightForWidth())
        self.widget_7.setSizePolicy(sizePolicy)
        self.widget_7.setObjectName("widget_7")
        self.formLayout_3 = QtWidgets.QFormLayout(self.widget_7)
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.formLayout_3.setObjectName("formLayout_3")
        self.autoSaveEnabledCheckBox_4 = QtWidgets.QCheckBox(self.widget_7)
        self.autoSaveEnabledCheckBox_4.setChecked(True)
        self.autoSaveEnabledCheckBox_4.setObjectName("autoSaveEnabledCheckBox_4")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.autoSaveEnabledCheckBox_4)
        self.widget_8 = QtWidgets.QWidget(self.widget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_8.sizePolicy().hasHeightForWidth())
        self.widget_8.setSizePolicy(sizePolicy)
        self.widget_8.setObjectName("widget_8")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_8)
        self.horizontalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(2)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_6 = QtWidgets.QLabel(self.widget_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QtCore.QSize(70, 0))
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        self.autosaveSpinBox_4 = QtWidgets.QSpinBox(self.widget_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.autosaveSpinBox_4.sizePolicy().hasHeightForWidth())
        self.autosaveSpinBox_4.setSizePolicy(sizePolicy)
        self.autosaveSpinBox_4.setMinimum(15)
        self.autosaveSpinBox_4.setMaximum(1000)
        self.autosaveSpinBox_4.setObjectName("autosaveSpinBox_4")
        self.horizontalLayout_5.addWidget(self.autosaveSpinBox_4)
        self.autosaveTimeUnit_4 = QtWidgets.QLabel(self.widget_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.autosaveTimeUnit_4.sizePolicy().hasHeightForWidth())
        self.autosaveTimeUnit_4.setSizePolicy(sizePolicy)
        self.autosaveTimeUnit_4.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.autosaveTimeUnit_4.setObjectName("autosaveTimeUnit_4")
        self.horizontalLayout_5.addWidget(self.autosaveTimeUnit_4)
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.widget_8)
        self.saveNickNameCheckBox = QtWidgets.QCheckBox(self.widget_7)
        self.saveNickNameCheckBox.setObjectName("saveNickNameCheckBox")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.saveNickNameCheckBox)
        self.saveVideoPathCheckBox = QtWidgets.QCheckBox(self.widget_7)
        self.saveVideoPathCheckBox.setObjectName("saveVideoPathCheckBox")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.saveVideoPathCheckBox)
        self.verticalLayout_6.addWidget(self.widget_7)
        self.stackedWidget.addWidget(self.pageQcDocument)
        self.pageLanguage = QtWidgets.QWidget()
        self.pageLanguage.setObjectName("pageLanguage")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.pageLanguage)
        self.verticalLayout_2.setContentsMargins(-1, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_2 = QtWidgets.QWidget(self.pageLanguage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 18)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.widget_2)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setScaledContents(True)
        self.label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.verticalLayout_2.addWidget(self.widget_2)
        self.widget_3 = QtWidgets.QWidget(self.pageLanguage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setObjectName("widget_3")
        self.formLayout = QtWidgets.QFormLayout(self.widget_3)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label_7 = QtWidgets.QLabel(self.widget_3)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.comboBox = QtWidgets.QComboBox(self.widget_3)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBox)
        self.verticalLayout_2.addWidget(self.widget_3)
        self.stackedWidget.addWidget(self.pageLanguage)
        self.pageAbout = QtWidgets.QWidget()
        self.pageAbout.setObjectName("pageAbout")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.pageAbout)
        self.verticalLayout_13.setContentsMargins(-1, 0, 0, 0)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.widget_15 = QtWidgets.QWidget(self.pageAbout)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_15.sizePolicy().hasHeightForWidth())
        self.widget_15.setSizePolicy(sizePolicy)
        self.widget_15.setObjectName("widget_15")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.widget_15)
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 18)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.label_11 = QtWidgets.QLabel(self.widget_15)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_14.addWidget(self.label_11)
        self.verticalLayout_13.addWidget(self.widget_15)
        self.widget_16 = QtWidgets.QWidget(self.pageAbout)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_16.sizePolicy().hasHeightForWidth())
        self.widget_16.setSizePolicy(sizePolicy)
        self.widget_16.setObjectName("widget_16")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.widget_16)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.tabWidget_3 = QtWidgets.QTabWidget(self.widget_16)
        self.tabWidget_3.setDocumentMode(True)
        self.tabWidget_3.setObjectName("tabWidget_3")
        self.sdasd = QtWidgets.QWidget()
        self.sdasd.setObjectName("sdasd")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.sdasd)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.aboutBrowser = QtWidgets.QTextBrowser(self.sdasd)
        self.aboutBrowser.setObjectName("aboutBrowser")
        self.horizontalLayout_9.addWidget(self.aboutBrowser)
        self.tabWidget_3.addTab(self.sdasd, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.tab_3)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.creditsBrowser = QtWidgets.QTextBrowser(self.tab_3)
        self.creditsBrowser.setObjectName("creditsBrowser")
        self.horizontalLayout_10.addWidget(self.creditsBrowser)
        self.tabWidget_3.addTab(self.tab_3, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.tab_5)
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.licenceBrowser = QtWidgets.QTextBrowser(self.tab_5)
        self.licenceBrowser.setObjectName("licenceBrowser")
        self.horizontalLayout_11.addWidget(self.licenceBrowser)
        self.tabWidget_3.addTab(self.tab_5, "")
        self.horizontalLayout_8.addWidget(self.tabWidget_3)
        self.verticalLayout_13.addWidget(self.widget_16)
        self.stackedWidget.addWidget(self.pageAbout)
        self.horizontalLayout.addWidget(self.stackedWidget)
        self.verticalLayout.addWidget(self.widget)
        self.buttonBox = QtWidgets.QDialogButtonBox(PreferencesView)
        font = QtGui.QFont()
        font.setKerning(True)
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Apply | QtWidgets.QDialogButtonBox.Close | QtWidgets.QDialogButtonBox.RestoreDefaults)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(PreferencesView)
        self.navigationList.setCurrentRow(0)
        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_3.setCurrentIndex(0)
        self.buttonBox.rejected.connect(PreferencesView.reject)
        self.buttonBox.accepted.connect(PreferencesView.accept)
        self.autoSaveEnabledCheckBox_4.toggled['bool'].connect(self.widget_8.setEnabled)
        self.navigationList.currentRowChanged['int'].connect(self.stackedWidget.setCurrentIndex)
        QtCore.QMetaObject.connectSlotsByName(PreferencesView)

    def retranslateUi(self, PreferencesView):
        _translate = QtCore.QCoreApplication.translate
        PreferencesView.setWindowTitle(_translate("PreferencesView", "Dialog"))
        __sortingEnabled = self.navigationList.isSortingEnabled()
        self.navigationList.setSortingEnabled(False)
        item = self.navigationList.item(0)
        item.setText(_translate("PreferencesView", "General"))
        item = self.navigationList.item(1)
        item.setText(_translate("PreferencesView", "Appearance"))
        item = self.navigationList.item(2)
        item.setText(_translate("PreferencesView", "MPV Settings"))
        item = self.navigationList.item(3)
        item.setText(_translate("PreferencesView", "QC Document"))
        item = self.navigationList.item(4)
        item.setText(_translate("PreferencesView", "Language"))
        item = self.navigationList.item(5)
        item.setText(_translate("PreferencesView", "About"))
        self.navigationList.setSortingEnabled(__sortingEnabled)
        self.label_2.setText(_translate("PreferencesView", "General"))
        self.authorLabel.setText(_translate("PreferencesView", "Nick name"))
        self.label_3.setText(_translate("PreferencesView", "Comment types"))
        self.label_9.setText(_translate("PreferencesView", "Appearance"))
        self.label_10.setText(_translate("PreferencesView", "Window Title"))
        self.window_title_combo_box.setItemText(0, _translate("PreferencesView", "Display default title"))
        self.window_title_combo_box.setItemText(1, _translate("PreferencesView", "Display video title"))
        self.window_title_combo_box.setItemText(2, _translate("PreferencesView", "Display video path"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tabGeneral), _translate("PreferencesView", "General"))
        self.label_5.setText(_translate("PreferencesView", "MPV Settings"))
        self.label_8.setText(_translate("PreferencesView", "Changes will be applied after restart."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("PreferencesView", "mpv.conf"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("PreferencesView", "input.conf"))
        self.label_4.setText(_translate("PreferencesView", "QC Document"))
        self.autoSaveEnabledCheckBox_4.setText(_translate("PreferencesView", "Auto save enabled"))
        self.label_6.setText(_translate("PreferencesView", "each"))
        self.autosaveTimeUnit_4.setText(_translate("PreferencesView", "seconds"))
        self.saveNickNameCheckBox.setText(_translate("PreferencesView", "Save nick name to QC document"))
        self.saveVideoPathCheckBox.setText(_translate("PreferencesView", "Save video path to QC document"))
        self.label.setText(_translate("PreferencesView", "Language"))
        self.label_7.setText(_translate("PreferencesView", "Language"))
        self.comboBox.setItemText(0, _translate("PreferencesView", "English"))
        self.comboBox.setItemText(1, _translate("PreferencesView", "German"))
        self.label_11.setText(_translate("PreferencesView", "About"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.sdasd), _translate("PreferencesView", "About"))
        self.creditsBrowser.setHtml(_translate("PreferencesView",
                                               "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                               "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                               "p, li { white-space: pre-wrap; }\n"
                                               "</style></head><body style=\" font-family:\'Fira Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">mpv<br />GPLv2+ &lt;mpv.io&gt; </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">libmpv build<br />GPLv3 &lt;lachs0r&gt; </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">python-mpv<br />AGPLv3 &lt;jaseg&gt; </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">PyQt5<br />GPLv3 &lt;Riverbank Computing Limited&gt; </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Qt5<br />LGPLv3 &lt;The Qt Company Ltd and other contributors&gt; </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Requests<br />Apache Version 2 &lt;Kenneth Reitz&gt; </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">KDE Framework<br />LGPLv3&lt;KDE Community&gt; </p></body></html>"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_3), _translate("PreferencesView", "Credits"))
        self.licenceBrowser.setHtml(_translate("PreferencesView",
                                               "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                               "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                               "p, li { white-space: pre-wrap; }\n"
                                               "</style></head><body style=\" font-family:\'Fira Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
                                               "<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">GNU GENERAL PUBLIC LICENSE<br />Version 3, 29 June 2007</p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Copyright (C) 2007 Free Software Foundation, Inc. &lt;http://fsf.org/&gt; <br />Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed.</p>\n"
                                               "<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Preamble </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The GNU General Public License is a free, copyleft license for software and other kinds of works. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The licenses for most software and other practical works are designed to take away your freedom to share and change the works. By contrast, the GNU General Public License is intended to guarantee your freedom to share and change all versions of a program--to make sure it remains free software for all its users. We, the Free Software Foundation, use the GNU General Public License for most of our software; it applies also to any other work released this way by its authors. You can apply it to your programs, too. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">When we speak of free software, we are referring to freedom, not price. <br />Our General Public Licenses are designed to make sure that you have the freedom to distribute copies of free software (and charge for them if you wish), that you receive source code or can get it if you want it, that you can change the software or use pieces of it in new free programs, and that you know you can do these things. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">To protect your rights, we need to prevent others from denying you these rights or asking you to surrender the rights. Therefore, you have certain responsibilities if you distribute copies of the software, or if you modify it: responsibilities to respect the freedom of others. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">For example, if you distribute copies of such a program, whether gratis or for a fee, you must pass on to the recipients the same freedoms that you received. You must make sure that they, too, receive or can get the source code. And you must show them these terms so they know their rights. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Developers that use the GNU GPL protect your rights with two steps: (1) assert copyright on the software, and (2) offer you this License giving you legal permission to copy, distribute and/or modify it. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">For the developers\' and authors\' protection, the GPL clearly explains that there is no warranty for this free software. For both users\' and authors\' sake, the GPL requires that modified versions be marked as changed, so that their problems will not be attributed erroneously to authors of previous versions. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Some devices are designed to deny users access to install or run modified versions of the software inside them, although the manufacturer can do so. This is fundamentally incompatible with the aim of protecting users\' freedom to change the software. The systematic pattern of such abuse occurs in the area of products for individuals to use, which is precisely where it is most unacceptable. Therefore, we have designed this version of the GPL to prohibit the practice for those products. If such problems arise substantially in other domains, we stand ready to extend this provision to those domains in future versions of the GPL, as needed to protect the freedom of users. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Finally, every program is threatened constantly by software patents. States should not allow patents to restrict development and use of software on general-purpose computers, but in those that do, we wish to avoid the special danger that patents applied to a free program could make it effectively proprietary. To prevent this, the GPL assures that patents cannot be used to render the program non-free. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The precise terms and conditions for copying, distribution and modification follow. </p>\n"
                                               "<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">TERMS AND CONDITIONS </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0. Definitions. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&quot;This License&quot; refers to version 3 of the GNU General Public License. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&quot;Copyright&quot; also means copyright-like laws that apply to other kinds of works, such as semiconductor masks. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&quot;The Program&quot; refers to any copyrightable work licensed under this License. Each licensee is addressed as &quot;you&quot;. &quot;Licensees&quot; and &quot;recipients&quot; may be individuals or organizations. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">To &quot;modify&quot; a work means to copy from or adapt all or part of the work in a fashion requiring copyright permission, other than the making of an exact copy. The resulting work is called a &quot;modified version&quot; of the earlier work or a work &quot;based on&quot; the earlier work. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">A &quot;covered work&quot; means either the unmodified Program or a work based on the Program. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">To &quot;propagate&quot; a work means to do anything with it that, without permission, would make you directly or secondarily liable for infringement under applicable copyright law, except executing it on a computer or modifying a private copy. Propagation includes copying, distribution (with or without modification), making available to the public, and in some countries other activities as well. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">To &quot;convey&quot; a work means any kind of propagation that enables other parties to make or receive copies. Mere interaction with a user through a computer network, with no transfer of a copy, is not conveying. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">An interactive user interface displays &quot;Appropriate Legal Notices&quot; to the extent that it includes a convenient and prominently visible feature that (1) displays an appropriate copyright notice, and (2) tells the user that there is no warranty for the work (except to the extent that warranties are provided), that licensees may convey the work under this License, and how to view a copy of this License. If the interface presents a list of user commands or options, such as a menu, a prominent item in the list meets this criterion. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1. Source Code. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The &quot;source code&quot; for a work means the preferred form of the work for making modifications to it. &quot;Object code&quot; means any non-source form of a work. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">A &quot;Standard Interface&quot; means an interface that either is an official standard defined by a recognized standards body, or, in the case of interfaces specified for a particular programming language, one that is widely used among developers working in that language. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The &quot;System Libraries&quot; of an executable work include anything, other than the work as a whole, that (a) is included in the normal form of packaging a Major Component, but which is not part of that Major Component, and (b) serves only to enable use of the work with that Major Component, or to implement a Standard Interface for which an implementation is available to the public in source code form. A &quot;Major Component&quot;, in this context, means a major essential component (kernel, window system, and so on) of the specific operating system (if any) on which the executable work runs, or a compiler used to produce the work, or an object code interpreter used to run it. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The &quot;Corresponding Source&quot; for a work in object code form means all the source code needed to generate, install, and (for an executable work) run the object code and to modify the work, including scripts to control those activities. However, it does not include the work\'s System Libraries, or general-purpose tools or generally available free programs which are used unmodified in performing those activities but which are not part of the work. For example, Corresponding Source includes interface definition files associated with source files for the work, and the source code for shared libraries and dynamically linked subprograms that the work is specifically designed to require, such as by intimate data communication or control flow between those subprograms and other parts of the work. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The Corresponding Source need not include anything that users can regenerate automatically from other parts of the Corresponding Source. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The Corresponding Source for a work in source code form is that same work. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2. Basic Permissions. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">All rights granted under this License are granted for the term of copyright on the Program, and are irrevocable provided the stated conditions are met. This License explicitly affirms your unlimited permission to run the unmodified Program. The output from running a covered work is covered by this License only if the output, given its content, constitutes a covered work. This License acknowledges your rights of fair use or other equivalent, as provided by copyright law. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You may make, run and propagate covered works that you do not convey, without conditions so long as your license otherwise remains in force. You may convey covered works to others for the sole purpose of having them make modifications exclusively for you, or provide you with facilities for running those works, provided that you comply with the terms of this License in conveying all material for which you do not control copyright. Those thus making or running the covered works for you must do so exclusively on your behalf, under your direction and control, on terms that prohibit them from making any copies of your copyrighted material outside their relationship with you. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Conveying under any other circumstances is permitted solely under the conditions stated below. Sublicensing is not allowed; section 10 makes it unnecessary. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">3. Protecting Users\' Legal Rights From Anti-Circumvention Law. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">No covered work shall be deemed part of an effective technological measure under any applicable law fulfilling obligations under article 11 of the WIPO copyright treaty adopted on 20 December 1996, or similar laws prohibiting or restricting circumvention of such measures. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">When you convey a covered work, you waive any legal power to forbid circumvention of technological measures to the extent such circumvention is effected by exercising rights under this License with respect to the covered work, and you disclaim any intention to limit operation or modification of the work as a means of enforcing, against the work\'s users, your or third parties\' legal rights to forbid circumvention of technological measures. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">4. Conveying Verbatim Copies. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You may convey verbatim copies of the Program\'s source code as you receive it, in any medium, provided that you conspicuously and appropriately publish on each copy an appropriate copyright notice; keep intact all notices stating that this License and any non-permissive terms added in accord with section 7 apply to the code; keep intact all notices of the absence of any warranty; and give all recipients a copy of this License along with the Program. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You may charge any price or no price for each copy that you convey, and you may offer support or warranty protection for a fee. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">5. Conveying Modified Source Versions. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You may convey a work based on the Program, or the modifications to produce it from the Program, in the form of source code under the terms of section 4, provided that you also meet all of these conditions: </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:20px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">a) The work must carry prominent notices stating that you modified it, and giving a relevant date. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:20px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">b) The work must carry prominent notices stating that it is released under this License and any conditions added under section 7. This requirement modifies the requirement in section 4 to &quot;keep intact all notices&quot;. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:20px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">c) You must license the entire work, as a whole, under this License to anyone who comes into possession of a copy. This License will therefore apply, along with any applicable section 7 additional terms, to the whole of the work, and all its parts, regardless of how they are packaged. This License gives no permission to license the work in any other way, but it does not invalidate such permission if you have separately received it. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:20px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">d) If the work has interactive user interfaces, each must display Appropriate Legal Notices; however, if the Program has interactive interfaces that do not display Appropriate Legal Notices, your work need not make them do so. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">A compilation of a covered work with other separate and independent works, which are not by their nature extensions of the covered work, and which are not combined with it such as to form a larger program, in or on a volume of a storage or distribution medium, is called an &quot;aggregate&quot; if the compilation and its resulting copyright are not used to limit the access or legal rights of the compilation\'s users beyond what the individual works permit. Inclusion of a covered work in an aggregate does not cause this License to apply to the other parts of the aggregate. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">6. Conveying Non-Source Forms. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You may convey a covered work in object code form under the terms of sections 4 and 5, provided that you also convey the machine-readable Corresponding Source under the terms of this License, in one of these ways: </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:20px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">a) Convey the object code in, or embodied in, a physical product (including a physical distribution medium), accompanied by the Corresponding Source fixed on a durable physical medium customarily used for software interchange. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:20px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">b) Convey the object code in, or embodied in, a physical product (including a physical distribution medium), accompanied by a written offer, valid for at least three years and valid for as long as you offer spare parts or customer support for that product model, to give anyone who possesses the object code either (1) a copy of the Corresponding Source for all the software in the product that is covered by this License, on a durable physical medium customarily used for software interchange, for a price no more than your reasonable cost of physically performing this conveying of source, or (2) access to copy the Corresponding Source from a network server at no charge. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:20px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">c) Convey individual copies of the object code with a copy of the written offer to provide the Corresponding Source. This alternative is allowed only occasionally and noncommercially, and only if you received the object code with such an offer, in accord with subsection 6b. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:20px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">d) Convey the object code by offering access from a designated place (gratis or for a charge), and offer equivalent access to the Corresponding Source in the same way through the same place at no further charge. You need not require recipients to copy the Corresponding Source along with the object code. If the place to copy the object code is a network server, the Corresponding Source may be on a different server (operated by you or a third party) that supports equivalent copying facilities, provided you maintain clear directions next to the object code saying where to find the Corresponding Source. Regardless of what server hosts the Corresponding Source, you remain obligated to ensure that it is available for as long as needed to satisfy these requirements. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:20px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">e) Convey the object code using peer-to-peer transmission, provided you inform other peers where the object code and Corresponding Source of the work are being offered to the general public at no charge under subsection 6d. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">A separable portion of the object code, whose source code is excluded from the Corresponding Source as a System Library, need not be included in conveying the object code work. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">A &quot;User Product&quot; is either (1) a &quot;consumer product&quot;, which means any tangible personal property which is normally used for personal, family, or household purposes, or (2) anything designed or sold for incorporation into a dwelling. In determining whether a product is a consumer product, doubtful cases shall be resolved in favor of coverage. For a particular product received by a particular user, &quot;normally used&quot; refers to a typical or common use of that class of product, regardless of the status of the particular user or of the way in which the particular user actually uses, or expects or is expected to use, the product. A product is a consumer product regardless of whether the product has substantial commercial, industrial or non-consumer uses, unless such uses represent the only significant mode of use of the product. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&quot;Installation Information&quot; for a User Product means any methods, procedures, authorization keys, or other information required to install and execute modified versions of a covered work in that User Product from a modified version of its Corresponding Source. The information must suffice to ensure that the continued functioning of the modified object code is in no case prevented or interfered with solely because modification has been made. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">If you convey an object code work under this section in, or with, or specifically for use in, a User Product, and the conveying occurs as part of a transaction in which the right of possession and use of the User Product is transferred to the recipient in perpetuity or for a fixed term (regardless of how the transaction is characterized), the Corresponding Source conveyed under this section must be accompanied by the Installation Information. But this requirement does not apply if neither you nor any third party retains the ability to install modified object code on the User Product (for example, the work has been installed in ROM). </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The requirement to provide Installation Information does not include a requirement to continue to provide support service, warranty, or updates for a work that has been modified or installed by the recipient, or for the User Product in which it has been modified or installed. Access to a network may be denied when the modification itself materially and adversely affects the operation of the network or violates the rules and protocols for communication across the network. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Corresponding Source conveyed, and Installation Information provided, in accord with this section must be in a format that is publicly documented (and with an implementation available to the public in source code form), and must require no special password or key for unpacking, reading or copying. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">7. Additional Terms. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&quot;Additional permissions&quot; are terms that supplement the terms of this License by making exceptions from one or more of its conditions. Additional permissions that are applicable to the entire Program shall be treated as though they were included in this License, to the extent that they are valid under applicable law. If additional permissions apply only to part of the Program, that part may be used separately under those permissions, but the entire Program remains governed by this License without regard to the additional permissions. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">When you convey a copy of a covered work, you may at your option remove any additional permissions from that copy, or from any part of it. (Additional permissions may be written to require their own removal in certain cases when you modify the work.) You may place additional permissions on material, added by you to a covered work, for which you have or can give appropriate copyright permission. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Notwithstanding any other provision of this License, for material you add to a covered work, you may (if authorized by the copyright holders of that material) supplement the terms of this License with terms: </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:20px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">a) Disclaiming warranty or limiting liability differently from the terms of sections 15 and 16 of this License; or </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:20px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">b) Requiring preservation of specified reasonable legal notices or author attributions in that material or in the Appropriate Legal Notices displayed by works containing it; or</p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:20px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">c) Prohibiting misrepresentation of the origin of that material, or requiring that modified versions of such material be marked in reasonable ways as different from the original version; or </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:20px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">d) Limiting the use for publicity purposes of names of licensors or authors of the material; or</p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:20px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">e) Declining to grant rights under trademark law for use of some trade names, trademarks, or service marks; or </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:20px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">f) Requiring indemnification of licensors and authors of that material by anyone who conveys the material (or modified versions of it) with contractual assumptions of liability to the recipient, for any liability that these contractual assumptions directly impose on those licensors and authors. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">All other non-permissive additional terms are considered &quot;further restrictions&quot; within the meaning of section 10. If the Program as you received it, or any part of it, contains a notice stating that it is governed by this License along with a term that is a further restriction, you may remove that term. If a license document contains a further restriction but permits relicensing or conveying under this License, you may add to a covered work material governed by the terms of that license document, provided that the further restriction does not survive such relicensing or conveying. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">If you add terms to a covered work in accord with this section, you must place, in the relevant source files, a statement of the additional terms that apply to those files, or a notice indicating where to find the applicable terms. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Additional terms, permissive or non-permissive, may be stated in the form of a separately written license, or stated as exceptions; the above requirements apply either way. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">8. Termination. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You may not propagate or modify a covered work except as expressly provided under this License. Any attempt otherwise to propagate or modify it is void, and will automatically terminate your rights under this License (including any patent licenses granted under the third paragraph of section 11). </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">However, if you cease all violation of this License, then your license from a particular copyright holder is reinstated (a) provisionally, unless and until the copyright holder explicitly and finally terminates your license, and (b) permanently, if the copyright holder fails to notify you of the violation by some reasonable means prior to 60 days after the cessation. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Moreover, your license from a particular copyright holder is reinstated permanently if the copyright holder notifies you of the violation by some reasonable means, this is the first time you have received notice of violation of this License (for any work) from that copyright holder, and you cure the violation prior to 30 days after your receipt of the notice. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Termination of your rights under this section does not terminate the licenses of parties who have received copies or rights from you under this License. If your rights have been terminated and not permanently reinstated, you do not qualify to receive new licenses for the same material under section 10. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">9. Acceptance Not Required for Having Copies. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You are not required to accept this License in order to receive or run a copy of the Program. Ancillary propagation of a covered work occurring solely as a consequence of using peer-to-peer transmission to receive a copy likewise does not require acceptance. However, nothing other than this License grants you permission to propagate or modify any covered work. These actions infringe copyright if you do not accept this License. Therefore, by modifying or propagating a covered work, you indicate your acceptance of this License to do so. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">10. Automatic Licensing of Downstream Recipients. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Each time you convey a covered work, the recipient automatically receives a license from the original licensors, to run, modify and propagate that work, subject to this License. You are not responsible for enforcing compliance by third parties with this License. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">An &quot;entity transaction&quot; is a transaction transferring control of an organization, or substantially all assets of one, or subdividing an organization, or merging organizations. If propagation of a covered work results from an entity transaction, each party to that transaction who receives a copy of the work also receives whatever licenses to the work the party\'s predecessor in interest had or could give under the previous paragraph, plus a right to possession of the Corresponding Source of the work from the predecessor in interest, if the predecessor has it or can get it with reasonable efforts. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You may not impose any further restrictions on the exercise of the rights granted or affirmed under this License. For example, you may not impose a license fee, royalty, or other charge for exercise of rights granted under this License, and you may not initiate litigation (including a cross-claim or counterclaim in a lawsuit) alleging that any patent claim is infringed by making, using, selling, offering for sale, or importing the Program or any portion of it. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">11. Patents. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">A &quot;contributor&quot; is a copyright holder who authorizes use under this License of the Program or a work on which the Program is based. The work thus licensed is called the contributor\'s &quot;contributor version&quot;. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">A contributor\'s &quot;essential patent claims&quot; are all patent claims owned or controlled by the contributor, whether already acquired or hereafter acquired, that would be infringed by some manner, permitted by this License, of making, using, or selling its contributor version, but do not include claims that would be infringed only as a consequence of further modification of the contributor version. For purposes of this definition, &quot;control&quot; includes the right to grant patent sublicenses in a manner consistent with the requirements of this License. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Each contributor grants you a non-exclusive, worldwide, royalty-free patent license under the contributor\'s essential patent claims, to make, use, sell, offer for sale, import and otherwise run, modify and propagate the contents of its contributor version. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">In the following three paragraphs, a &quot;patent license&quot; is any express agreement or commitment, however denominated, not to enforce a patent (such as an express permission to practice a patent or covenant not to sue for patent infringement). To &quot;grant&quot; such a patent license to a party means to make such an agreement or commitment not to enforce a patent against the party. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">If you convey a covered work, knowingly relying on a patent license, and the Corresponding Source of the work is not available for anyone to copy, free of charge and under the terms of this License, through a publicly available network server or other readily accessible means, then you must either (1) cause the Corresponding Source to be so available, or (2) arrange to deprive yourself of the benefit of the patent license for this particular work, or (3) arrange, in a manner consistent with the requirements of this License, to extend the patent license to downstream recipients. &quot;Knowingly relying&quot; means you have actual knowledge that, but for the patent license, your conveying the covered work in a country, or your recipient\'s use of the covered work in a country, would infringe one or more identifiable patents in that country that you have reason to believe are valid. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">If, pursuant to or in connection with a single transaction or arrangement, you convey, or propagate by procuring conveyance of, a covered work, and grant a patent license to some of the parties receiving the covered work authorizing them to use, propagate, modify or convey a specific copy of the covered work, then the patent license you grant is automatically extended to all recipients of the covered work and works based on it. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">A patent license is &quot;discriminatory&quot; if it does not include within the scope of its coverage, prohibits the exercise of, or is conditioned on the non-exercise of one or more of the rights that are specifically granted under this License. You may not convey a covered work if you are a party to an arrangement with a third party that is in the business of distributing software, under which you make payment to the third party based on the extent of your activity of conveying the work, and under which the third party grants, to any of the parties who would receive the covered work from you, a discriminatory patent license (a) in connection with copies of the covered work conveyed by you (or copies made from those copies), or (b) primarily for and in connection with specific products or compilations that contain the covered work, unless you entered into that arrangement, or that patent license was granted, prior to 28 March 2007. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Nothing in this License shall be construed as excluding or limiting any implied license or other defenses to infringement that may otherwise be available to you under applicable patent law. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">12. No Surrender of Others\' Freedom. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">If conditions are imposed on you (whether by court order, agreement or otherwise) that contradict the conditions of this License, they do not excuse you from the conditions of this License. If you cannot convey a covered work so as to satisfy simultaneously your obligations under this License and any other pertinent obligations, then as a consequence you may not convey it at all. For example, if you agree to terms that obligate you to collect a royalty for further conveying from those to whom you convey the Program, the only way you could satisfy both those terms and this License would be to refrain entirely from conveying the Program. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">13. Use with the GNU Affero General Public License. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Notwithstanding any other provision of this License, you have permission to link or combine any covered work with a work licensed under version 3 of the GNU Affero General Public License into a single combined work, and to convey the resulting work. The terms of this License will continue to apply to the part which is the covered work, but the special requirements of the GNU Affero General Public License, section 13, concerning interaction through a network will apply to the combination as such. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">14. Revised Versions of this License. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The Free Software Foundation may publish revised and/or new versions of the GNU General Public License from time to time. Such new versions will be similar in spirit to the present version, but may differ in detail to address new problems or concerns. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Each version is given a distinguishing version number. If the Program specifies that a certain numbered version of the GNU General Public License &quot;or any later version&quot; applies to it, you have the option of following the terms and conditions either of that numbered version or of any later version published by the Free Software Foundation. If the Program does not specify a version number of the GNU General Public License, you may choose any version ever published by the Free Software Foundation. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">If the Program specifies that a proxy can decide which future versions of the GNU General Public License can be used, that proxy\'s public statement of acceptance of a version permanently authorizes you to choose that version for the Program. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Later license versions may give you additional or different permissions. However, no additional obligations are imposed on any author or copyright holder as a result of your choosing to follow a later version. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">15. Disclaimer of Warranty. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW. EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM &quot;AS IS&quot; WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">16. Limitation of Liability. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS), EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">17. Interpretation of Sections 15 and 16. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">If the disclaimer of warranty and limitation of liability provided above cannot be given local legal effect according to their terms, reviewing courts shall apply local law that most closely approximates an absolute waiver of all civil liability in connection with the Program, unless a warranty or assumption of liability accompanies a copy of the Program in return for a fee. </p>\n"
                                               "<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">END OF TERMS AND CONDITIONS </p>\n"
                                               "<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">How to Apply These Terms to Your New Programs </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">If you develop a new program, and you want it to be of the greatest possible use to the public, the best way to achieve this is to make it free software which everyone can redistribute and change under these terms. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">To do so, attach the following notices to the program. It is safest to attach them to the start of each source file to most effectively state the exclusion of warranty; and each file should have at least the &quot;copyright&quot; line and a pointer to where the full notice is found. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:20px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&lt;one line to give the program\'s name and a brief idea of what it does.&gt; <br />Copyright (C) &lt;year&gt; &lt;name of author&gt; </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:20px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:20px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:20px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You should have received a copy of the GNU General Public License along with this program. If not, see &lt;http://www.gnu.org/licenses/&gt;. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Also add information on how to contact you by electronic and paper mail. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">If the program does terminal interaction, make it output a short notice like this when it starts in an interactive mode: </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:20px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&lt;program&gt; Copyright (C) &lt;year&gt; &lt;name of author&gt;<br />This program comes with ABSOLUTELY NO WARRANTY; for details type `show w\'. This is free software, and you are welcome to redistribute it under certain conditions; type `show c\' for details. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The hypothetical commands `show w\' and `show c\' should show the appropriate parts of the General Public License. Of course, your program\'s commands might be different; for a GUI interface, you would use an &quot;about box&quot;. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You should also get your employer (if you work as a programmer) or school, if any, to sign a &quot;copyright disclaimer&quot; for the program, if necessary. For more information on this, and how to apply and follow the GNU GPL, see &lt;http://www.gnu.org/licenses/&gt;. </p>\n"
                                               "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The GNU General Public License does not permit incorporating your program into proprietary programs. If your program is a subroutine library, you may consider it more useful to permit linking proprietary applications with the library. If this is what you want to do, use the GNU Lesser General Public License instead of this License. But first, please read &lt;http://www.gnu.org/philosophy/why-not-lgpl.html&gt;. </p></body></html>"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_5), _translate("PreferencesView", "Licence"))
