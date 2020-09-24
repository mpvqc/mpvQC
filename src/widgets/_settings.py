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

from src import settings

_translate = QCoreApplication.translate


class _Settings:

    @staticmethod
    def edit_comment_types(widget_context_menu):
        from src.uihandler import EditCommentTypesDialog
        EditCommentTypesDialog().exec_()
        widget_context_menu.update_entries()

    @staticmethod
    def edit_nickname(parent):
        s = settings.Setting_Custom_General_NICKNAME

        dialog = QInputDialog(parent)
        dialog.setInputMode(QInputDialog.TextInput)
        dialog.setWindowTitle(_translate("SettingsDialogNickname", "Edit Nickname"))
        dialog.setLabelText(_translate("SettingsDialogNickname", "New nickname:"))
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
            action.setChecked(idx == s.value)
            action.triggered.connect(lambda x, a=idx, f=set_window_title: f(a))

            group.addAction(action)

    @staticmethod
    def setup_dark_theme(action: QAction, callback: Callable):
        s = settings.Setting_Custom_Appearance_General_DARK_THEME

        def toggle():
            s.value = not s.value
            callback()

        action.setChecked(s.value)
        action.triggered.connect(toggle)

    @staticmethod
    def setup_languages(menu: QMenu, callback: Callable):
        s = settings.Setting_Custom_Language_LANGUAGE

        languages = {
            "English": ("en", _translate("LanguageSelection", "English")),
            "German": ("de", _translate("LanguageSelection", "German")),
            "Italian": ("it", _translate("LanguageSelection", "Italian"))
        }

        menu.clear()

        def on_language_change(loc):
            s.value = loc
            callback()

        for english, _tuple in languages.items():
            action = menu.addAction(_translate("LanguageSelection", english))
            action.setIconVisibleInMenu(True)
            action.setCheckable(True)
            action.setChecked(s.value == _tuple[0])
            action.triggered.connect(lambda a, loc=_tuple[0], f=on_language_change: f(loc))

        # If language is something other than 'en', 'de', 'it'
        if menu.actions() and all(not v.isChecked() for v in menu.actions()):
            s.value = "en"
            callback()

    @staticmethod
    def edit_mpv_conf():
        from src.uihandler import EditConfDialog

        dialog = EditConfDialog(settings.Setting_Custom_Configuration_MPV, title="mpv.conf")
        dialog.setWindowTitle(_translate("SettingsDialogEditConfig", "Edit mpv.conf"))

        if dialog.exec_():
            settings.save()

    @staticmethod
    def edit_input_conf():
        from src.uihandler import EditConfDialog

        dialog = EditConfDialog(settings.Setting_Custom_Configuration_INPUT, title="input.conf")
        dialog.setWindowTitle(_translate("SettingsDialogEditConfig", "Edit input.conf"))

        if dialog.exec_():
            settings.save()

    @staticmethod
    def setup_document(action_save_path: QAction, action_save_nickname: QAction):
        s_save_path = settings.Setting_Custom_QcDocument_WRITE_VIDEO_PATH_TO_FILE
        s_save_nick = settings.Setting_Custom_QcDocument_WRITE_NICK_TO_FILE

        action_save_path.setChecked(s_save_path.value)
        action_save_nickname.setChecked(s_save_nick.value)

        def toggle(settings_obj):
            settings_obj.value = not settings_obj.value

        action_save_path.toggled.connect(lambda _, settings_obj=s_save_path, f=toggle: f(settings_obj))
        action_save_nickname.toggled.connect(lambda _, settings_obj=s_save_nick, f=toggle: f(settings_obj))

    @staticmethod
    def setup_document_backup(action: QAction, callback: Callable):
        s = settings.Setting_Custom_QcDocument_AUTOSAVE_ENABLED

        def toggle():
            s.value = not s.value
            callback()

        action.setChecked(s.value)
        action.triggered.connect(toggle)

    @staticmethod
    def edit_document_backup_interval(parent, callback: Callable):
        s = settings.Setting_Custom_QcDocument_AUTOSAVE_INTERVAL

        dialog = QInputDialog(parent)
        dialog.setInputMode(QInputDialog.IntInput)
        dialog.setWindowTitle(_translate("SettingsDialogBackupInterval", "Set Backup Interval"))
        dialog.setLabelText(_translate("SettingsDialogBackupInterval", "Set backup interval in seconds:"))
        dialog.setIntMinimum(15)
        dialog.setIntMaximum(3600)
        dialog.setIntValue(s.value)
        dialog.resize(400, 0)

        ok = dialog.exec_()
        interval = dialog.intValue()

        if ok:
            if interval:
                s.value = interval
                callback()
            else:
                s.reset()

    @staticmethod
    def display_about_dialog():
        from src.uihandler import AboutDialog
        AboutDialog().exec_()


UserSettings = _Settings()
