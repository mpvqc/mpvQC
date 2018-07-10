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

from PyQt5.QtCore import QModelIndex, QAbstractItemModel, Qt, QTime, pyqtSignal
from PyQt5.QtWidgets import QWidget, QStyleOptionViewItem, QComboBox, QAbstractSpinBox, QTimeEdit, \
    QStyledItemDelegate

from src import settings
from src.gui import TIME_FORMAT, TYPEWRITER_FONT


class NotifiableItemDelegate(QStyledItemDelegate):
    """
    The parent delegate class for providing common actions for all custom delegates.
    """

    # Signal is called, after edit was done successfully (and not aborted!)
    editing_done = pyqtSignal()


class CommentTimeDelegate(NotifiableItemDelegate):
    """
    Delegate for the time column.
    """

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
        editor = QTimeEdit(parent)
        editor.setFont(TYPEWRITER_FONT)
        editor.setDisplayFormat(TIME_FORMAT)
        editor.setCurrentSection(QTimeEdit.SecondSection)
        editor.setFrame(False)
        editor.setAlignment(Qt.AlignLeft)
        editor.setButtonSymbols(QAbstractSpinBox.NoButtons)
        editor.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        editor.setKeyboardTracking(True)
        editor.setProperty("showGroupSeparator", False)
        editor.setCalendarPopup(False)
        return editor

    def setEditorData(self, editor: QWidget, index: QModelIndex):
        editor: QTimeEdit
        editor.setTime(QTime.fromString(index.model().data(index, Qt.EditRole), TIME_FORMAT))
        editor.setSelectedSection(QTimeEdit.SecondSection)

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex):
        editor: QTimeEdit
        editor.interpretText()
        model.setData(index, editor.text(), Qt.EditRole)
        self.editing_done.emit()

    def updateEditorGeometry(self, editor: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
        editor.setGeometry(option.rect)


class CommentTypeDelegate(NotifiableItemDelegate):
    """
    Delegate for the comment type column.
    """

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
        editor = QComboBox(parent)
        for ct in settings.Setting_Custom_General_COMMENT_TYPES.value:
            editor.addItem(ct)
        return editor

    def setEditorData(self, editor: QWidget, index: QModelIndex):
        editor: QComboBox = editor
        editor.setCurrentIndex(max(0, editor.findText(index.model().data(index, Qt.EditRole))))
        editor.setFont(TYPEWRITER_FONT)

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex):
        editor: QComboBox = editor
        model.setData(index, editor.currentText(), Qt.EditRole)
        self.editing_done.emit()

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
        self.editing_done.emit()
