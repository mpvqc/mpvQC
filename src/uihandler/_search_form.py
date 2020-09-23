# Copyright (C) 2016-2018 Frechdachs <frechdachs@rekt.cc>
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


from PyQt5.QtCore import Qt, QEvent, QModelIndex
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QWidget

from src.ui import Ui_SearchForm
from src.uiutil import SearchResult, SpecialCharacterValidator


class SearchHandler(QWidget):

    def __init__(self, main_handler):
        super().__init__(parent=main_handler)

        self.__latest_query = ""
        self.__latest_result: SearchResult = None
        self.__latest_match = QModelIndex()

        self.__main_handler = main_handler
        self.__widget_comments = main_handler.widget_comments

        self.__ui = Ui_SearchForm()
        self.__ui.setupUi(self)

        self.__ui.searchLineEdit.setValidator(SpecialCharacterValidator())
        self.__ui.searchLineEdit.textChanged.connect(lambda query: self.invoke_search(query=query, top_down=True))

        self.__ui.previousButton.clicked.connect(lambda b: self.invoke_search(top_down=False))
        self.__ui.nextButton.clicked.connect(lambda b: self.invoke_search(top_down=True))
        self.__ui.searchCloseButton.clicked.connect(self.hide)

    def invoke_search(self, top_down: bool, query: str = None):
        if query is None:
            query = self.__ui.searchLineEdit.text()

        result: SearchResult = self.__widget_comments.perform_search(query=query,
                                                                     top_down=top_down,
                                                                     new_query=query != self.__latest_query,
                                                                     last_index=self.__latest_match)

        self.__latest_query = query
        self.__latest_result = result
        self.__latest_match = result.match

        self.__latest_result.highlight_change_request.connect(self.__ui.searchResultLabel.setText)
        self.__latest_result.highlight_result()

    def keyPressEvent(self, e: QKeyEvent):
        key = e.key()
        mod = e.modifiers()

        if key == Qt.Key_F and mod == Qt.ControlModifier:
            if self.isHidden():
                self.show()
            else:
                self.hide()
        elif key == Qt.Key_Up and mod == Qt.NoModifier:
            pass
        elif key == Qt.Key_Down and mod == Qt.NoModifier:
            pass
        elif key == Qt.Key_Return:  # Enter
            if mod == Qt.ShiftModifier:
                self.invoke_search(top_down=False)
            elif mod == Qt.ControlModifier:
                self.__widget_comments.keyPressEvent(e)
            else:
                self.invoke_search(top_down=True)
        elif key == Qt.Key_Escape and mod == Qt.NoModifier:
            self.hide()

    def changeEvent(self, e: QEvent):
        e_type = e.type()

        if e_type == QEvent.LanguageChange:
            self.__ui.retranslateUi(None)
            if self.__latest_result:
                self.__latest_result.highlight_changed()

    def hide(self):
        if not self.isHidden():
            super(SearchHandler, self).hide()
            self.__widget_comments.setFocus()

    def show(self):
        if self.isHidden():
            super(SearchHandler, self).show()

        if not self.__ui.searchLineEdit.hasFocus():
            self.__latest_query = ""
            self.__ui.searchLineEdit.setFocus()
            self.__ui.searchLineEdit.selectAll()
