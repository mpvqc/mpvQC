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


from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from src import get_settings
from src.ui import Ui_CommentTypesDialog


class EditCommentTypesDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.__ui = Ui_CommentTypesDialog()
        self.__ui.setupUi(self)

        self.reset_button = self.__ui.buttonBox.addButton(QDialogButtonBox.Reset)
        self.reset_button.clicked.connect(self.reset)

        from src.widgets import PreferenceCommentTypesWidget

        self.widget = PreferenceCommentTypesWidget(self.__ui.lineEdit,
                                                   self.__ui.listWidget,
                                                   self.__ui.buttonAdd,
                                                   self.__ui.buttonRemove,
                                                   self.__ui.buttonUp,
                                                   self.__ui.buttonDown)

        for ct in get_settings().comment_types:
            self.__ui.listWidget.addItem(ct)

    def accept(self):
        """
        Action when apply button is pressed.
        """

        get_settings().comment_types = self.widget.items()
        super(EditCommentTypesDialog, self).accept()

    def reset(self):
        self.__ui.listWidget.clear()

        for ct in get_settings().comment_types_default():
            self.__ui.listWidget.addItem(ct)

    def mousePressEvent(self, mouse_ev: QMouseEvent):
        """
        On mouse pressed event (pressed anywhere except the comment type widgets)
        the focus needs to be removed from the comment type widgets.
        """

        super().mousePressEvent(mouse_ev)
        self.widget.remove_focus()
