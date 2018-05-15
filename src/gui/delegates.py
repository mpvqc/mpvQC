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

from PyQt5.QtCore import QModelIndex, QAbstractItemModel, Qt, QTime
from PyQt5.QtWidgets import QItemDelegate, QWidget, QStyleOptionViewItem, QComboBox, QDateTimeEdit, \
    QAbstractSpinBox, QTimeEdit

from src import settings
from src.gui.globals import TYPEWRITER_FONT, TIME_FORMAT


class NotifiableItemDelegate(QItemDelegate):
    """
    The parent delegate class for providing common actions for all custom delegates.
    """

    def __init__(self, parent, after_edited=None):
        super().__init__(parent)
        self.after_edit_done = after_edited

    def _after_edit_done(self):
        if self.after_edit_done is not None:
            self.after_edit_done()


class CommentTimeDelegate(NotifiableItemDelegate):
    """
    Delegate for the time column.
    """

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
        dte = QTimeEdit(parent)
        dte.setFrame(False)
        dte.setAlignment(Qt.AlignLeft)
        dte.setButtonSymbols(QAbstractSpinBox.NoButtons)
        dte.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        dte.setKeyboardTracking(True)
        dte.setProperty("showGroupSeparator", False)
        dte.setCurrentSection(QDateTimeEdit.HourSection)
        dte.setCalendarPopup(False)
        dte.setCurrentSectionIndex(0)
        dte.setDisplayFormat(TIME_FORMAT)
        dte.setFont(TYPEWRITER_FONT)
        return dte

    def setEditorData(self, editor: QWidget, index: QModelIndex):
        editor: QDateTimeEdit
        editor.setTime(QTime.fromString(index.model().data(index, Qt.EditRole), TIME_FORMAT))

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex):
        editor: QDateTimeEdit
        model.setData(index, editor.text(), Qt.EditRole)
        self._after_edit_done()

    def updateEditorGeometry(self, editor: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
        editor.setGeometry(option.rect)


class CommentTypeDelegate(NotifiableItemDelegate):
    """
    Delegate for the comment type column.
    """

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
        combo_box = QComboBox(parent)
        for ct in settings.Setting_Custom_General_COMMENT_TYPES.value:
            combo_box.addItem(ct)
        return combo_box

    def setEditorData(self, editor: QWidget, index: QModelIndex):
        editor: QComboBox = editor
        editor.setCurrentIndex(max(0, editor.findText(index.model().data(index, Qt.EditRole))))
        editor.setFont(TYPEWRITER_FONT)

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex):
        editor: QComboBox = editor
        model.setData(index, editor.currentText(), Qt.EditRole)
        self._after_edit_done()

    def updateEditorGeometry(self, editor: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
        editor.setGeometry(option.rect)

    # noinspection PyTypeChecker
    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex):
        return self.createEditor(None, option, index).sizeHint()


class CommentNoteDelegate(NotifiableItemDelegate):
    """
    Delegate for the comment note column.
    """

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex):
        super().setModelData(editor, model, index)
        self._after_edit_done()
