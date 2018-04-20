import io
import json
import sys
from os import path, getenv
from pathlib import Path
from typing import List

from PyQt5.QtCore import QObject, QTranslator
from appdirs import unicode

try:
    to_unicode = unicode
except NameError:
    to_unicode = str

from tmpv import DIRECTORY_PROGRAM, APPLICATION_NAME, APPLICATION_VERSION, SYSTEM_LOCALE


class Configuration(QObject):
    __jkey_mpvqc_version = "mpvQC_version"
    __jkey_this_json_full_path = "this_json_full_path"
    __jkey_author = "author"
    __jkey_language = "language"
    __jkey_comment_types_active = "comment_types_active"
    __jkey_comment_types_inactive = "comment_types_inactive"
    __jkey_autosave_interval_seconds = "autosave_interval_seconds"
    __jkey_comment_table_entry_font = "comment_table_entry_font"
    __jkey_softsub_overwrite_video_font_enabled = "softsub_overwrite_video_font_enabled"
    __jkey_softsub_overwrite_video_font_font = "softsub_overwrite_video_font_font"

    __def_version = APPLICATION_VERSION
    __def_author = "author"
    __def_language = SYSTEM_LOCALE
    __def_comment_types_active = ["Spelling", "Punctuation", "Translation", "Phrasing", "Timing", "Typeset", "Note"]
    __def_comment_types_inactive = []
    __def_autosave_interval_seconds = 90
    __def_comment_table_entry_font = ""
    __def_softsub_overwrite_video_font_enabled = False
    __def_softsub_overwrite_video_font_font = ""

    def __init__(self, this_json_full_path: str, mpvqc_version: str, author: str, language: str,
                 comment_types_active: List[str], comment_types_inactive: List[str], autosave_interval_seconds: int,
                 comment_table_entry_font: str, softsub_overwrite_video_font_enabled: bool,
                 softsub_overwrite_video_font_font: str):
        #
        super().__init__()
        self.mpvQC_version: str = mpvqc_version
        self.this_json_full_path: str = this_json_full_path
        self.author: str = author
        self.language: str = language
        self.comment_types_active = comment_types_active
        self.comment_types_inactive = comment_types_inactive
        self.autosave_interval_seconds = autosave_interval_seconds
        self.comment_table_entry_font = comment_table_entry_font
        self.softsub_overwrite_video_font_enabled = softsub_overwrite_video_font_enabled
        self.softsub_overwrite_video_font_font = softsub_overwrite_video_font_font

    def save(self):
        with io.open(self.this_json_full_path, 'w', encoding='utf8') as outfile:
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
    def __map_dict_to_configuration(dict_map, json_file):
        return Configuration(
            this_json_full_path=dict_map.get(Configuration.__jkey_this_json_full_path, json_file),
            mpvqc_version=dict_map.get(Configuration.__jkey_mpvqc_version, Configuration.__def_version),
            author=dict_map.get(Configuration.__jkey_author, Configuration.__def_author),
            language=dict_map.get(Configuration.__jkey_language, Configuration.__def_language),
            comment_types_active=dict_map.get(Configuration.__jkey_comment_types_active,
                                              Configuration.__def_comment_types_active),
            comment_types_inactive=dict_map.get(Configuration.__jkey_comment_types_inactive,
                                                Configuration.__def_comment_types_inactive),
            autosave_interval_seconds=int(dict_map.get(Configuration.__jkey_autosave_interval_seconds,
                                                       Configuration.__def_autosave_interval_seconds)),
            comment_table_entry_font=dict_map.get(Configuration.__jkey_comment_table_entry_font,
                                                  Configuration.__def_comment_table_entry_font),
            softsub_overwrite_video_font_enabled=bool(
                dict_map.get(Configuration.__jkey_softsub_overwrite_video_font_enabled,
                             Configuration.__def_softsub_overwrite_video_font_enabled)),
            softsub_overwrite_video_font_font=dict_map.get(
                Configuration.__jkey_softsub_overwrite_video_font_font,
                Configuration.__def_softsub_overwrite_video_font_font)
        )


class Paths:
    pass

    def __init__(self):
        self.cfg = "cfg"
        self.auto_save = "autosave"

        self.application_name = APPLICATION_NAME
        self.dir_program = DIRECTORY_PROGRAM
        self.dir_main_config = self.__find_dir_config()

        self.__require_dir_base_plus(base=self.dir_main_config, plus=self.cfg)
        self.__require_dir_base_plus(base=self.dir_main_config, plus=self.auto_save)
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

    def __require_dir_base_plus(self, base, plus):
        Paths.__create_dir_if_not_exists(path.join(base, plus))

    @staticmethod
    def load() -> 'Paths':
        return Paths()

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
        __Holder.paths = Paths.load()

    return __Holder.paths


_locale_structure = path.join(get_paths().dir_program, "locale", "{}", "LC_MESSAGES")


def provide_translator() -> QTranslator:
    q = QTranslator()

    trans_dir = _locale_structure.format(SYSTEM_LOCALE.upper())
    trans_present = path.isdir(trans_dir)

    if trans_present:
        q.load("ui_trans", trans_dir)
    else:
        q.load("ui_trans", _locale_structure.format("EN_US".upper()))

    return q
