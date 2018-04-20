import io
import json
import sys
from enum import Enum
from os import path, getenv
from pathlib import Path
from typing import List, Dict

from PyQt5.QtCore import QObject, QTranslator
from appdirs import unicode

try:
    to_unicode = unicode
except NameError:
    to_unicode = str

from tmpv import DIRECTORY_PROGRAM, APPLICATION_NAME, APPLICATION_VERSION, SYSTEM_LOCALE


class _Settings(Enum):
    """Tuple: (json_key, default value)"""

    VERSION = ("version", APPLICATION_VERSION)
    AUTHOR = ("author", "author")
    LANGUAGE = ("language", SYSTEM_LOCALE)
    COMMENT_TYPES_ACTIVE = (
        "comment_types_active", ["Spelling", "Punctuation", "Translation", "Phrasing", "Timing", "Typeset", "Note"])
    COMMENT_TYPES_INACTIVE = ("comment_types_inactive", [])
    AUTOSAVE_INTERVAL_SECONDS = ("autosave_interval_seconds", 90)
    COMMENT_TABLE_ENTRY_FONT = ("comment_table_entry_font", "")
    SOFTSUB_OVERWRITE_VIDEO_FONT_ENABLED = ("softsub_overwrite_video_font_enabled", False)
    SOFTSUB_OVERWRITE_VIDEO_FONT_FONT = ("softsub_overwrite_video_font_font", "")


class Configuration(QObject):
    __CONFIG_PATH = None

    class Parser:
        def __init__(self, dictionary: Dict):
            self.dictionary = dictionary

        def get(self, key: _Settings):
            return self.dictionary.get(key.value[0], key.value[1])

    def __init__(self):
        super().__init__()

        self.version: str = None
        self.author: str = None
        self.language: str = None
        self.comment_types_active: List[str] = None
        self.comment_types_inactive: List[str] = None
        self.autosave_interval_seconds: int = None
        self.comment_table_entry_font: str = None
        self.softsub_overwrite_video_font_enabled: bool = None
        self.softsub_overwrite_video_font_font: str = None

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
        s = _Settings

        c.version = d.get(s.VERSION)
        c.author = d.get(s.AUTHOR)
        c.language = d.get(s.LANGUAGE)

        c.comment_types_active = d.get(s.COMMENT_TYPES_ACTIVE)
        c.comment_types_inactive = d.get(s.COMMENT_TYPES_INACTIVE)

        c.autosave_interval_seconds = int(d.get(s.AUTOSAVE_INTERVAL_SECONDS))
        c.comment_table_entry_font = d.get(s.COMMENT_TABLE_ENTRY_FONT)

        c.softsub_overwrite_video_font_enabled = bool(d.get(s.SOFTSUB_OVERWRITE_VIDEO_FONT_ENABLED))
        c.softsub_overwrite_video_font_font = d.get(s.SOFTSUB_OVERWRITE_VIDEO_FONT_FONT)
        return c


class Paths:
    pass

    def __init__(self):
        self.cfg = "cfg"
        self.auto_save = "autosave"

        self.application_name = APPLICATION_NAME
        self.dir_program = DIRECTORY_PROGRAM
        self.dir_main_config = self.__find_dir_config()

        Paths.__require_dir_base_plus(base=self.dir_main_config, plus=self.cfg)
        Paths.__require_dir_base_plus(base=self.dir_main_config, plus=self.auto_save)
        self.file_cfg = self.__find_file_options()

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
        expected_options_file = "{}.json".format(self.application_name)
        json_file = path.join(self.dir_main_config, self.cfg, expected_options_file)

        if not path.isfile(json_file):
            Configuration.create_default(json_file)
        return Configuration.load_from(json_file)

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
        __Holder.config = get_paths().file_cfg

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
