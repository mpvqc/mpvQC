import sys
from os import path, getenv
from pathlib import Path

from appdirs import unicode

from src import constants

try:
    to_unicode = unicode
except NameError:
    to_unicode = str


class Paths:
    # todo rework
    FILE_SETTINGS = "settings.json"
    FILE_INPUT_CONF = "input.conf"
    FILE_MPV_CONF = "mpv.conf"

    DIR_CFG = "cfg"
    DIR_AUTO_SAVE = "autosave"

    def __init__(self):
        from tmpv import APPLICATION_NAME, DIRECTORY_PROGRAM

        self.application_name = APPLICATION_NAME
        self.dir_program = DIRECTORY_PROGRAM

        # /home/user/.config
        self.dir_main_config = self.__find_dir_config()

        # /home/user/.config/cfg
        self.dir_main_cfg = path.join(self.dir_main_config, Paths.DIR_CFG)

        Paths.__require_dir_base_plus(base=self.dir_main_config, plus=Paths.DIR_CFG)
        Paths.__require_dir_base_plus(base=self.dir_main_config, plus=Paths.DIR_AUTO_SAVE)

        self.settings_json = self.__find_settings_json()
        self.input_conf = self.__create_input_conf_if_not_exists()
        self.mpv_conf = self.__create_mpv_conf_if_not_exists()
        print(self.__dict__)

    def __find_dir_config(self):

        if path.isfile(path.join(self.dir_program, "portable")):
            return self.dir_program

        if sys.platform.startswith("win32"):
            conf_location = path.join(getenv("APPDATA"), self.application_name)
        else:
            conf_location = path.expanduser("~/.config/{}".format(self.application_name))

        Paths.__create_dir_if_not_exists(conf_location)

        return conf_location

    def __find_settings_json(self):
        return path.join(self.dir_main_config, Paths.DIR_CFG, Paths.FILE_SETTINGS)

    def __create_input_conf_if_not_exists(self):
        input_conf = path.join(self.dir_main_config, Paths.DIR_CFG, Paths.FILE_INPUT_CONF)
        Paths.__write(constants.CFG_INPUT, input_conf)
        return input_conf

    def __create_mpv_conf_if_not_exists(self) -> path:
        mpv_conf = path.join(self.dir_main_config, Paths.DIR_CFG, Paths.FILE_MPV_CONF)
        Paths.__write(constants.CFG_MPV, mpv_conf)
        return mpv_conf

    @staticmethod
    def __write(content, target_path):
        if not path.isfile(target_path):
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(content)

    @staticmethod
    def __require_dir_base_plus(base, plus):
        Paths.__create_dir_if_not_exists(path.join(base, plus))

    @staticmethod
    def __create_dir_if_not_exists(p):
        if not path.isdir(p):
            c = Path(p)
            c.mkdir(parents=True)


class __Holder:
    paths: Paths = None


def get_paths() -> Paths:
    if __Holder.paths is None:
        __Holder.paths = Paths()

    return __Holder.paths
