import io
import json
import sys
from enum import Enum
from os import path, getenv
from pathlib import Path
from typing import List, Dict

from PyQt5.QtCore import QTranslator
from appdirs import unicode

from src import constants

try:
    to_unicode = unicode
except NameError:
    to_unicode = str

from tmpv import DIRECTORY_PROGRAM, APPLICATION_NAME, APPLICATION_VERSION, SYSTEM_LOCALE


class Settings(Enum):
    """Tuple: (json_key, default value)"""

    VERSION = ("version", APPLICATION_VERSION)
    NICKNAME = ("nickname", "nickname")
    LANGUAGE = ("language", SYSTEM_LOCALE)
    COMMENT_TYPES = (
        "comment_types", ["Spelling", "Punctuation", "Translation", "Phrasing", "Timing", "Typeset", "Note"])
    AUTOSAVE_INTERVAL_SECONDS = ("autosave_interval_seconds", 90)
    COMMENT_TABLE_ENTRY_FONT = ("comment_table_entry_font", "")
    SOFTSUB_OVERWRITE_VIDEO_FONT_ENABLED = ("softsub_overwrite_video_font_enabled", False)
    SOFTSUB_OVERWRITE_VIDEO_FONT_FONT = ("softsub_overwrite_video_font_font", "")

    QC_DOC_WRITE_VIDEO_PATH_TO_FILE = ("qc_doc_write_video_path_to_file", True)
    QC_DOC_WRITE_NICKNAME_TO_FILE = ("qc_doc_write_nick_name_to_file", True)

    PLAYER_LAST_PLAYED_DIRECTORY = ("player_last_played_directory", "")


class Configuration:
    __CONFIG_PATH = None

    class Parser:
        def __init__(self, dictionary: Dict):
            self.dictionary = dictionary

        def get(self, key: Settings):
            return self.dictionary.get(key.value[0], key.value[1])

    def __init__(self):
        super().__init__()

        self.version: str = None
        self.nickname: str = None
        self.language: str = None
        self.comment_types: List[str] = None
        self.autosave_interval_seconds: int = None
        self.comment_table_entry_font: str = None
        self.softsub_overwrite_video_font_enabled: bool = None
        self.softsub_overwrite_video_font_font: str = None
        self.qc_doc_write_video_path_to_file: bool = None
        self.qc_doc_write_nick_name_to_file: bool = None
        self.player_last_played_directory: str = None

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def save(self):
        with io.open(Configuration.__CONFIG_PATH, 'w', encoding='utf8') as outfile:
            str_ = json.dumps(self.__dict__, indent=4, separators=(',', ': '), ensure_ascii=False)
            outfile.write(to_unicode(str_))

    @staticmethod
    def load_from(json_file) -> 'Configuration':
        with open(json_file) as data_file:
            c = Configuration.__map_dict_to_configuration(json.load(data_file), json_file)
        return c

    @staticmethod
    def create_default(json_file):
        Configuration.__map_dict_to_configuration({}, json_file).save()

    @staticmethod
    def __map_dict_to_configuration(dictionary, json_file):
        Configuration.__CONFIG_PATH = json_file

        c = Configuration()
        d = Configuration.Parser(dictionary)
        s = Settings

        c.version = d.get(s.VERSION)
        c.nickname = d.get(s.NICKNAME)
        c.language = d.get(s.LANGUAGE)

        c.comment_types = d.get(s.COMMENT_TYPES)

        c.autosave_interval_seconds = int(d.get(s.AUTOSAVE_INTERVAL_SECONDS))
        c.comment_table_entry_font = d.get(s.COMMENT_TABLE_ENTRY_FONT)

        c.softsub_overwrite_video_font_enabled = bool(d.get(s.SOFTSUB_OVERWRITE_VIDEO_FONT_ENABLED))
        c.softsub_overwrite_video_font_font = d.get(s.SOFTSUB_OVERWRITE_VIDEO_FONT_FONT)

        c.qc_doc_write_video_path_to_file = bool(d.get(s.QC_DOC_WRITE_VIDEO_PATH_TO_FILE))
        c.qc_doc_write_nick_name_to_file = bool(d.get(s.QC_DOC_WRITE_NICKNAME_TO_FILE))

        c.player_last_played_directory = d.get(s.PLAYER_LAST_PLAYED_DIRECTORY)
        return c


class Paths:
    FILE_SETTINGS = "settings.json"
    FILE_INPUT_CONF = "input.conf"
    FILE_MPV_CONF = "mpv.conf"

    def __init__(self):
        self.cfg = "cfg"
        self.auto_save = "autosave"

        self.application_name = APPLICATION_NAME
        self.dir_program = DIRECTORY_PROGRAM

        # /home/user/.config
        self.dir_main_config = self.__find_dir_config()

        # /home/user/.config/cfg
        self.dir_main_cfg = path.join(self.dir_main_config, self.cfg)

        Paths.__require_dir_base_plus(base=self.dir_main_config, plus=self.cfg)
        Paths.__require_dir_base_plus(base=self.dir_main_config, plus=self.auto_save)

        self.file_settings = self.__find_file_options()
        self.input_conf = self.__create_input_conf_if_not_exists()
        self.mpv_conf = self.__create_mpv_conf_if_not_exists()

    def __find_dir_config(self):

        if path.isfile(path.join(self.dir_program, "portable")):
            return self.dir_program

        if sys.platform.startswith("win32"):
            conf_location = path.join(getenv("APPDATA"), self.application_name)
        else:
            conf_location = path.expanduser("~/.config/{}".format(self.application_name))

        Paths.__create_dir_if_not_exists(conf_location)

        return conf_location

    def __find_file_options(self) -> Configuration:
        json_file = path.join(self.dir_main_config, self.cfg, Paths.FILE_SETTINGS)

        if not path.isfile(json_file):
            Configuration.create_default(json_file)
        return Configuration.load_from(json_file)

    def __create_input_conf_if_not_exists(self):
        input_conf = path.join(self.dir_main_config, self.cfg, Paths.FILE_INPUT_CONF)
        Paths.__write(constants.CFG_INPUT, input_conf)
        return input_conf

    def __create_mpv_conf_if_not_exists(self) -> path:
        mpv_conf = path.join(self.dir_main_config, self.cfg, Paths.FILE_MPV_CONF)
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
    config: Configuration = None
    paths: Paths = None


def get_config() -> Configuration:
    if __Holder.config is None:
        __Holder.config = get_paths().file_settings

    return __Holder.config


def get_paths() -> Paths:
    if __Holder.paths is None:
        __Holder.paths = Paths()

    return __Holder.paths


def get_translator() -> QTranslator:
    _locale_structure = path.join(get_paths().dir_program, "locale", "{}", "LC_MESSAGES")

    q = QTranslator()

    trans_dir = _locale_structure.format(SYSTEM_LOCALE.upper())
    trans_present = path.isdir(trans_dir)

    if trans_present:
        q.load("ui_trans", trans_dir)
    else:
        q.load("ui_trans", _locale_structure.format("EN_US".upper()))

    return q
