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


from typing import Callable

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QPushButton, QAbstractItemView, QInputDialog, QMenu, \
    QActionGroup, QAction

from src import settings
from src.gui.generated.editCommentTypes import Ui_editCommentTypeDialog

_translate = QCoreApplication.translate


class _Settings:

    @staticmethod
    def edit_comment_types(widget_context_menu):
        from src.gui.uihandler.editCommentTypes import EditCommentTypesDialog
        EditCommentTypesDialog().exec_()
        widget_context_menu.update_entries()

    @staticmethod
    def edit_nickname(parent, ):
        s = settings.Setting_Custom_General_NICKNAME

        dialog = QInputDialog(parent)
        dialog.setInputMode(QInputDialog.TextInput)
        dialog.setWindowTitle(_translate("SettingsDialog", "Edit username"))
        dialog.setLabelText(_translate("SettingsDialog", "New username:"))
        dialog.resize(400, 0)
        dialog.setTextValue(s.value)

        ok = dialog.exec_()
        txt = dialog.textValue()

        if ok:
            if txt:
                s.value = txt
            else:
                s.reset()

    @staticmethod
    def setup_menu_window_title(menu: QMenu, callback: Callable):
        s = settings.Setting_Custom_Appearance_General_WINDOW_TITLE

        def set_window_title(idx_):
            s.value = idx_
            callback()

        group = QActionGroup(menu)
        for idx, action in enumerate(menu.actions()):
            action.setCheckable(True)
            action.setChecked(idx == s.value)
            action.triggered.connect(lambda x, a=idx, f=set_window_title: f(a))

            group.addAction(action)

    @staticmethod
    def setup_dark_theme(action: QAction, callback: Callable):
        s = settings.Setting_Custom_Appearance_General_DARK_THEME

        def toggle():
            s.value = not s.value
            callback()

        action.setCheckable(True)
        action.setChecked(s.value)
        action.triggered.connect(toggle)


UserSettings = _Settings()
