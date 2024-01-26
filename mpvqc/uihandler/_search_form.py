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


from PyQt5.QtCore import Qt, pyqtSignal, QEvent, pyqtSlot, QCoreApplication
from PyQt5.QtGui import QKeyEvent, QMouseEvent
from PyQt5.QtWidgets import QWidget

from mpvqc.ui_loader import init_from_resources
from mpvqc.uiutil import SpecialCharacterValidator

_translate = QCoreApplication.translate


class SearchHandler(QWidget):
    sig_shown = pyqtSignal()
    sig_hidden = pyqtSignal()

    # Invoked, when the query changed. p1='The new query'
    sig_query_changed = pyqtSignal(str)
    sig_result_next = pyqtSignal()
    sig_result_previous = pyqtSignal()
    sig_edit_comment = pyqtSignal()

    def __init__(self, main_handler):
        super().__init__(parent=main_handler)
        self.__ui = init_from_resources(self, "qrc:/data/ui/search_form.ui")

        self.__ui_label_search_result = self.__ui.searchResultLabel

        self.__ui_line_edit_search = self.__ui.searchLineEdit
        self.__ui_line_edit_search.setValidator(SpecialCharacterValidator())
        self.__ui_line_edit_search.textChanged.connect(self.sig_query_changed.emit)

        self.__ui_button_previous = self.__ui.previousButton
        self.__ui_button_previous.clicked.connect(self.sig_result_previous.emit)

        self.__ui_button_next = self.__ui.nextButton
        self.__ui_button_next.clicked.connect(self.sig_result_next.emit)

        self.__ui_button_close = self.__ui.searchCloseButton
        self.__ui_button_close.clicked.connect(self.hide)

        self.__current, self.__total = -1, -1

    def keyPressEvent(self, e: QKeyEvent):
        key, mod = e.key(), e.modifiers()

        if key == Qt.Key_F and mod == Qt.ControlModifier:
            if self.isHidden():
                self.show()
            elif not self.__ui_line_edit_search.hasFocus():
                self.__ui_line_edit_search.setFocus()
            else:
                self.hide()
        elif mod == Qt.NoModifier and (key == Qt.Key_Up or key == Qt.Key_Down):
            pass
        elif key == Qt.Key_Return:  # Enter
            if mod == Qt.ShiftModifier:
                self.sig_result_previous.emit()
            elif mod == Qt.ControlModifier:
                self.sig_edit_comment.emit()
            else:
                self.sig_result_next.emit()
        elif key == Qt.Key_Escape and mod == Qt.NoModifier:
            self.hide()
        else:
            e.ignore()
        e.accept()

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        if not self.__ui_line_edit_search.hasFocus():
            previous_widget = self.previousInFocusChain()
            self.setFocus()
            previous_widget.setFocus()

    def changeEvent(self, e: QEvent):
        e_type = e.type()

        if e_type == QEvent.LanguageChange:
            self.__ui.retranslateUi(None)
            self.on_search_highlight_changed(self.__current, self.__total)

    def hide(self):
        if not self.isHidden():
            super(SearchHandler, self).hide()
            self.sig_hidden.emit()

    def show(self):
        if self.isHidden():
            super(SearchHandler, self).show()
            self.__ui_line_edit_search.setFocus()
            self.__ui_line_edit_search.selectAll()
            self.sig_shown.emit()

    @pyqtSlot(int, int)
    def on_search_highlight_changed(self, current: int, total: int):
        self.__current, self.__total = current, total
        if total > 0:
            if current == 1 and total == 1:
                info = _translate("SearchForm", "{0} comment").format(1)
            else:
                info = _translate("SearchForm", "{0} of {1} comments").format(current, total)
        elif current == 0 and total == 0:
            info = _translate("SearchForm", "Phrase not found")
        else:
            info = ""

        self.__ui_label_search_result.setText(info)
