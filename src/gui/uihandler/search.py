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

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QWidget

from src.gui.generated.search import Ui_SearchForm
from src.gui.searchutils import SearchResult
from src.gui.utils import SpecialCharacterValidator


class SearchHandler(QWidget):

    def __init__(self, main_handler):
        super().__init__(parent=main_handler)

        self.__latest_query = ""
        self.__latest_result: SearchResult = None

        self.__main_handler = main_handler
        self.__widget_comments = main_handler.widget_comments

        self.__ui = Ui_SearchForm()
        self.__ui.setupUi(self)

        self.__ui.searchLineEdit.setValidator(SpecialCharacterValidator())
        self.__ui.searchLineEdit.textChanged.connect(lambda query: self.invoke_search(query, top_down=True))
        self.__ui.searchCloseButton.clicked.connect(self.hide)

    def invoke_search(self, query: str, top_down: bool):
        result: SearchResult = self.__widget_comments.perform_search(query, top_down, query != self.__latest_query)
        self.__latest_query = query

        # Disconnect buttons
        disconnect_signal(self.__ui.previousButton.clicked)
        disconnect_signal(self.__ui.nextButton.clicked)

        # Connect buttons -> result
        self.__ui.previousButton.clicked.connect(lambda b: self.invoke_search(query, top_down=False))
        self.__ui.nextButton.clicked.connect(lambda b: self.invoke_search(query, top_down=True))

        # Connect result <- buttons
        result.highlight_change_request.connect(self.__update_result_label)
        result.highlight_result()

        self.__latest_result = result

    def keyPressEvent(self, e: QKeyEvent):
        key = e.key()
        mod = e.modifiers()

        if key == Qt.Key_F and mod == Qt.ControlModifier:
            self.show()
        elif key == Qt.Key_Up and mod == Qt.NoModifier:
            pass
        elif key == Qt.Key_Down and mod == Qt.NoModifier:
            pass
        elif key == Qt.Key_Return:
            if mod == Qt.ShiftModifier:
                self.invoke_search(self.__ui.searchLineEdit.text(), top_down=False)
            elif mod == Qt.ControlModifier:
                self.__widget_comments.keyPressEvent(e)
            else:
                self.invoke_search(self.__ui.searchLineEdit.text(), top_down=True)
        elif key == Qt.Key_Escape and mod == Qt.NoModifier:
            self.hide()

    def hide(self):
        if not self.isHidden():
            super(SearchHandler, self).hide()
            self.__widget_comments.setFocus()

    def show(self):
        if self.isHidden():
            super(SearchHandler, self).show()

        if not self.__ui.searchLineEdit.hasFocus():
            self.__ui.searchLineEdit.setFocus()
            self.__ui.searchLineEdit.selectAll()

    def __update_result_label(self, new_text):
        self.__ui.searchResultLabel.setText(new_text)

    def changeEvent(self, e: QEvent):
        e_type = e.type()

        if e_type == QEvent.LanguageChange:
            self.__ui.retranslateUi(None)
            if self.__latest_result:
                self.__latest_result.highlight_changed()


def disconnect_signal(signal):
    try:
        signal.disconnect()
    except TypeError:
        pass
