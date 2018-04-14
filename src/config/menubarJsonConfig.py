import json
from typing import List

from PyQt5.QtWidgets import QMainWindow, QMenu, QAction, QActionGroup

from src.config.MenuBar import MenuBarActionInvoke, MenuBarJsonKey, MenuBarActionKey, MenuBarTheme, MenuBarLanguage

MENUBAR_CONFIG_FILE: str = "config/menubar.json"


class MBItem:

    def __init__(self,
                 name: str,
                 checkable: bool,
                 shortcut: str,
                 key_action: str,
                 key_language: str,
                 menu_order: int,
                 enabled: bool,
                 is_menu: bool):
        """ Create an object of a Menu Bar Action. """

        self.name: str = name
        self.checkable: bool = checkable
        self.shortcut: str = shortcut
        self.key_action: str = key_action
        self.key_language: str = key_language
        self.menu_order: int = menu_order
        self.enabled: bool = enabled
        self.is_menu: bool = is_menu


class MBSubItem:
    def __init__(self, name: str, enabled: bool):
        self.name = name
        self.enabled = enabled


class MenubarJsonConfig:
    def __init__(self):
        """ JsonConfigLoader is the access point to all hard coded config settings. """

        with open(MENUBAR_CONFIG_FILE) as json_data:
            json_settings_file = json.load(json_data)

        self.menubar_file = MenubarJsonConfig.__parse_mb_item(json_file=json_settings_file,
                                                              json_key=MenuBarJsonKey.MENU_FILE)
        self.menubar_video = MenubarJsonConfig.__parse_mb_item(json_file=json_settings_file,
                                                               json_key=MenuBarJsonKey.MENU_VIDEO)
        self.menubar_options = MenubarJsonConfig.__parse_mb_item(json_file=json_settings_file,
                                                                 json_key=MenuBarJsonKey.MENU_OPTIONS)
        self.menubar_help = MenubarJsonConfig.__parse_mb_item(json_file=json_settings_file,
                                                              json_key=MenuBarJsonKey.MENU_HELP)

        self.submenu_theme = MenubarJsonConfig.__parse_submenu_item(json_file=json_settings_file,
                                                                    json_key=MenuBarJsonKey.SUBMENU_THEME)
        self.submenu_language = MenubarJsonConfig.__parse_submenu_item(json_file=json_settings_file,
                                                                       json_key=MenuBarJsonKey.SUBMENU_LANGUAGE)

        self.menubar_title_file = json_settings_file[MenuBarJsonKey.LANGUAGE_KEY_MENU_FILE.value]
        self.menubar_title_video = json_settings_file[MenuBarJsonKey.LANGUAGE_KEY_MENU_VIDEO.value]
        self.menubar_title_options = json_settings_file[MenuBarJsonKey.LANGUAGE_KEY_MENU_OPTIONS.value]
        self.menubar_title_help = json_settings_file[MenuBarJsonKey.LANGUAGE_KEY_MENU_HELP.value]

    @staticmethod
    def __parse_mb_item(json_file, json_key: MenuBarJsonKey) -> List[MBItem]:
        """
        Takes the json_file and returns all items found by json_key.

        :rtype: List[MBItem]
        """

        ret_list_mb_action: List[MBItem] = []

        for item in json_file[json_key.value]:
            ret_list_mb_action.append(MBItem(**item))

        return ret_list_mb_action

    @staticmethod
    def __parse_submenu_item(json_file, json_key: MenuBarJsonKey) -> List[MBSubItem]:
        ret_list_mb_sub_items: List[MBSubItem] = []

        for item in json_file[json_key.value]:
            ret_list_mb_sub_items.append(MBSubItem(**item))

        return ret_list_mb_sub_items


class MenuBarLoader:

    def __init__(self, action_receiver: MenuBarActionInvoke, main_window: QMainWindow):
        self.receiver: MenuBarActionInvoke = action_receiver
        self.main_window = main_window
        self.mjc = MenubarJsonConfig()

    def load_menu_bar(self) -> List[QMenu]:
        mn_file = self.__create_menu(title=self.mjc.menubar_title_file,
                                     items=self.mjc.menubar_file)
        mn_video = self.__create_menu(title=self.mjc.menubar_title_video,
                                      items=self.mjc.menubar_video)
        mn_options = self.__create_menu(title=self.mjc.menubar_title_options,
                                        items=self.mjc.menubar_options)
        mn_help = self.__create_menu(title=self.mjc.menubar_title_help,
                                     items=self.mjc.menubar_help)

        return [mn_file, mn_video, mn_options, mn_help]

    def __create_menu(self, title: str, items: List[MBItem]) -> QMenu:
        items.sort(key=lambda x: x.menu_order)
        ret_menu = QMenu(title=title, parent=self.main_window)

        index = 0
        for item in items:
            while index < item.menu_order:
                ret_menu.addSeparator()
                index += 1

            if item.is_menu:
                qitem = QMenu(item.key_language, self.main_window)

                MenuBarLoader.__setup_sub_menu_menu_items(receiver=self.receiver,
                                                          key_action=item.key_action,
                                                          mjc=self.mjc,
                                                          q_menu=qitem,
                                                          parent=self.main_window)

                ret_menu.addMenu(qitem)
            else:
                qitem = QAction(item.key_language, self.main_window)

                qitem.setShortcut(item.shortcut)

                action = MenuBarLoader.__setup_action(receiver=self.receiver,
                                                      key_action=item.key_action)

                if item.checkable:
                    qitem.setCheckable(True)

                    action = MenuBarLoader.__setup_checkable_action(receiver=self.receiver,
                                                                    key_action=item.key_action,
                                                                    qitem=qitem)

                qitem.triggered.connect(action)

                ret_menu.addAction(qitem)

            qitem.setDisabled(not item.enabled)
            index += 1

        return ret_menu

    @staticmethod
    def __setup_action(receiver: MenuBarActionInvoke,
                       key_action: str):

        def func(x: str):
            return {
                MenuBarActionKey.ACTION_NEW_QC_DOCUMENT.value:
                    lambda c, fun=receiver.on_new_qc_document_pressed: fun(),

                MenuBarActionKey.ACTION_OPEN_QC_DOCUMENT.value:
                    lambda c, fun=receiver.on_open_qc_document_pressed: fun(),

                MenuBarActionKey.ACTION_SAVE_QC_DOCUMENT.value:
                    lambda c, fun=receiver.on_save_qc_document_pressed: fun(),

                MenuBarActionKey.ACTION_SAVE_QC_DOCUMENT_AS.value:
                    lambda c, fun=receiver.on_save_qc_document_as_pressed: fun(),

                MenuBarActionKey.ACTION_EXIT.value:
                # lambda c, fun=receiver.error_occurred, arg1=key_action: fun(arg1),
                    lambda c, fun=receiver.on_exit_pressed: fun(),

                MenuBarActionKey.ACTION_OPEN_VIDEO_FILE.value:
                    lambda c, fun=receiver.on_open_video_file_pressed: fun(),

                MenuBarActionKey.ACTION_OPEN_NETWORK_STREAM.value:
                    lambda c, fun=receiver.on_open_network_stream_pressed: fun(),

                MenuBarActionKey.ACTION_RESIZE_VIDEO_TO_ITS_ORIGINAL_RESOLUTION.value:
                    lambda c, fun=receiver.on_resize_video_to_its_original_resolution_pressed: fun(),

                MenuBarActionKey.ACTION_NICKNAME.value:
                    lambda c, fun=receiver.on_nickname_pressed: fun(),

                MenuBarActionKey.ACTION_COMMENT_TYPES.value:
                    lambda c, fun=receiver.on_comment_types_pressed: fun(),

                MenuBarActionKey.ACTION_AUTOSAVE_INTERVAL.value:
                    lambda c, fun=receiver.on_autosave_interval_pressed: fun(),

                MenuBarActionKey.ACTION_WRITE_VIDEO_PATH_TO_QC_DOCUMENT.value:
                    lambda c, fun=receiver.on_write_video_path_to_qc_document_pressed: fun(),

                MenuBarActionKey.ACTION_FONT.value:
                    lambda c, fun=receiver.on_font_pressed: fun(),

                MenuBarActionKey.ACTION_MONOSPACE_FONT.value:
                    lambda c, fun=receiver.on_monospace_font_pressed: fun(),

                # MenuBarActionKey.ACTION_THEME.value:
                #     lambda c, fun=receiver.on_theme_pressed: fun(),
                #
                # MenuBarActionKey.ACTION_LANGUAGE.value:
                #     lambda c, fun=receiver.on_language_pressed: fun(),

                MenuBarActionKey.ACTION_EDIT_INPUTCONF.value:
                    lambda c, fun=receiver.on_edit_inputconf_pressed: fun(),

                MenuBarActionKey.ACTION_EDIT_MPVCONF.value:
                    lambda c, fun=receiver.on_edit_mpv_conf_pressed: fun(),

                MenuBarActionKey.ACTION_RESTORE_DEFAULT_CONFIGURATION.value:
                    lambda c, fun=receiver.on_restore_default_configuration_pressed: fun(),

                MenuBarActionKey.ACTION_CHECK_FOR_UPDATES.value:
                    lambda c, fun=receiver.on_check_for_updates_pressed: fun(),

                MenuBarActionKey.ACTION_ABOUT_QT.value:
                    lambda c, fun=receiver.on_about_qt_pressed: fun(),

                MenuBarActionKey.ACTION_ABOUT_MPV.value:
                    lambda c, fun=receiver.on_about_mpvqc_pressed: fun()

            }.get(x, lambda c, fun=receiver.error_occurred, arg1=key_action: fun(arg1))

        return func(key_action)

    @staticmethod
    def __setup_checkable_action(receiver: MenuBarActionInvoke,
                                 key_action,
                                 qitem: QAction):

        return {

            MenuBarActionKey.ACTION_WRITE_VIDEO_PATH_TO_QC_DOCUMENT.value:
                lambda c, fun=receiver.on_checked_write_video_path_to_qc_document_selected, arg1=qitem:
                fun(arg1.isChecked())

        }.get(key_action, lambda c, fun=receiver.error_occurred, arg1=key_action: fun(arg1))

    @staticmethod
    def __setup_sub_menu_menu_items(receiver: MenuBarActionInvoke,
                                    key_action,
                                    mjc: MenubarJsonConfig,
                                    q_menu: QMenu,
                                    parent):

        if key_action == MenuBarActionKey.ACTION_THEME.value:
            theme = receiver.get_active_theme().name
            MenuBarLoader.__insert_sub_menu(items=mjc.submenu_theme,
                                            receiver=receiver,
                                            q_menu=q_menu,
                                            parent=parent,
                                            invoke=theme)

        elif key_action == MenuBarActionKey.ACTION_LANGUAGE.value:
            language = receiver.get_active_language().name
            MenuBarLoader.__insert_sub_menu(items=mjc.submenu_language,
                                            receiver=receiver,
                                            q_menu=q_menu,
                                            parent=parent,
                                            invoke=language)
        else:
            receiver.error_occurred(key_action)

    @staticmethod
    def __insert_sub_menu(items: List[MBSubItem],
                          receiver: MenuBarActionInvoke,
                          q_menu: QMenu,
                          parent,
                          invoke: str):

        action_group = QActionGroup(parent)

        for item in items:
            action = QAction(item.name)
            action.setCheckable(True)

            item_name_upper = item.name.upper()

            on_click = MenuBarLoader.__setup_sub_action(receiver=receiver,
                                                        sub_item_name=item_name_upper)
            action.triggered.connect(on_click)

            action_group.addAction(action)

            if invoke == item_name_upper:
                on_click(item_name_upper)
                action.setChecked(True)

            q_menu.addAction(action)

    @staticmethod
    def __setup_sub_action(receiver: MenuBarActionInvoke, sub_item_name: str):

        def func(x: str):
            return {

                MenuBarTheme.SYSTEM.name:
                    lambda c, fun=receiver.on_theme_selected, arg1=MenuBarTheme.SYSTEM: fun(arg1),

                MenuBarTheme.FUSION.name:
                    lambda c, fun=receiver.on_theme_selected, arg1=MenuBarTheme.FUSION: fun(arg1),

                MenuBarTheme.FUSION_DARK.name:
                    lambda c, fun=receiver.on_theme_selected, arg1=MenuBarTheme.FUSION_DARK: fun(arg1),

                MenuBarLanguage.ENGLISH.name:
                    lambda c, fun=receiver.on_language_selected, arg1=MenuBarLanguage.ENGLISH: fun(arg1),

                MenuBarLanguage.GERMAN.name:
                    lambda c, fun=receiver.on_language_selected, arg1=MenuBarLanguage.GERMAN: fun(arg1)

            }.get(x, lambda c, fun=receiver.error_occurred, arg1=sub_item_name: fun(arg1))

        return func(sub_item_name)
