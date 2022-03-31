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
from PyQt5.QtWidgets import QInputDialog, QMenu, QActionGroup, QAction

from mpvqc import get_settings

_translate = QCoreApplication.translate


class _Settings:

    @staticmethod
    def edit_comment_types(callback: Callable):
        from mpvqc.uihandler import EditCommentTypesDialog
        EditCommentTypesDialog().exec_()
        callback()

    @staticmethod
    def edit_nickname(parent):
        s = get_settings()

        dialog = QInputDialog(parent)
        dialog.setInputMode(QInputDialog.TextInput)
        dialog.setWindowTitle(_translate("SettingsDialogNickname", "Edit Nickname"))
        dialog.setLabelText(_translate("SettingsDialogNickname", "New nickname:"))
        dialog.resize(400, 0)
        dialog.setTextValue(s.export_nickname)

        ok = dialog.exec_()
        txt = dialog.textValue().strip()

        if ok:
            if txt:
                s.export_nickname = txt
            else:
                s.export_nickname_reset()

    @staticmethod
    def setup_menu_window_title(menu: QMenu, callback: Callable):
        s = get_settings()

        def set_window_title(idx_):
            s.window_title_info = idx_
            callback()

        group = QActionGroup(menu)
        for idx, action in enumerate(menu.actions()):
            action.setChecked(idx == s.window_title_info)
            action.triggered.connect(lambda x, a=idx, f=set_window_title: f(a))

            group.addAction(action)

    @staticmethod
    def setup_dark_theme(action: QAction, callback: Callable):
        s = get_settings()

        def toggle():
            s.dark_theme = not s.dark_theme
            callback()

        action.setChecked(s.dark_theme)
        action.triggered.connect(toggle)

    @staticmethod
    def setup_languages(menu: QMenu, callback: Callable):
        s = get_settings()

        languages = {
            "English": ("en", _translate("LanguageSelection", "English")),
            "German": ("de", _translate("LanguageSelection", "German")),
            "Hebrew": ("he", _translate("LanguageSelection", "Hebrew")),
            "Italian": ("it", _translate("LanguageSelection", "Italian")),
            "Spanish": ("es", _translate("LanguageSelection", "Spanish")),
        }

        menu.clear()

        def on_language_change(loc):
            s.language = loc
            callback()

        for english, _tuple in languages.items():
            action = menu.addAction(_translate("LanguageSelection", english))
            action.setIconVisibleInMenu(True)
            action.setCheckable(True)
            action.setChecked(s.language == _tuple[0])
            action.triggered.connect(lambda a, loc=_tuple[0], f=on_language_change: f(loc))

        # If language is not found -> return English
        if menu.actions() and all(not v.isChecked() for v in menu.actions()):
            s.language = "en"
            callback()

    @staticmethod
    def edit_mpv_conf():
        from mpvqc.uihandler import EditConfDialogMpvConf

        dialog = EditConfDialogMpvConf("mpv.conf")
        dialog.setWindowTitle(_translate("SettingsDialogEditConfig", "Edit mpv.conf"))
        dialog.exec_()

    @staticmethod
    def edit_input_conf():
        from mpvqc.uihandler import EditConfDialogInputConf

        dialog = EditConfDialogInputConf("input.conf")
        dialog.setWindowTitle(_translate("SettingsDialogEditConfig", "Edit input.conf"))
        dialog.exec_()

    @staticmethod
    def setup_document(action_save_path: QAction, action_save_nickname: QAction):
        s = get_settings()

        action_save_path.setChecked(s.export_write_video_path)
        action_save_nickname.setChecked(s.export_write_nickname)

        def toggle_save_path():
            s.export_write_video_path = not s.export_write_video_path

        def toggle_save_nickname():
            s.export_write_nickname = not s.export_write_nickname

        action_save_path.toggled.connect(lambda _, f=toggle_save_path: f())
        action_save_nickname.toggled.connect(lambda _, f=toggle_save_nickname: f())

    @staticmethod
    def edit_backup_preferences(parent, qc_manager):
        from mpvqc.uihandler import DialogBackup
        DialogBackup(parent, qc_manager).exec_()

    @staticmethod
    def display_about_dialog():
        from mpvqc.uihandler import AboutDialog
        AboutDialog().exec_()


UserSettings = _Settings()
