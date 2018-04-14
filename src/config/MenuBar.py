from abc import ABCMeta, abstractmethod
from enum import Enum

from PyQt5.QtWidgets import QAction, QMenu


class MenuBarJsonKey(Enum):
    MENU_FILE: str = "menu_file"
    MENU_VIDEO: str = "menu_video"
    MENU_OPTIONS: str = "menu_options"
    MENU_HELP: str = "menu_help"

    SUBMENU_THEME: str = "submenu_theme"
    SUBMENU_LANGUAGE: str = "submenu_language"

    LANGUAGE_KEY_MENU_FILE: str = "key_language_menu_file"
    LANGUAGE_KEY_MENU_VIDEO: str = "key_language_menu_video"
    LANGUAGE_KEY_MENU_OPTIONS: str = "key_language_menu_options"
    LANGUAGE_KEY_MENU_HELP: str = "key_language_menu_help"


class MenuBarActionKey(Enum):
    ACTION_NEW_QC_DOCUMENT: str = "new_qc_document"
    ACTION_OPEN_QC_DOCUMENT: str = "open_qc_document"
    ACTION_SAVE_QC_DOCUMENT: str = "save_qc_document"
    ACTION_SAVE_QC_DOCUMENT_AS: str = "save_qc_document_as"
    ACTION_EXIT: str = "exit"

    ACTION_OPEN_VIDEO_FILE: str = "open_video_file"
    ACTION_OPEN_NETWORK_STREAM: str = "open_network_stream"
    ACTION_RESIZE_VIDEO_TO_ITS_ORIGINAL_RESOLUTION: str = "resize_video_to_its_original_resolution"

    ACTION_NICKNAME: str = "nickname"
    ACTION_COMMENT_TYPES: str = "comment_types"
    ACTION_AUTOSAVE_INTERVAL: str = "autosave_interval"
    ACTION_WRITE_VIDEO_PATH_TO_QC_DOCUMENT: str = "write_video_path_to_qc_document"
    ACTION_FONT: str = "font"
    ACTION_MONOSPACE_FONT: str = "monospace_font"
    ACTION_THEME: str = "theme"
    ACTION_LANGUAGE: str = "language"
    ACTION_EDIT_INPUTCONF: str = "edit_input.conf"
    ACTION_EDIT_MPVCONF: str = "edit_mpv.conf"
    ACTION_RESTORE_DEFAULT_CONFIGURATION: str = "restore_default_configuration"

    ACTION_CHECK_FOR_UPDATES: str = "check_for_updates"
    ACTION_ABOUT_QT: str = "about_qt"
    ACTION_ABOUT_MPV: str = "about_mpvqc"


class MenuBarTheme(Enum):
    SYSTEM = 0,
    FUSION = 1,
    FUSION_DARK = 2


class MenuBarLanguage(Enum):
    ENGLISH = 0,
    GERMAN = 1


class MenuBarActionInvoke:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.write_video_path_to_document: bool = True

    @abstractmethod
    def get_checked_write_video_path_to_qc_document(self) -> bool:
        # raise NotImplementedError
        return True
        pass

    @abstractmethod
    def get_active_theme(self) -> MenuBarTheme:
        """ Will select item (single selection), will set selected theme. """

        print("SETUP MENU THEMES")
        # raise NotImplementedError
        return MenuBarTheme.SYSTEM

    @abstractmethod
    def get_active_language(self) -> MenuBarLanguage:
        """ Will select item (single selection), will set selected language. """
        print("SETUP LANGUAGE")
        # raise NotImplementedError

        return MenuBarLanguage.ENGLISH

    @abstractmethod
    def on_new_qc_document_pressed(self):
        # raise NotImplementedError
        print("NEW_QC")

    @abstractmethod
    def on_open_qc_document_pressed(self):
        # raise NotImplementedError
        print("OPEN_DOC")

    @abstractmethod
    def on_save_qc_document_pressed(self): raise NotImplementedError

    @abstractmethod
    def on_save_qc_document_as_pressed(self): raise NotImplementedError

    @abstractmethod
    def on_exit_pressed(self):
        # raise NotImplementedError
        print("EXIT_PRESSED")

    @abstractmethod
    def on_open_video_file_pressed(self): raise NotImplementedError

    @abstractmethod
    def on_open_network_stream_pressed(self): raise NotImplementedError

    @abstractmethod
    def on_resize_video_to_its_original_resolution_pressed(self): raise NotImplementedError

    @abstractmethod
    def on_nickname_pressed(self): raise NotImplementedError

    @abstractmethod
    def on_comment_types_pressed(self): raise NotImplementedError

    @abstractmethod
    def on_autosave_interval_pressed(self): raise NotImplementedError

    @abstractmethod
    def on_write_video_path_to_qc_document_pressed(self): raise NotImplementedError

    @abstractmethod
    def on_font_pressed(self): raise NotImplementedError

    @abstractmethod
    def on_monospace_font_pressed(self): raise NotImplementedError

    @abstractmethod
    def on_edit_inputconf_pressed(self): raise NotImplementedError

    @abstractmethod
    def on_edit_mpv_conf_pressed(self): raise NotImplementedError

    @abstractmethod
    def on_restore_default_configuration_pressed(self): raise NotImplementedError

    @abstractmethod
    def on_check_for_updates_pressed(self): raise NotImplementedError

    @abstractmethod
    def on_about_qt_pressed(self): raise NotImplementedError

    @abstractmethod
    def on_about_mpvqc_pressed(self): raise NotImplementedError

    @abstractmethod
    def on_theme_selected(self, theme: MenuBarTheme):
        # raise NotImplementedError

        print("THEME {}".format(theme.name))
        pass

    @abstractmethod
    def on_language_selected(self, language: MenuBarLanguage):
        # raise NotImplementedError

        print("LANGUAGE {}".format(language.name))
        pass

    @abstractmethod
    def on_checked_write_video_path_to_qc_document_selected(self, status: bool):
        print("WRITE PATH {}".format(status))
        pass

    def error_occurred(self, here):
        print("Error occurred: ", here)
