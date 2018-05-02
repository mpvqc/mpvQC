import sys
from os import path, getenv
from pathlib import Path

from appdirs import unicode

try:
    to_unicode = unicode
except NameError:
    to_unicode = str


class Files:
    # todo rewrite and get rid of class since its not boilerplate java :)
    __NAME_FOLDER_CONFIGURATION = "configuration"
    __NAME_FOLDER_AUTOSAVE = "autosave"

    __NAME_FILE_SETTINGS = "settings.json"
    __NAME_FILE_CONF_INPUT = "input.conf"
    __NAME_FILE_CONF_MPV = "mpv.conf"

    __DIRECTORY_ROOT_CONFIGURATION: path = None
    DIRECTORY_PROGRAM: path = None

    DIRECTORY_CONFIGURATION = None
    __DIRECTORY_AUTOSAVE = None

    FILE_CONF_INPUT = None
    FILE_CONF_MPV = None
    FILE_SETTINGS = None

    __APPLICATION_NAME = None

    @staticmethod
    def require_folder_structure() -> None:
        """
        Will setup all non existing folders and files.
        """

        from start import APPLICATION_NAME, DIRECTORY_PROGRAM

        Files.__APPLICATION_NAME = APPLICATION_NAME
        Files.DIRECTORY_PROGRAM = DIRECTORY_PROGRAM

        Files.__DIRECTORY_ROOT_CONFIGURATION = Files.__find_directory_root_configuration()
        Files.__DIRECTORY_AUTOSAVE = Files.__find_directory_autosave()
        Files.DIRECTORY_CONFIGURATION = Files.__find_directory_configuration()

        Files.FILE_CONF_INPUT = path.join(Files.DIRECTORY_CONFIGURATION, Files.__NAME_FILE_CONF_INPUT)
        Files.FILE_CONF_MPV = path.join(Files.DIRECTORY_CONFIGURATION, Files.__NAME_FILE_CONF_MPV)
        Files.FILE_SETTINGS = path.join(Files.DIRECTORY_CONFIGURATION, Files.__NAME_FILE_SETTINGS)

    @staticmethod
    def __find_directory_root_configuration():
        if path.isfile(path.join(Files.DIRECTORY_PROGRAM, "portable")):
            return Files.DIRECTORY_PROGRAM

        if sys.platform.startswith("win32"):
            conf_location = path.join(getenv("APPDATA"), Files.__APPLICATION_NAME)
        else:
            conf_location = path.expanduser("~/.config/{}".format(Files.__APPLICATION_NAME))

        Files.__create_dir_if_not_exists(conf_location)
        return conf_location

    @staticmethod
    def __find_directory_configuration():
        p = path.join(Files.__DIRECTORY_ROOT_CONFIGURATION, Files.__NAME_FOLDER_CONFIGURATION)
        Files.__create_dir_if_not_exists(p)
        return p

    @staticmethod
    def __find_directory_autosave():
        p = path.join(Files.__DIRECTORY_ROOT_CONFIGURATION, Files.__NAME_FOLDER_AUTOSAVE)
        Files.__create_dir_if_not_exists(p)
        return p

    @staticmethod
    def __create_dir_if_not_exists(p):
        if not path.isdir(p):
            c = Path(p)
            c.mkdir(parents=True)


Files.require_folder_structure()
