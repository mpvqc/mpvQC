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


from PyQt5.QtCore import QModelIndex, QAbstractItemModel, Qt, QTime, pyqtSignal, QSize
from PyQt5.QtWidgets import QWidget, QStyleOptionViewItem, QComboBox, QAbstractSpinBox, QTimeEdit, \
    QStyledItemDelegate

from mpvqc import get_settings
from mpvqc.uiutil._utils import SpecialCharacterValidator

# Time format
TIME_FORMAT = "HH:mm:ss"


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
        editor.setDisplayFormat(TIME_FORMAT)
        editor.setCurrentSection(QTimeEdit.SecondSection)
        editor.setFrame(False)
        editor.setAlignment(Qt.AlignCenter)
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
        for ct in get_settings().comment_types:
            editor.addItem(ct)
        return editor

    def setEditorData(self, editor: QWidget, index: QModelIndex):
        editor: QComboBox = editor
        editor.setCurrentIndex(max(0, editor.findText(index.model().data(index, Qt.EditRole))))

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex):
        editor: QComboBox = editor
        model.setData(index, editor.currentText(), Qt.EditRole)
        self.editing_done.emit()

    def updateEditorGeometry(self, editor: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
        editor.setGeometry(option.rect)

    # noinspection PyTypeChecker
    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex):
        editor: QComboBox = self.createEditor(self.parent(), option, index)
        size_hint = editor.sizeHint()
        return QSize(size_hint.width() + editor.iconSize().width(), size_hint.height())


class CommentNoteDelegate(NotifiableItemDelegate):
    """
    Delegate for the comment note column.
    """

    _VALIDATOR = SpecialCharacterValidator()

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
        editor = super(CommentNoteDelegate, self).createEditor(parent, option, index)
        editor.setValidator(CommentNoteDelegate._VALIDATOR)
        return editor

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex):
        super(CommentNoteDelegate, self).setModelData(editor, model, index)
        self.editing_done.emit()
