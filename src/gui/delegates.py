from PyQt5.QtCore import QModelIndex, QAbstractItemModel, Qt, QCoreApplication, QTime
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QItemDelegate, QWidget, QStyleOptionViewItem, QComboBox, QDateTimeEdit, \
    QAbstractSpinBox, QTimeEdit

from src.settings import Settings

_translate = QCoreApplication.translate
TYPEWRITER_FONT = QFont("monospace")
TYPEWRITER_FONT.setStyleHint(QFont.TypeWriter)


class CommentTypeParentDelegate(QItemDelegate):
    """
    The parent delegate class for providing common actions for all custom delegates.
    """

    TIME_FORMAT = "hh:mm:ss"

    def __init__(self, parent, after_edited=None):
        super().__init__(parent)
        self.after_edit_done = after_edited

    def _after_edit_done(self):
        if self.after_edit_done is not None:
            self.after_edit_done()


class CommentTimeDelegate(CommentTypeParentDelegate):
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
        dte.setDisplayFormat(CommentTimeDelegate.TIME_FORMAT)
        dte.setFont(TYPEWRITER_FONT)
        return dte

    def setEditorData(self, editor: QWidget, index: QModelIndex):
        editor: QDateTimeEdit
        editor.setTime(QTime.fromString(index.model().data(index, Qt.EditRole), CommentTimeDelegate.TIME_FORMAT))

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex):
        editor: QDateTimeEdit
        model.setData(index, editor.text(), Qt.EditRole)
        self._after_edit_done()

    def updateEditorGeometry(self, editor: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
        editor.setGeometry(option.rect)


class CommentTypeDelegate(CommentTypeParentDelegate):
    """
    Delegate for the comment type column.
    """

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
        combo_box = QComboBox(parent)
        for ct in Settings.Holder.COMMENT_TYPES.value:
            combo_box.addItem(ct)
        return combo_box

    def setEditorData(self, editor: QWidget, index: QModelIndex):
        editor: QComboBox = editor
        editor.setCurrentIndex(max(0, editor.findText(index.model().data(index, Qt.EditRole))))

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex):
        editor: QComboBox = editor
        model.setData(index, editor.currentText(), Qt.EditRole)
        self._after_edit_done()

    def updateEditorGeometry(self, editor: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
        editor.setGeometry(option.rect)


class CommentNoteDelegate(CommentTypeParentDelegate):
    """
    Delegate for the comment note column.
    """

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex):
        super().setModelData(editor, model, index)
        self._after_edit_done()
