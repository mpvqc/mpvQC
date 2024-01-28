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


from enum import Enum
from typing import List

from PyQt5.QtCore import QObject, QRegExp, Qt, QItemSelection
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QLineEdit, QListWidget, QPushButton, QListWidgetItem


class PreferenceCommentTypesWidget(QObject):
    """
    This class is used in the preference popup to create the comment type list widget.

    It combines a QLineEdit, a QListWidget and four QPushButtons to a list widgets.

    It is imitating the basic functionality of a KEditListWidget.
    """

    class __Mode(Enum):
        ADD = 0
        EDIT = 1

    def __init__(self, line_edit: QLineEdit, list_widget: QListWidget, button_add: QPushButton,
                 button_remove: QPushButton, button_up: QPushButton, button_down: QPushButton):

        """
        All of the given widgets will define the Comment Types Widget.

        :param line_edit: The line edit to enter new comment types
        :param list_widget: The list widgets to move items up and down or delete items.
        :param button_add: The button which allows to add an item
        :param button_remove: The button which allows to remove an item
        :param button_up: The button which allows to move up an item
        :param button_down: The button which allows to move down an item
        """

        super().__init__()

        self.__mode: PreferenceCommentTypesWidget.__Mode = PreferenceCommentTypesWidget.__Mode.ADD

        self.__line_edit = line_edit
        self.__line_edit.textChanged.connect(lambda txt, fun=self.__on_text_changed_line_edit: fun(txt))
        self.__line_edit.setValidator(QRegExpValidator(QRegExp("[^\\[\\]]*")))

        self.__list_widget = list_widget
        self.__list_widget.selectionModel().selectionChanged.connect(
            lambda selected, deselected, fun=self.__on_row_selection_changed: fun(selected, deselected))

        self.__button_add = button_add
        self.__button_add.clicked.connect(lambda _, fun=self.__on_pressed_button_add: fun())

        self.__button_remove = button_remove
        self.__button_remove.clicked.connect(lambda _, fun=self.__on_pressed_button_remove: fun())

        self.__button_up = button_up
        self.__button_up.clicked.connect(lambda _, fun=self.__on_pressed_button_up: fun())

        self.__button_down = button_down
        self.__button_down.clicked.connect(lambda _, fun=self.__on_pressed_button_down: fun())

    def __on_text_changed_line_edit(self, text) -> None:
        if self.__mode == PreferenceCommentTypesWidget.__Mode.ADD:
            self.__button_add.setEnabled(bool(text))
        else:
            self.__list_widget.item(self.__get_selected_row()).setText(self.__line_edit.text())

    def __on_pressed_button_add(self) -> None:
        self.__add_item(self.__line_edit.text())
        self.__line_edit.clear()
        self.__list_widget.selectionModel().clearSelection()
        self.__line_edit.setFocus()

    def __on_pressed_button_remove(self) -> None:
        self.__list_widget.model().removeRows(self.__get_selected_row(), 1)
        self.__list_widget.selectionModel().clearSelection()
        self.__line_edit.clear()

    def __on_pressed_button_up(self) -> None:
        idx: int = self.__get_selected_row()
        itm = self.__list_widget.takeItem(idx)
        self.__list_widget.insertItem(idx - 1, itm)
        self.__list_widget.setCurrentRow(idx - 1)

    def __on_pressed_button_down(self) -> None:
        idx: int = self.__get_selected_row()
        itm = self.__list_widget.takeItem(idx)
        self.__list_widget.insertItem(idx + 1, itm)
        self.__list_widget.setCurrentRow(idx + 1)

    def __add_item(self, text) -> None:
        item = QListWidgetItem(text)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.__list_widget.insertItem(0, item)

    def __get_selected_row(self) -> int:
        return self.__list_widget.selectionModel().selectedRows()[0].row()

    def __get_selected_item(self) -> QListWidgetItem:
        return self.__list_widget.item(self.__get_selected_row())

    def __on_row_selection_changed(self, selected: QItemSelection, deselected: QItemSelection) -> None:
        is_valid_selected = bool(selected)

        if is_valid_selected:
            self.__mode = PreferenceCommentTypesWidget.__Mode.EDIT
            self.__line_edit.setText(self.__get_selected_item().text())
            self.__line_edit.setFocus()
        else:
            self.__mode = PreferenceCommentTypesWidget.__Mode.ADD

        self.__button_remove.setEnabled(is_valid_selected)
        self.__button_up.setEnabled(is_valid_selected and selected.indexes()[0].row() != 0)
        self.__button_down.setEnabled(
            is_valid_selected and selected.indexes()[0].row() != self.__list_widget.model().rowCount() - 1)

    def remove_focus(self) -> None:
        """
        Will remove the focus from the line edit.
        """

        if self.__list_widget.selectionModel().selectedIndexes():
            self.__list_widget.clearSelection()
            self.__line_edit.clear()

            for btn in [self.__button_add, self.__button_remove, self.__button_up, self.__button_down]:
                btn.setEnabled(False)

    def items(self) -> List[str]:
        """
        Returns the items of the list widgets.
        """

        ret_list = []
        for row in range(0, self.__list_widget.count()):
            content = self.__list_widget.item(row).text()
            ret_list.append(str(content))

        return ret_list
