# -*- coding: utf-8 -*-



# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SearchForm(object):
    def setupUi(self, SearchForm):
        SearchForm.setObjectName("SearchForm")
        SearchForm.setWindowModality(QtCore.Qt.NonModal)
        SearchForm.resize(601, 32)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SearchForm.sizePolicy().hasHeightForWidth())
        SearchForm.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtWidgets.QHBoxLayout(SearchForm)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.searchLineEdit = QtWidgets.QLineEdit(SearchForm)
        self.searchLineEdit.setMinimumSize(QtCore.QSize(250, 0))
        self.searchLineEdit.setObjectName("searchLineEdit")
        self.horizontalLayout.addWidget(self.searchLineEdit)
        self.previousButton = QtWidgets.QPushButton(SearchForm)
        self.previousButton.setEnabled(True)
        self.previousButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.previousButton.setText("")
        icon = QtGui.QIcon.fromTheme("go-up")
        self.previousButton.setIcon(icon)
        self.previousButton.setFlat(True)
        self.previousButton.setObjectName("previousButton")
        self.horizontalLayout.addWidget(self.previousButton)
        self.nextButton = QtWidgets.QPushButton(SearchForm)
        self.nextButton.setEnabled(True)
        self.nextButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.nextButton.setText("")
        icon = QtGui.QIcon.fromTheme("go-down")
        self.nextButton.setIcon(icon)
        self.nextButton.setFlat(True)
        self.nextButton.setObjectName("nextButton")
        self.horizontalLayout.addWidget(self.nextButton)
        self.searchResultLabel = QtWidgets.QLabel(SearchForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchResultLabel.sizePolicy().hasHeightForWidth())
        self.searchResultLabel.setSizePolicy(sizePolicy)
        self.searchResultLabel.setText("")
        self.searchResultLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.searchResultLabel.setObjectName("searchResultLabel")
        self.horizontalLayout.addWidget(self.searchResultLabel)
        self.searchCloseButton = QtWidgets.QPushButton(SearchForm)
        self.searchCloseButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.searchCloseButton.setText("")
        icon = QtGui.QIcon.fromTheme("window-close")
        self.searchCloseButton.setIcon(icon)
        self.searchCloseButton.setFlat(True)
        self.searchCloseButton.setObjectName("searchCloseButton")
        self.horizontalLayout.addWidget(self.searchCloseButton)

        self.retranslateUi(SearchForm)
        QtCore.QMetaObject.connectSlotsByName(SearchForm)

    def retranslateUi(self, SearchForm):
        _translate = QtCore.QCoreApplication.translate
        self.searchLineEdit.setPlaceholderText(_translate("SearchForm", "Find in comments"))

